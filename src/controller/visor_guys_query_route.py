from flask import Flask, request, jsonify, Response
from src.config.service_provider_init import openai_client
from src.open_ai.function_tools import (
    retrieve_client_invoices_data_tool,
    retrieve_client_balance_sheets_data_tool,
    retrieve_client_cash_flows_data_tool,
    retrieve_client_expenses_data_tool,
    retrieve_client_income_statements_data_tool,
)
from src.open_ai.production_prompts import user_query_interpretation_prompt, user_retrieval_function_call_prompt, user_calculate_prompt
import json
from src.functions.merge_retrieval import (
    retrieve_client_invoices_data,
    retrieve_client_balance_sheets_data,
    retrieve_client_cash_flows_data,
    retrieve_client_expenses_data,
    retrieve_client_income_statements_data,
)
import pandas as pd
from src.config.service_provider_init import mongodb_atlas_client
import os


def visor_guys_query_route_controller():
    print("visor_guys_query_route_controller runs")

    # access JSON payload in http request body and then parse it to a Python dictionary
    request_payload = request.json

    # The .get() method is used instead of direct key access as it returns None if the key is not found, instead of throwing an error
    user_query = request_payload.get("user_query")
    print("user_query:", user_query)

    # define messages for the chat completion AI model to interpret the user query intention
    user_query_interpretation_messages = [
        {"role": "system", "content": user_query_interpretation_prompt},
        {"role": "user", "content": user_query},
    ]

    # determine the user query intention for data retrieval or data metrics calculation
    user_query_interpretation_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=user_query_interpretation_messages,
        temperature=0.2,
        top_p=0.1,
        response_format={"type": "json_object"},
    )

    # openai chat completion API response will result in a JSON string
    # convert the JSON string response to a Python dictionary and access the "intent" key value
    user_query_interpretation_result = json.loads(user_query_interpretation_response.choices[0].message.content)["intent"]
    print("user_query_interpretation_result:", user_query_interpretation_result)

    # --------------------------------------------------- RETRIEVAL INTENT CONDITIONS ---------------------------------------------------

    if user_query_interpretation_result == "retrieval":
        print("retrieval intent detected")

        # define messages for the chat completion AI model to intelligently choose a target function to execute based on user query
        function_call_messages = [
            {"role": "system", "content": user_retrieval_function_call_prompt},
            {"role": "user", "content": user_query},
        ]
        # define tools for the chat completion AI model to intelligently choose a target function to execute based on user query
        tools = [
            retrieve_client_invoices_data_tool,
            retrieve_client_balance_sheets_data_tool,
            retrieve_client_cash_flows_data_tool,
            retrieve_client_expenses_data_tool,
            retrieve_client_income_statements_data_tool,
        ]

        function_call_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=function_call_messages,
            temperature=0.2,
            top_p=0.1,
            tools=tools,
            tool_choice="auto",
        )

        # the "function_call_response_message" here will result in either text-based response (like normal chatCompletion) or tool-based response json for function call
        function_call_response_message = function_call_response.choices[0].message

        # If responds with tool-based function call in json format:
        if function_call_response_message.tool_calls:
            available_functions = {
                "retrieve_client_invoices_data": retrieve_client_invoices_data,
                "retrieve_client_balance_sheets_data": retrieve_client_balance_sheets_data,
                "retrieve_client_cash_flows_data": retrieve_client_cash_flows_data,
                "retrieve_client_expenses_data": retrieve_client_expenses_data,
                "retrieve_client_income_statements_data": retrieve_client_income_statements_data,
            }

            tool_call = function_call_response_message.tool_calls[0]
            target_function_name = tool_call.function.name
            target_function_args_json = tool_call.function.arguments.lower()

            # convert the JSON string (all letter lower cased) to a Python dictionary for function arguments
            target_function_args = json.loads(target_function_args_json)
            print("target_function_name:", target_function_name)
            print("target_function_arguments:", target_function_args)

            # call and execute the target retrieval function and return its retrieved results
            target_function_to_call = available_functions[target_function_name]
            function_result = target_function_to_call(**target_function_args)

            # print("function_result:", function_result["retrieval_result"])

            # Convert the retrieved data to a pandas DataFrame and save it as a CSV file in backend
            df = pd.DataFrame(function_result["retrieval_result"])
            df.to_csv("data.csv", index=False)

            # upload the CSV file to openai's file storage
            with open("data.csv", "rb") as file:
                new_file_uploaded = openai_client.files.create(file=file, purpose="assistants")

            # find and delete the old previous CSV file by id from openai's file storage
            user_db = mongodb_atlas_client.user
            target_collection = user_db["user_info"]
            previous_file_id = target_collection.find_one({"end_user_organization_name": "visor guys moving"})["file_id"]
            if previous_file_id:
                openai_client.files.delete(previous_file_id)

            # and then delete the local CSV file
            print("deleting local CSV file")
            os.remove("data.csv")

            # finally, update the user's database document with the new file id
            new_file_id = new_file_uploaded.id
            target_collection.update_one(
                {"end_user_organization_name": "visor guys moving"},
                {"$set": {"file_id": new_file_id}},
            )

            return jsonify({"queryResult": function_result["retrieval_result"], "category": function_result["category"]})

        # If responds with text-based response:
        if function_call_response_message.content:
            return jsonify({"queryResult": function_call_response_message.content, "category": "text"})

    # --------------------------------------------------- CALCULATE INTENT CONDITIONS ---------------------------------------------------

    if user_query_interpretation_result == "calculate":
        print("calculate intent detected")

        # retrieve the latest file id from the user's database document
        user_db = mongodb_atlas_client.user
        target_collection = user_db["user_info"]
        current_file_id = target_collection.find_one({"end_user_organization_name": "visor guys moving"})["file_id"]
        # print("current_file_id:", current_file_id)

        # create an openai assistant with the latest file id
        data_analysis_assistant = openai_client.beta.assistants.create(
            instructions=user_calculate_prompt,
            model="gpt-4-turbo",
            tools=[{"type": "code_interpreter"}],
            tool_resources={"code_interpreter": {"file_ids": [current_file_id]}},
        )

        data_analysis_thread = openai_client.beta.threads.create(messages=[{"role": "user", "content": user_query}])

        run = openai_client.beta.threads.runs.create_and_poll(
            thread_id=data_analysis_thread.id,
            assistant_id=data_analysis_assistant.id,
        )

        # the run result is the message that can be attach to a particular thread
        if run.status == "completed":
            print("run status complete")
            assistant_response_content = openai_client.beta.threads.messages.list(thread_id=data_analysis_thread.id).data[0].content[0]
            if assistant_response_content.type == "image_file":
                image_file_id = assistant_response_content.image_file.file_id
                image_file = openai_client.files.retrieve(image_file_id)
                image_file_content = openai_client.files.content(image_file_id).read()
                # print("image_file:", image_file)
                # print("image_file_content:", image_file_content)

                return Response(image_file_content, mimetype="image/png")

            if assistant_response_content.type == "text":
                assistant_response = assistant_response_content.text.value
                return jsonify({"queryResult": assistant_response, "category": "assistant"})

        else:
            print("run status else")
            print(run.status)
            return jsonify({"queryResult": "Sorry something went wrong, I could not complete the task.", "category": "assistant"})
