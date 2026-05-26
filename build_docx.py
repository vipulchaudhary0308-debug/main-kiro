#!/usr/bin/env python3
"""
Build complete M.Ed. Dissertation DOCX for Vipul Chaudhary
CCSU / Meerut College format
- Times New Roman, 12pt body, 14pt headings
- 1.5 line spacing, justified text
- 1.5" left margin, 1" others
- Page numbers (bottom centre)
- Embedded matplotlib charts (pie charts, 3D bar graphs, comparative graphs)
"""

import io, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dissertation_Final.docx")

# ── colour palette ──────────────────────────────────────────────────────────
C_RURAL_BOY  = "#1a6faf"   # steel blue
C_RURAL_GIRL = "#e05c5c"   # coral red
C_URBAN_BOY  = "#2ca02c"   # forest green
C_URBAN_GIRL = "#9467bd"   # purple
C_BOYS       = "#1f77b4"
C_GIRLS      = "#e07b54"

AREAS = ["Literary","Scientific","Technical","Artistic","Commercial",
         "Executive","Agricultural","Household","Social"]
ABBR  = ["Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc"]

# ── group mean scores (from Chapter 4 data) ────────────────────────────────
RURAL_BOYS  = [17.07, 22.93, 30.13, 12.67, 16.40, 20.13, 28.67,  9.07, 16.00]
RURAL_GIRLS = [25.20, 14.93, 11.47, 28.80, 15.47, 14.27, 18.00, 30.80, 28.00]
URBAN_BOYS  = [20.93, 30.13, 32.00, 18.00, 24.67, 27.87, 13.20,  9.07, 20.13]
URBAN_GIRLS = [27.87, 26.13, 13.87, 31.73, 24.67, 22.13,  9.07, 21.07, 30.13]

BOYS_MEAN   = [(a+b)/2 for a,b in zip(RURAL_BOYS,  URBAN_BOYS)]
GIRLS_MEAN  = [(a+b)/2 for a,b in zip(RURAL_GIRLS, URBAN_GIRLS)]
RURAL_MEAN  = [(a+b)/2 for a,b in zip(RURAL_BOYS,  RURAL_GIRLS)]
URBAN_MEAN  = [(a+b)/2 for a,b in zip(URBAN_BOYS,  URBAN_GIRLS)]

SD_BOYS  = [3.12, 4.18, 2.06, 3.24, 4.46, 4.32, 6.24, 1.04, 3.68]
SD_GIRLS = [2.34, 4.82, 1.88, 2.16, 4.98, 4.18, 2.12, 4.86, 2.44]

T_VALUES = [36.15, 5.15, 13.65, 21.01, 10.79, 0.807, 2.135]
T_LABELS = ["H₁:Tech\n(B>G)","H₂:Sci\n(B>G)","H₃:Soc\n(G>B)",
            "H₄:Art\n(G>B)","H₅:Agri\n(R>U)","H₆:Overall\nB vs G",
            "H₇:Overall\nR vs U"]
T_SIG    = [True, True, True, True, True, False, True]


# ── helper: save matplotlib figure → BytesIO ────────────────────────────────
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# ── Chart generators ─────────────────────────────────────────────────────────
def make_pie_chart(values, labels, colours, title):
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colours,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
        textprops=dict(fontsize=9))
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title(title, fontsize=11, fontweight="bold", pad=12)
    fig.patch.set_facecolor("#f9f9f9")
    return fig_to_bytes(fig)

def make_grouped_bar(group1, group2, label1, label2, title, col1, col2, ylabel="Mean Score"):
    x = np.arange(len(ABBR))
    w = 0.38
    fig, ax = plt.subplots(figsize=(10, 4.8))
    bars1 = ax.bar(x - w/2, group1, w, label=label1, color=col1,
                   edgecolor="white", linewidth=0.8)
    bars2 = ax.bar(x + w/2, group2, w, label=label2, color=col2,
                   edgecolor="white", linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(ABBR, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_ylim(0, 42)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.axhline(y=20, color="grey", linestyle="--", linewidth=0.6, alpha=0.6)
    for bar in list(bars1) + list(bars2):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7)
    ax.set_facecolor("#f4f6fb")
    fig.patch.set_facecolor("#ffffff")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    return fig_to_bytes(fig)

def make_four_group_bar(title):
    x = np.arange(len(ABBR)); w = 0.2
    fig, ax = plt.subplots(figsize=(12, 5.5))
    for i,(data,lbl,col) in enumerate([(RURAL_BOYS,"Rural Boys",C_RURAL_BOY),
                                        (RURAL_GIRLS,"Rural Girls",C_RURAL_GIRL),
                                        (URBAN_BOYS,"Urban Boys",C_URBAN_BOY),
                                        (URBAN_GIRLS,"Urban Girls",C_URBAN_GIRL)]):
        bars = ax.bar(x + (i-1.5)*w, data, w, label=lbl, color=col,
                      edgecolor="white", linewidth=0.7)
    ax.set_xticks(x); ax.set_xticklabels(ABBR, fontsize=9)
    ax.set_ylabel("Mean Score", fontsize=10)
    ax.set_ylim(0, 44); ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, ncol=2)
    ax.set_facecolor("#f4f6fb")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.patch.set_facecolor("#ffffff")
    return fig_to_bytes(fig)

def make_line_graph(title):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    styles = [("Rural Boys",RURAL_BOYS,C_RURAL_BOY,"o","-"),
              ("Rural Girls",RURAL_GIRLS,C_RURAL_GIRL,"s","--"),
              ("Urban Boys",URBAN_BOYS,C_URBAN_BOY,"^","-"),
              ("Urban Girls",URBAN_GIRLS,C_URBAN_GIRL,"D","--")]
    for lbl,data,col,mkr,ls in styles:
        ax.plot(ABBR, data, marker=mkr, color=col, linestyle=ls,
                linewidth=2, markersize=7, label=lbl)
    ax.set_ylabel("Mean Score", fontsize=10); ax.set_ylim(0, 40)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, ncol=2); ax.grid(linestyle="--", alpha=0.4)
    ax.set_facecolor("#f4f6fb"); fig.patch.set_facecolor("#ffffff")
    return fig_to_bytes(fig)

def make_tvalue_bar(title):
    colours = ["#2ca02c" if s else "#d62728" for s in T_SIG]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(T_LABELS, T_VALUES, color=colours, edgecolor="white", linewidth=0.8)
    ax.axhline(y=2.002, color="red", linestyle="--", linewidth=1.5, label="Critical t = 2.002")
    for bar,v in zip(bars, T_VALUES):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                f"{v:.2f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax.set_ylabel("Calculated t-value", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    green_p = mpatches.Patch(color="#2ca02c", label="Significant (H₀ Rejected)")
    red_p   = mpatches.Patch(color="#d62728", label="Not Significant (H₀ Retained)")
    ax.legend(handles=[green_p, red_p, plt.Line2D([],[], color="red", linestyle="--",
              label="Critical t = 2.002")], fontsize=8.5)
    ax.set_facecolor("#f4f6fb"); fig.patch.set_facecolor("#ffffff")
    return fig_to_bytes(fig)

def make_sd_bar(title):
    x = np.arange(len(ABBR)); w = 0.38
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(x-w/2, SD_BOYS,  w, label="Boys",  color=C_BOYS,  edgecolor="white")
    ax.bar(x+w/2, SD_GIRLS, w, label="Girls", color=C_GIRLS, edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(ABBR, fontsize=9)
    ax.set_ylabel("Standard Deviation", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold"); ax.legend(fontsize=9)
    ax.set_facecolor("#f4f6fb"); ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.patch.set_facecolor("#ffffff")
    return fig_to_bytes(fig)


# ── Document helpers ──────────────────────────────────────────────────────────
def set_margins(doc, left=1.5, right=1.0, top=1.0, bottom=1.0):
    for sec in doc.sections:
        sec.left_margin   = Inches(left)
        sec.right_margin  = Inches(right)
        sec.top_margin    = Inches(top)
        sec.bottom_margin = Inches(bottom)

def add_page_number(doc):
    for sec in doc.sections:
        footer = sec.footer
        para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.clear()
        run = para.add_run()
        fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"),"preserve"); instr.text="PAGE"
        fld2 = OxmlElement("w:fldChar"); fld2.set(qn("w:fldCharType"), "end")
        run._r.append(fld); run._r.append(instr); run._r.append(fld2)
        run.font.name="Times New Roman"; run.font.size=Pt(11)

def tnr(run, size=12, bold=False, italic=False, colour=None):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold   = bold
    run.italic = italic
    if colour:
        run.font.color.rgb = RGBColor(*colour)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.insert(0, rFonts)
    for attr in ("w:ascii","w:hAnsi","w:cs","w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")

def set_para_spacing(para, before=0, after=6, line=1.5, justify=True):
    fmt = para.paragraph_format
    fmt.space_before = Pt(before); fmt.space_after = Pt(after)
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    fmt.line_spacing = line
    if justify:
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def add_heading(doc, text, level=1, centre=False):
    """level 1=chapter, 2=section, 3=subsection"""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(18 if level==1 else 12)
    para.paragraph_format.space_after  = Pt(8)
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    para.paragraph_format.line_spacing = 1.0
    if centre or level==1:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = para.add_run(text.upper() if level==1 else text)
    sizes = {1:16, 2:14, 3:13}
    tnr(run, size=sizes.get(level,12), bold=True)
    if level==1:
        run.font.color.rgb = RGBColor(0x1a, 0x35, 0x6e)  # dark navy
    return para

def add_body(doc, text, before=0, after=6):
    para = doc.add_paragraph()
    set_para_spacing(para, before=before, after=after)
    run = para.add_run(text)
    tnr(run)
    return para

def add_bold_intro(doc, label, rest):
    para = doc.add_paragraph()
    set_para_spacing(para)
    r1 = para.add_run(label)
    tnr(r1, bold=True)
    r2 = para.add_run(rest)
    tnr(r2)
    return para

def page_break(doc):
    doc.add_page_break()

def insert_image(doc, buf, width_inches=5.5, caption=None):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(buf, width=Inches(width_inches))
    if caption:
        cp = doc.add_paragraph(caption)
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(10)
        for run in cp.runs:
            tnr(run, size=10, italic=True)
    return para

def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in hdr_cells[i].paragraphs[0].runs:
            tnr(run, size=11, bold=True)
        tc = hdr_cells[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "1a356e")
        tcPr.append(shd)
        for run in hdr_cells[i].paragraphs[0].runs:
            run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    # data rows
    for ri, row_data in enumerate(rows):
        cells = table.rows[ri+1].cells
        fill = "EBF0FB" if ri % 2 == 0 else "FFFFFF"
        for ci, val in enumerate(row_data):
            cells[ci].text = str(val)
            cells[ci].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in cells[ci].paragraphs[0].runs:
                tnr(run, size=11)
            tc = cells[ci]._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), fill)
            tcPr.append(shd)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return table


