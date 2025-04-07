import argparse
import os
import json
import re
from pathlib import Path
from tools.ocr.extract import batch_process_folder, load_field_config
from tools.nlp_parser.document_type_detector import analyze_document  # updated import
import pandas as pd

def classify_folder(folder_path=None, output_path=None, field_config_path=None, nlp_summary=False, rename=False, single_file=None):
    field_config = load_field_config(field_config_path)
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_data = []

    files = [Path(single_file)] if single_file else Path(folder_path).rglob("*.*")
    for file in files:
        if not file.suffix.lower() in ['.pdf', '.jpg', '.jpeg', '.png']:
            continue

        print(f"\n--- Processing: {file.name} ---")
        extracted_data_path = output_dir / f"{file.stem}_extracted.json"

        # OCR Field Extraction
        os.system(f'python tools/ocr/extract.py --file "{file}" --output "{output_dir}" --config "{field_config_path}"')
        if not extracted_data_path.exists():
            print(f"⚠️ No OCR data found for {file.name}.")
            continue

        # Load extracted fields
        if extracted_data_path.exists():
            with open(extracted_data_path, 'r') as f:
                ocr_data = json.load(f)
        else:
            ocr_data = {}

        record = {
            "File Name": file.name,
            "Clio Fields Found": list(ocr_data.get("clio_fields", {}).keys()),
            "Missing Fields": ocr_data.get("field_report", {}).get("missing_fields", []),
            "Path": str(file),
        }
        if nlp_summary:
            if file.suffix.lower() not in [".pdf", ".txt", ".png", ".jpg", ".jpeg"]:
                print(f"⚠️ Skipping NLP for unsupported file type: {file.suffix}")
                summary_data.append(record)
                continue  # ✅ skip before using nlp_result

            print("📘 Running NLP summarizer...")
            nlp_result = analyze_document(str(file))
            summary = nlp_result.get("summary", {})

            # Update record with NLP results
            record.update({
                "Document Type": summary.get("document_type"),
                "Earliest Date": summary.get("date_filed"),
                "Entities": ", ".join(nlp_result.get("entities", {}).get("ORG", []) + nlp_result.get("entities", {}).get("PERSON", []))
            })

            # Save structured NLP summary
            output_file = output_dir / f"{file.stem}_nlp.json"
            with open(output_file, "w") as f:
                json.dump(nlp_result, f, indent=2)

            # Optional rename
            if rename and summary.get("document_type") and summary.get("date_filed"):
                matter = extract_matter_from_path(file)
                new_name = f"{matter} - {summary['document_type']} - {summary['date_filed']}{file.suffix}"
                new_path = file.parent / new_name
                try:
                    os.rename(file, new_path)
                    record["Renamed To"] = new_path.name
                except Exception as e:
                    record["Renamed To"] = f"Failed: {e}"

        summary_data.append(record)

    # Save summary
    df = pd.DataFrame(summary_data)
    excel_out = output_dir / "document_classification_summary.xlsx"
    df.to_excel(excel_out, index=False)
    print(f"\n✅ Summary Excel saved to: {excel_out}")

def extract_matter_from_path(file_path):
    try:
        parts = Path(file_path).parts
        for part in parts:
            if re.match(r"\d{4}-\d{5}", part):
                return part
    except:
        pass
    return "UNKNOWN"

def main():
    parser = argparse.ArgumentParser(description="Classify documents using OCR + NLP")
    parser.add_argument("--folder", help="Folder containing documents to process")
    parser.add_argument("--file", help="Path to a single file to classify")
    parser.add_argument("--output", default="ocr_reports", help="Where to save extracted metadata")
    parser.add_argument("--config", default="tools/ocr/field_config.yml", help="Path to field config YAML")
    parser.add_argument("--nlp-summary", action="store_true", help="Run NLP-based document classification and tagging")
    parser.add_argument("--rename-based-on-nlp", action="store_true", help="Auto-rename documents using extracted metadata")
    args = parser.parse_args()

    if args.file:
        classify_folder(output_path=args.output, field_config_path=args.config, nlp_summary=args.nlp_summary, rename=args.rename_based_on_nlp, single_file=args.file)
    elif args.folder:
        classify_folder(args.folder, args.output, args.config, args.nlp_summary, args.rename_based_on_nlp)
    else:
        print("⚠️ Please provide either --file or --folder.")

if __name__ == "__main__":
    main()
