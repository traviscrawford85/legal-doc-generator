# validators/schema_validator.py

def _get_value_from_context(context: dict, dotted_key: str) -> bool:
    keys = dotted_key.split(".")
    current = context
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    return True

def validate_schema_against_context(schema_dict: dict, context: dict) -> list:
    """
    Checks each required dotted-path field in the schema exists in the context.
    
    Returns:
        List of missing field paths.
    """
    required_fields = schema_dict.get("required_fields", [])
    missing = []

    for path in required_fields:
        if not _get_value_from_context(context, path):
            missing.append(path)

    return missing

def _flatten_context(context: dict, prefix="") -> list:
    """
    Recursively flattens a nested dictionary into a list of dotted paths.
    """
    paths = []
    for key, value in context.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            paths.extend(_flatten_context(value, full_key))
        else:
            paths.append(full_key)
    return paths

def find_extra_fields_in_context(schema_dict: dict, context: dict) -> list:
    """
    Returns list of context fields that are NOT in schema's required_fields.
    """
    required_fields = set(schema_dict.get("required_fields", []))
    context_fields = set(_flatten_context(context))
    extra_fields = context_fields - required_fields
    return sorted(extra_fields)

