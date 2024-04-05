from flask import Flask, request, jsonify, Response
from src.config.service_provider import openai_client
from src.prompts.system import system_prompt1
from src.functions.retrieval import retrieve_filtered_data, retrieve_data_in_date_range
import json
import pandas as pd


def query_handler():
    print("query_handler controller runs")
    # access JSON in request body and directly convert / parse it to a Python dictionary
    data = request.json

    # The .get() method is used instead of direct key access as it returns None if the key is not found, instead of throwing an error
    user_query = data.get("userQuery")
    print("user_query:", user_query)

    # define tools for the chat completion AI model to intelligently choose a target function to execute based on user query
    tools = [
        {
            "type": "function",
            "function": {
                "name": "retrieve_filtered_data",
                "description": (
                    "Retrieves data from specified financial collections with optional filters. "
                    "Primarily call this function when the user query contains one or more financial collections with or without potential filtering based on year and month."
                    "Example calls: retrieve_filtered_data(['revenue'], {'year': 2024}) or retrieve_filtered_data(['revenue', 'expense'], {})."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collections": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Target collections, e.g., ['revenue', 'expense'] or ['working_hours'].",
                        },
                        "filter_option": {
                            "type": "object",
                            "description": "Optional filters, e.g., {'year': 2023, 'month': 'may'} or {'year': 2023}.",
                        },
                    },
                    "required": ["collections"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_data_in_date_range",
                "description": (
                    "Retrieves data from a single financial collection within a specified date range. "
                    "Primarily call this function when the user query clearly indicate a date range contains both start and end for a single target financial collection."
                    "Example call: retrieve_data_in_date_range('revenue', 2023, 5, 2024, 2)."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collection_name": {
                            "type": "string",
                            "description": "The target financial collection to query, e.g., 'revenue'.",
                        },
                        "start_year": {
                            "type": "number",
                            "description": "Start year, e.g., 2023.",
                        },
                        "start_month": {
                            "type": "number",
                            "description": "Start month, e.g., 1 for January.",
                        },
                        "end_year": {
                            "type": "number",
                            "description": "End year, e.g., 2024.",
                        },
                        "end_month": {
                            "type": "number",
                            "description": "End month, e.g., 2 for February.",
                        },
                    },
                    "required": ["collection_name", "start_year", "start_month", "end_year", "end_month"],
                },
            },
        },
    ]

    # set up message for completion with system prompt and user query
    messages = [{"role": "system", "content": system_prompt1()}, {"role": "user", "content": user_query}]

    # setup the prompt for the API model

    completion_response = openai_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0.2,
        top_p=0.1,
        tools=tools,
        tool_choice="auto",
    )

    # this message will contain either text-based response or tool-based response for function arguments
    completion_response_message = completion_response.choices[0].message

    # this is the condition where a tool call is made by the AI model
    if completion_response_message.tool_calls:
        print("function called")
        available_functions = {
            "retrieve_filtered_data": retrieve_filtered_data,
            "retrieve_data_in_date_range": retrieve_data_in_date_range,
        }

        for tool_call in completion_response_message.tool_calls:
            function_name = tool_call.function.name
            print("function_name:", function_name)
            print("function_arguments (lowered):", tool_call.function.arguments.lower())

            function_to_call = available_functions[function_name]
            # convert the JSON string (all letter lower cased) to a Python dictionary for function arguments
            function_args = json.loads(tool_call.function.arguments.lower())
            # call and execute the function on server side and return the result
            retrieved_result = function_to_call(**function_args)
            print("retrieved_result:", retrieved_result)

            # convert retrieved_result to pandas dataframe
            df = pd.DataFrame(retrieved_result)
            pivoted_df = df.pivot_table(index=["year", "month", "month_n"], columns="category", values="value").reset_index()
            sorted_df = pivoted_df.sort_values(by=["year", "month_n"], ascending=[False, False])
            category_columns = [col for col in sorted_df.columns if col not in ["year", "month", "month_n"]]
            column_order = ["year", "month", "month_n"] + category_columns
            final_df = sorted_df[column_order]

            print("final_df:", final_df)

            # Convert DataFrame to JSON
            df_data = final_df.to_json(orient="split")

            print("json.loads(df_data):", json.loads(df_data))
            return jsonify({"botResponse": json.loads(df_data)})

    # this is the condition where the AI model directly provides a text-based response
    else:
        print("no function called")
        response = completion_response_message.content
        print("response:", response)

        # using jsonify to convert the Python dictionary to a JSON object and return it as a response payload to the client
        return jsonify({"botResponse": response})
