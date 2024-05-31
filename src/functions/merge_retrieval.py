from src.config.service_provider_init import visor_guys_merge_client
from src.utils.merge_data_process import (
    transform_invoices,
    filter_invoices_by_date,
    transform_balance_sheets,
    filter_balance_sheets_by_date,
    transform_cash_flows_sheets,
    filter_cash_flows_by_date,
    transform_expenses,
    filter_expenses_by_date,
    transform_income_statements,
    filter_income_statements_by_date,
)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for invoice data retrieval


def retrieve_client_invoices_data(start_date=None, end_date=None):
    # we first fetch all pages of invoices data for Visor Guys through merge API and then transform the raw data
    cursor = ""
    full_transformed_result = []
    while cursor != None:
        current_page_raw_retrieved_result = visor_guys_merge_client.accounting.invoices.list(
            cursor=cursor,
            expand="company",
            page_size=100,
        )
        current_page_transformed_result = transform_invoices(current_page_raw_retrieved_result)
        cursor = current_page_raw_retrieved_result.next
        full_transformed_result.extend(current_page_transformed_result)

    # we then filter the transformed data based on the date range provided from user query
    retrieval_result = filter_invoices_by_date(
        full_transformed_items=full_transformed_result,
        start_date=start_date,
        end_date=end_date,
    )

    return {"category": "invoices", "retrieval_result": retrieval_result}


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for balance sheet data retrieval


def retrieve_client_balance_sheets_data(start_date=None, end_date=None):
    # we first fetch all pages of balance sheets data for Visor Guys through merge API and then transform the raw data
    cursor = ""
    full_transformed_result = []
    while cursor != None:
        current_page_raw_retrieved_result = visor_guys_merge_client.accounting.balance_sheets.list(
            cursor=cursor,
            expand="company",
            page_size=100,
        )
        current_page_transformed_result = transform_balance_sheets(current_page_raw_retrieved_result)
        full_transformed_result.extend(current_page_transformed_result)
        cursor = current_page_raw_retrieved_result.next

    # we then filter the transformed data based on the date range provided from user query
    retrieval_result = filter_balance_sheets_by_date(
        full_transformed_items=full_transformed_result,
        start_date=start_date,
        end_date=end_date,
    )

    return {"category": "balanceSheets", "retrieval_result": retrieval_result}


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for cash flow data retrieval


def retrieve_client_cash_flows_data(start_date=None, end_date=None):
    # we first fetch all pages of balance sheets data for Visor Guys through merge API and then transform the raw data
    cursor = ""
    full_transformed_result = []
    while cursor != None:
        current_page_raw_retrieved_result = visor_guys_merge_client.accounting.cash_flow_statements.list(
            cursor=cursor,
            expand="company",
            page_size=100,
        )
        current_page_transformed_result = transform_cash_flows_sheets(current_page_raw_retrieved_result)
        full_transformed_result.extend(current_page_transformed_result)
        cursor = current_page_raw_retrieved_result.next

    # we then filter the transformed data based on the date range provided from user query

    retrieval_result = filter_cash_flows_by_date(
        full_transformed_items=full_transformed_result,
        start_date=start_date,
        end_date=end_date,
    )

    return {"category": "cashFlows", "retrieval_result": retrieval_result}


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
#  for expense data retrieval


def retrieve_client_expenses_data(start_date=None, end_date=None):
    # we first fetch all pages of balance sheets data for Visor Guys through merge API and then transform the raw data
    cursor = ""
    full_transformed_result = []
    while cursor != None:
        current_page_raw_retrieved_result = visor_guys_merge_client.accounting.expenses.list(
            cursor=cursor,
            expand="company",
            page_size=100,
        )
        current_page_transformed_result = transform_expenses(current_page_raw_retrieved_result)
        full_transformed_result.extend(current_page_transformed_result)
        cursor = current_page_raw_retrieved_result.next

    # we then filter the transformed data based on the date range provided from user query
    retrieval_result = filter_expenses_by_date(
        full_transformed_items=full_transformed_result,
        start_date=start_date,
        end_date=end_date,
    )

    return {"category": "expenses", "retrieval_result": retrieval_result}


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for income statement data retrieval


def retrieve_client_income_statements_data(start_date=None, end_date=None):
    # we first fetch all pages of balance sheets data for Visor Guys through merge API and then transform the raw data
    cursor = ""
    full_transformed_result = []
    while cursor != None:
        current_page_raw_retrieved_result = visor_guys_merge_client.accounting.income_statements.list(
            cursor=cursor,
            expand="company",
            page_size=100,
        )
        current_page_transformed_result = transform_income_statements(current_page_raw_retrieved_result)
        full_transformed_result.extend(current_page_transformed_result)
        cursor = current_page_raw_retrieved_result.next

    # we then filter the transformed data based on the date range provided from user query
    retrieval_result = filter_income_statements_by_date(
        full_transformed_items=full_transformed_result,
        start_date=start_date,
        end_date=end_date,
    )

    return {"category": "incomeStatements", "retrieval_result": retrieval_result}
