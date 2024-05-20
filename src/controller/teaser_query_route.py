from flask import request, jsonify
from src.config.service_provider_init import openai_client
from src.open_ai.teaser_prompts import function_call_prompt, user_query_interpret_prompt, calculate_prompt
from src.functions.teaser_retrieval import retrieve_filtered_data, retrieve_data_in_date_range, retrieve_by_category_value_threshold
import json
import pandas as pd
from src.open_ai.function_tools import retrieve_filtered_data_tool, retrieve_data_in_date_range_tool, retrieve_by_category_value_threshold_tool


def teaser_query_route_controller():
    print("teaser_query_route_controller runs")

    # access JSON payload in http request body and then parse it to a Python dictionary
    request_payload_data = request.json

    # The .get() method is used instead of direct key access as it returns None if the key is not found, instead of throwing an error
    user_query = request_payload_data.get("user_query")
    print("user_query:", user_query)

    # define tools for the chat completion AI model to intelligently choose a target function to execute based on user query
    tools = [retrieve_filtered_data_tool, retrieve_data_in_date_range_tool, retrieve_by_category_value_threshold_tool]

    # set up message for chat completion api with system prompt and user query
    user_query_interpretation_messages = [{"role": "system", "content": user_query_interpret_prompt}, {"role": "user", "content": user_query}]
    function_call_messages = [{"role": "system", "content": function_call_prompt}, {"role": "user", "content": user_query}]

    # to interpret user query and determine the intent
    user_query_interpretation_response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
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
        print("retrieval intent path")
        function_call_response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
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
            print("df:", df)
            pivoted_df = df.pivot_table(index=["year", "month", "month_n"], columns="category", values="value").reset_index()
            print(1)
            sorted_df = pivoted_df.sort_values(by=["year", "month_n"], ascending=[False, False])
            print(2)
            category_columns = [col for col in sorted_df.columns if col not in ["year", "month", "month_n"]]
            print(3)
            column_order = ["year", "month", "month_n"] + category_columns
            final_df = sorted_df[column_order]
            print(4)

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
