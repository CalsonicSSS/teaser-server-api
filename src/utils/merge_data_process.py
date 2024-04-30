from datetime import datetime, timezone
from src.utils.shareables import merge_field_converter


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for invoice data


def transform_invoices(current_page_raw_retrieved_result):
    current_page_transformed_items = []
    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "type": merge_field_converter(item.type),
            "status": merge_field_converter(item.status),
            "number": merge_field_converter(item.number),
            "issueDate": merge_field_converter(item.issue_date),
            "dueDate": merge_field_converter(item.due_date),
            "paidOnDate": merge_field_converter(item.paid_on_date),
            "company": merge_field_converter(item.company),
            "memo": merge_field_converter(item.memo),
            "contact": merge_field_converter(item.contact),
            "currency": merge_field_converter(item.currency),
            "totalTaxAmount": merge_field_converter(item.total_tax_amount),
            "totalAmount": merge_field_converter(item.total_amount),
            "totalDiscount": merge_field_converter(item.total_discount),
            "balance": merge_field_converter(item.balance),
        }

        # Handle multiple lines in each invoice line item
        full_line_item_desc = ""
        for line_item in item.line_items:
            full_line_item_desc += f"""description: {line_item.description} (unit price: {line_item.unit_price}, quantity: {line_item.quantity}, total:{line_item.total_amount})\n\n"""

        current_page_transformed_item["lineItems"] = merge_field_converter(full_line_item_desc)
        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


# we have to use original datetime object to compare with the datetime object and then convert it to string
def filter_invoices_by_date(full_transformed_items, start_date=None, end_date=None):
    filtered_items = []

    for item in full_transformed_items:
        # Filtering between two dates
        if start_date and end_date:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if start_date_dt <= item["issueDate"] <= end_date_dt:
                item["issueDate"] = item["issueDate"].strftime("%Y-%m-%d")
                item["dueDate"] = item["dueDate"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        # Filtering after a specific date
        elif start_date:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)

            if item["issueDate"] >= start_date_dt:
                item["issueDate"] = item["issueDate"].strftime("%Y-%m-%d")
                item["dueDate"] = item["dueDate"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        # Filtering before a specific date
        elif end_date:
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if item["issueDate"] <= end_date_dt:
                item["issueDate"] = item["issueDate"].strftime("%Y-%m-%d")
                item["dueDate"] = item["dueDate"].strftime("%Y-%m-%d")
                filtered_items.append(item)

    return filtered_items


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for balance sheet data


def transform_balance_sheets(current_page_raw_retrieved_result):
    current_page_transformed_items = []

    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "name": merge_field_converter(item.name),
            "currency": merge_field_converter(item.currency),
            "date": merge_field_converter(item.date),
            "netAssets": merge_field_converter(item.net_assets),
        }

        # handle each line item in each asset, liability, and equity
        assets = ""
        for line_item in item.assets:
            assets += f"name: {line_item.name} value: {line_item.value}\n\n"

        liabilities = ""
        for line_item in item.liabilities:
            liabilities += f"name: {line_item.name} value: {line_item.value}\n\n"

        equity = ""
        for line_item in item.equity:
            equity += f"name: {line_item.name} value: {line_item.value}\n\n"

        current_page_transformed_item["assets"] = merge_field_converter(assets)
        current_page_transformed_item["liabilities"] = merge_field_converter(liabilities)
        current_page_transformed_item["equity"] = merge_field_converter(equity)

        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


def filter_balance_sheets_by_date(full_transformed_items, start_date=None, end_date=None):
    filtered_items = []

    for item in full_transformed_items:
        if start_date and end_date:  # Filtering between two dates
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if start_date_dt <= item["date"] <= end_date_dt:
                item["date"] = item["date"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif start_date:  # Filtering after a specific date
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)

            if item["date"] >= start_date_dt:
                item["date"] = item["date"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif end_date:  # Filtering before a specific date
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if item["date"] <= end_date_dt:
                item["date"] = item["date"].strftime("%Y-%m-%d")
                filtered_items.append(item)

    return filtered_items


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for cash flow data


def transform_cash_flows_sheets(current_page_raw_retrieved_result):
    current_page_transformed_items = []
    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "name": merge_field_converter(item.name),
            "currency": merge_field_converter(item.currency),
            "startPeriod": merge_field_converter(item.start_period),
            "endPeriod": merge_field_converter(item.end_period),
            "cashAtBeginningOfPeriod": merge_field_converter(item.cash_at_beginning_of_period),
            "cashAtEndOfPeriod": merge_field_converter(item.cash_at_end_of_period),
        }

        # handle each line item in each asset, liability, and equity
        operating_activities = ""
        for line_item in item.operating_activities:
            operating_activities += f"name: {line_item.name} value: {line_item.value}\n\n"
        investing_activities = ""
        for line_item in item.investing_activities:
            investing_activities += f"name: {line_item.name} value: {line_item.value}\n\n"
        financing_activities = ""
        for line_item in item.financing_activities:
            financing_activities += f"name: {line_item.name} value: {line_item.value}\n\n"

        current_page_transformed_item["operatingActivities"] = merge_field_converter(operating_activities)
        current_page_transformed_item["investingActivities"] = merge_field_converter(investing_activities)
        current_page_transformed_item["financingActivities"] = merge_field_converter(financing_activities)
        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


