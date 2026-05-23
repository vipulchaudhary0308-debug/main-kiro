#!/usr/bin/env python3
"""
Build the M.Ed. Dissertation as a single Microsoft Word (.docx) file
in CCS University format:
    - Times New Roman 12 pt
    - Double-line spacing (1.5 used here for body, double-equivalent feel)
    - 1.5" left margin, 1" right/top/bottom
    - Justified body text
    - Page numbers (bottom-center)
    - Page breaks between major sections
"""

import os
import pypandoc

DISS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dissertation")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dissertation_Final.docx")

# Order of files (front matter first, then chapters)
FILES = [
    "00_front_matter.md",
    "01_chapter1_introduction.md",
    "02_chapter2_review_of_literature.md",
    "03_chapter3_methodology.md",
    "04_chapter4_analysis_interpretation.md",
    "05_chapter5_summary_findings.md",
    "06_bibliography.md",
    "07_appendices.md",
]

# Concatenate the markdown into one big buffer with hard page breaks between chapters
combined_md_path = os.path.join(DISS_DIR, "_combined.md")
with open(combined_md_path, "w", encoding="utf-8") as out:
    for i, f in enumerate(FILES):
        full = os.path.join(DISS_DIR, f)
        with open(full, "r", encoding="utf-8") as src:
            txt = src.read()
        out.write(txt)
        # Hard page break (Pandoc raw block) before next file
        if i < len(FILES) - 1:
            out.write('\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n')

# Run pandoc
extra_args = [
    "--from=markdown+pipe_tables+raw_attribute",
    "--to=docx",
    f"--output={OUT}",
    "--standalone",
    "-V", "geometry:left=1.5in,right=1in,top=1in,bottom=1in",
]

pypandoc.convert_file(
    combined_md_path,
    "docx",
    format="markdown-yaml_metadata_block+pipe_tables+raw_attribute",
    outputfile=OUT,
    extra_args=[
        "-V", "geometry:left=1.5in,right=1in,top=1in,bottom=1in",
    ],
)

# Now post-process the docx to apply CCS-Univ. formatting:
#  - All body paragraphs: Times New Roman 12, line-spacing 2.0, justified
#  - Headings: Times New Roman bold (sizes by level)
#  - Page numbers in footer (centered)
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document(OUT)

# Set page margins on all sections (CCS U: 1.5 left, 1 elsewhere)
for section in doc.sections:
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)

# Apply font + line spacing to every run / paragraph
HEADING_SIZES = {
    "Heading 1": 16,
    "Heading 2": 14,
    "Heading 3": 13,
    "Heading 4": 12,
    "Heading 5": 12,
    "Heading 6": 12,
}

for para in doc.paragraphs:
    style_name = para.style.name if para.style else ""
    if style_name in HEADING_SIZES:
        size_pt = HEADING_SIZES[style_name]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER if style_name in ("Heading 1", "Heading 2") else WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.line_spacing = 1.5
    else:
        size_pt = 12
        if para.alignment is None:
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.line_spacing = 2.0
        para.paragraph_format.space_after = Pt(6)

    for run in para.runs:
        run.font.name = "Times New Roman"
        # Ensure East-Asian font is also TNR (some systems otherwise fall back)
        rPr = run._element.get_or_add_rPr()
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rPr.insert(0, rFonts)
        rFonts.set(qn("w:ascii"), "Times New Roman")
        rFonts.set(qn("w:hAnsi"), "Times New Roman")
        rFonts.set(qn("w:cs"), "Times New Roman")
        rFonts.set(qn("w:eastAsia"), "Times New Roman")
        run.font.size = Pt(size_pt)
        if style_name in HEADING_SIZES:
            run.bold = True

# Apply font to table cells too
for table in doc.tables:
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                para.paragraph_format.line_spacing = 1.15
                for run in para.runs:
                    run.font.name = "Times New Roman"
                    rPr = run._element.get_or_add_rPr()
                    rFonts = rPr.find(qn("w:rFonts"))
                    if rFonts is None:
                        rFonts = OxmlElement("w:rFonts")
                        rPr.insert(0, rFonts)
                    rFonts.set(qn("w:ascii"), "Times New Roman")
                    rFonts.set(qn("w:hAnsi"), "Times New Roman")
                    rFonts.set(qn("w:cs"), "Times New Roman")
                    rFonts.set(qn("w:eastAsia"), "Times New Roman")
                    run.font.size = Pt(11)

# Add a centered page-number field in the footer
def add_page_number(footer):
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)

for section in doc.sections:
    add_page_number(section.footer)

doc.save(OUT)
size_kb = os.path.getsize(OUT) / 1024
print(f"OK -> {OUT}  ({size_kb:.1f} KB)")

# Cleanup the combined markdown file
os.remove(combined_md_path)
