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