def filter_cash_flows_by_date(full_transformed_items, start_date=None, end_date=None):
    filtered_items = []

    for item in full_transformed_items:
        if start_date and end_date:  # Filtering between two dates
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if start_date_dt <= item["startPeriod"] <= end_date_dt:
                item["startPeriod"] = item["startPeriod"].strftime("%Y-%m-%d")
                item["endPeriod"] = item["endPeriod"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif start_date:  # Filtering after a specific date
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)

            if item["startPeriod"] >= start_date_dt:
                item["startPeriod"] = item["startPeriod"].strftime("%Y-%m-%d")
                item["endPeriod"] = item["endPeriod"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif end_date:  # Filtering before a specific date
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if item["startPeriod"] <= end_date_dt:
                item["startPeriod"] = item["startPeriod"].strftime("%Y-%m-%d")
                item["endPeriod"] = item["endPeriod"].strftime("%Y-%m-%d")
                filtered_items.append(item)

    return filtered_items


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for expenses data


def transform_expenses(current_page_raw_retrieved_result):
    current_page_transformed_items = []
    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "transactionDate": merge_field_converter(item.transaction_date),
            "totalAmount": merge_field_converter(item.total_amount),
            "currency": merge_field_converter(item.currency),
            "account": merge_field_converter(item.account),
            "subTotal": merge_field_converter(item.sub_total),
            "totalTaxAmount": merge_field_converter(item.total_tax_amount),
            "contact": merge_field_converter(item.contact),
            "company": merge_field_converter(item.company),
            "memo": merge_field_converter(item.memo),
        }

        full_line_item_desc = ""
        for line_item in item.lines:
            full_line_item_desc += f"net amount: {line_item.net_amount} contact: {line_item.contact} company: {line_item.company} description: {line_item.description}\n\n"

        current_page_transformed_item["lineItems"] = merge_field_converter(full_line_item_desc)
        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


def filter_expenses_by_date(full_transformed_items, start_date=None, end_date=None):
    filtered_items = []
    for item in full_transformed_items:
        if start_date and end_date:  # Filtering between two dates
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if start_date_dt <= item["transactionDate"] <= end_date_dt:
                item["transactionDate"] = item["transactionDate"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif start_date:  # Filtering after a specific date
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)

            if item["transactionDate"] >= start_date_dt:
                item["transactionDate"] = item["transactionDate"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif end_date:  # Filtering before a specific date
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if item["transactionDate"] <= end_date_dt:
                item["transactionDate"] = item["transactionDate"].strftime("%Y-%m-%d")
                filtered_items.append(item)

    return filtered_items


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for income statement data


def transform_income_statements(current_page_raw_retrieved_result):
    current_page_transformed_items = []
    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "name": merge_field_converter(item.name),
            "currency": merge_field_converter(item.currency),
            "company": merge_field_converter(item.company),
            "startPeriod": merge_field_converter(item.start_period),
            "endPeriod": merge_field_converter(item.end_period),
            "grossProfit": merge_field_converter(item.gross_profit),
            "netIncome": merge_field_converter(item.net_income),
            "netOperatingIncome": merge_field_converter(item.net_operating_income),
        }

        # handle each line item in income, cost of sales, operating expenses, and non-operating expenses
        incomes = ""
        for line_item in item.income:
            incomes += f"name: {line_item.name} value: {line_item.value}\n\n"

        cost_of_sales = ""
        for line_item in item.cost_of_sales:
            cost_of_sales += f"name: {line_item.name} value: {line_item.value}\n\n"

        operating_expenses = ""
        for line_item in item.operating_expenses:
            operating_expenses += f"name: {line_item.name} value: {line_item.value}\n\n"

        non_operating_expenses = ""
        for line_item in item.non_operating_expenses:
            non_operating_expenses += f"name: {line_item.name} value: {line_item.value}\n\n"

        current_page_transformed_item["incomes"] = merge_field_converter(incomes)
        current_page_transformed_item["costOfSales"] = merge_field_converter(cost_of_sales)
        current_page_transformed_item["operatingExpenses"] = merge_field_converter(operating_expenses)
        current_page_transformed_item["nonOperatingExpenses"] = merge_field_converter(non_operating_expenses)

        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


def filter_income_statements_by_date(full_transformed_items, start_date=None, end_date=None):
    filtered_items = []
    for item in full_transformed_items:
        if start_date and end_date:  # Filtering between two dates
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if start_date_dt <= item["startPeriod"] <= end_date_dt:
                item["startPeriod"] = item["startPeriod"].strftime("%Y-%m-%d")
                item["endPeriod"] = item["endPeriod"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif start_date:  # Filtering after a specific date
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_date_dt = start_date_dt.replace(tzinfo=timezone.utc)

            if item["startPeriod"] >= start_date_dt:
                item["startPeriod"] = item["startPeriod"].strftime("%Y-%m-%d")
                item["endPeriod"] = item["endPeriod"].strftime("%Y-%m-%d")
                filtered_items.append(item)

        elif end_date:  # Filtering before a specific date
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_date_dt = end_date_dt.replace(tzinfo=timezone.utc)

            if item["startPeriod"] <= end_date_dt:
                item["startPeriod"] = item["startPeriod"].strftime("%Y-%m-%d")
                item["endPeriod"] = item["endPeriod"].strftime("%Y-%m-%d")
                filtered_items.append(item)

    return filtered_items
