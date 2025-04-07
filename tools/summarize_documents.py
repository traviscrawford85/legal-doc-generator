import argparse
import os
import csv
import re
from pathlib import Path
from datetime import datetime
import pandas as pd

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

def guess_category_from_folder(path):
    parent = Path(path).parent
    return parent.name if parent.name.lower() not in ["open", "closed"] else "Uncategorized"

def summarize_file(file_path, output_path, filters):
    file = Path(file_path)
    if filters and file.suffix.lower() not in filters:
        print("⚠️ File type not in allowed filters. Skipping.")
        return

    metadata = extract_matter_metadata(file.parent.name)
    mod_time = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")

    record = {
        "Original Name": file.name,
        "Modified Date": mod_time,
        "Extension": file.suffix,
        "Client": metadata["client_name"],
        "Practice Area": metadata["practice_area"],
        "Matter": metadata["matter_display_number"],
        "Category": guess_category_from_folder(file)
    }

    df = pd.DataFrame([record])
    df.to_excel(output_path, index=False)
    print(f"\n📊 Summary saved to: {output_path}")
    print("📁 1 document processed.")

def summarize_folder(folder_path, output_path, filters):
    folder = Path(folder_path)
    records = []

    for file in folder.rglob("*.*"):
        if filters and file.suffix.lower() not in filters:
            continue

        metadata = extract_matter_metadata(file.parent.name)
        mod_time = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")

        records.append({
            "Original Name": file.name,
            "Modified Date": mod_time,
            "Extension": file.suffix,
            "Client": metadata["client_name"],
            "Practice Area": metadata["practice_area"],
            "Matter": metadata["matter_display_number"],
            "Category": guess_category_from_folder(file)
        })

    if records:
        df = pd.DataFrame(records)
        df.sort_values(by=["Matter", "Category", "Modified Date"], inplace=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for category, group in df.groupby("Category"):
                group.to_excel(writer, sheet_name=category[:31], index=False)

        print(f"\n📊 Summary grouped by category saved to: {output_path}")
        print(f"📁 Total documents processed: {len(records)}")
    else:
        print("⚠️ No supported document types found in the folder.")

def main():
    parser = argparse.ArgumentParser(description="Summarize files in a matter folder or single file")
    parser.add_argument("--folder", help="Path to the matter folder")
    parser.add_argument("--file", help="Path to a single file to summarize")
    parser.add_argument("--output", default="summary_report.xlsx", help="Path to save the summary Excel file")
    parser.add_argument("--types", nargs="*", default=[".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".mp4"], help="List of allowed file extensions")
    args = parser.parse_args()

    filters = [ext.lower() for ext in args.types]

    if args.file:
        summarize_file(args.file, args.output, filters)
    elif args.folder:
        summarize_folder(args.folder, args.output, filters)
    else:
        print("⚠️ Please provide either --folder or --file argument.")

if __name__ == "__main__":
    main()
