from flask import Flask, request, jsonify
import requests
from src.config.service_provider_init import merge_api_key
from src.config.service_provider_init import mongodb_atlas_client
import uuid


def create_link_token_route_controller():
    print("create_link_token_route_controller runs")

    request_payload = request.json

    end_user_organization_name = request_payload.get("end_user_organization_name")
    end_user_email_address = request_payload.get("end_user_email_address")
    end_user_origin_id = str(uuid.uuid4())

    link_token_url = "https://api.merge.dev/api/integrations/create-link-token"
    headers = {"Authorization": f"Bearer {merge_api_key}"}
    body = {
        "end_user_origin_id": end_user_origin_id,
        "end_user_organization_name": end_user_organization_name,
        "end_user_email_address": end_user_email_address,
        "categories": ["accounting"],
    }

    user_db = mongodb_atlas_client.user
    target_collection = user_db["user_info"]
    target_collection.insert_one(
        {
            "end_user_origin_id": end_user_origin_id,
            "end_user_email_address": end_user_email_address,
            "end_user_organization_name": end_user_organization_name,
        }
    )

    link_token_response_result = requests.post(link_token_url, data=body, headers=headers)
    link_token = link_token_response_result.json().get("link_token")

    return jsonify({"linkToken": link_token, "endUserOriginId": end_user_origin_id})


# ------------------------------------------------------------------------------------------------------


def swap_account_token_route_controller():
    print("swap_account_token_route_controller runs")

    request_payload = request.json
    public_token = request_payload.get("public_token")
    end_user_origin_id = request_payload.get("end_user_origin_id")

    headers = {"Authorization": f"Bearer {merge_api_key}"}
    account_token_url = "https://api.merge.dev/api/integrations/account-token/{}".format(public_token)
    account_token_result = requests.get(account_token_url, headers=headers)
    account_token = account_token_result.json().get("account_token")

    # save this account_token to the same user's database document
    # this account_token should be only used in backend server to access the user's data
    user_db = mongodb_atlas_client.user
    target_collection = user_db["user_info"]
    target_collection.update_one(
        {"end_user_origin_id": end_user_origin_id},
        {"$set": {"account_token": account_token}},
    )

    return jsonify({"serverResponse": "Success"})
