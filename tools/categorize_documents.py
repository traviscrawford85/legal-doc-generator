import argparse
import os
import re
import shutil
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

# Load mapping from config file
def load_category_map(path="category_map.yml"):
    if not Path(path).exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("map", {})

# Extract matter metadata
def extract_matter_metadata(folder_path):
    match = re.search(r"(?P<practice>.+?) - (?P<number>\d{4}-\d{5}) (?P<name>.+)$", folder_path)
    if match:
        return {
            "matter_display_number": match.group("number") + " " + match.group("name"),
            "practice_area": match.group("practice"),
            "client_name": match.group("name")
        }
    return {
        "matter_display_number": "UNKNOWN",
        "practice_area": "UNKNOWN",
        "client_name": "UNKNOWN"
    }

# Standardize folder name to Clio category
def map_folder_to_category(path, category_map):
    folder_name = Path(path).parent.name
    return category_map.get(folder_name, folder_name)

# Process folder
def categorize_documents(folder_path, output_path, category_map, filters, relocate, dry_run):
    folder = Path(folder_path)
    records = []

    for file in folder.rglob("*.*"):
        if not file.is_file() or (filters and file.suffix.lower() not in filters):
            continue

        metadata = extract_matter_metadata(file.parent.name)
        mod_time = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")
        category = map_folder_to_category(file, category_map)

        record = {
            "Original Name": file.name,
            "Modified Date": mod_time,
            "Extension": file.suffix,
            "Client": metadata["client_name"],
            "Practice Area": metadata["practice_area"],
            "Matter": metadata["matter_display_number"],
            "Category": category,
            "Original Path": str(file)
        }

        if relocate:
            dest_folder = file.parent / category
            new_path = dest_folder / file.name

            if dry_run:
                print(f"🟡 Would move: {file} → {new_path}")
                record["New Path"] = str(new_path) + " (dry run)"
            else:
                dest_folder.mkdir(exist_ok=True)
                try:
                    shutil.move(str(file), str(new_path))
                    record["New Path"] = str(new_path)
                except Exception as e:
                    record["New Path"] = f"Failed to move: {e}"

        records.append(record)

    if records:
        df = pd.DataFrame(records)
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for category, group in df.groupby("Category"):
                group.to_excel(writer, sheet_name=category[:31], index=False)
        print(f"\n📊 Categorized Excel workbook saved to: {output_path}")
        print(f"📁 Total documents processed: {len(records)}")
    else:
        print("⚠️ No supported document types found in the folder.")

# CLI
def main():
    parser = argparse.ArgumentParser(description="Categorize and optionally relocate documents by folder mapping")
    parser.add_argument("--folder", required=True, help="Path to the matter folder")
    parser.add_argument("--output", default="categorized_summary.xlsx", help="Path to save the Excel summary")
    parser.add_argument("--map", default="category_map.yml", help="Path to folder-to-category mapping YAML file")
    parser.add_argument("--types", nargs="*", default=[".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".mp4"], help="Allowed file extensions")
    parser.add_argument("--relocate", choices=["yes", "no"], default="no", help="Move files into category folders")
    parser.add_argument("--dry-run", action="store_true", help="Simulate file moves without changing anything")
    args = parser.parse_args()

    filters = [ext.lower() for ext in args.types]
    category_map = load_category_map(args.map)
    relocate_flag = args.relocate == "yes"

    categorize_documents(args.folder, args.output, category_map, filters, relocate_flag, args.dry_run)

if __name__ == "__main__":
    main()
