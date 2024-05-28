from src.config.service_provider_init import mongodb_atlas_client


# Retrieve target financial data with filters from specified collection(s).
# collections: str[] (required), filter: dict (required)
def retrieve_filtered_data(collections, filter):
    final_retrieval = []
    financial_main_db = mongodb_atlas_client.financial_main

    for collection in collections:
        target_collection = financial_main_db[collection]
        retrieval_result = list(target_collection.find(filter, {"_id": 0}))
        final_retrieval.extend(retrieval_result)
    return final_retrieval


# --------------------------------------------------------------------------------------------------------------------


# Retrieve financial data from a specified MongoDB Atlas collection within specified date range.
# collection_name, start_year, start_month, end_year, end_month are all required
def retrieve_data_in_date_range(collection_name: str, start_year: int, start_month: int, end_year: int, end_month: int):
    financial_main_db = mongodb_atlas_client.financial_main
    collection = financial_main_db[collection_name]

    # Assuming year is stored as an integer and month_n as an integer too
    # Adjust the logic to capture the range from May 2023 to February 2024
    query = {
        "$or": [
            # Data from the start year, starting from May
            {"year": start_year, "month_n": {"$gte": start_month}},
            # Data from the end year, up to February
            {"year": end_year, "month_n": {"$lte": end_month}},
        ]
    }

    # Handle case where start and end year are the same
    if start_year == end_year:
        query = {"year": start_year, "month_n": {"$gte": start_month, "$lte": end_month}}

    return list(collection.find(query, {"_id": 0}))


# --------------------------------------------------------------------------------------------------------------------


# retrieval by a target collection with value threshold conditions
def retrieve_by_category_value_threshold(collection_name: str, threshold_value: list, threshold_condition: str):
    financial_main_db = mongodb_atlas_client.financial_main
    collection = financial_main_db[collection_name]

    if threshold_condition == "gt":
        return list(collection.find({"value": {"$gt": threshold_value[0]}}, {"_id": 0}))
    elif threshold_condition == "lt":
        return list(collection.find({"value": {"$lt": threshold_value[0]}}, {"_id": 0}))
    elif threshold_condition == "in-between":
        return list(collection.find({"value": {"$gt": threshold_value[0], "$lt": threshold_value[1]}}, {"_id": 0}))