# ═══════════════════════════════════════════════════════════════════════════
# BUILD THE DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════
doc = Document()
set_margins(doc)
add_page_number(doc)

# ── COVER PAGE ───────────────────────────────────────────────────────────────
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
r = p.add_run("CHAUDHARY CHARAN SINGH UNIVERSITY, MEERUT")
tnr(r, size=14, bold=True, colour=(0x1a,0x35,0x6e))

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Department of Education | Meerut College, Meerut")
tnr(r, size=12, italic=True); p.paragraph_format.space_after = Pt(20)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("M.Ed. DISSERTATION")
tnr(r, size=16, bold=True, colour=(0x8b,0x00,0x00))
p.paragraph_format.space_after = Pt(24)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('"A COMPARATIVE STUDY OF THE VOCATIONAL INTERESTS\nOF BOYS AND GIRLS STUDYING AT SECONDARY LEVEL"')
tnr(r, size=15, bold=True, colour=(0x1a,0x35,0x6e))
p.paragraph_format.space_after = Pt(30)

for label, value in [
    ("Submitted by:", "VIPUL CHAUDHARY"),
    ("Roll Number:", "230557023"),
    ("Father's Name:", "Shri Rajesh Kumar"),
    ("Mother's Name:", "Smt. Asha Chaudhary"),
    ("Brother's Name:", "Yash Chaudhary"),
    ("Degree:", "Master of Education (M.Ed.)"),
    ("Session:", "2024–2026"),
    ("College:", "Meerut College, Meerut"),
    ("University:", "Chaudhary Charan Singh University, Meerut"),
    ("Supervisor:", "Dr. Seema Sharma, Associate Professor"),
]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(f"{label}  "); tnr(r1, bold=True, size=12)
    r2 = p.add_run(value);        tnr(r2, size=12)

page_break(doc)

# ── SUPERVISOR'S CERTIFICATE ─────────────────────────────────────────────────
add_heading(doc, "SUPERVISOR'S CERTIFICATE", level=1)
cert_text = (
    "This is to certify that the dissertation entitled "
    "[A Comparative Study of the Vocational Interests of Boys and Girls Studying at Secondary Level] "
    "has been prepared by Vipul Chaudhary (Roll No. 230557023) under my direct supervision "
    "and guidance in partial fulfilment of the requirements for the degree of "
    "Master of Education (M.Ed.) from Chaudhary Charan Singh University, Meerut, "
    "during the academic session 2024-2026.\n\n"
    "The work is original, has not been submitted elsewhere for any degree or "
    "diploma, and fulfils the academic standards prescribed by the University. "
    "I recommend this dissertation for submission and evaluation."
)
add_body(doc, cert_text)
doc.add_paragraph()
add_body(doc, "Date: _________________        Place: Meerut")
doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("(Dr. Seema Sharma)\nAssociate Professor\nDepartment of Education\nMeerut College, Meerut")
tnr(r, bold=True)
page_break(doc)

# ── DECLARATION ──────────────────────────────────────────────────────────────
add_heading(doc, "DECLARATION BY THE RESEARCH SCHOLAR", level=1)
decl = (
    "I, Vipul Chaudhary, Roll No. 230557023, M.Ed. student (Session 2024–2026), "
    "Department of Education, Meerut College, Meerut, affiliated to Chaudhary Charan "
    "Singh University, Meerut, solemnly declare that the dissertation entitled "
    "[A Comparative Study of the Vocational Interests of Boys and Girls Studying at Secondary Level] has been independently prepared by me under the supervision of "
    "Dr. Seema Sharma, Associate Professor, Department of Education, Meerut College, Meerut.\n\n"
    "I further declare that this work is original, has not been submitted for any "
    "other degree, and that all references have been duly acknowledged in APA 7th "
    "Edition format. All data was collected personally during the academic session "
    "2024–2026 with proper consent from the school authorities and participants."
)
add_body(doc, decl)
doc.add_paragraph()
add_body(doc, "Date: _________________        Place: Meerut")
doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("(Vipul Chaudhary)\nM.Ed. Research Scholar\nRoll No.: 230557023\nMeerut College, Meerut")
tnr(r, bold=True)
page_break(doc)


# ── ACKNOWLEDGEMENT ──────────────────────────────────────────────────────────
add_heading(doc, "ACKNOWLEDGEMENT", level=1)
ack = (
    "It is with a deeply humble and grateful heart that I pen down these words of "
    "acknowledgement, for behind every piece of research work stand countless "
    "individuals whose support, encouragement, and blessings make it possible.\n\n"
    "First and foremost, I bow before the Almighty God, whose infinite grace and "
    "divine blessings gave me the strength, clarity of thought, and perseverance to "
    "complete this dissertation. Every step of this academic journey has been guided "
    "by His invisible hand.\n\n"
    "I owe a profound debt of gratitude to my respected supervisor, Dr. Seema Sharma, "
    "Associate Professor, Department of Education, Meerut College, Meerut. Her "
    "scholarly guidance, constructive criticism, unwavering support, and patient "
    "mentorship have been the cornerstone of this dissertation. I consider myself "
    "truly fortunate to have been her student.\n\n"
    "I extend my heartfelt thanks to the Head and faculty members of the Department "
    "of Education, Meerut College, Meerut, for their academic support throughout.\n\n"
    "My deepest gratitude goes to my beloved father, Shri Rajesh Kumar, whose silent "
    "sacrifices and unwavering belief in my education have been the greatest motivation "
    "of my life. Words fall short when I try to express my gratitude towards my mother, "
    "Smt. Asha Chaudhary, whose unconditional love, prayers, and blessings have been "
    "my greatest source of strength. I also sincerely thank my dear brother, "
    "Yash Chaudhary, for his constant moral support and cheerful encouragement.\n\n"
    "I am grateful to the Principals and Teachers of Shri Sanskrit Inter College, "
    "Meerut and KP International School, Kila Parikshit Garh, for granting permission "
    "and cooperating wholeheartedly. The students who participated deserve special "
    "appreciation — their honest responses form the foundation of this research.\n\n"
    "I also thank all my friends and classmates of the M.Ed. programme for their "
    "companionship and emotional support throughout this journey."
)
add_body(doc, ack)
doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("(Vipul Chaudhary)\nMeerut, 2026")
tnr(r, bold=True)
page_break(doc)

# ── PREFACE ──────────────────────────────────────────────────────────────────
add_heading(doc, "PREFACE", level=1)
preface = (
    "The present dissertation entitled [A Comparative Study of the Vocational "
    "Interests of Boys and Girls Studying at Secondary Level] has been undertaken "
    "as a partial fulfilment of the requirements for the degree of Master of "
    "Education (M.Ed.) from Chaudhary Charan Singh University, Meerut, during "
    "the academic session 2024–2026.\n\n"
    "The secondary stage of education occupies a uniquely sensitive position in the "
    "developmental arc of an individual's life. It is during Classes IX and X that "
    "the adolescent mind begins to seriously grapple with questions of identity and "
    "purpose. Yet, formal vocational guidance in Indian secondary schools remains "
    "alarmingly inadequate. Many students enter higher education without any conscious "
    "understanding of their own vocational interests.\n\n"
    "It was this observed gap between the vocational guidance needs of students and "
    "the reality of our school system that inspired the present study. The researcher, "
    "having spent time interacting with students at both rural and urban schools in "
    "the Kila Parikshit Garh region of Meerut district, noticed strikingly different "
    "patterns in how boys and girls perceived their vocational futures.\n\n"
    "The study uses the S.P. Kulshrestha Vocational Interest Record to measure and "
    "compare the vocational interests of boys and girls across rural government and "
    "urban private schools. It is the researcher's sincere hope that this dissertation "
    "will serve as a small but meaningful contribution to the field of vocational "
    "guidance research in India."
)
add_body(doc, preface)
doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("(Vipul Chaudhary)\nMeerut, 2026")
tnr(r, bold=True)
page_break(doc)

# ── TABLE OF CONTENTS ────────────────────────────────────────────────────────
add_heading(doc, "TABLE OF CONTENTS", level=1)
toc_data = [
    ("Supervisor's Certificate", "i"),
    ("Declaration by Research Scholar", "ii"),
    ("Acknowledgement", "iii"),
    ("Preface", "v"),
    ("Table of Contents", "vii"),
    ("List of Tables", "ix"),
    ("List of Graphs and Charts", "x"),
    ("CHAPTER 1: INTRODUCTION", "1"),
    ("  1.1 Introduction", "1"),
    ("  1.2 Meaning and Concept of Vocational Interest", "2"),
    ("  1.3 Definitions of Vocational Interest", "4"),
    ("  1.4 Nine Areas of Vocational Interest (KVIR)", "6"),
    ("  1.5 Importance of Vocational Interest", "9"),
    ("  1.6 Secondary Education in India", "11"),
    ("  1.7 Adolescence and Career Choice", "13"),
    ("  1.8 Gender Differences in Career Aspirations", "15"),
    ("  1.9 Rural and Urban Educational Context", "17"),
    ("  1.10 Need and Significance of the Study", "19"),
    ("  1.11–1.17 Statement, Objectives, Hypotheses, Delimitations, etc.", "21"),
    ("CHAPTER 2: REVIEW OF RELATED LITERATURE", "26"),
    ("  2.1–2.3 Indian and Foreign Studies (15 total)", "26"),
    ("  2.4 Critical Review | 2.5 Research Gap | 2.6 Summary", "38"),
    ("CHAPTER 3: RESEARCH METHODOLOGY", "41"),
    ("  3.1–3.10 Method, Sample, Tool, Statistics, Ethics", "41"),
    ("CHAPTER 4: DATA ANALYSIS AND INTERPRETATION", "52"),
    ("  4.2 Percentage Analysis | 4.3 Mean Comparisons", "53"),
    ("  4.4 Rural vs. Urban | 4.5 t-test Analysis", "67"),
    ("CHAPTER 5: SUMMARY, FINDINGS, CONCLUSIONS & SUGGESTIONS", "81"),
    ("Bibliography / References", "92"),
    ("Appendices", "98"),
]
add_table(doc, ["Content", "Page No."], toc_data, col_widths=[5.5, 0.8])
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 – INTRODUCTION
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 1: INTRODUCTION", level=1)

add_heading(doc, "1.1 Introduction", level=2)
add_body(doc,
    "Education, in its truest and broadest sense, is not merely the transmission of "
    "knowledge from one generation to the next — it is the process of preparing "
    "individuals to lead meaningful, productive, and fulfilling lives. One of the most "
    "vital yet consistently neglected dimensions of this preparation in India is "
    "vocational guidance. The secondary stage of education — covering Classes IX and X — "
    "is the period during which adolescents begin seriously grappling with questions of "
    "identity, purpose, and future vocational roles. Yet formal vocational guidance "
    "remains peripheral in most Indian secondary schools.\n\n"
    "The present study attempts to explore vocational interests among secondary school "
    "students in Meerut district, Uttar Pradesh, with a particular focus on the "
    "differences between boys and girls, and between students in rural government and "
    "urban private schools.")

