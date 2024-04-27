from datetime import datetime, timezone
import pandas as pd


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# for invoice data


def transform_invoices(current_page_raw_retrieved_result):
    current_page_transformed_items = []
    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "type": item.type.lower(),
            "status": item.status.lower(),
            "issueDate": item.issue_date,
            "dueDate": item.due_date,
            "currency": item.currency,
            "totalTaxAmount": item.total_tax_amount,
            "totalAmount": item.total_amount,
            "totalDiscount": item.total_discount,
            "balance": item.balance,
        }

        # Handle multiple lines in each invoice line item
        full_line_item_desc = ""
        for line_item in item.line_items:
            full_line_item_desc += f"description: {line_item.description} (unit price: {line_item.unit_price}, quantity: {line_item.quantity}, total:{line_item.total_amount})\n\n"
        current_page_transformed_item["lineItems"] = full_line_item_desc

        current_page_transformed_items.append(current_page_transformed_item)
    return current_page_transformed_items


# we have to use original datetime object to compare with the datetime object and then convert it to string
def filter_invoice_by_date(full_transformed_items, start_date=None, end_date=None):
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
            "name": item.name,
            "currency": item.currency,
            "date": item.date,
            "netAssets": "none" if item.net_assets == None else item.net_assets,
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

        current_page_transformed_item["assets"] = "none" if assets == "" else assets
        current_page_transformed_item["liabilities"] = "none" if liabilities == "" else liabilities
        current_page_transformed_item["equity"] = "none" if equity == "" else equity
        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


def filter_balance_sheet_by_date(full_transformed_items, start_date=None, end_date=None):
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


def transform_cash_flow_sheets(current_page_raw_retrieved_result):
    current_page_transformed_items = []
    for item in current_page_raw_retrieved_result.results:
        current_page_transformed_item = {
            "name": item.name,
            "currency": item.currency,
            "startPeriod": item.start_period,
            "endPeriod": item.end_period,
            "cashAtBeginningOfPeriod": item.cash_at_beginning_of_period,
            "cashAtEndOfPeriod": item.cash_at_end_of_period,
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

        current_page_transformed_item["operatingActivities"] = "none" if operating_activities == "" else operating_activities
        current_page_transformed_item["investingActivities"] = "none" if investing_activities == "" else investing_activities
        current_page_transformed_item["financingActivities"] = "none" if financing_activities == "" else financing_activities
        current_page_transformed_items.append(current_page_transformed_item)

    return current_page_transformed_items


def filter_cash_flow_by_date(full_transformed_items, start_date=None, end_date=None):
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
            "transactionDate": item.transaction_date,
            "totalAmount": item.total_amount,
            "currency": item.currency,
            "account": "none" if item.account == None else item.account,
            "subTotal": item.sub_total,
            "totalTaxAmount": item.total_tax_amount,
            "contact": "none" if item.contact == None else item.contact,
            "company": "none" if item.company == None else item.company,
            "memo": "none" if item.memo == None else item.memo,
        }

        full_line_item_desc = ""
        for line_item in item.lines:
            full_line_item_desc += f"net amount: {line_item.net_amount} contact: {line_item.contact} company: {line_item.company} description: {line_item.description}\n\n"
        current_page_transformed_item["lineItems"] = full_line_item_desc

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
