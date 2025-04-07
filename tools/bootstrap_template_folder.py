import argparse
import subprocess
from pathlib import Path


def run_extract_schemas(template_dir, schema_dir):
    print("\n🔍 Extracting schemas from templates...")
    subprocess.run([
        "python",
        "tools/extract_all_schemas_from_folder.py",
        str(template_dir),
        "--output",
        str(schema_dir)
    ], check=True)


def run_generate_contexts(schema_dir, context_dir):
    print("\n📦 Generating stub contexts from schemas...")
    subprocess.run([
        "python",
        "tools/generate_stub_contexts_for_all_schemas.py",
        str(schema_dir),
        "--output",
        str(context_dir)
    ], check=True)


def main():
    parser = argparse.ArgumentParser(description="Bootstrap full schema and context set from DOCX templates")
    parser.add_argument("templates", help="Folder containing .docx templates")
    parser.add_argument("--schemas", help="Folder to save generated schema files", default="schemas")
    parser.add_argument("--contexts", help="Folder to save generated context files", default="content")
    args = parser.parse_args()

    template_dir = Path(args.templates)
    schema_dir = Path(args.schemas)
    context_dir = Path(args.contexts)

    run_extract_schemas(template_dir, schema_dir)
    run_generate_contexts(schema_dir, context_dir)

    print("\n✅ Bootstrapping complete! You now have:")
    print(f"- Schemas in: {schema_dir.resolve()}")
    print(f"- Contexts in: {context_dir.resolve()}")


if __name__ == "__main__":
    main()