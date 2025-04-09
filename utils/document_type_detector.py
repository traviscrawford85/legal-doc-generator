# utils/document_type_detector.py

import os
import yaml
import re

def load_rules(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def detect_type(text, rules):
    for category, rule in rules.items():
        for keyword in rule.get("keywords", []):
            if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
                return category
    return "Unclassified"

def detect_type_from_file(file_path, rules):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        from utils.ocr import ocr_pdf_if_needed
        ocr_result = ocr_pdf_if_needed(file_path)
        text = ocr_result["text"]
    elif ext == ".txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        return {"file": file_path, "type": "Unsupported"}

    doc_type = detect_type(text or "", rules)
    return {"file": file_path, "type": doc_type}

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Classify documents by type using YAML rules.")
    parser.add_argument("input", help="Path to a .pdf, .txt, or folder of files")
    parser.add_argument("--rules", default="utils/document_rules.yml", help="Path to YAML rules file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    rules = load_rules(args.rules)
    inputs = []

    if os.path.isfile(args.input):
        inputs = [args.input]
    elif os.path.isdir(args.input):
        inputs = [
            os.path.join(args.input, f)
            for f in os.listdir(args.input)
            if f.lower().endswith((".pdf", ".txt"))
        ]
    else:
        print("❌ Input not found.")
        exit(1)

    results = [detect_type_from_file(f, rules) for f in inputs]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(f"{result['file']} => {result['type']}")
