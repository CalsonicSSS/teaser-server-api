from flask import Flask, request, jsonify, Response
from src.config.service_provider_init import openai_client
from src.open_ai.teaser_prompts import function_call_prompt, user_query_interpret_prompt, calculate_prompt
from src.functions.teaser_retrieval import retrieve_filtered_data, retrieve_data_in_date_range, retrieve_by_category_value_threshold
import json
import pandas as pd


def teaser_query_route_controller():
    print("teaser_query_route_controller runs")

    # access JSON payload in http request body and then parse it to a Python dictionary
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
                    "Retrieves financial data from specified financial collections with optional filters."
                    "Primarily call this function when the user query contains one or more financial collections with or without potential filtering based on year and month."
                    "this function should always be first considered when the user query contains financial collections."
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
                    "Retrieves financial data from a single financial collection within a specified date range. "
                    "Only to call this function when the user query clearly indicate a date range contains both start and end for a single target financial collection."
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
        {
            "type": "function",
            "function": {
                "name": "retrieve_by_category_value_threshold",
                "description": (
                    "Retrieve financial data based on value threshold conditions for a specified collection."
                    "Only to call this function when the user query contains a collection name, a threshold condition, and one or two threshold values."
                    "Example calls: retrieve_by_category_value_threshold('revenue', [10000], 'gt'), retrieve_by_category_value_threshold('expense', [1000, 30000], 'in-between')."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collection_name": {"type": "string", "description": "The target financial data collection to query."},
                        "threshold_value": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list containing the threshold value(s); single number for 'gt' or 'lt', two numbers for 'in-between' (the first position is always smaller value than the second position).",
                        },
                        "threshold_condition": {
                            "type": "string",
                            "enum": ["gt", "lt", "in-between"],
                            "description": "The condition for filtering data: greater than ('gt'), less than ('lt'), or in-between.",
                        },
                    },
                    "required": ["collection_name", "threshold_value", "threshold_condition"],
                },
            },
        },
    ]

    # set up message for chat completion api with system prompt and user query
    user_query_interpretation_messages = [{"role": "system", "content": user_query_interpret_prompt}, {"role": "user", "content": user_query}]
    function_call_messages = [{"role": "system", "content": function_call_prompt}, {"role": "user", "content": user_query}]

    # to interpret user query and determine the intent
    user_query_interpretation_response = openai_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=user_query_interpretation_messages,
        temperature=0.2,
        top_p=0.1,
        response_format={"type": "json_object"},
    )

    user_query_interpretation_response_json = user_query_interpretation_response.choices[0].message.content
    print("user_query_interpretation_response_json:", user_query_interpretation_response_json)

    # convert json string to python dictionary
    user_query_interpretation_response_dict = json.loads(user_query_interpretation_response_json)
    print("user_query_interpretation_response_dict:", user_query_interpretation_response_dict)

    # --------------------------------------------------- RETRIEVAL INTENT CONDITION ---------------------------------------------------

    if user_query_interpretation_response_dict["intent"] == "retrieval":
        function_call_response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=function_call_messages,
            temperature=0.2,
            top_p=0.1,
            tools=tools,
            tool_choice="auto",
        )

        # the response message here will contain either text-based response or tool-based response json for function call
        function_call_response_message = function_call_response.choices[0].message

        # this is the condition where a tool call is made by the AI model
        if function_call_response_message.tool_calls:
            print("function called")
            available_functions = {
                "retrieve_filtered_data": retrieve_filtered_data,
                "retrieve_data_in_date_range": retrieve_data_in_date_range,
                "retrieve_by_category_value_threshold": retrieve_by_category_value_threshold,
            }

            tool_call = function_call_response_message.tool_calls[0]
            target_function_name = tool_call.function.name
            print("target_function_name:", target_function_name)
            print("function_arguments (lowered):", tool_call.function.arguments.lower())

            target_function_to_call = available_functions[target_function_name]
            # convert the JSON string (all letter lower cased) to a Python dictionary for function arguments
            target_function_args = json.loads(tool_call.function.arguments.lower())
            # call and execute the function on server side and return the result
            retrieved_result = target_function_to_call(**target_function_args)
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
            response = function_call_response_message.content
            print("response:", response)

            # using jsonify to convert the Python dictionary to a JSON string as a response payload and send directly to the client side after return statement
            return jsonify({"botResponse": response})

    # --------------------------------------------------- CALCULATE INTENT ---------------------------------------------------

    if user_query_interpretation_response_dict["intent"] == "calculate":
        print("create financial analyzer assistant")
        financial_analyzer_assistant = openai_client.beta.assistants.create(
            name="financial_analyzer",
            instructions=calculate_prompt,
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo-preview",
        )

        print("create thread")
        print("user_query:", user_query)
        thread_1 = openai_client.beta.threads.create(messages=[{"role": "user", "content": user_query}])

        print("now create and poll run")
        # the particular assistant is attached to a particular thread with id and then run them together
        run = openai_client.beta.threads.runs.create_and_poll(
            thread_id=thread_1.id,
            assistant_id=financial_analyzer_assistant.id,
        )

        print("completion hits!")
        # the run result is the message that can be attach to a particular thread
        if run.status == "completed":
            print("run status complete")
            messages = openai_client.beta.threads.messages.list(thread_id=thread_1.id)
            print("run result", messages.data[0].content[0].text.value)
            return jsonify({"botResponse": messages.data[0].content[0].text.value})
        else:
            print("run status else")
            print(run.status)
            return jsonify({"botResponse": "Sorry, I could not complete the task."})
