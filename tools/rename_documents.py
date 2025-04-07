import argparse
import os
import re
from pathlib import Path
from datetime import datetime

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

def rename_documents(folder_path):
    folder = Path(folder_path)
    metadata = extract_matter_metadata(folder.name)
    renamed_count = 0

    for file in folder.glob("*.*"):
        if file.suffix.lower() not in ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.mp4']:
            continue

        mod_time = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")
        new_name = f"{metadata['matter_display_number']} - {file.stem} - {mod_time}{file.suffix}"
        new_path = file.parent / new_name

        try:
            os.rename(file, new_path)
            renamed_count += 1
            print(f"✅ Renamed: {file.name} -> {new_name}")
        except Exception as e:
            print(f"❌ Failed to rename {file.name}: {e}")

    print(f"\n🔁 Renamed {renamed_count} document(s).")

def main():
    parser = argparse.ArgumentParser(description="Rename documents in a matter folder using Clio naming convention")
    parser.add_argument("--folder", required=True, help="Path to the matter folder")
    args = parser.parse_args()

    rename_documents(args.folder)

if __name__ == "__main__":
    main()