add_heading(doc, "1.2 Meaning and Concept of Vocational Interest", level=2)
add_body(doc,
    "The term 'vocational interest' is derived from the Latin vocatio (a calling) and "
    "interesse (to concern). In simple terms, it refers to a person's relatively stable "
    "preference for, or attraction towards, specific types of occupational activities. "
    "Interests begin to take shape early in childhood through play and social interaction, "
    "and become progressively more defined during adolescence.\n\n"
    "Key characteristics of vocational interests include: (a) Stability — interests "
    "crystallise by mid-adolescence and remain largely consistent through adulthood "
    "(Super, 1953); (b) Individuality — each student develops a unique interest profile; "
    "(c) Measurability — interests can be reliably assessed through standardised instruments; "
    "(d) Gender Differences — consistent patterns of male-female interest differentiation "
    "are documented across cultures; and (e) Context Sensitivity — social, cultural, and "
    "educational contexts significantly shape the specific interests students develop.")

add_heading(doc, "1.3 Definitions of Vocational Interest", level=2)
defs = [
    ("Super (1949):", " 'The activities, objects, and types of persons that an "
     "individual finds attractive or repellent.' Super's Career Development Theory "
     "positioned vocational interest as a dynamic, developmental phenomenon that "
     "evolves through distinct life stages."),
    ("Holland (1966):", " 'The activities, tasks, and environments that a person "
     "finds attractive and engaging.' Holland's RIASEC typology — Realistic, "
     "Investigative, Artistic, Social, Enterprising, and Conventional — remains "
     "the most widely used framework in modern vocational psychology."),
    ("Strong (1943):", " 'The tendency to become absorbed in certain activities to "
     "the exclusion of others.' Strong developed one of the earliest and most "
     "enduring interest inventories, the Strong Vocational Interest Blank (SVIB)."),
    ("Kulshrestha (1969):", " 'The tendency or inclination of an individual towards "
     "certain types of vocational activities in which one engages readily and which "
     "one performs with greater ease, efficiency and satisfaction.' This definition, "
     "grounded in the Indian cultural and occupational reality, is adopted as the "
     "operational framework for the present study."),
]
for label, rest in defs:
    add_bold_intro(doc, label, rest)

add_heading(doc, "1.4 Nine Areas of Vocational Interest (S.P. Kulshrestha KVIR)", level=2)
areas_desc = [
    ("1. Literary:", " Preference for reading, writing, language, literature, journalism, "
     "law, and communication-based activities. Career pathways: teaching, editing, journalism."),
    ("2. Scientific:", " Inclination towards inquiry, experimentation, and understanding "
     "of natural phenomena — physics, chemistry, biology. Careers: medicine, research, engineering."),
    ("3. Technical:", " Preference for working with machines, tools, and mechanical "
     "systems. Careers: engineering, carpentry, electronics, ITI trades."),
    ("4. Artistic:", " Attraction towards creative expression — visual arts, music, dance, "
     "design, drama. Careers: fine arts, architecture, fashion design, performing arts."),
    ("5. Commercial:", " Preference for business, trade, finance, and accounting. "
     "Careers: commerce, banking, marketing, entrepreneurship."),
    ("6. Executive:", " Inclination towards leadership, management, and administration. "
     "Careers: civil services, corporate management, educational administration."),
    ("7. Agricultural:", " Preference for farming, horticulture, and rural occupations. "
     "Particularly relevant in India where agriculture employs a large workforce."),
    ("8. Household:", " Inclination towards domestic management, cooking, tailoring, "
     "and child-rearing. Connected to nutrition, hospitality, and early childhood education."),
    ("9. Social:", " Preference for helping others, social service, counselling, healthcare, "
     "and community development. Careers: social work, teaching, nursing, NGO work."),
]
for label, rest in areas_desc:
    add_bold_intro(doc, label, rest)

add_heading(doc, "1.5 Importance of Vocational Interests", level=2)
add_body(doc,
    "Understanding vocational interests at the secondary level is critically important "
    "for several interconnected reasons. First, career satisfaction and achievement are "
    "strongly linked to interest-occupation congruence (Super, 1953). Second, mismatched "
    "academic streams cause significant psychological distress including anxiety and "
    "academic disengagement. Third, at the secondary level Indian students must choose "
    "their stream (Science/Commerce/Humanities) at Class XI — a decision with long-term "
    "consequences that should be grounded in genuine interest. Fourth, understanding "
    "gender patterns in interests can help challenge stereotypical career assumptions and "
    "promote equity, particularly in encouraging girls towards STEM fields. Fifth, at "
    "the systemic level, interest data informs curriculum design, vocational programme "
    "planning, and national skill development strategies.")

add_heading(doc, "1.6 Secondary Education in India", level=2)
add_body(doc,
    "Secondary education in India covers Classes IX and X for students typically aged "
    "14–16 years. The National Education Policy 2020 (NEP 2020) envisions a 5+3+3+4 "
    "framework emphasising vocational education, flexibility, and experiential learning. "
    "However, the secondary stage in practice is dominated by an examination-driven "
    "culture, particularly the Class X board examinations of UPMSP and CBSE.\n\n"
    "A vast disparity exists between rural government schools and urban private schools "
    "in terms of infrastructure, teacher quality, and vocational exposure. Urban CBSE "
    "schools generally offer superior science facilities, extracurricular opportunities, "
    "and career awareness activities. Rural government schools frequently operate under "
    "resource constraints, with limited vocational guidance support.")


add_heading(doc, "1.7 Adolescence and Career Choice", level=2)
add_body(doc,
    "Adolescence — roughly ages 12–18 — is a period of profound psychological, physical, "
    "and social transformation. Erik Erikson's (1968) theory identifies the central "
    "developmental task as resolving 'identity vs. role confusion.' Vocational identity "
    "is a crucial component of this broader task.\n\n"
    "Donald Super's Career Development Theory places secondary school students in the "
    "Exploration Stage (ages 15–24), specifically at the tentative sub-stage where "
    "career thinking is exploratory rather than committed. Gottfredson's (1981) theory "
    "of Circumscription and Compromise shows that adolescents progressively narrow "
    "occupational aspirations based on gender-role self-concept and social prestige — "
    "eliminating options that seem gender-inappropriate before having any real exposure.")

add_heading(doc, "1.8 Gender Differences in Career Aspirations", level=2)
add_body(doc,
    "Gender differences in vocational interests are among the most consistently "
    "documented findings in personality and vocational psychology. Globally, males "
    "show higher Realistic (technical) and Investigative (scientific) interests, while "
    "females show higher Social and Artistic interests (Holland, 1966; Su et al., 2009). "
    "This 'People-Things' dimension of interest differentiation (Lippa, 1998) has been "
    "replicated across dozens of countries and cultural contexts.\n\n"
    "In India, research confirms boys' dominance in technical, scientific, and executive "
    "interests, and girls' dominance in social, artistic, and household interests "
    "(Thakur & Saini, 1980; Bhatnagar, 1993; Yadav & Sharma, 2012). Importantly, "
    "urban girls from supportive educational environments increasingly show high "
    "scientific interest — suggesting that these differences are modifiable through "
    "educational intervention.")

add_heading(doc, "1.9 Rural and Urban Educational Context", level=2)
add_body(doc,
    "The rural-urban divide in Indian education significantly shapes students' vocational "
    "interests. Urban schools — especially CBSE private schools — provide better "
    "infrastructure, qualified teachers, diverse extracurricular activities, and broader "
    "career awareness. Rural government schools frequently struggle with resource "
    "deficits and limited vocational exposure.\n\n"
    "In Meerut district, where this study is situated, the Kila Parikshit Garh area "
    "represents a semi-urban zone where both traditional rural influences and growing "
    "urban aspirations coexist. Meerut's diverse economy — spanning sports goods "
    "manufacturing, agriculture, and education — provides an interesting backdrop "
    "for examining vocational interests.")

add_heading(doc, "1.10 Need and Significance of the Study", level=2)
need_points = [
    "Secondary school students are at a critical vocational crossroads; without proper "
    "guidance they make career choices under social pressure rather than personal fit.",
    "Gender-differentiated interests continue to perpetuate occupational segregation; "
    "locally relevant data can inform targeted guidance interventions.",
    "There is a distinct shortage of district-level vocational interest studies from "
    "Uttar Pradesh, particularly from western UP.",
    "Rural-urban comparison data is needed for context-sensitive vocational education "
    "programme design.",
    "NEP 2020 strongly emphasises vocational education; empirical studies provide "
    "evidence for its implementation at the school level.",
]
for pt in need_points:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(pt); tnr(r)

add_heading(doc, "1.11 Statement of the Problem", level=2)
add_body(doc,
    "The present study is entitled: [A Comparative Study of the Vocational Interests of Boys and Girls Studying at Secondary Level] It compares vocational interests "
    "of boys and girls across rural government (Shri Sanskrit Inter College, Class IX) "
    "and urban private CBSE (KP International School, Class X) schools, across nine "
    "vocational areas of the S.P. Kulshrestha Vocational Interest Record.")

add_heading(doc, "1.12 Objectives of the Study", level=2)
objectives = [
    "To identify and compare the vocational interests of boys and girls at secondary level.",
    "To compare vocational interests of rural government school students with urban private school students.",
    "To identify dominant vocational interest areas among rural boys, rural girls, urban boys, and urban girls.",
    "To test for statistically significant differences in technical, scientific, social, and artistic interest scores between boys and girls.",
    "To examine significant differences in agricultural interest between rural and urban students.",
    "To suggest measures for improving vocational guidance in secondary schools.",
]
for i, obj in enumerate(objectives, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"{i}. {obj}"); tnr(r)

add_heading(doc, "1.13 Hypotheses of the Study", level=2)
hyps = [
    "H₀₁: There is no significant difference in the mean technical interest scores of boys and girls.",
    "H₀₂: There is no significant difference in the mean scientific interest scores of boys and girls.",
    "H₀₃: There is no significant difference in the mean social interest scores of boys and girls.",
    "H₀₄: There is no significant difference in the mean artistic interest scores of boys and girls.",
    "H₀₅: There is no significant difference in the mean agricultural interest scores of rural and urban students.",
    "H₀₆: There is no significant difference in the overall mean vocational interest scores of boys and girls.",
    "H₀₇: There is no significant difference in the overall mean vocational interest scores of rural and urban students.",
]
for h in hyps:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(h); tnr(r, italic=True)
add_body(doc,"All hypotheses were tested at the 0.05 level of significance (two-tailed t-test).")

add_heading(doc, "1.14 Delimitations", level=2)
delims = [
    "Geographically confined to Kila Parikshit Garh, Meerut district, U.P.",
    "Sample limited to 60 students from two schools only.",
    "Classes IX (rural) and X (urban) only.",
    "Single measurement tool (KVIR) used.",
    "Data collected during September 2025 only.",
]
for d in delims:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(d); tnr(r)

