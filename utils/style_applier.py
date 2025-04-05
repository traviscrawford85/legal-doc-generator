from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def apply_styles(document, style_conf):
    # Set margins
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(style_conf['margin_top'])
        section.bottom_margin = Inches(style_conf['margin_bottom'])
        section.left_margin = Inches(style_conf['margin_left'])
        section.right_margin = Inches(style_conf['margin_right'])

    # Apply to each paragraph
    for paragraph in document.paragraphs:
        paragraph_format = paragraph.paragraph_format
        paragraph_format.line_spacing = style_conf['line_spacing']
        paragraph_format.space_after = Pt(style_conf['paragraph_spacing'])
        paragraph.alignment = {
            "left": WD_ALIGN_PARAGRAPH.LEFT,
            "center": WD_ALIGN_PARAGRAPH.CENTER,
            "right": WD_ALIGN_PARAGRAPH.RIGHT,
        }.get(style_conf['alignment'], WD_ALIGN_PARAGRAPH.LEFT)

        for run in paragraph.runs:
            run.font.name = style_conf['font_name']
            run.font.size = Pt(style_conf['font_size'])
            # Ensure the font is applied for East Asian languages (needed for Word)
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), style_conf['font_name'])
