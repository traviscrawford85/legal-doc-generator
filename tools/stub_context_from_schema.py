import argparse
import yaml
from pathlib import Path

def build_stub_context(required_fields):
    context = {}
    for path in required_fields:
        keys = path.split(".")
        current = context
        for i, key in enumerate(keys):
            if key not in current:
                if i == len(keys) - 1:
                    current[key] = ""
                else:
                    current[key] = {}
            elif not isinstance(current[key], dict):
                current[key] = {"_value": current[key]}
            current = current[key]
    return context

def main():
    parser = argparse.ArgumentParser(description="Generate a stub context YAML from a schema file")
    parser.add_argument("schema", help="Path to the schema YAML file")
    parser.add_argument("-o", "--output", help="Output path for context YAML", required=False)
    args = parser.parse_args()

    schema_path = Path(args.schema)
    output_path = Path(args.output) if args.output else schema_path.with_name("stub_context.yml")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    required_fields = schema.get("required_fields", [])
    stub_context = build_stub_context(required_fields)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(stub_context, f, sort_keys=False)

    print(f"✅ Stub context saved to: {output_path}")

if __name__ == "__main__":
    main()