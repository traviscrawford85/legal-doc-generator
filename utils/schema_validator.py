import yaml

def load_schema(schema_path):
    with open(schema_path, "r") as f:
        return yaml.safe_load(f)

def flatten_keys(data, parent_key=''):
    keys = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            keys.extend(flatten_keys(v, new_key))
    else:
        keys.append(parent_key)
    return keys

def validate_context_against_schema(context, schema):
    errors = []
    present_keys = set(flatten_keys(context))
    for field in schema.get("required_fields", []):
        if field not in present_keys:
            errors.append(f"Missing required field: {field}")
    return errors