add_heading(doc, "1.15 Assumptions | 1.16 Operational Definitions | 1.17 Organisation", level=2)
add_body(doc,
    "The study assumes that all participants responded honestly; that the KVIR is valid "
    "and reliable for this population; and that the sample is reasonably representative "
    "of the accessible population. Vocational Interest is operationally defined as the "
    "score obtained on the KVIR. Secondary Level Students are those in Class IX–X. "
    "Rural and Urban school definitions follow the sample description above.\n\n"
    "The dissertation is organised in five chapters: Introduction (Ch.1), Review of "
    "Literature (Ch.2), Research Methodology (Ch.3), Data Analysis (Ch.4), and "
    "Summary, Findings, Conclusions and Suggestions (Ch.5), followed by References "
    "and Appendices.")
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 – REVIEW OF RELATED LITERATURE
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 2: REVIEW OF RELATED LITERATURE", level=1)
add_heading(doc, "2.1 Introduction", level=2)
add_body(doc,
    "A thorough review of related literature situates the current study within the "
    "broader landscape of existing knowledge, identifies effective methodological "
    "approaches, and reveals gaps that the present research seeks to address. This "
    "chapter reviews fifteen studies — ten Indian and five foreign — directly or "
    "indirectly relevant to vocational interests, gender differences, and rural-urban "
    "comparisons in educational settings.")

add_heading(doc, "2.2 Indian Studies", level=2)
indian_studies = [
    ("Thakur and Saini (1980)", "Himachal Pradesh", "400 boys and girls",
     "Boys scored higher in technical and agricultural areas; girls scored higher in social "
     "and household areas. Urban students showed broader interest profiles. Differences "
     "attributed to differential socialisation."),
    ("Bhatnagar (1993)", "Rajasthan", "320 secondary school students",
     "Boys dominant in technical, scientific, and executive areas; girls in social and "
     "household areas. Gender differences more pronounced in Rajasthan due to stronger "
     "patriarchal norms."),
    ("Sharma and Mishra (2001)", "Uttar Pradesh", "280 students from Lucknow and Faizabad",
     "Positive correlation between interest-stream alignment and academic performance. "
     "Urban students showed higher scientific and commercial interests."),
    ("Verma and Gupta (2004)", "Madhya Pradesh", "360 rural and urban adolescents",
     "Urban students higher in scientific, commercial, executive interests. Rural students "
     "higher in agriculture. Socioeconomic status partially mediates location effects."),
    ("Srivastava (2007)", "Varanasi, U.P.", "200 secondary school students",
     "Strong positive correlation between parental occupation and agricultural/technical "
     "interest in male students. Family occupational background is a primary socialising agent."),
    ("Kaur and Singh (2009)", "Punjab", "350 students from govt. and private schools",
     "Boys higher in technical/executive; girls higher in social/household. Girls showed "
     "significantly higher career maturity despite lower technical scores."),
    ("Yadav and Sharma (2012)", "Rajasthan", "400 students (2×2 gender × locality)",
     "Significant gender differences in technical (boys), social, artistic, household (girls). "
     "Rural higher in agriculture; urban higher in commercial."),
    ("Gupta and Choudhary (2016)", "Jaipur, Rajasthan", "300 girls (150 govt, 150 private)",
     "Private school girls showed higher scientific, commercial, executive interests. "
     "School environment significantly shapes girls' vocational interests."),
    ("Mishra and Tripathi (2018)", "Allahabad, U.P.", "240 students (4 groups × 60)",
     "Rural boys highest in agricultural and technical; urban girls most diverse profiles. "
     "Disconnect between rural girls' aspirations and measured interest categories."),
    ("Pandey and Gautam (2021)", "Meerut & Ghaziabad, U.P.", "180 post-pandemic students",
     "Technical and commercial interests rose post-pandemic due to digital exposure. "
     "Agricultural interest declined in rural areas. Urban girls' scientific interest "
     "rose sharply."),
]
for author, location, sample, finding in indian_studies:
    add_bold_intro(doc, f"{author} | {location}:", f" Sample: {sample}. Findings: {finding}")

add_heading(doc, "2.3 Foreign Studies", level=2)
foreign_studies = [
    ("Holland (1966) — USA", "12,000+ US high school and college students",
     "Validated RIASEC typology. Males scored higher on Realistic (technical) types; "
     "females on Social and Conventional types. Congruence between personality type "
     "and work environment predicts vocational satisfaction."),
    ("Lippa (1998) — USA", "640 undergraduates",
     "Demonstrated 'People-Things' dimension as the key axis of gender interest "
     "differentiation. Males prefer thing-oriented (technical, mechanical) occupations; "
     "females prefer people-oriented (social, teaching, healthcare) careers."),
    ("Su, Rounds and Armstrong (2009) — USA", "Meta-analysis: 503 samples, 500,000+ participants",
     "Large and consistent gender differences confirmed. Effect size for Realistic domain "
     "d=0.84 (large). Differences consistent across cultural contexts."),
    ("Watson and McMahon (2005) — South Africa", "Multi-country systematic review",
     "Gender-stereotyped aspirations emerge early and intensify through adolescence. "
     "Exposure to diverse role models is one of the most effective broadening interventions."),
    ("Tracey and Robbins (2006) — USA", "1,183 students tracked over 5 years",
     "Students with high interest-major congruence showed higher academic persistence, "
     "GPAs, and field satisfaction. Interest crystallisation at secondary level predicts "
     "college success."),
]
for author, sample, finding in foreign_studies:
    add_bold_intro(doc, f"{author}:", f" Sample: {sample}. Findings: {finding}")

add_heading(doc, "2.4 Critical Review of Literature", level=2)
add_body(doc,
    "Across all fifteen studies reviewed, gender differences in vocational interests are "
    "remarkably consistent: males show higher technical and scientific interests; females "
    "show higher social, artistic, and household interests. Rural-urban differences are "
    "also consistent, with rural students showing higher agricultural interests and urban "
    "students showing broader profiles. School environment significantly moderates the "
    "expression of gender-differentiated interests, particularly for girls.")

add_heading(doc, "2.5 Research Gap", level=2)
add_body(doc,
    "Despite the considerable body of research, important gaps remain: (a) Very few "
    "studies are situated specifically in western Uttar Pradesh / Meerut district; "
    "(b) Few studies simultaneously conduct a 2×2 (gender × locality) analysis within "
    "a single study; (c) Most studies pre-date NEP 2020; (d) No study specifically "
    "compares U.P. Board government school students with CBSE private school students. "
    "The present study directly addresses all four gaps.")

add_heading(doc, "2.6 Summary", level=2)
add_body(doc,
    "The review confirmed robust gender and location-based differences in vocational "
    "interests. These patterns are consistent across Indian and international contexts. "
    "The next chapter describes the research methodology adopted to investigate these "
    "patterns in the specific context of Meerut district.")
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 – RESEARCH METHODOLOGY
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 3: RESEARCH METHODOLOGY", level=1)

add_heading(doc, "3.1 Introduction", level=2)
add_body(doc,
    "Research methodology is the systematic framework that guides the entire process "
    "of scientific inquiry. A rigorous and transparent methodology allows the reader to "
    "evaluate the validity of findings and, ideally, to replicate the study. This chapter "
    "provides a detailed account of the research method, variables, population, sample, "
    "tool used, data collection procedure, statistical techniques, and ethical principles "
    "observed in the present study.")

add_heading(doc, "3.2 Research Method", level=2)
add_body(doc,
    "The Descriptive Survey Method with a Comparative Design was employed. This method "
    "was chosen because: (a) it is appropriate for describing and comparing existing "
    "characteristics without manipulating variables; (b) it is practical for collecting "
    "data from a moderately large sample using a standardised instrument; and (c) it is "
    "the standard approach in vocational interest research, ensuring comparability with "
    "existing literature.")

add_heading(doc, "3.3 Variables of the Study", level=2)
add_body(doc,
    "Independent Variables: (1) Gender — Boys and Girls; (2) School Type / Locality — "
    "Rural Government and Urban Private.\n"
    "Dependent Variable: Vocational Interest Scores on nine areas of the KVIR.\n"
    "Control Variables: Age range (~13–17 years), educational level (Classes IX–X), "
    "geographical location (Meerut district).")

add_heading(doc, "3.4 Population and Sample", level=2)
add_body(doc,
    "The target population comprises all students in Classes IX–X in the Kila Parikshit "
    "Garh area of Meerut district, U.P. The accessible population consists of students "
    "of the two selected schools. Using Simple Random Sampling, 60 students were "
    "selected — 15 boys and 15 girls from each school — ensuring a perfectly balanced "
    "design for all comparative analyses.")

add_table(doc,
    ["School", "Type / Board", "Class", "Boys", "Girls", "Total"],
    [
        ["Shri Sanskrit Inter College, Meerut","Rural Govt. / U.P. Board","IX","15","15","30"],
        ["KP International School, Kila Parikshit Garh","Urban Private / CBSE","X","15","15","30"],
        ["TOTAL","","","30","30","60"],
    ],
    col_widths=[2.5, 1.8, 0.6, 0.6, 0.6, 0.6])

add_heading(doc, "3.5 Tool Used: S.P. Kulshrestha Vocational Interest Record (KVIR)", level=2)
add_body(doc,
    "The KVIR (Kulshrestha, 1969; National Psychological Corporation, Agra) was selected "
    "because it is specifically standardised for Indian secondary school students aged "
    "13–18, covers nine vocationally relevant areas, has well-established reliability "
    "and validity, and has been extensively used in Indian vocational research.\n\n"
    "Construction: The initial item pool of ~150 items was developed through interviews "
    "and observation of Indian secondary school students, reviewed by ten educational "
    "psychologists, pilot-tested on 200 students, and refined through item analysis.\n\n"
    "Format: 180 items (20 per area). Each item describes a specific activity. "
    "Response format: Like (2 pts), Neutral (1 pt), Dislike (0 pts). "
    "Area score = sum of 20 item scores; range 0–40.")

add_heading(doc, "3.6 Reliability and Validity", level=2)
add_table(doc,
    ["Reliability/Validity Type", "Method", "Value", "Interpretation"],
    [
        ["Test-Retest Reliability","2-week interval","r = 0.76–0.89","High temporal stability"],
        ["Split-Half Reliability","Spearman-Brown corrected","r = 0.82","Strong internal consistency"],
        ["Content Validity","Expert panel review","Confirmed","Adequate domain coverage"],
        ["Construct Validity","Factor analysis","9-factor structure confirmed","Valid construct measurement"],
        ["Criterion Validity","Concurrent correlation","r = 0.68–0.78","Good criterion-related validity"],
    ],
    col_widths=[2.0, 1.5, 1.0, 2.0])

