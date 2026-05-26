#!/usr/bin/env python3
"""
Build the M.Ed. Dissertation as a single Microsoft Word (.docx) file
in CCS University format:
  - Times New Roman 12 pt body
  - 1.5-line spacing for body, 1.15 for tables
  - 1.5" left margin, 1" right / top / bottom
  - Justified body text
  - Centred page numbers in footer
  - Hard page-breaks between major sections
"""

import os
import pypandoc
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DISS = os.path.join(BASE, "dissertation")
OUT  = os.path.join(BASE, "Dissertation_Final.docx")
TMP  = os.path.join(DISS, "_combined.md")

# ── ordered source files ───────────────────────────────────────────────────
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

PAGE_BREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'


def strip_yaml_front_matter(text: str) -> str:
    """Remove a leading YAML front-matter block (--- ... ---) if present."""
    stripped = text.lstrip()
    if stripped.startswith("---"):
        # find the closing ---
        end = stripped.find("\n---", 3)
        if end != -1:
            return stripped[end + 4:].lstrip()
    return text


# ── 1. concatenate markdown ────────────────────────────────────────────────
print("Concatenating markdown files …")
with open(TMP, "w", encoding="utf-8") as out:
    for i, fname in enumerate(FILES):
        path = os.path.join(DISS, fname)
        with open(path, "r", encoding="utf-8") as src:
            content = src.read()
        content = strip_yaml_front_matter(content)
        out.write(content)
        if i < len(FILES) - 1:
            out.write(PAGE_BREAK)

# ── 2. pandoc → docx ──────────────────────────────────────────────────────
print("Running pandoc …")
pypandoc.convert_file(
    TMP,
    "docx",
    format="markdown-yaml_metadata_block+pipe_tables+raw_attribute",
    outputfile=OUT,
    extra_args=["--standalone", "--wrap=none"],
)

# ── 3. post-process with python-docx ──────────────────────────────────────
print("Post-processing formatting …")
doc = Document(OUT)

# — page margins —
for section in doc.sections:
    section.left_margin   = Inches(1.5)
    section.right_margin  = Inches(1.0)
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)

HEADING_SIZES = {
    "Heading 1": 16,
    "Heading 2": 14,
    "Heading 3": 13,
    "Heading 4": 12,
    "Heading 5": 12,
    "Heading 6": 12,
}

def set_tnr(run, pt):
    run.font.name = "Times New Roman"
    run.font.size = Pt(pt)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")

# — paragraphs —
for para in doc.paragraphs:
    sname = para.style.name if para.style else ""
    if sname in HEADING_SIZES:
        pt = HEADING_SIZES[sname]
        para.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
            if sname in ("Heading 1", "Heading 2")
            else WD_ALIGN_PARAGRAPH.LEFT
        )
        pf = para.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        for run in para.runs:
            set_tnr(run, pt)
            run.bold = True
    else:
        pt = 12
        if para.alignment is None:
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = para.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_after = Pt(6)
        for run in para.runs:
            set_tnr(run, pt)

# — tables —
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                pf = para.paragraph_format
                pf.space_after = Pt(2)
                pf.space_before = Pt(2)
                for run in para.runs:
                    set_tnr(run, 11)

# — centred page numbers in footer —
def add_page_number(footer):
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    for tag, text in [
        ("w:fldChar",   {"w:fldCharType": "begin"}),
        ("w:instrText", " PAGE "),
        ("w:fldChar",   {"w:fldCharType": "end"}),
    ]:
        el = OxmlElement(tag)
        if isinstance(text, dict):
            for k, v in text.items():
                el.set(qn(k), v)
            if tag == "w:instrText":
                el.set(qn("xml:space"), "preserve")
                el.text = " PAGE "
        else:
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)
    set_tnr(run, 11)

for section in doc.sections:
    add_page_number(section.footer)

doc.save(OUT)
size_kb = os.path.getsize(OUT) / 1024
print(f"\n✓  Saved → {OUT}  ({size_kb:.1f} KB)")

# — cleanup —
os.remove(TMP)
print("Temporary combined file removed.")
