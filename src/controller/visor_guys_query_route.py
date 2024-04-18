from flask import Flask, request, jsonify, Response
from src.config.service_provider_init import openai_client


def visor_guys_query_route_controller():
    print("visor_guys_query_route_controller runs")
    # access JSON payload in request body and directly convert / parse it to a Python dictionary
    data = request.json

    # The .get() method is used instead of direct key access as it returns None if the key is not found, instead of throwing an error
    user_query = data.get("user_query")
    print("user_query:", user_query)

    openai_chat_completion_message = [{"role": "system", "content": "you are a help general AI assistant"}, {"role": "user", "content": user_query}]

    calculate_response = openai_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=openai_chat_completion_message,
        temperature=0.2,
        top_p=0.1,
    )

    print("calculate_response:", calculate_response)
    calculate_response_message = calculate_response.choices[0].message.content

    return jsonify({"serverResponse": calculate_response_message})