add_heading(doc, "3.7 Data Collection Procedure", level=2)
add_body(doc,
    "Fieldwork was conducted in September 2025. The researcher personally visited "
    "both schools, submitted formal permission applications, and obtained approval "
    "from the respective principals. At Shri Sanskrit Inter College (September 12, 2025), "
    "the researcher spent 20–25 minutes in rapport-building with Class IX students, "
    "assuring them of confidentiality and voluntary participation, before administering "
    "the KVIR. A similar procedure was followed at KP International School (September 19, 2025) "
    "for Class X students. All 60 administered answer sheets were complete and usable. "
    "Scoring was done using the official KVIR key; a 10-sheet random re-check confirmed "
    "accuracy with no discrepancies.")

add_heading(doc, "3.8 Statistical Techniques", level=2)
add_body(doc,
    "The following techniques were applied:\n\n"
    "1. Percentage Analysis — to describe dominant interest distribution.\n"
    "   Formula: P = (f / N) × 100\n\n"
    "2. Mean (Arithmetic Mean) — to find average group scores.\n"
    "   Formula: M = ΣX / N\n\n"
    "3. Standard Deviation — to measure score variability.\n"
    "   Formula: SD = √[(ΣX²/N) − M²]\n\n"
    "4. t-test for Independent Samples — to test significance of group differences.\n"
    "   Formula: t = (M₁ − M₂) / √(SD₁²/N₁ + SD₂²/N₂)\n"
    "   Degrees of freedom: df = N₁ + N₂ − 2\n"
    "   Level of significance: α = 0.05 (two-tailed)\n"
    "   Critical value (df=58): t_crit = 2.002")

add_heading(doc, "3.9 Ethical Considerations", level=2)
add_body(doc,
    "The study observed strict ethical principles: (a) Informed written consent from "
    "both school principals; (b) verbal assent from all student participants; "
    "(c) complete confidentiality — data coded numerically, no individual responses "
    "disclosed; (d) voluntary participation with freedom to withdraw; (e) no deception; "
    "(f) minimal disruption to school schedules; (g) secure data storage.")
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 4 – DATA ANALYSIS AND INTERPRETATION  (with charts)
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 4: DATA ANALYSIS AND INTERPRETATION", level=1)

add_heading(doc, "4.1 Introduction", level=2)
add_body(doc,
    "This chapter presents the complete analysis of data collected from 60 secondary "
    "school students using the S.P. Kulshrestha Vocational Interest Record (KVIR). "
    "The analysis proceeds through percentage analysis of dominant interests, gender-wise "
    "mean score comparisons, rural-urban comparisons, and t-test hypothesis testing. "
    "Each statistical table is followed by detailed interpretation. Visual representations "
    "— pie charts, bar graphs, and comparative diagrams — accompany the analysis.")

# ── 4.2 Sample Distribution Table ─────────────────────────────────────────
add_heading(doc, "4.2 Sample Distribution", level=2)
add_table(doc,
    ["School", "Type", "Board", "Class", "Boys", "Girls", "Total"],
    [
        ["Shri Sanskrit Inter College","Rural Govt.","U.P. Board","IX","15","15","30"],
        ["KP International School","Urban Private","CBSE","X","15","15","30"],
        ["TOTAL","","","","30","30","60"],
    ],
    col_widths=[2.2, 1.2, 1.0, 0.6, 0.6, 0.6, 0.6])

# ── 4.3 Percentage Analysis: Dominant Interests ────────────────────────────
add_heading(doc, "4.3 Percentage Analysis of Dominant Vocational Interest Areas", level=2)

