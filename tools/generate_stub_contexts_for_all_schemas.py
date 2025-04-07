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
    parser = argparse.ArgumentParser(description="Generate stub context YAML files from all schema files in a folder")
    parser.add_argument("schema_folder", help="Folder containing .schema.yml files")
    parser.add_argument("--output", help="Folder to save context files", default="content")
    args = parser.parse_args()

    schema_folder = Path(args.schema_folder)
    output_folder = Path(args.output)
    output_folder.mkdir(parents=True, exist_ok=True)

    for schema_file in schema_folder.glob("*.schema.yml"):
        with open(schema_file, "r", encoding="utf-8") as f:
            schema = yaml.safe_load(f)

        required_fields = schema.get("required_fields", [])
        stub_context = build_stub_context(required_fields)

        output_path = output_folder / f"{schema_file.stem}.context.yml"
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(stub_context, f, sort_keys=False)
        print(f"✅ Stub context saved to: {output_path}")

if __name__ == "__main__":
    main()