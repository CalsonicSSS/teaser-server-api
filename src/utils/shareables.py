def merge_field_converter(field):
    result = "none" if field is None or field == "" else field
    if type(result) == str:
        result = result.lower().replace("_", " ")
    if type(result) == int or type(result) == float:
        result = str(result)
    return result