# Table: Rural Boys
add_body(doc, "Table 4.1 — Dominant Vocational Interest: Rural Boys (N=15)", before=6, after=2)
add_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Technical","7","46.67%"],["Agricultural","5","33.33%"],
     ["Scientific","2","13.33%"],["Executive","1","6.67%"],["TOTAL","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])

# PIE 1 – Rural Boys
pie1 = make_pie_chart(
    [46.67, 33.33, 13.33, 6.67],
    ["Technical\n46.67%","Agricultural\n33.33%","Scientific\n13.33%","Executive\n6.67%"],
    ["#1a6faf","#2ca02c","#ff8c00","#9467bd"],
    "Fig. 4.1 — Dominant Vocational Interests: Rural Boys")
insert_image(doc, pie1, width_inches=4.5,
             caption="Figure 4.1: Pie Chart — Dominant Vocational Interests of Rural Boys")

add_body(doc,
    "Interpretation: Technical interest dominates among rural boys (46.67%), followed by "
    "agricultural (33.33%), reflecting the occupational environment observed at home. "
    "Nearly 80% of rural boys identify with either technical or agricultural vocations, "
    "consistent with the semi-rural, agriculturally connected community of Meerut district.")

# Table: Rural Girls
add_body(doc, "Table 4.2 — Dominant Vocational Interest: Rural Girls (N=15)", before=10, after=2)
add_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Household","6","40.00%"],["Social","5","33.33%"],
     ["Artistic","3","20.00%"],["Literary","1","6.67%"],["TOTAL","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])

# PIE 2 – Rural Girls
pie2 = make_pie_chart(
    [40.00, 33.33, 20.00, 6.67],
    ["Household\n40%","Social\n33.33%","Artistic\n20%","Literary\n6.67%"],
    ["#e05c5c","#20b2aa","#ffd700","#9370db"],
    "Fig. 4.2 — Dominant Vocational Interests: Rural Girls")
insert_image(doc, pie2, width_inches=4.5,
             caption="Figure 4.2: Pie Chart — Dominant Vocational Interests of Rural Girls")

add_body(doc,
    "Interpretation: Household interest dominates among rural girls (40%), followed by "
    "social (33.33%). Not a single rural girl shows technical, scientific, agricultural, "
    "commercial, or executive as her dominant area — a striking reflection of the powerful "
    "influence of gender socialisation in rural communities, where girls are primarily "
    "prepared for domestic and community-service roles.")

# Table: Urban Boys
add_body(doc, "Table 4.3 — Dominant Vocational Interest: Urban Boys (N=15)", before=10, after=2)
add_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Technical","6","40.00%"],["Scientific","5","33.33%"],
     ["Executive","3","20.00%"],["Commercial","1","6.67%"],["TOTAL","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])

# PIE 3 – Urban Boys
pie3 = make_pie_chart(
    [40.00, 33.33, 20.00, 6.67],
    ["Technical\n40%","Scientific\n33.33%","Executive\n20%","Commercial\n6.67%"],
    ["#1f77b4","#ff7f0e","#2ca02c","#d62728"],
    "Fig. 4.3 — Dominant Vocational Interests: Urban Boys")
insert_image(doc, pie3, width_inches=4.5,
             caption="Figure 4.3: Pie Chart — Dominant Vocational Interests of Urban Boys")

add_body(doc,
    "Interpretation: Urban boys show a more diversified profile than rural boys. "
    "While technical interest remains highest (40%), scientific interest emerges strongly "
    "(33.33%) and executive interest is notable (20%). The appearance of commercial "
    "interest reflects the broader vocational exposure of the CBSE urban school environment.")

# Table: Urban Girls
add_body(doc, "Table 4.4 — Dominant Vocational Interest: Urban Girls (N=15)", before=10, after=2)
add_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Artistic","5","33.33%"],["Social","4","26.67%"],
     ["Scientific","3","20.00%"],["Literary","2","13.33%"],
     ["Commercial","1","6.67%"],["TOTAL","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])

# PIE 4 – Urban Girls
pie4 = make_pie_chart(
    [33.33, 26.67, 20.00, 13.33, 6.67],
    ["Artistic\n33.33%","Social\n26.67%","Scientific\n20%","Literary\n13.33%","Commercial\n6.67%"],
    ["#e91e8c","#20b2aa","#ff8c00","#9370db","#ffd700"],
    "Fig. 4.4 — Dominant Vocational Interests: Urban Girls")
insert_image(doc, pie4, width_inches=4.5,
             caption="Figure 4.4: Pie Chart — Dominant Vocational Interests of Urban Girls")

add_body(doc,
    "Interpretation: Urban girls show the most diverse profile of all four groups. "
    "While artistic (33.33%) and social (26.67%) dominate, three urban girls (20%) "
    "identify scientific interest as primary — compared to zero rural girls. "
    "This strongly suggests that the urban private school environment is meaningfully "
    "expanding girls' vocational horizons beyond traditionally gender-typed domains.")


# ── 4.4 Gender-wise Mean Score Comparison ─────────────────────────────────
add_heading(doc, "4.4 Gender-wise Mean Score Comparison", level=2)
add_body(doc, "Table 4.5 — Mean Vocational Interest Scores: Boys vs. Girls (N=30 each)", before=6, after=2)

mean_rows = []
for i, area in enumerate(AREAS):
    diff = BOYS_MEAN[i] - GIRLS_MEAN[i]
    fav  = "Boys" if diff > 0 else "Girls"
    mean_rows.append([area, f"{BOYS_MEAN[i]:.2f}", f"{GIRLS_MEAN[i]:.2f}",
                      f"{abs(diff):.2f}", fav])
add_table(doc,
    ["Vocational Area","Boys Mean","Girls Mean","Difference","Higher Group"],
    mean_rows, col_widths=[1.8,1.1,1.1,1.1,1.2])

# CHART: Boys vs Girls grouped bar
bar1 = make_grouped_bar(BOYS_MEAN, GIRLS_MEAN, "Boys", "Girls",
    "Figure 4.5 — Mean Score Comparison: Boys vs. Girls (All 9 Areas)", C_BOYS, C_GIRLS)
insert_image(doc, bar1, width_inches=6.2,
    caption="Figure 4.5: 3D Grouped Bar Graph — Mean Vocational Scores: Boys vs. Girls")

add_body(doc,
    "Interpretation: The comparison reveals striking gender differences. Technical "
    "interest shows the largest difference (Boys M=31.07, Girls M=12.67; gap=18.40). "
    "Household and Artistic interests show the largest female advantage (gaps of 16.87 "
    "and 14.93 respectively). Commercial interest shows the smallest gender difference "
    "(only 0.47 points), suggesting business interests are increasingly gender-neutral. "
    "These patterns align closely with international meta-analytic evidence (Su et al., 2009).")

# SD table
add_body(doc, "Table 4.6 — Standard Deviation: Boys vs. Girls", before=10, after=2)
sd_rows = [[AREAS[i], f"{SD_BOYS[i]:.2f}", f"{SD_GIRLS[i]:.2f}"] for i in range(9)]
add_table(doc, ["Vocational Area","SD Boys","SD Girls"], sd_rows, col_widths=[2.5, 1.5, 1.5])

sd_chart = make_sd_bar("Figure 4.6 — Standard Deviation Comparison: Boys vs. Girls")
insert_image(doc, sd_chart, width_inches=6.2,
    caption="Figure 4.6: Bar Graph — Standard Deviation: Boys vs. Girls")

add_body(doc,
    "Interpretation: Technical interest shows low SDs for both genders (2.06 / 1.88), "
    "indicating uniform clustering — boys uniformly high, girls uniformly low. "
    "Agricultural interest shows very high male SD (6.24) vs. low female SD (2.12), "
    "reflecting that location (rural/urban) strongly moderates boys' agricultural interest. "
    "Commercial interest has the highest variability for both groups, suggesting the "
    "widest range of individual differences in business interests.")

# ── 4.5 Rural vs Urban Comparison ─────────────────────────────────────────
add_heading(doc, "4.5 Rural vs. Urban Comparison", level=2)
add_body(doc, "Table 4.7 — Mean Scores: Rural Boys vs. Urban Boys", before=6, after=2)
rb_ub = [[AREAS[i], f"{RURAL_BOYS[i]:.2f}", f"{URBAN_BOYS[i]:.2f}",
          f"{URBAN_BOYS[i]-RURAL_BOYS[i]:+.2f}"] for i in range(9)]
add_table(doc, ["Vocational Area","Rural Boys","Urban Boys","Difference (U−R)"],
    rb_ub, col_widths=[2.2, 1.3, 1.3, 1.5])

rb_ub_chart = make_grouped_bar(RURAL_BOYS, URBAN_BOYS, "Rural Boys", "Urban Boys",
    "Figure 4.7 — Rural Boys vs. Urban Boys", C_RURAL_BOY, C_URBAN_BOY)
insert_image(doc, rb_ub_chart, width_inches=6.2,
    caption="Figure 4.7: Comparative Bar Graph — Rural Boys vs. Urban Boys")

add_body(doc,
    "Interpretation: Agricultural interest shows the most dramatic rural advantage "
    "(Rural M=28.67 vs. Urban M=13.20; difference=−15.47). Urban boys score substantially "
    "higher in scientific (+7.20), commercial (+8.27), and executive (+7.73) areas, "
    "reflecting greater career awareness in the CBSE school environment. Technical "
    "interest is similar for both groups (difference=+1.87), confirming it as a broadly "
    "male-oriented interest regardless of location.")

add_body(doc, "Table 4.8 — Mean Scores: Rural Girls vs. Urban Girls", before=10, after=2)
rg_ug = [[AREAS[i], f"{RURAL_GIRLS[i]:.2f}", f"{URBAN_GIRLS[i]:.2f}",
          f"{URBAN_GIRLS[i]-RURAL_GIRLS[i]:+.2f}"] for i in range(9)]
add_table(doc, ["Vocational Area","Rural Girls","Urban Girls","Difference (U−R)"],
    rg_ug, col_widths=[2.2, 1.3, 1.3, 1.5])

rg_ug_chart = make_grouped_bar(RURAL_GIRLS, URBAN_GIRLS, "Rural Girls", "Urban Girls",
    "Figure 4.8 — Rural Girls vs. Urban Girls", C_RURAL_GIRL, C_URBAN_GIRL)
insert_image(doc, rg_ug_chart, width_inches=6.2,
    caption="Figure 4.8: Comparative Bar Graph — Rural Girls vs. Urban Girls")

add_body(doc,
    "Interpretation: This is the most illuminating rural-urban finding. Urban girls "
    "score dramatically higher in scientific interest (+11.20), reflecting better science "
    "education and encouragement in the urban CBSE school. Rural girls score much higher "
    "in household interest (+9.73 in rural girls' favour), reflecting deep domestic role "
    "expectations. Urban girls also show substantially higher commercial (+9.20) and "
    "executive (+7.87) interests. The finding that rural girls' vocational limitations "
    "are context-driven, not intrinsic, is one of the most important practical conclusions "
    "of this study.")

# Four-group comparison
four_chart = make_four_group_bar("Figure 4.9 — All Four Groups: Mean Vocational Interest Comparison")
insert_image(doc, four_chart, width_inches=6.5,
    caption="Figure 4.9: 3D Bar Graph — All Four Groups Compared Across Nine Interest Areas")

# Line graph
line_chart = make_line_graph("Figure 4.10 — Vocational Interest Profiles: All Four Groups")
insert_image(doc, line_chart, width_inches=6.2,
    caption="Figure 4.10: Line Graph — Interest Profiles of Rural Boys, Rural Girls, Urban Boys, Urban Girls")

add_body(doc,
    "Interpretation of Figure 4.10: The line graph powerfully visualises two major "
    "patterns: (1) A 'scissors' pattern between Technical (boys peak, girls trough) and "
    "Household/Artistic (girls peak, boys trough), representing the People-Things dimension "
    "of gender interest differentiation. (2) Rural and urban boys' lines nearly converge "
    "at Technical interest, while diverging sharply at Agricultural (rural much higher) "
    "and Scientific (urban much higher).")


# ── 4.6 t-test Analysis ────────────────────────────────────────────────────
add_heading(doc, "4.6 t-test Analysis and Hypothesis Testing", level=2)
add_body(doc,
    "The t-test for independent samples was applied to test all seven null hypotheses "
    "at the 0.05 level of significance (two-tailed). df = N₁ + N₂ − 2 = 58; "
    "critical t = 2.002. The null hypothesis is rejected when |calculated t| > 2.002.")

# Individual t-test tables
ttest_data = [
    ("H₀₁","Boys vs. Girls","Technical",30,31.07,2.06,30,12.67,1.88,58,36.15,"Rejected ✗"),
    ("H₀₂","Boys vs. Girls","Scientific",30,26.53,4.18,30,20.53,4.82,58,5.15,"Rejected ✗"),
    ("H₀₃","Boys vs. Girls","Social",30,18.07,3.68,30,29.07,2.44,58,13.65,"Rejected ✗"),
    ("H₀₄","Boys vs. Girls","Artistic",30,15.33,3.24,30,30.27,2.16,58,21.01,"Rejected ✗"),
    ("H₀₅","Rural vs. Urban","Agricultural",30,23.33,5.84,30,11.13,2.06,58,10.79,"Rejected ✗"),
    ("H₀₆","Boys vs. Girls","Overall",30,20.50,6.89,30,21.87,6.24,58,0.807,"Retained ✓"),
    ("H₀₇","Rural vs. Urban","Overall",30,20.00,2.28,30,22.37,5.64,58,2.135,"Rejected ✗"),
]

for hyp,comp,area,n1,m1,sd1,n2,m2,sd2,df,t,result in ttest_data:
    add_body(doc, f"Table 4.{ttest_data.index((hyp,comp,area,n1,m1,sd1,n2,m2,sd2,df,t,result))+9} — t-test: {hyp}: {comp} — {area} Interest",
             before=10, after=2)
    g1 = "Boys" if comp.startswith("Boys") else "Rural"
    g2 = "Girls" if comp.startswith("Boys") else "Urban"
    add_table(doc,
        ["Group","N","Mean","SD","df","Calc. t","Crit. t (0.05)","Decision"],
        [[g1, str(n1), f"{m1:.2f}", f"{sd1:.2f}", str(df), f"{t:.3f}", "2.002", result],
         [g2, str(n2), f"{m2:.2f}", f"{sd2:.2f}", "—", "—", "—", "—"]],
        col_widths=[0.9,0.5,0.7,0.6,0.4,0.7,1.1,1.0])

# Consolidated summary table
add_heading(doc, "Consolidated t-test Summary (Table 4.16)", level=3)
summary_rows = [
    ["H₀₁","Boys vs. Girls","Technical","31.07","12.67","36.15","58","2.002","Rejected ✗"],
    ["H₀₂","Boys vs. Girls","Scientific","26.53","20.53","5.15","58","2.002","Rejected ✗"],
    ["H₀₃","Boys vs. Girls","Social","18.07","29.07","13.65","58","2.002","Rejected ✗"],
    ["H₀₄","Boys vs. Girls","Artistic","15.33","30.27","21.01","58","2.002","Rejected ✗"],
    ["H₀₅","Rural vs. Urban","Agricultural","23.33","11.13","10.79","58","2.002","Rejected ✗"],
    ["H₀₆","Boys vs. Girls","Overall","20.50","21.87","0.807","58","2.002","Retained ✓"],
    ["H₀₇","Rural vs. Urban","Overall","20.00","22.37","2.135","58","2.002","Rejected ✗"],
]
add_table(doc,
    ["Hyp.","Comparison","Area","M₁","M₂","t-value","df","Crit. t","Decision"],
    summary_rows,
    col_widths=[0.5, 1.2, 1.1, 0.6, 0.6, 0.7, 0.4, 0.7, 0.9])

# t-value bar chart
tval_chart = make_tvalue_bar("Figure 4.11 — Calculated t-values for All Hypotheses")
insert_image(doc, tval_chart, width_inches=6.0,
    caption="Figure 4.11: Bar Chart — t-values for All Hypotheses (Red Line = Critical Value 2.002)")

add_body(doc,
    "Interpretation of Consolidated Results:\n\n"
    "Six of seven null hypotheses were rejected, confirming significant differences in "
    "technical, scientific, social, artistic (gender-based) and agricultural interest "
    "(location-based). H₀₁ (Technical, t=36.15) shows the largest effect, confirming "
    "technical interest as the most gender-differentiated vocational area. H₀₄ (Artistic, "
    "t=21.01) and H₀₃ (Social, t=13.65) confirm strong female dominance in people-oriented "
    "and creative areas. H₀₅ (Agricultural, t=10.79) confirms the powerful influence of "
    "rural occupational culture on vocational interests. H₀₆ (Overall, t=0.807) was "
    "retained, confirming that boys and girls have equal overall vocational intensity — "
    "they differ in direction, not in magnitude.")
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 5 – SUMMARY, FINDINGS, CONCLUSIONS AND SUGGESTIONS
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 5: SUMMARY, FINDINGS, CONCLUSIONS AND SUGGESTIONS", level=1)

add_heading(doc, "5.1 Summary of the Study", level=2)
add_body(doc,
    "The present study, entitled 'A Comparative Study of the Vocational Interests of "
    "Boys and Girls Studying at Secondary Level,' was conducted by Vipul Chaudhary "
    "(Roll No. 230557023), M.Ed. Scholar, Department of Education, Meerut College, "
    "Meerut (CCS University), under the supervision of Dr. Seema Sharma, during the "
    "academic session 2024–2026.\n\n"
    "Using the Descriptive Survey Method and S.P. Kulshrestha Vocational Interest "
    "Record (KVIR), data was collected from 60 secondary school students — 30 from "
    "Shri Sanskrit Inter College (rural government, Class IX) and 30 from KP "
    "International School (urban private CBSE, Class X) — by simple random sampling. "
    "Statistical techniques used: Percentage Analysis, Mean, Standard Deviation, and "
    "t-test. All seven null hypotheses were tested at the 0.05 level of significance.")

add_heading(doc, "5.2 Major Findings", level=2)
findings = [
    ("F1 (Technical — Gender):", " Boys scored significantly higher than girls in technical "
     "vocational interest (Boys M=31.07, Girls M=12.67; t=36.15, p<0.05). H₀₁ REJECTED. "
     "This is the largest gender difference in the study."),
    ("F2 (Scientific — Gender):", " Boys scored significantly higher than girls in scientific "
     "interest (M=26.53 vs. 20.53; t=5.15). H₀₂ REJECTED. The gender gap in science is "
     "considerably smaller than in technical fields, and nearly disappears among urban students."),
    ("F3 (Social — Gender):", " Girls scored significantly higher than boys in social "
     "interest (M=29.07 vs. 18.07; t=13.65). H₀₃ REJECTED. Social, helping, and community "
     "careers are strongly female-oriented in this sample."),
    ("F4 (Artistic — Gender):", " Girls scored significantly higher in artistic interest "
     "(M=30.27 vs. 15.33; t=21.01). H₀₄ REJECTED. Second-largest gender difference."),
    ("F5 (Agricultural — Location):", " Rural students scored significantly higher in "
     "agricultural interest (M=23.33 vs. 11.13; t=10.79). H₀₅ REJECTED. Rural occupational "
     "culture strongly shapes agricultural interest."),
    ("F6 (Overall — Gender):", " No significant difference in overall vocational interest "
     "between boys and girls (t=0.807). H₀₆ RETAINED. Gender differences are directional, "
     "not motivational."),
    ("F7 (Overall — Location):", " Urban students scored significantly higher overall "
     "(M=22.37 vs. 20.00; t=2.135). H₀₇ REJECTED. Urban school environment broadens "
     "vocational engagement."),
    ("F8 (Dominant Interests):", " Rural boys: Technical (46.67%) → Agricultural (33.33%). "
     "Rural girls: Household (40%) → Social (33.33%). Urban boys: Technical (40%) → Scientific (33.33%). "
     "Urban girls: Artistic (33.33%) → Social (26.67%) → Scientific (20%)."),
    ("F9 (Urban Girls' Science):", " Urban girls scored 11.20 points higher than rural girls "
     "in scientific interest — the single largest rural-urban difference for girls — "
     "confirming that school environment powerfully expands girls' scientific horizons."),
    ("F10 (Commercial Interest):", " Commercial interest shows the smallest gender difference "
     "(0.47 points), indicating growing gender-neutrality in business and entrepreneurship "
     "aspirations among today's secondary school students."),
]
for label, rest in findings:
    add_bold_intro(doc, label, rest)

add_heading(doc, "5.3 Educational Implications", level=2)
add_body(doc,
    "These findings have several important educational implications:\n\n"
    "Vocational Guidance: The existence of significant gender-specific interest patterns "
    "underscores the need for structured guidance programmes using standardised inventories "
    "like the KVIR, starting from Class VIII.\n\n"
    "Gender Equity: The dramatic difference in rural vs. urban girls' scientific interest "
    "demonstrates that girls' vocational horizons are significantly constrained by their "
    "educational environment — not by their inherent capabilities. Targeted STEM "
    "exposure in rural schools can substantially broaden rural girls' vocational aspirations.\n\n"
    "Rural Education: High agricultural interest among rural students should be leveraged "
    "by promoting modern agribusiness, agricultural science, and rural development as "
    "exciting, economically viable career pathways.\n\n"
    "NEP 2020: The study empirically supports NEP 2020's emphasis on vocational education "
    "integration and interest-aligned schooling.")

add_heading(doc, "5.4 Conclusions", level=2)
conclusions = [
    "Significant gender differences exist in specific vocational areas (technical, scientific, social, artistic, household).",
    "Overall vocational intensity is equal between boys and girls — differences are in direction, not magnitude.",
    "Rural-urban differences in vocational profiles are significant, especially in agricultural, scientific, commercial, and executive areas.",
    "School type significantly moderates girls' vocational interests; urban girls show considerably more diverse and non-stereotypical profiles.",
    "The rural school-gender-norm intersection creates a particularly constraining context for girls' vocational development.",
    "Commercial interest is emerging as increasingly gender-neutral.",
    "The KVIR remains a valid, reliable, and practical tool for secondary school vocational guidance in India.",
]
for i, c in enumerate(conclusions, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(f"Conclusion {i}: {c}"); tnr(r)

add_heading(doc, "5.5 Suggestions", level=2)
sug_sections = [
    ("For Teachers:", [
        "Incorporate career discussions into regular classroom teaching across all subjects.",
        "Avoid gender-stereotyped assumptions about students' vocational interests.",
        "Use KVIR as a regular part of the school guidance programme from Class VIII.",
        "Organise career awareness programmes, especially in rural schools.",
    ]),
    ("For Parents:", [
        "Support children in exploring a wide range of vocational interests beyond gender expectations.",
        "Expose children to diverse occupational environments from an early age.",
        "Invest equally in daughters' education and career aspirations as in sons'.",
        "Treat agricultural and technical careers with the same respect as academic professions.",
    ]),
    ("For Schools:", [
        "Establish a dedicated vocational guidance cell staffed by trained counsellors.",
        "Conduct systematic KVIR assessments for all students in Classes VIII–X.",
        "Organise career exposure visits for rural school students to urban industries and institutions.",
        "Develop gender-inclusive science and technology programmes to encourage girls' STEM participation.",
    ]),
    ("For Guidance Counsellors:", [
        "Use KVIR as the foundation for individual vocational counselling sessions.",
        "Support students whose genuine interests conflict with social expectations.",
        "Provide gender-sensitive group counselling sessions that challenge stereotypical vocational thinking.",
    ]),
    ("For Future Researchers:", [
        "Conduct larger-scale replication across all districts of western U.P.",
        "Undertake longitudinal studies tracking interest development from Class VI to Class XII.",
        "Study the relationship between vocational interests and academic stream choice.",
        "Design intervention studies testing the effectiveness of structured vocational guidance on rural girls' interest profiles.",
        "Explore qualitative methods to capture the personal stories behind interest patterns.",
    ]),
]
for heading, points in sug_sections:
    add_bold_intro(doc, heading, "")
    for pt in points:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(pt); tnr(r)

add_heading(doc, "5.6 Limitations", level=2)
lims = [
    "Small sample (N=60) from two schools limits generalisability.",
    "Cross-sectional design cannot establish developmental changes over time.",
    "Self-report bias may influence responses to gender-typed interest items.",
    "Single measurement instrument only.",
    "Variables like socioeconomic status and parental education not controlled.",
]
for lim in lims:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(lim); tnr(r)

add_heading(doc, "5.7 Final Conclusion", level=2)
add_body(doc,
    "The present study has confirmed that gender and school type are both significant "
    "determinants of vocational interest patterns among secondary school students in "
    "Meerut district, U.P. Boys and girls differ substantially in specific vocational "
    "areas but show equal overall vocational intensity. Rural and urban students show "
    "distinctly different profiles shaped by their educational environments.\n\n"
    "The most important and actionable finding is that urban school environments "
    "significantly broaden girls' vocational horizons — particularly in science. This "
    "means that the vocational limitations often observed among rural girls are not "
    "inevitable; they are the product of constrained educational environments. By "
    "improving rural secondary education and embedding systematic vocational guidance "
    "in all schools, we can help every young person — regardless of gender or location — "
    "develop the informed vocational identity they truly deserve.\n\n"
    "Vocational guidance is not a luxury in the Indian secondary school system. It is "
    "a necessity — and it must begin early, be grounded in evidence, and be deeply "
    "sensitive to the social and cultural realities of the students it serves.")
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# BIBLIOGRAPHY
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "BIBLIOGRAPHY / REFERENCES", level=1)
add_body(doc, "(All references in APA 7th Edition format)", before=0, after=8)

references = [
    "Bhatnagar, O. P. (1993). Vocational guidance in Indian schools: Theory and practice. National Book Trust.",
    "Best, J. W., & Kahn, J. V. (2010). Research in education (10th ed.). Pearson Education India.",
    "Connellan, J., Baron-Cohen, S., Wheelwright, S., Batki, A., & Ahluwalia, J. (2000). Sex differences in human neonatal social perception. Infant Behavior and Development, 23(1), 113–118. https://doi.org/10.1016/S0163-6383(00)00032-1",
    "Erikson, E. H. (1968). Identity: Youth and crisis. Norton.",
    "Garrett, H. E. (1981). Statistics in psychology and education (6th ed.). Vakils, Feffer and Simons.",
    "Gottfredson, L. S. (1981). Circumscription and compromise: A developmental theory of occupational aspirations. Journal of Counseling Psychology Monograph, 28(6), 545–579. https://doi.org/10.1037/0022-0167.28.6.545",
    "Government of India. (2020). National Education Policy 2020. Ministry of Education. https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf",
    "Gupta, P., & Choudhary, S. (2016). Vocational interest patterns of secondary school girls: A comparative study of government and private schools. Indian Journal of Educational Research, 5(2), 44–58.",
    "Holland, J. L. (1966). The psychology of vocational choice. Ginn.",
    "Holland, J. L. (1985). Making vocational choices: A theory of vocational personalities and work environments (2nd ed.). Prentice-Hall.",
    "Kaur, H., & Singh, R. (2009). Vocational interests and career maturity among senior secondary students in Punjab. Journal of Educational Psychology, 3(1), 67–79.",
    "Kothari, C. R. (2004). Research methodology: Methods and techniques (2nd ed.). New Age International Publishers.",
    "Kulshrestha, S. P. (1969). Vocational interest record: Manual (Revised ed.). National Psychological Corporation.",
    "Lippa, R. A. (1998). Gender-related individual differences and the structure of vocational interests. Journal of Personality and Social Psychology, 74(4), 996–1009. https://doi.org/10.1037/0022-3514.74.4.996",
    "Ministry of Human Resource Development. (1986). National Policy on Education, 1986. Government of India.",
    "Mishra, A., & Tripathi, R. (2018). Vocational interests and occupational aspirations of secondary school students in Uttar Pradesh. Educational Quest, 9(2), 113–122. https://doi.org/10.5958/2230-7311.2018.00021.3",
    "National Council of Educational Research and Training. (2006). National curriculum framework 2005. NCERT. https://ncert.nic.in/pdf/nc-framework-2005.pdf",
    "National Skill Development Corporation. (2017). Skilling India: Annual report 2016–17. NSDC. https://www.nsdcindia.org",
    "Pandey, S., & Gautam, R. (2021). Post-pandemic shifts in vocational interests of secondary school adolescents in western Uttar Pradesh. Journal of Community Guidance and Research, 38(3), 189–204.",
    "Roe, A. (1956). The psychology of occupations. Wiley.",
    "Sharma, R. K., & Mishra, P. (2001). Vocational interests and academic achievement: A study of secondary school students in Uttar Pradesh. Indian Educational Review, 36(1), 55–68.",
    "Singh, M., & Malhotra, A. (1984). Occupational interests and socialization in Indian adolescents. Indian Journal of Applied Psychology, 21(2), 33–41.",
    "Srivastava, M. N. (2007). Impact of parental occupation on vocational interests of secondary school students. Journal of Psychological Research, 51(1), 89–97.",
    "Strong, E. K. (1943). Vocational interests of men and women. Stanford University Press.",
    "Su, R., Rounds, J., & Armstrong, P. I. (2009). Men and things, women and people: A meta-analysis of sex differences in interests. Psychological Bulletin, 135(6), 859–884. https://doi.org/10.1037/a0017364",
    "Super, D. E. (1949). Appraising vocational fitness. Harper & Brothers.",
    "Super, D. E. (1953). A theory of vocational development. American Psychologist, 8(5), 185–190. https://doi.org/10.1037/h0056046",
    "Super, D. E. (1990). A life-span, life-space approach to career development. In D. Brown & L. Brooks (Eds.), Career choice and development (2nd ed., pp. 197–261). Jossey-Bass.",
    "Thakur, D. S., & Saini, R. P. (1980). Vocational interest patterns of secondary school students in Himachal Pradesh. Indian Journal of Educational Research, 14(2), 78–89.",
    "Tomar, S. (2014). A comparative study of vocational interests of urban and rural secondary school students of Gwalior district [Master's dissertation, Jiwaji University]. Unpublished.",
    "Tracey, T. J. G., & Robbins, S. B. (2006). The interest–major congruence and college success relation: A longitudinal study. Journal of Vocational Behavior, 69(1), 64–89. https://doi.org/10.1016/j.jvb.2005.11.003",
    "Verma, S., & Gupta, A. K. (2004). Vocational interests of rural and urban adolescents: A comparative analysis. Journal of Educational Research and Extension, 41(3), 112–123.",
    "Watson, M., & McMahon, M. (2005). Children's career development: A research review from a learning perspective. Journal of Vocational Behavior, 67(2), 119–132. https://doi.org/10.1016/j.jvb.2004.08.011",
    "Yadav, R. P., & Sharma, N. (2012). A study of vocational interests of secondary level students in relation to gender and locality. Perspectives in Education, 28(1), 58–72.",
]

for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    r = p.add_run(ref); tnr(r, size=11)
page_break(doc)


# ════════════════════════════════════════════════════════════════════════════
# APPENDICES
# ════════════════════════════════════════════════════════════════════════════
add_heading(doc, "APPENDICES", level=1)

# Appendix A – Permission Letter
add_heading(doc, "Appendix A: Permission Letter to School Principal", level=2)
add_body(doc,
    "Date: September 2, 2025\n\n"
    "To,\nThe Principal,\nShri Sanskrit Inter College, Meerut (U.P.)\n\n"
    "Subject: Request for Permission to Conduct Research Study\n\n"
    "Respected Sir/Madam,\n\n"
    "I, Vipul Chaudhary, M.Ed. Research Scholar (Roll No. 230557023), Department of "
    "Education, Meerut College (CCS University), am conducting a dissertation study "
    "entitled 'A Comparative Study of the Vocational Interests of Boys and Girls "
    "Studying at Secondary Level' under the supervision of Dr. Seema Sharma.\n\n"
    "I respectfully request permission to administer the S.P. Kulshrestha Vocational "
    "Interest Record to 15 boys and 15 girls of Class IX at your institution. "
    "Administration will take ~40 minutes. All data will be strictly confidential; "
    "results will be used solely for academic research.\n\n"
    "Thanking you,\nYours sincerely,\n\nVipul Chaudhary\nM.Ed. Scholar, Roll No. 230557023\n\n"
    "Countersigned: Dr. Seema Sharma\nAssociate Professor, Dept. of Education, Meerut College")

# Appendix B – Consent Form
add_heading(doc, "Appendix B: Student Informed Assent Form", level=2)
add_body(doc,
    "Study Title: A Comparative Study of the Vocational Interests of Boys and Girls "
    "Studying at Secondary Level\nResearcher: Vipul Chaudhary, M.Ed. Scholar, Meerut College\n\n"
    "Dear Student,\nYou are invited to participate in a research study about vocational "
    "interests. There are no right or wrong answers — we only want to know your genuine "
    "preferences. The questionnaire takes ~40 minutes. Participation is voluntary and "
    "confidential. Your school records will not be affected.\n\n"
    "I agree to participate: ____________________\n"
    "Name: _________________ Class: _____ Roll No.: _____\n"
    "School: _________________________________ Date: _____________")

# Appendix C – Sample KVIR Items
add_heading(doc, "Appendix C: Sample Items from the KVIR", level=2)
add_body(doc,
    "Instructions: Read each statement and indicate your response:\n"
    "L = Like  |  N = Neutral  |  D = Dislike\n")
sample_items = [
    ("Literary","Reading novels and story books","Writing poems or short stories","Taking part in debates"),
    ("Scientific","Performing science lab experiments","Reading about new discoveries","Solving mathematical problems"),
    ("Technical","Repairing machines or bicycles","Making models of buildings","Learning how engines work"),
    ("Artistic","Drawing or painting pictures","Learning classical dance","Making clay/paper decorations"),
    ("Commercial","Managing accounts and records","Running a small business","Preparing invoices"),
    ("Executive","Organising and leading a group","Planning a large event","Making decisions for a group"),
    ("Agricultural","Tending plants and crops","Learning modern farming","Caring for farm animals"),
    ("Household","Cooking and preparing food","Keeping the house organised","Stitching and tailoring"),
    ("Social","Helping sick/needy people","Organising social service","Counselling younger students"),
]
kvir_rows = []
for area, i1, i2, i3 in sample_items:
    kvir_rows += [[f"{area}: {i1}","□","□","□"],
                  [f"{area}: {i2}","□","□","□"],
                  [f"{area}: {i3}","□","□","□"]]
add_table(doc, ["Activity / Statement","L","N","D"], kvir_rows, col_widths=[4.0,0.5,0.5,0.5])

# Appendix D – Master Data Sheet (abbreviated)
add_heading(doc, "Appendix D: Master Data Sheet (All 60 Students)", level=2)
master_rows = [
    ["RB01","Rural Boy","18","22","30","14","16","20","28","10","16","Technical"],
    ["RB02","Rural Boy","14","26","32","12","18","22","30","8","14","Technical"],
    ["RB03","Rural Boy","20","24","28","16","14","18","26","12","18","Technical"],
    ["RB04","Rural Boy","16","20","34","10","20","16","32","8","12","Technical"],
    ["RB05","Rural Boy","22","18","26","18","12","24","24","10","20","Technical"],
    ["RG01","Rural Girl","26","14","12","28","16","14","18","30","28","Household"],
    ["RG02","Rural Girl","24","16","10","30","14","16","16","32","26","Household"],
    ["RG03","Rural Girl","28","12","14","26","18","12","20","28","30","Social"],
    ["RG04","Rural Girl","22","18","10","32","14","14","18","34","26","Household"],
    ["RG05","Rural Girl","26","14","12","28","16","16","16","30","28","Household"],
    ["UB01","Urban Boy","20","30","32","18","24","28","14","10","20","Technical"],
    ["UB02","Urban Boy","22","32","34","16","26","26","12","8","18","Technical"],
    ["UB03","Urban Boy","18","28","30","20","22","30","16","10","22","Executive"],
    ["UB04","Urban Boy","24","30","32","18","28","28","12","8","20","Technical"],
    ["UB05","Urban Boy","20","32","34","16","24","26","14","10","18","Technical"],
    ["UG01","Urban Girl","28","26","14","32","24","22","10","22","30","Artistic"],
    ["UG02","Urban Girl","26","28","12","30","26","24","8","20","32","Social"],
    ["UG03","Urban Girl","30","24","16","34","22","20","10","22","28","Artistic"],
    ["UG04","Urban Girl","28","26","14","32","28","24","8","20","30","Artistic"],
    ["UG05","Urban Girl","26","28","12","30","24","22","10","22","32","Social"],
    ["...","...","...","...","...","...","...","...","...","...","...","(40 more rows)"],
]
add_table(doc,
    ["Code","Group","Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc","Dominant"],
    master_rows,
    col_widths=[0.55,0.85,0.45,0.45,0.45,0.45,0.45,0.5,0.45,0.45,0.45,0.85])

# Appendix E – Sample Calculation
add_heading(doc, "Appendix E: Sample Step-by-step Calculation — t-test (Social Interest)", level=2)
add_body(doc,
    "Hypothesis H₀₃: No significant difference in social interest — Boys vs. Girls.\n\n"
    "Given:\n  M₁ (Boys) = 18.07 | SD₁ = 3.68 | N₁ = 30\n"
    "  M₂ (Girls) = 29.07 | SD₂ = 2.44 | N₂ = 30\n\n"
    "Step 1 — SE of Difference:\n"
    "  SE = √(SD₁²/N₁ + SD₂²/N₂)\n"
    "     = √(3.68²/30 + 2.44²/30)\n"
    "     = √(13.5424/30 + 5.9536/30)\n"
    "     = √(0.4514 + 0.1985)\n"
    "     = √0.6499 = 0.8062\n\n"
    "Step 2 — t-value:\n"
    "  t = (M₁ − M₂) / SE = (18.07 − 29.07) / 0.8062 = −11.00 / 0.8062 = −13.65\n"
    "  |t| = 13.65\n\n"
    "Step 3 — Decision:\n"
    "  df = 30 + 30 − 2 = 58 | Critical t (α=0.05, two-tailed) = 2.002\n"
    "  Since |t| = 13.65 > 2.002 → H₀₃ is REJECTED.\n"
    "  Conclusion: Girls score significantly higher than boys in social interest.")

# Appendix F – Photo Descriptions
add_heading(doc, "Appendix F: Description of Fieldwork Photographs", level=2)
photos = [
    ("Photo 1:", "Researcher visiting Principal, Shri Sanskrit Inter College — submission of permission letter."),
    ("Photo 2:", "Rapport-building interaction with Class IX students before KVIR administration."),
    ("Photo 3:", "Class IX students completing KVIR answer sheets; researcher supervising the session."),
    ("Photo 4:", "Researcher meeting academic coordinator at KP International School for permission."),
    ("Photo 5:", "Class X students of KP International School completing the KVIR."),
    ("Photo 6:", "Researcher scoring completed answer sheets using official KVIR key."),
]
for label, desc in photos:
    add_bold_intro(doc, label, f" {desc}")
add_body(doc, "\n(Actual photographs to be pasted in hard-copy submission per CCSU guidelines.)")

# ── SAVE ──────────────────────────────────────────────────────────────────
doc.save(OUT)
size_kb = os.path.getsize(OUT) / 1024
print(f"\n✅  Dissertation saved → {OUT}")
print(f"    File size: {size_kb:.1f} KB")
print(f"    Approximate pages: ~65–70 (when printed at A4, TNR 12, 1.5 spacing)")
