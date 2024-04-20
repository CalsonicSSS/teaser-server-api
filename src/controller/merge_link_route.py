from flask import Flask, request, jsonify
import requests
from src.config.service_provider_init import merge_api_key
from src.config.service_provider_init import mongodb_atlas_client
import uuid


def create_link_token_route_controller():
    print("create_link_token_route_controller runs")

    user_data = request.json

    print("user_data: ", user_data)

    link_token_url = "https://api.merge.dev/api/integrations/create-link-token"
    headers = {"Authorization": f"Bearer {merge_api_key}"}
    body = {
        "end_user_origin_id": str(uuid.uuid4()),
        "end_user_organization_name": user_data["end_user_organization_name"],
        "end_user_email_address": user_data["end_user_email_address"],
        "categories": ["accounting"],
    }

    print("body: ", body)

    link_token_response_result = requests.post(link_token_url, data=body, headers=headers)
    link_token = link_token_response_result.json().get("link_token")

    print("link_token: ", link_token)

    return jsonify({"linkToken": link_token})


# ------------------------------------------------------------------------------------------------------


def swap_account_token_route_controller():
    print("swap_account_token_route_controller runs")

    swap_data = request.json
    print("swap_data: ", swap_data)

    public_token = swap_data.get("public_token")

    headers = {"Authorization": f"Bearer {merge_api_key}"}
    account_token_url = "https://api.merge.dev/api/integrations/account-token/{}".format(public_token)
    account_token_result = requests.get(account_token_url, headers=headers)
    account_token = account_token_result.json().get("account_token")

    # make comprehensive user data object
    user_data = {
        "end_user_organization_name": swap_data.get("end_user_organization_name"),
        "end_user_email_address": swap_data.get("end_user_email_address"),
        "account_token": account_token,
    }

    user_db = mongodb_atlas_client.user
    target_collection = user_db["user_info"]
    target_collection.insert_one(user_data)

    return jsonify({"serverResponse": "Success"})
