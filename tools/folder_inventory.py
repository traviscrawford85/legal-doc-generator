import os
import argparse
from collections import defaultdict
from tabulate import tabulate

def scan_folder(path):
    folder_count = 0
    file_count = 0
    file_types = defaultdict(int)

    for root, dirs, files in os.walk(path):
        folder_count += len(dirs)
        file_count += len(files)
        for file in files:
            ext = os.path.splitext(file)[1].lower() or "no_ext"
            file_types[ext] += 1

    print(f"Total folders: {folder_count}")
    print(f"Total files: {file_count}")
    print("File types:")
    for ext, count in sorted(file_types.items()):
        print(f"  {ext}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count folders, files, and file types in a directory.")
    parser.add_argument("path", help="Path to the folder to scan")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print("Error: Path does not exist.")
    elif not os.path.isdir(args.path):
        print("Error: Path is not a folder.")
    else:
        scan_folder(args.path)

      

