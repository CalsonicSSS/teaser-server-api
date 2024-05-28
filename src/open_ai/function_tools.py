# ---------------------------------------------------- For Teaser -------------------------------------------------------------

retrieve_filtered_data_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_filtered_data",
        "description": (
            "Retrieves data from specified collections with filters."
            "Primarily call this function when user query either only contains collection name(s) (revenue, expense, parts_orders, working_hours) without filters, or with a filter based on year or/and month."
            "this function should always be first considered over others when the user query contains collections."
            "Example calls: retrieve_filtered_data(['revenue'], {'year': 2024})"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "collections": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of collection names, can be single or multiple within array depends which data category user wants to retrieve (e.g., ['revenue'] or ['revenue','expense'])",
                },
                "filter": {
                    "type": "object",
                    "description": (
                        "contains filter conditions based on year or/and month for the specified collection(s). e.g: if query contains 'in 2023 may', filter should gives: {'year': 2023, 'month': 'may'}; if query contains only year 'in 2024', filter should gives {'year': 2024}; if query contains multiple years 'in 2023 and 2024', it should gives {'year': {'$in': [2023, 2024]}}."
                    ),
                },
            },
            "required": ["collections", "filter"],
        },
    },
}

retrieve_data_in_date_range_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_data_in_date_range",
        "description": (
            "Retrieves data from a single collection within a specified date range. "
            "Only to call this function when the user query fully and clearly indicate a date range contains both start and end for a target collection."
            "Example call: retrieve_data_in_date_range('revenue', 2023, 5, 2024, 2)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "collection_name": {
                    "type": "string",
                    "description": "the single name of the collection (e.g., 'revenue', 'expense', 'parts_orders', or 'working_hours')",
                },
                "start_year": {
                    "type": "number",
                    "description": "Start year in number, (e.g., 2023)",
                },
                "start_month": {
                    "type": "number",
                    "description": "Start month in number, (e.g 5 for may)",
                },
                "end_year": {
                    "type": "number",
                    "description": "End year in number, (e.g., 2024)",
                },
                "end_month": {
                    "type": "number",
                    "description": "End month in number, (e.g 7 for july)",
                },
            },
            "required": ["collection_name", "start_year", "start_month", "end_year", "end_month"],
        },
    },
}
retrieve_by_category_value_threshold_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_by_category_value_threshold",
        "description": (
            "Retrieve data based on value threshold conditions for a specified collection."
            "Only to call this function when the user query contains a collection name, a threshold condition, and one or two threshold values."
            "Example calls: retrieve_by_category_value_threshold('revenue', [10000], 'gt'), retrieve_by_category_value_threshold('expense', [1000, 30000], 'in-between')."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "collection_name": {
                    "type": "string",
                    "description": "the single name of the collection (e.g., 'revenue', 'expense', 'parts_orders', or 'working_hours')",
                },
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
}


# ---------------------------------------------------- For Visor_Guys ----------------------------------------------------------


retrieve_client_invoices_data_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_client_invoices_data",
        "description": (
            "Usage: Retrieve client company invoice data within a specified date range base on 'start_date' and 'end_date' argument values."
            "When to call: Use this function when the user query specifies the intention of retrieving or asking for their company invoice related data within specific dates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": (
                        "The beginning date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data after this start date. "
                        "Leave as None if no start date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "The ending date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data before this end date. "
                        "Leave as None if no end date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
            },
            "required": [],
        },
    },
}

retrieve_client_balance_sheets_data_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_client_balance_sheets_data",
        "description": (
            "Usage: Retrieve client company balance sheet data within a specified date range base on 'start_date' and 'end_date' argument values."
            "When to call: Use this function when the user query specifies the intention of retrieving or asking for their company balance sheet related data within specific dates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": (
                        "The beginning date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data after this start date. "
                        "Leave as None if no start date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "The ending date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data before this end date. "
                        "Leave as None if no end date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
            },
            "required": [],
        },
    },
}

retrieve_client_cash_flows_data_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_client_cash_flows_data",
        "description": (
            "Usage: Retrieve client company cash flow data within a specified date range base on 'start_date' and 'end_date' argument values."
            "When to call: Use this function when the user query specifies the intention of retrieving or asking for their company cash flow related data within specific dates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": (
                        "The beginning date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data after this start date. "
                        "Leave as None if no start date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "The ending date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data before this end date. "
                        "Leave as None if no end date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
            },
            "required": [],
        },
    },
}

retrieve_client_expenses_data_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_client_expenses_data",
        "description": (
            "Usage: Retrieve client company expenses data within a specified date range base on 'start_date' and 'end_date' argument values."
            "When to call: Use this function when the user query specifies the intention of retrieving or asking for their company expenses related data within specific dates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": (
                        "The beginning date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data after this start date. "
                        "Leave as None if no start date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "The ending date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data before this end date. "
                        "Leave as None if no end date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
            },
            "required": [],
        },
    },
}

retrieve_client_income_statements_data_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_client_income_statements_data",
        "description": (
            "Usage: Retrieve client company income statement data within a specified date range base on 'start_date' and 'end_date' argument values."
            "When to call: Use this function when the user query specifies the intention of retrieving or asking for their company income statement related data within specific dates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": (
                        "The beginning date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data after this start date. "
                        "Leave as None if no start date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "The ending date within a specified date range, formatted as 'YYYY-MM-DD'. "
                        "Use to filter results to include only data before this end date. "
                        "Leave as None if no end date is specified nor needed by the user query."
                    ),
                    "default": None,
                },
            },
            "required": [],
        },
    },
}
