#!/usr/bin/env python

import argparse
import yaml
from pathlib import Path
from validators.schema_validator import (validate_schema_against_context, find_extra_fields_in_context)
from validators.template_validator import validate_template_against_context

def load_yaml(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_template(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(
        description="Validate Jinja Template, Matter Context, and Document Schema."
    )
    parser.add_argument(
        "--schema", required=True, help="Path to the document schema YAML file (e.g., pip_lor_schema.yml)"
    )
    parser.add_argument(
        "--context", required=True, help="Path to the matter context YAML file (e.g., pip_lor_context.yml)"
    )
    parser.add_argument(
        "--template", required=True, help="Path to the Jinja template file (e.g., pip_letter_of_representation.jinja)"
    )
    
    args = parser.parse_args()

    schema_path = Path(args.schema)
    context_path = Path(args.context)
    template_path = Path(args.template)
    
    try:
        schema = load_yaml(schema_path)
        context = load_yaml(context_path)
        template_str = load_template(template_path)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # Validate Schema vs. Context
    missing_fields = validate_schema_against_context(schema, context)
    if missing_fields:
        print("❌ Schema Validation Failed. Missing fields in context:")
        for field in missing_fields:
            print(f"  - {field}")
    else:
        print("✅ Schema Validation Passed: All required fields exist in the context.")

    # Check for extra fields in context
    extra_fields = find_extra_fields_in_context(schema, context)
    if extra_fields:
        print("\n⚠️  Extra fields found in context (not in schema):")
        for field in extra_fields:
            print(f"  - {field}")
    else:
        print("✅ No extra fields in context.")

    # Validate Template vs. Context
    missing_vars = validate_template_against_context(template_str, context)
    if missing_vars:
        print("\n❌ Template Validation Failed. Missing variables in context:")
        for var in missing_vars:
            print(f"  - {var}")
    else:
        print("✅ Template Validation Passed: All template variables exist in the context.")

if __name__ == "__main__":
    main()

