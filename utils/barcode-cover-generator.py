import os
import argparse
import re
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import inch

def generate_cover(display_number, output_dir):
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', display_number)
    filename = f"Clio_Barcode_Cover_{safe_name}.pdf"
    path = os.path.join(output_dir, filename)
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "Clio Matter Barcode Cover Sheet")

    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, height - 1.5 * inch, f"Matter Display Number: {display_number}")
    barcode = code128.Code128(display_number, barHeight=0.5 * inch, barWidth=1.2)
    barcode.drawOn(c, 1 * inch, height - 2.25 * inch)

    doc_types = [
        "Pleadings", "Correspondence", "Medical Records", "Invoices", "Discovery",
        "Checks", "Receipts", "Medical Bill", "Deposition", "Contract",
        "Settlement Agreement", "Settlment Check", "Expert Report",  "Other"
    ]
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, height - 3 * inch, "Document Type:")
    c.setFont("Helvetica", 12)
    cols = 3
    col_width = 2.2 * inch
    row_height = 0.3 * inch
    start_x = 1.2 * inch
    start_y = height - 3.4 * inch

    for i, doc_type in enumerate(doc_types):
        col = i % cols
        row = i // cols
        x = start_x + col * col_width
        y = start_y - row * row_height
        c.drawString(x, y, f"[  ] {doc_type}")


    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, height - 6.2 * inch, "Date: ____________________")
    c.drawString(1 * inch, height - 6.8 * inch, "Notes:")
    c.rect(1 * inch, height - 9.5 * inch, 6 * inch, 2.5 * inch)

    c.save()
    print(f"Saved: {path}")

def main():
    parser = argparse.ArgumentParser(description="Generate Clio barcode cover sheets.")
    parser.add_argument("--matter", help="Single Matter Display Number input")
    parser.add_argument("--csv", help="CSV file with Matter Display Numbers")
    parser.add_argument("--excel", help="Excel file with Matter Display Numbers")
    parser.add_argument("--column", default="Matter Display Number", help="Column name for matter numbers")
    parser.add_argument("--output", default=".", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.matter:
        generate_cover(args.matter.strip(), args.output)
    elif args.csv:
        df = pd.read_csv(args.csv)
        for display_number in df[args.column].dropna().astype(str):
            generate_cover(display_number.strip(), args.output)
    elif args.excel:
        df = pd.read_excel(args.excel)
        for display_number in df[args.column].dropna().astype(str):
            generate_cover(display_number.strip(), args.output)
    else:
        print("Please provide --matter, --csv, or --excel input.")

if __name__ == "__main__":
    main()
