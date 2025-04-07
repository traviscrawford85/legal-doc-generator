import csv
import json
import yaml
import argparse
from pathlib import Path
from typing import Union

def safe_nested_set(root, keys, value):
    """Recursively build nested dictionary with conflict resolution."""
    current = root
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            current[key] = value
        else:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                current[key] = {"_value": current[key]}
            current = current[key]

def csv_to_structured(input_csv: Union[str, Path], output_path: Union[str, Path] = None, fmt: str = "yaml"):
    context = {}
    with open(input_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_field = row.get("Merge Field", "")
            if not isinstance(raw_field, str):
                continue
            field = raw_field.strip(" <>")
            value = row.get("Value", "")
            keys = field.split(".")
            safe_nested_set(context, keys, value)

    # Serialize to desired format
    if fmt.lower() == "yaml":
        result = yaml.dump(context, sort_keys=False, allow_unicode=True)
        suffix = ".yml"
    elif fmt.lower() == "json":
        result = json.dumps(context, indent=2)
        suffix = ".json"
    else:
        raise ValueError("Format must be 'yaml' or 'json'")

    # Save if output path is provided
    if output_path:
        output_path = Path(output_path).with_suffix(suffix)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Saved to: {output_path}")
    else:
        print(result)

    return context

# Example usage:
# csv_to_structured("MergeFields.csv", "pip_lor_context", fmt="yaml")
