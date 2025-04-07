# 🧾 Legal Document Generator

A toolkit for automating legal document generation, classification, and template bootstrapping using DOCX, YAML, OCR, and NLP.

---

## 🚀 Key Features

### 📄 Template & Document Generator
- Convert CSV to YAML context files
- Validate Jinja templates against schemas and context
- Generate DOCX from Jinja templates

### ⚙️ Bootstrap Tools
- Extract merge fields from DOCX templates
- Auto-generate validation schemas and context stubs

### 🔍 OCR + NLP Classifier (Integrated from submodules)
- Detect and extract text from scanned PDFs and images
- Classify documents by type (e.g., "Complaint", "Motion")
- Summarize key entities (e.g., people, organizations, dates)
- Export structured results to JSON or Excel

---

## 🛠️ How to Use

### 1. Bootstrap from Templates
```bash
python tools/bootstrap_template_folder.py <TEMPLATE_FOLDER> --schemas schemas/ --contexts content/
```
Creates:
- Schema files (YAML)
- Context stubs

### 2. Validate Template Setup
```bash
python tools/validate_doc.py --schema schemas/pip_lor.schema.yml --context content/pip_lor_context.yml --template templates/pip_letter.jinja

```

### 3. Classify & Summarize Documents
```bash
python -m tools.classify_documents --folder <FOLDER> --output ocr_reports --nlp-summary
```
Options:
- `--file <FILE>` to run on a single file
- `--rename-based-on-nlp` to rename based on contents

### 4. Summarize a Folder
```bash
python tools/summarize_documents.py --folder <FOLDER> --output summary.csv
```
Or generate an Excel workbook grouped by category:
```bash
python tools/categorize_documents.py --folder <FOLDER> --output categorized_summary.xlsx
```

---

## 📦 Project Structure
```
legal-doc-generator/
├── tools/
│   ├── bootstrap_template_folder.py
│   ├── validate_doc.py
│   ├── classify_documents.py
│   ├── summarize_documents.py
│   ├── categorize_documents.py
│   └── ocr/          ← doc-ocr-clio submodule
│   └── nlp_parser/   ← nlp-legal-parser submodule
├── content/          ← YAML context files
├── schemas/          ← Schema definitions
├── templates/        ← DOCX/Jinja templates
└── requirements.txt
```

---

## 📘 CHANGELOG

### Added
- `classify_documents.py` with support for OCR/NLP analysis
- NLP summarizer + auto file renaming based on contents
- `bootstrap_template_folder.py` to generate schemas and contexts
- Excel + CSV output summaries for batch document analysis

### Fixed
- Windows path quoting issues for file/subprocess handling
- UTF-8 loading errors on DOCX templates with Clio merge fields
- Skipping unsupported file types during classification

### Improved
- `.gitignore` for clean development environments
- Submodule structure for OCR/NLP tools
- Output folder naming and error handling on file locks

---

## ✅ Next Steps
- Integrate Clio API tagging + auto-relocation
- Build a GUI or shell menu interface
- Add support for PDF categorization via Clio document types

