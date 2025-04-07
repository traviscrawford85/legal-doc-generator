import argparse
import yaml
from pathlib import Path

def flatten_keys(data, prefix=""):
    paths = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            paths.extend(flatten_keys(value, full_key))
        else:
            paths.append(full_key)
    return paths

def convert_nested_schema_to_required_fields(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    schema_name = schema.get("schema", "unnamed_schema")

    # Remove top-level metadata keys
    nested_part = {k: v for k, v in schema.items() if k != "schema"}

    # Flatten required field paths
    required_fields = flatten_keys(nested_part)

    flat_schema = {
        "schema": schema_name,
        "required_fields": sorted(required_fields)
    }

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(flat_schema, f, sort_keys=False)
    print(f"✅ Converted schema saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert nested YAML schema to flat required_fields format.")
    parser.add_argument("input", help="Input nested schema YAML file")
    parser.add_argument("-o", "--output", help="Output YAML file", required=False)

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}_flat.yml")

    convert_nested_schema_to_required_fields(input_path, output_path)
