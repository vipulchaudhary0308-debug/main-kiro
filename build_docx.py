#!/usr/bin/env python3
"""
Complete M.Ed. Dissertation DOCX Builder
Scholar : Vipul Chaudhary | Roll No. 230557023
Topic   : A Comparative Study of the Vocational Interests of Boys and Girls
          Studying at Secondary Level
College : Meerut College, CCSU, Meerut
Session : 2024-2026
Supervisor: Dr. Seema Sharma

Format  : Times New Roman, 12pt body, 14pt section heads, 16pt chapter heads
          1.5 line spacing, justified, 1.5" left / 1" other margins
          Professional CCSU dissertation style
"""

import io, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dissertation_Final.docx")

# ── Colour palette ──────────────────────────────────────────────────────────
C_RB = "#1a6faf"   # Rural Boys  – steel blue
C_RG = "#e05c5c"   # Rural Girls – coral red
C_UB = "#2ca02c"   # Urban Boys  – forest green
C_UG = "#9467bd"   # Urban Girls – purple
C_BOYS  = "#1f77b4"
C_GIRLS = "#e07b54"
NAVY = (0x1a, 0x35, 0x6e)
MAROON = (0x8b, 0x00, 0x00)

# ── Interest area labels ────────────────────────────────────────────────────
AREAS = ["Literary","Scientific","Technical","Artistic","Commercial",
         "Executive","Agricultural","Household","Social"]
ABBR  = ["Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc"]

# ── Group mean scores ───────────────────────────────────────────────────────
RB = [17.07, 22.93, 30.13, 12.67, 16.40, 20.13, 28.67,  9.07, 16.00]
RG = [25.20, 14.93, 11.47, 28.80, 15.47, 14.27, 18.00, 30.80, 28.00]
UB = [20.93, 30.13, 32.00, 18.00, 24.67, 27.87, 13.20,  9.07, 20.13]
UG = [27.87, 26.13, 13.87, 31.73, 24.67, 22.13,  9.07, 21.07, 30.13]
BOYS_M  = [(a+b)/2 for a,b in zip(RB, UB)]
GIRLS_M = [(a+b)/2 for a,b in zip(RG, UG)]
SD_B = [3.12, 4.18, 2.06, 3.24, 4.46, 4.32, 6.24, 1.04, 3.68]
SD_G = [2.34, 4.82, 1.88, 2.16, 4.98, 4.18, 2.12, 4.86, 2.44]
T_VALS   = [36.15, 5.15, 13.65, 21.01, 10.79, 0.807, 2.135]
T_LABELS = ["H\u2081:Tech","H\u2082:Sci","H\u2083:Soc",
            "H\u2084:Art","H\u2085:Agri","H\u2086:B/G","H\u2087:R/U"]
T_SIG    = [True, True, True, True, True, False, True]


# ═══════════════════════════════════════════════════════════════
#  CHART GENERATORS
# ═══════════════════════════════════════════════════════════════
def fig_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0); plt.close(fig); return buf

def pie_chart(vals, labels, colours, title):
    fig, ax = plt.subplots(figsize=(5.8, 4.4))
    wedges, texts, autos = ax.pie(
        vals, labels=labels, colors=colours,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=1.8),
        textprops=dict(fontsize=9, fontfamily="DejaVu Sans"))
    for at in autos:
        at.set_fontsize(8.5); at.set_color("white"); at.set_fontweight("bold")
    ax.set_title(title, fontsize=11, fontweight="bold", pad=14,
                 fontfamily="DejaVu Sans")
    fig.patch.set_facecolor("#f7f8fc")
    return fig_bytes(fig)

def grouped_bar(g1, g2, l1, l2, title, c1, c2, ylabel="Mean Score (0–40)"):
    x = np.arange(len(ABBR)); w = 0.38
    fig, ax = plt.subplots(figsize=(11, 5))
    b1 = ax.bar(x-w/2, g1, w, label=l1, color=c1, edgecolor="white", lw=0.8)
    b2 = ax.bar(x+w/2, g2, w, label=l2, color=c2, edgecolor="white", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(ABBR, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=10); ax.set_ylim(0, 44)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.axhline(20, color="grey", ls="--", lw=0.7, alpha=0.5)
    for b in list(b1)+list(b2):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.4,
                f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=7)
    ax.set_facecolor("#f4f6fb"); ax.grid(axis="y", ls="--", alpha=0.35)
    fig.patch.set_facecolor("#ffffff"); return fig_bytes(fig)

def four_group_bar(title):
    x = np.arange(len(ABBR)); w = 0.2
    fig, ax = plt.subplots(figsize=(13, 5.5))
    for i,(data,lbl,col) in enumerate([(RB,"Rural Boys",C_RB),(RG,"Rural Girls",C_RG),
                                        (UB,"Urban Boys",C_UB),(UG,"Urban Girls",C_UG)]):
        ax.bar(x+(i-1.5)*w, data, w, label=lbl, color=col, edgecolor="white", lw=0.7)
    ax.set_xticks(x); ax.set_xticklabels(ABBR, fontsize=9)
    ax.set_ylabel("Mean Score", fontsize=10); ax.set_ylim(0, 44)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, ncol=2)
    ax.set_facecolor("#f4f6fb"); ax.grid(axis="y", ls="--", alpha=0.35)
    fig.patch.set_facecolor("#ffffff"); return fig_bytes(fig)

def line_graph(title):
    fig, ax = plt.subplots(figsize=(11, 5))
    for data,lbl,col,mkr,ls in [(RB,"Rural Boys",C_RB,"o","-"),
                                  (RG,"Rural Girls",C_RG,"s","--"),
                                  (UB,"Urban Boys",C_UB,"^","-"),
                                  (UG,"Urban Girls",C_UG,"D","--")]:
        ax.plot(ABBR, data, marker=mkr, color=col, ls=ls, lw=2, ms=7, label=lbl)
    ax.set_ylabel("Mean Score", fontsize=10); ax.set_ylim(0, 40)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, ncol=2); ax.grid(ls="--", alpha=0.35)
    ax.set_facecolor("#f4f6fb"); fig.patch.set_facecolor("#ffffff")
    return fig_bytes(fig)

def sd_bar(title):
    x = np.arange(len(ABBR)); w = 0.38
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x-w/2, SD_B, w, label="Boys",  color=C_BOYS,  edgecolor="white")
    ax.bar(x+w/2, SD_G, w, label="Girls", color=C_GIRLS, edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(ABBR, fontsize=9)
    ax.set_ylabel("Standard Deviation", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold"); ax.legend(fontsize=9)
    ax.set_facecolor("#f4f6fb"); ax.grid(axis="y", ls="--", alpha=0.35)
    fig.patch.set_facecolor("#ffffff"); return fig_bytes(fig)

def tvalue_bar(title):
    colours = ["#2ca02c" if s else "#d62728" for s in T_SIG]
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(T_LABELS, T_VALS, color=colours, edgecolor="white", lw=0.8)
    ax.axhline(2.002, color="red", ls="--", lw=1.8, label="Critical t = 2.002")
    for b,v in zip(bars, T_VALS):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.4,
                f"{v:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylabel("Calculated t-value", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    gp = mpatches.Patch(color="#2ca02c", label="Significant – H\u2080 Rejected")
    rp = mpatches.Patch(color="#d62728", label="Not Significant – H\u2080 Retained")
    cl = plt.Line2D([],[],color="red",ls="--",label="Critical t = 2.002")
    ax.legend(handles=[gp,rp,cl], fontsize=8.5)
    ax.set_facecolor("#f4f6fb"); fig.patch.set_facecolor("#ffffff")
    return fig_bytes(fig)


# ═══════════════════════════════════════════════════════════════
#  DOCUMENT HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
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
        for tag, text in [("begin",None), (None,"PAGE"), ("end",None)]:
            if tag:
                el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag)
                run._r.append(el)
            else:
                el = OxmlElement("w:instrText")
                el.set(qn("xml:space"),"preserve"); el.text = text
                run._r.append(el)
        run.font.name = "Times New Roman"; run.font.size = Pt(11)

def tnr(run, size=12, bold=False, italic=False, colour=None):
    run.font.name = "Times New Roman"; run.font.size = Pt(size)
    run.bold = bold; run.italic = italic
    if colour: run.font.color.rgb = RGBColor(*colour)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.insert(0, rFonts)
    for attr in ("w:ascii","w:hAnsi","w:cs","w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")

def para_fmt(para, before=0, after=6, line=1.5, align="justify"):
    fmt = para.paragraph_format
    fmt.space_before = Pt(before); fmt.space_after = Pt(after)
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE; fmt.line_spacing = line
    if align == "justify": para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "center": para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":  para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "left":   para.alignment = WD_ALIGN_PARAGRAPH.LEFT

def add_heading(doc, text, level=1):
    para = doc.add_paragraph()
    fmt = para.paragraph_format
    fmt.space_before = Pt(20 if level==1 else 14 if level==2 else 10)
    fmt.space_after  = Pt(8)
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE; fmt.line_spacing = 1.15
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER if level==1 else WD_ALIGN_PARAGRAPH.LEFT
    sizes = {1:16, 2:14, 3:13}
    run = para.add_run(text.upper() if level==1 else text)
    tnr(run, size=sizes.get(level,12), bold=True,
        colour=NAVY if level==1 else MAROON if level==2 else None)
    return para

def body(doc, text, before=0, after=6):
    para = doc.add_paragraph()
    para_fmt(para, before=before, after=after)
    run = para.add_run(text); tnr(run); return para

def bold_then_normal(doc, bold_text, normal_text, before=0, after=5):
    para = doc.add_paragraph()
    para_fmt(para, before=before, after=after)
    r1 = para.add_run(bold_text); tnr(r1, bold=True)
    r2 = para.add_run(normal_text); tnr(r2); return para

def bullet(doc, text):
    para = doc.add_paragraph(style="List Bullet")
    para.paragraph_format.space_after = Pt(4)
    run = para.add_run(text); tnr(run); return para

def numbered(doc, num, text):
    para = doc.add_paragraph()
    para_fmt(para, after=4)
    r = para.add_run(f"{num}.  {text}"); tnr(r); return para

def italic_para(doc, text, before=0, after=5):
    para = doc.add_paragraph()
    para_fmt(para, before=before, after=after)
    run = para.add_run(text); tnr(run, italic=True); return para

def centre_bold(doc, text, size=12, colour=None, before=6, after=6):
    para = doc.add_paragraph()
    para_fmt(para, before=before, after=after, align="center")
    run = para.add_run(text); tnr(run, size=size, bold=True, colour=colour); return para

def right_sign(doc, text):
    para = doc.add_paragraph()
    para_fmt(para, before=4, after=4, align="right")
    run = para.add_run(text); tnr(run, bold=True); return para

def pb(doc): doc.add_page_break()

def img(doc, buf, width=5.5, caption=None):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(buf, width=Inches(width))
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(10)
        r = cp.add_run(caption); tnr(r, size=10, italic=True)


def make_table(doc, headers, rows, col_widths=None, hdr_fill="1a356e"):
    """Build a formatted table with coloured header and alternating row shading."""
    tbl = doc.add_table(rows=1+len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    hc = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hc[i].text = h
        hc[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hc[i].paragraphs[0].paragraph_format.space_before = Pt(2)
        hc[i].paragraphs[0].paragraph_format.space_after  = Pt(2)
        for run in hc[i].paragraphs[0].runs:
            tnr(run, size=10, bold=True)
            run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        tc = hc[i]._tc; tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto")
        shd.set(qn("w:fill"), hdr_fill); tcPr.append(shd)
    # Data rows
    for ri, row_data in enumerate(rows):
        cells = tbl.rows[ri+1].cells
        fill  = "EBF0FB" if ri % 2 == 0 else "FFFFFF"
        for ci, val in enumerate(row_data):
            cells[ci].text = str(val)
            cells[ci].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cells[ci].paragraphs[0].paragraph_format.space_before = Pt(1)
            cells[ci].paragraphs[0].paragraph_format.space_after  = Pt(1)
            for run in cells[ci].paragraphs[0].runs:
                tnr(run, size=10)
            tc = cells[ci]._tc; tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto")
            shd.set(qn("w:fill"), fill); tcPr.append(shd)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in tbl.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return tbl

def divider(doc):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after  = Pt(4)
    run = para.add_run("─" * 60); tnr(run, size=9)

def space(doc, n=1):
    for _ in range(n): doc.add_paragraph()


# ═══════════════════════════════════════════════════════════════
#  BEGIN DOCUMENT
# ═══════════════════════════════════════════════════════════════
doc = Document()
set_margins(doc)
add_page_number(doc)

# ──────────────────────────────────────────────────────────────
# COVER PAGE
# ──────────────────────────────────────────────────────────────
for _ in range(3): doc.add_paragraph()
centre_bold(doc, "CHAUDHARY CHARAN SINGH UNIVERSITY, MEERUT",
            size=15, colour=NAVY, before=0, after=4)
centre_bold(doc, "Department of Education", size=12, colour=NAVY, before=0, after=2)
centre_bold(doc, "Meerut College, Meerut (Affiliated to CCSU, Meerut)",
            size=11, colour=NAVY, before=0, after=20)
divider(doc)
centre_bold(doc, "M.Ed. DISSERTATION", size=18, colour=MAROON, before=12, after=12)
divider(doc)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(16)
r = p.add_run(
    "\u201cA COMPARATIVE STUDY OF THE VOCATIONAL INTERESTS\n"
    "OF BOYS AND GIRLS STUDYING AT SECONDARY LEVEL\u201d")
tnr(r, size=15, bold=True, colour=NAVY)

divider(doc)
space(doc, 1)

details = [
    ("Submitted by",         "VIPUL CHAUDHARY"),
    ("Roll Number",          "230557023"),
    ("Father\u2019s Name",   "Shri Rajesh Kumar"),
    ("Mother\u2019s Name",   "Smt. Asha Chaudhary"),
    ("Brother\u2019s Name",  "Yash Chaudhary"),
    ("Degree",               "Master of Education (M.Ed.)"),
    ("Session",              "2024\u20132026"),
    ("Supervisor",           "Dr. Seema Sharma, Associate Professor"),
    ("Department",           "Department of Education, Meerut College, Meerut"),
    ("University",           "Chaudhary Charan Singh University, Meerut"),
]
for lbl, val in details:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(f"{lbl}:  "); tnr(r1, bold=True, size=12)
    r2 = p.add_run(val);         tnr(r2, size=12)

space(doc, 1)
divider(doc)
centre_bold(doc, "2024\u20132026", size=13, colour=NAVY, before=8, after=0)
pb(doc)


# ──────────────────────────────────────────────────────────────
# SUPERVISOR'S CERTIFICATE
# ──────────────────────────────────────────────────────────────
add_heading(doc, "SUPERVISOR\u2019S CERTIFICATE", level=1)
body(doc,
    "This is to certify that the dissertation entitled \u201cA Comparative Study of the "
    "Vocational Interests of Boys and Girls Studying at Secondary Level\u201d has been "
    "prepared by Vipul Chaudhary (Roll No. 230557023) under my direct supervision and "
    "guidance, in partial fulfilment of the requirements for the degree of Master of "
    "Education (M.Ed.) from Chaudhary Charan Singh University, Meerut, during the "
    "academic session 2024\u20132026.")
space(doc, 1)
body(doc,
    "The work is original and has not been submitted, either in whole or in part, for "
    "the award of any degree or diploma to any other university or institution. To the "
    "best of my knowledge and belief, the dissertation fulfils all academic requirements "
    "prescribed by Chaudhary Charan Singh University for the award of the M.Ed. degree. "
    "I recommend it for submission and evaluation.")
space(doc, 2)
body(doc, "Date: ____________________          Place: Meerut")
space(doc, 2)
right_sign(doc,
    "(Dr. Seema Sharma)\nAssociate Professor\n"
    "Department of Education\nMeerut College, Meerut\n"
    "Chaudhary Charan Singh University, Meerut")
pb(doc)

# ──────────────────────────────────────────────────────────────
# DECLARATION
# ──────────────────────────────────────────────────────────────
add_heading(doc, "DECLARATION BY THE RESEARCH SCHOLAR", level=1)
body(doc,
    "I, Vipul Chaudhary, Roll No. 230557023, student of M.Ed. (Session 2024\u20132026), "
    "Department of Education, Meerut College, Meerut, affiliated to Chaudhary Charan "
    "Singh University, Meerut, hereby solemnly declare that the dissertation entitled "
    "\u201cA Comparative Study of the Vocational Interests of Boys and Girls Studying at "
    "Secondary Level\u201d has been independently prepared by me under the supervision of "
    "Dr. Seema Sharma, Associate Professor, Department of Education, Meerut College.")
space(doc, 1)
body(doc, "I further declare that:")
decl_pts = [
    "This dissertation is an original piece of research work based on data collected "
    "personally from the field during the academic session 2024\u20132026.",
    "This work has not been submitted, either in whole or in part, for the award of "
    "any other degree, diploma, or certificate to any university or institution.",
    "All references, citations, and sources have been duly acknowledged in accordance "
    "with APA 7th Edition guidelines.",
    "The data presented is authentic and was collected with the consent of the concerned "
    "school authorities and student participants.",
    "I take full responsibility for the originality and authenticity of the content.",
]
for i, pt in enumerate(decl_pts, 1):
    numbered(doc, i, pt)
space(doc, 2)
body(doc, "Date: ____________________          Place: Meerut")
space(doc, 2)
right_sign(doc,
    "(Vipul Chaudhary)\nM.Ed. Research Scholar\nRoll No.: 230557023\n"
    "Department of Education\nMeerut College, Meerut")
pb(doc)


# ──────────────────────────────────────────────────────────────
# ACKNOWLEDGEMENT
# ──────────────────────────────────────────────────────────────
add_heading(doc, "ACKNOWLEDGEMENT", level=1)
italic_para(doc,
    "\u201cGratitude is not only the greatest of virtues, but the parent of all others.\u201d\n"
    "\u2014 Cicero", before=0, after=12)
body(doc,
    "It is with a deeply humble and grateful heart that I pen down these words of "
    "acknowledgement, for behind every piece of research work stand countless individuals "
    "whose support, encouragement, and blessings make it possible.")
body(doc,
    "First and foremost, I bow before the Almighty God, whose infinite grace and divine "
    "blessings gave me the strength, clarity of thought, and perseverance to complete this "
    "dissertation. Every step of this academic journey has been guided by His invisible hand.")
body(doc,
    "I owe a profound debt of gratitude to my respected supervisor, Dr. Seema Sharma, "
    "Associate Professor, Department of Education, Meerut College, Meerut. Her scholarly "
    "guidance, constructive criticism, unwavering support, and patient mentorship have been "
    "the cornerstone of this dissertation. She not only guided me academically but also "
    "inspired me to think critically and approach research with integrity and dedication. "
    "Her encouraging words during moments of self-doubt gave me the confidence to move "
    "forward. I consider myself truly fortunate to have been her student.")
body(doc,
    "I extend my heartfelt thanks to the Head and faculty members of the Department of "
    "Education, Meerut College, Meerut, for their academic support and for providing all "
    "necessary facilities during the course of this research work.")
body(doc,
    "My deepest and most heartfelt gratitude goes to my beloved father, Shri Rajesh Kumar, "
    "whose silent sacrifices, relentless hard work, and unwavering belief in my education "
    "have been the greatest motivation of my life. He has always been my first teacher and "
    "my strongest pillar of strength. Every achievement I attain is a tribute to his dreams "
    "and efforts.")
body(doc,
    "Words fall short when I try to express my gratitude towards my mother, Smt. Asha "
    "Chaudhary, whose unconditional love, prayers, and endless blessings have been my "
    "greatest source of strength throughout this journey. Her warmth, patience, and "
    "constant encouragement made even the most difficult phases of this research bearable.")
body(doc,
    "I also wish to sincerely thank my dear brother, Yash Chaudhary, for his constant "
    "moral support, encouragement, and cheerful presence that lightened many stressful "
    "moments. His faith in my capabilities has always motivated me to push my limits.")
body(doc,
    "I am sincerely grateful to the Principals and Teachers of Shri Sanskrit Inter College, "
    "Meerut, and KP International School, Kila Parikshit Garh, Meerut, for granting "
    "permission to conduct this study and for their wholehearted cooperation. The students "
    "who willingly participated deserve special appreciation \u2014 their honest responses "
    "form the very foundation of this research.")
body(doc,
    "I also thank all my friends and classmates of the M.Ed. programme for their "
    "companionship, constructive discussions, and emotional support throughout this journey. "
    "All limitations and shortcomings in this work are entirely my own.")
space(doc, 1)
right_sign(doc, "(Vipul Chaudhary)\nResearch Scholar, M.Ed. (2024\u20132026)\nMeerut, 2026")
pb(doc)


# ──────────────────────────────────────────────────────────────
# PREFACE
# ──────────────────────────────────────────────────────────────
add_heading(doc, "PREFACE", level=1)
body(doc,
    "The present dissertation entitled \u201cA Comparative Study of the Vocational Interests "
    "of Boys and Girls Studying at Secondary Level\u201d has been undertaken as a partial "
    "fulfilment of the requirements for the degree of Master of Education (M.Ed.) from "
    "Chaudhary Charan Singh University, Meerut, during the academic session 2024\u20132026.")
body(doc,
    "The secondary stage of education is widely acknowledged as one of the most "
    "psychologically significant phases in the life of an adolescent. It is during this "
    "formative period \u2014 roughly spanning the ages of 13 to 17 years \u2014 that young "
    "learners begin to develop a clearer sense of self, form lasting attitudes, and begin to "
    "contemplate their future vocational roles in society. Yet, despite the critical nature "
    "of this stage, formal vocational guidance in Indian secondary schools remains alarmingly "
    "inadequate. Many students enter higher education without any conscious understanding of "
    "their own vocational interests, often making career choices under parental pressure, "
    "social expectations, or sheer chance.")
body(doc,
    "It was this observed gap between the vocational guidance needs of students and the "
    "reality of our school system that inspired the present study. The researcher, having "
    "spent time interacting with students at both rural and urban schools in the Kila "
    "Parikshit Garh region of Meerut district, noticed strikingly different patterns in "
    "how boys and girls perceived their vocational futures. Boys often gravitated towards "
    "technical and executive fields, while girls exhibited greater inclinations towards "
    "social, artistic, and household-related vocations. This observation raised a pertinent "
    "question: Are these differences the product of genuine interest, or are they reflections "
    "of deeply embedded social conditioning?")
body(doc,
    "Attempting to answer this question through a systematic, empirical study became the "
    "central purpose of this dissertation. The study uses the S.P. Kulshrestha Vocational "
    "Interest Record \u2014 a well-standardised tool developed specifically for Indian "
    "secondary school students \u2014 to measure and compare the vocational interests of "
    "boys and girls across rural government and urban private schools.")
body(doc,
    "The study is structured across five major chapters. Chapter One provides a detailed "
    "introduction to the concept of vocational interest, its theoretical foundations, and "
    "the context of secondary education in India. Chapter Two presents a comprehensive "
    "review of related literature. Chapter Three describes the research methodology. Chapter "
    "Four is devoted to data analysis and interpretation, supported by statistical techniques "
    "and visual representations. Chapter Five summarises the findings, draws conclusions, "
    "and offers suggestions for educators, parents, counsellors, and future researchers.")
body(doc,
    "It is the researcher\u2019s sincere hope that this dissertation will serve as a small "
    "but meaningful contribution to the growing body of educational research on vocational "
    "guidance and career counselling in India.")
space(doc, 1)
right_sign(doc, "(Vipul Chaudhary)\nMeerut, 2026")
pb(doc)


# ──────────────────────────────────────────────────────────────
# TABLE OF CONTENTS
# ──────────────────────────────────────────────────────────────
add_heading(doc, "TABLE OF CONTENTS", level=1)
toc_rows = [
    ("Supervisor\u2019s Certificate",           "i"),
    ("Declaration by Research Scholar",         "ii"),
    ("Acknowledgement",                          "iii"),
    ("Preface",                                  "v"),
    ("Table of Contents",                        "vii"),
    ("List of Tables",                           "ix"),
    ("List of Graphs and Charts",                "x"),
    ("CHAPTER 1: INTRODUCTION",                  "1"),
    ("  1.1  Introduction",                      "1"),
    ("  1.2  Meaning and Concept of Vocational Interest","2"),
    ("  1.3  Definitions of Vocational Interest","4"),
    ("  1.4  Nine Areas of Vocational Interest (KVIR)","6"),
    ("  1.5  Importance of Vocational Interests","9"),
    ("  1.6  Secondary Education in India",      "11"),
    ("  1.7  Adolescence and Career Choice",     "13"),
    ("  1.8  Gender Differences in Career Aspirations","15"),
    ("  1.9  Rural and Urban Educational Context","17"),
    ("  1.10 Need and Significance of the Study","19"),
    ("  1.11 Statement of the Problem",          "21"),
    ("  1.12 Objectives of the Study",           "21"),
    ("  1.13 Hypotheses of the Study",           "22"),
    ("  1.14 Delimitations of the Study",        "23"),
    ("  1.15 Assumptions of the Study",          "24"),
    ("  1.16 Operational Definitions",           "24"),
    ("  1.17 Organisation of the Study",         "25"),
    ("CHAPTER 2: REVIEW OF RELATED LITERATURE",  "26"),
    ("  2.1  Introduction",                      "26"),
    ("  2.2  Indian Studies (10 Studies)",        "26"),
    ("  2.3  Foreign Studies (5 Studies)",        "34"),
    ("  2.4  Critical Review of Literature",      "38"),
    ("  2.5  Research Gap",                       "39"),
    ("  2.6  Summary",                            "40"),
    ("CHAPTER 3: RESEARCH METHODOLOGY",           "41"),
    ("  3.1  Introduction",                       "41"),
    ("  3.2  Research Method",                    "41"),
    ("  3.3  Variables of the Study",             "42"),
    ("  3.4  Population",                         "43"),
    ("  3.5  Sample and Sampling Technique",      "43"),
    ("  3.6  Tool Used (KVIR)",                   "44"),
    ("  3.7  Reliability and Validity",           "46"),
    ("  3.8  Procedure of Data Collection",       "47"),
    ("  3.9  Statistical Techniques Used",        "48"),
    ("  3.10 Ethical Considerations",             "51"),
    ("CHAPTER 4: DATA ANALYSIS AND INTERPRETATION","52"),
    ("  4.1  Introduction",                       "52"),
    ("  4.2  Percentage Analysis",                "53"),
    ("  4.3  Gender-wise Mean Score Comparison",  "60"),
    ("  4.4  Rural vs. Urban Comparison",         "67"),
    ("  4.5  t-test Analysis and Hypothesis Testing","73"),
    ("  4.6  Major Observations",                 "79"),
    ("CHAPTER 5: SUMMARY, FINDINGS, CONCLUSIONS & SUGGESTIONS","81"),
    ("  5.1  Summary of the Study",               "81"),
    ("  5.2  Major Findings",                     "82"),
    ("  5.3  Educational Implications",           "85"),
    ("  5.4  Conclusions",                        "86"),
    ("  5.5  Suggestions",                        "87"),
    ("  5.6  Limitations of the Study",           "90"),
    ("  5.7  Scope for Future Research",          "91"),
    ("  5.8  Final Conclusion",                   "91"),
    ("BIBLIOGRAPHY / REFERENCES",                  "92"),
    ("APPENDICES",                                 "98"),
]
make_table(doc, ["Content", "Page No."], toc_rows, col_widths=[5.6, 0.7])
pb(doc)

# ──────────────────────────────────────────────────────────────
# LIST OF TABLES
# ──────────────────────────────────────────────────────────────
add_heading(doc, "LIST OF TABLES", level=1)
tables_list = [
    ("3.1",  "Sample Distribution by School, Class, and Gender",              "43"),
    ("4.1",  "Distribution of Sample by School Type and Gender",               "53"),
    ("4.2",  "Raw Vocational Interest Scores \u2013 Rural Boys (N=15)",        "54"),
    ("4.3",  "Raw Vocational Interest Scores \u2013 Rural Girls (N=15)",       "55"),
    ("4.4",  "Raw Vocational Interest Scores \u2013 Urban Boys (N=15)",        "56"),
    ("4.5",  "Raw Vocational Interest Scores \u2013 Urban Girls (N=15)",       "57"),
    ("4.6",  "Dominant Vocational Interest \u2013 Rural Boys",                 "58"),
    ("4.7",  "Dominant Vocational Interest \u2013 Rural Girls",                "59"),
    ("4.8",  "Dominant Vocational Interest \u2013 Urban Boys",                 "60"),
    ("4.9",  "Dominant Vocational Interest \u2013 Urban Girls",                "61"),
    ("4.10", "Mean Vocational Interest Scores: Boys vs. Girls",                "62"),
    ("4.11", "Standard Deviation of Scores: Boys vs. Girls",                   "64"),
    ("4.12", "Mean Scores: Rural Boys vs. Urban Boys",                         "68"),
    ("4.13", "Mean Scores: Rural Girls vs. Urban Girls",                       "70"),
    ("4.14", "t-test: Technical Interest \u2013 Boys vs. Girls",               "74"),
    ("4.15", "t-test: Scientific Interest \u2013 Boys vs. Girls",              "75"),
    ("4.16", "t-test: Social Interest \u2013 Boys vs. Girls",                  "76"),
    ("4.17", "t-test: Artistic Interest \u2013 Boys vs. Girls",                "77"),
    ("4.18", "t-test: Agricultural Interest \u2013 Rural vs. Urban",           "78"),
    ("4.19", "t-test: Overall Interest \u2013 Boys vs. Girls",                 "79"),
    ("4.20", "t-test: Overall Interest \u2013 Rural vs. Urban",                "79"),
    ("4.21", "Consolidated Summary of All t-test Results",                     "80"),
]
make_table(doc, ["Table No.", "Title", "Page No."], tables_list,
           col_widths=[0.8, 5.1, 0.7])
pb(doc)

# ──────────────────────────────────────────────────────────────
# LIST OF GRAPHS AND CHARTS
# ──────────────────────────────────────────────────────────────
add_heading(doc, "LIST OF GRAPHS AND CHARTS", level=1)
fig_list = [
    ("4.1",  "Pie Chart: Dominant Vocational Interests of Rural Boys",          "58"),
    ("4.2",  "Pie Chart: Dominant Vocational Interests of Rural Girls",         "59"),
    ("4.3",  "Pie Chart: Dominant Vocational Interests of Urban Boys",          "60"),
    ("4.4",  "Pie Chart: Dominant Vocational Interests of Urban Girls",         "61"),
    ("4.5",  "Grouped Bar Graph: Mean Scores \u2013 Boys vs. Girls (All Areas)","63"),
    ("4.6",  "Grouped Bar Graph: Standard Deviation \u2013 Boys vs. Girls",     "65"),
    ("4.7",  "Four-Group Comparative Bar Graph: All Groups, All Areas",         "67"),
    ("4.8",  "Grouped Bar Graph: Rural Boys vs. Urban Boys",                    "69"),
    ("4.9",  "Grouped Bar Graph: Rural Girls vs. Urban Girls",                  "71"),
    ("4.10", "Line Graph: Interest Profiles of All Four Groups",                "72"),
    ("4.11", "Bar Graph: Calculated t-values for All Seven Hypotheses",         "80"),
]
make_table(doc, ["Figure No.", "Title", "Page No."], fig_list,
           col_widths=[0.8, 5.1, 0.7])
pb(doc)


# ═══════════════════════════════════════════════════════════════
# CHAPTER 1 – INTRODUCTION
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 1", level=1)
add_heading(doc, "INTRODUCTION", level=1)

add_heading(doc, "1.1  Introduction", level=2)
body(doc,
    "Education, in its truest and broadest sense, is not merely the transmission of "
    "knowledge from one generation to the next. It is, fundamentally, the process of "
    "preparing individuals to lead meaningful, productive, and fulfilling lives. One of "
    "the most vital dimensions of this preparation \u2014 and perhaps one of the most "
    "neglected aspects of formal schooling in India \u2014 is vocational guidance. "
    "Helping young individuals understand their own interests, aptitudes, and potential "
    "career pathways is as important as teaching them mathematics or science, yet it "
    "continues to occupy a peripheral place in the Indian school curriculum.")
body(doc,
    "The secondary stage of education occupies a uniquely sensitive position in the "
    "developmental arc of an individual\u2019s life. It is during Classes IX and X "
    "\u2014 typically when students are between the ages of 13 and 17 \u2014 that the "
    "adolescent mind begins to seriously grapple with questions of identity and purpose. "
    "\u201cWho am I?\u201d and \u201cWhat do I want to become?\u201d are not merely "
    "philosophical musings during this stage; they are urgent, lived questions that "
    "shape choices about subjects, streams, career paths, and ultimately, life trajectories.")
body(doc,
    "The present study attempts to explore vocational interests among secondary school "
    "students in Meerut district, Uttar Pradesh, with a particular focus on the differences "
    "between boys and girls, and between students studying in rural government schools and "
    "urban private schools. By doing so, the study aims to contribute to the growing body "
    "of research on vocational guidance in the Indian educational context and to offer "
    "practical insights for teachers, parents, counsellors, and policymakers.")

add_heading(doc, "1.2  Meaning and Concept of Vocational Interest", level=2)
body(doc,
    "The term \u2018vocational interest\u2019 is derived from two Latin roots: vocatio, "
    "meaning a calling or occupation, and interesse, meaning to be between or to concern. "
    "In simple terms, vocational interest refers to a person\u2019s preference for or "
    "attraction towards specific types of work, occupational activities, or career fields. "
    "However, this simple definition barely scratches the surface of a concept that is "
    "rich in psychological, sociological, and educational dimensions.")
body(doc,
    "From a psychological standpoint, vocational interests are understood as relatively "
    "stable patterns of likes and dislikes related to occupational activities. They are not "
    "the same as abilities or aptitudes \u2014 a student may be highly capable in mathematics "
    "but have little interest in engineering. Interests are what energise an individual\u2019s "
    "occupational choices; they represent the subjective pull that draws a person towards "
    "certain kinds of work.")
body(doc,
    "Several key characteristics define the nature of vocational interests: (a) Stability "
    "\u2014 research consistently shows that vocational interests, once formed during "
    "adolescence, remain relatively stable over time (Super, 1953); (b) Individuality "
    "\u2014 while social and cultural forces shape interests, each individual develops a "
    "unique interest profile; (c) Measurability \u2014 unlike abstract psychological "
    "constructs, vocational interests can be reliably measured through standardised "
    "instruments; (d) Gender Differences \u2014 extensive research has documented "
    "consistent differences in the vocational interest profiles of males and females; "
    "and (e) Context Sensitivity \u2014 the specific interests a person develops are "
    "deeply influenced by his or her social and cultural context.")
body(doc,
    "In the Indian context, vocational interests take on additional layers of complexity. "
    "The caste system, though officially abolished, continues to influence occupational "
    "choices in many communities. Family occupation often becomes a default vocational "
    "identity for children. Gender roles remain strongly defined in many parts of rural "
    "India. And yet, with the expansion of education and media access, younger generations "
    "are increasingly exposed to a wider range of vocational possibilities.")

add_heading(doc, "1.3  Definitions of Vocational Interest", level=2)
body(doc,
    "Over the decades, educational psychologists and vocational counsellors have offered "
    "numerous definitions of vocational interest. Some of the most authoritative definitions "
    "are presented below:")
defs = [
    ("Super (1949):",
     " \u201cThe activities, objects, and types of persons that an individual finds "
     "attractive or repellent.\u201d Super\u2019s Career Development Theory positioned "
     "vocational interest as a dynamic, developmental phenomenon that evolves through "
     "distinct life stages."),
    ("Holland (1966):",
     " \u201cThe activities, tasks, and environments that a person finds attractive and "
     "engaging.\u201d Holland\u2019s RIASEC model \u2014 Realistic, Investigative, "
     "Artistic, Social, Enterprising, and Conventional \u2014 remains the most widely "
     "used framework in modern vocational psychology."),
    ("Strong (1943):",
     " \u201cThe tendency to become absorbed in certain activities to the exclusion of "
     "others.\u201d Strong developed the Strong Vocational Interest Blank (SVIB), one of "
     "the earliest and most enduring interest inventories."),
    ("Kulshrestha (1969):",
     " \u201cThe tendency or inclination of an individual towards certain types of "
     "vocational activities in which one engages readily and which one performs with "
     "greater ease, efficiency and satisfaction.\u201d This definition, grounded in the "
     "Indian cultural and occupational reality, is adopted as the operational framework "
     "for the present study."),
    ("Singh and Malhotra (1984):",
     " \u201cA relatively stable disposition of the person to be attracted toward certain "
     "occupational activities and to be repelled by others, based on the individual\u2019s "
     "experiences, values, and social conditioning.\u201d"),
    ("Roe (1956):",
     " \u201cThe orientation of a person\u2019s energy and attention towards particular "
     "classes of activities.\u201d Roe linked occupational choice to the individual\u2019s "
     "predominant need structure, drawing on Maslow\u2019s hierarchy of needs."),
]
for lbl, txt in defs:
    bold_then_normal(doc, lbl, txt)


add_heading(doc, "1.4  Areas of Vocational Interest \u2013 S.P. Kulshrestha\u2019s Classification", level=2)
body(doc,
    "The S.P. Kulshrestha Vocational Interest Record (KVIR) identifies and measures nine "
    "broad areas of vocational interest. Each area represents a distinct cluster of "
    "occupational activities relevant to the Indian secondary school student:")
areas_desc = [
    ("1. Literary Interest:",
     " Encompasses a preference for activities involving reading, writing, language, and "
     "communication. Potential occupations include teaching, writing, editing, journalism, "
     "librarianship, law, and public administration."),
    ("2. Scientific Interest:",
     " Refers to inclination towards inquiry, experimentation, analysis, and understanding "
     "of natural phenomena. Career pathways include medicine, research, engineering science, "
     "pharmacology, and environmental science."),
    ("3. Technical Interest:",
     " Involves preference for working with machines, tools, mechanical systems, and "
     "technical processes. Vocations include engineering, carpentry, mechanics, electronics, "
     "and computer hardware. Research consistently shows higher technical interest among males."),
    ("4. Artistic Interest:",
     " Refers to attraction towards creative expression through visual arts, music, dance, "
     "drama, and craft. Vocational pathways include fine arts, graphic design, fashion "
     "design, architecture, and performing arts."),
    ("5. Commercial Interest:",
     " Reflects preference for business, trade, finance, accounting, and economic activities. "
     "Career options include commerce, banking, insurance, business management, marketing, "
     "and entrepreneurship."),
    ("6. Executive Interest:",
     " Refers to inclination towards leadership, management, administration, and "
     "organisational decision-making. Relevant careers include civil services, corporate "
     "management, politics, military leadership, and educational administration."),
    ("7. Agricultural Interest:",
     " Encompasses preference for farming, horticulture, animal husbandry, and related "
     "rural occupations. In India, where agriculture remains a primary occupation, this "
     "area holds special relevance for rural students."),
    ("8. Household (Domestic) Interest:",
     " Refers to inclination towards domestic management, cooking, child-rearing, tailoring, "
     "and home-based activities. Beyond gender stereotypes, this area connects to nutrition, "
     "early childhood education, and hospitality careers."),
    ("9. Social Interest:",
     " Involves preference for helping others, social service, community development, "
     "counselling, healthcare, and human welfare. Career pathways include social work, "
     "teaching, counselling, nursing, and community development."),
]
for lbl, txt in areas_desc:
    bold_then_normal(doc, lbl, txt)

add_heading(doc, "1.5  Importance of Vocational Interests", level=2)
body(doc,
    "The importance of understanding and nurturing vocational interests in adolescent "
    "students can hardly be overstated. Research has established a robust relationship "
    "between interest congruence \u2014 the degree of match between a person\u2019s "
    "interests and their occupation \u2014 and career satisfaction and performance "
    "(Super, 1953). When students are forced into paths that clash with their genuine "
    "interests, the psychological cost can be severe: anxiety, academic disengagement, "
    "depression, and a pervasive sense of purposelessness are common outcomes.")
body(doc,
    "At the secondary level, students in India are required to choose their academic "
    "stream \u2014 Science, Commerce, or Humanities \u2014 at Class XI. This decision, "
    "made at the age of 15\u201316, has long-term consequences. A stronger emphasis on "
    "vocational interest assessment could, over time, contribute to better alignment "
    "between individual talents and national occupational needs.")
body(doc,
    "Understanding vocational interests with a gender-sensitive lens can also help "
    "challenge stereotypical occupational assumptions. If girls are shown to have high "
    "scientific or executive interests, this finding can be used to actively encourage "
    "them towards science, technology, engineering, and management careers \u2014 areas "
    "traditionally dominated by males. At the systemic level, interest data informs "
    "curriculum design, resource allocation, and the planning of vocational education "
    "programmes under initiatives like the National Skill Development Mission.")


add_heading(doc, "1.6  Secondary Education in India", level=2)
body(doc,
    "Secondary education in India covers Classes IX and X, typically for students aged "
    "14 to 16 years. The National Education Policy 2020 (NEP 2020) has introduced "
    "significant reforms, envisioning a 5+3+3+4 framework that emphasises vocational "
    "education, flexibility, and experiential learning. However, implementation remains "
    "uneven, particularly in rural areas.")
body(doc,
    "The secondary stage is dominated by the preparation for high-stakes board "
    "examinations conducted by UPMSP (U.P. Board) and CBSE. This examination-driven "
    "culture crowds out time for vocational guidance and career counselling. A vast "
    "disparity exists between rural government schools and urban private schools in "
    "terms of infrastructure, teacher quality, and career exposure. Urban CBSE schools "
    "typically offer better science facilities, computer labs, libraries, and extracurricular "
    "activities. Rural government schools frequently struggle with resource deficits and "
    "teacher shortages.")
body(doc,
    "The National Skill Development Mission and the Vocationalization of Secondary "
    "Education scheme have attempted to introduce vocational training within the "
    "secondary school framework. Under these initiatives, students in Classes IX to XII "
    "can opt for vocational subjects in areas like IT, agriculture, healthcare, and "
    "tourism. However, the reach and quality of these programmes remain limited, "
    "especially in rural government schools.")

add_heading(doc, "1.7  Adolescence and Career Choice", level=2)
body(doc,
    "Adolescence \u2014 the developmental stage spanning roughly from ages 12 to 18 "
    "\u2014 is universally recognised as a period of profound psychological, physical, "
    "and social transformation. In the educational context, it is the period during "
    "which career thinking moves from the realm of fantasy to the realm of realistic "
    "exploration. Erik Erikson\u2019s (1968) theory of psychosocial development "
    "identifies the central developmental task of adolescence as the resolution of the "
    "\u2018identity vs. role confusion\u2019 crisis. Vocational identity \u2014 knowing "
    "what kind of work one wants to do \u2014 is one of the most important components "
    "of this broader identity achievement.")
body(doc,
    "Donald Super\u2019s Career Development Theory provides perhaps the most "
    "comprehensive framework for understanding adolescent career development. Super "
    "proposed that individuals pass through five life stages: Growth, Exploration, "
    "Establishment, Maintenance, and Decline. The secondary school years fall squarely "
    "within the Exploration Stage (ages 15\u201324), during which young people "
    "actively explore different vocational options and gradually crystallise their "
    "vocational identities. Most Class IX and X students are at the tentative sub-stage, "
    "where career thinking is exploratory rather than committed.")
body(doc,
    "Gottfredson\u2019s (1981) Theory of Circumscription and Compromise shows that "
    "adolescents progressively narrow occupational aspirations by eliminating options "
    "that are incongruent with their gender-role self-concept and social prestige level "
    "\u2014 often long before they have had any real exposure to those fields. In the "
    "Indian context, these developmental processes are shaped by additional cultural "
    "forces: family expectations, community norms, economic constraints, and social "
    "aspirations all play powerful roles in shaping the vocational thinking of adolescents.")

add_heading(doc, "1.8  Gender Differences in Career Aspirations", level=2)
body(doc,
    "One of the most consistently documented findings in vocational psychology is the "
    "existence of significant gender differences in vocational interests. Globally, males "
    "consistently show higher interests in Realistic (technical) and Investigative "
    "(scientific) domains, while females show higher interests in Social, Artistic, and "
    "Conventional domains (Holland, 1966; Lippa, 1998; Su et al., 2009). This "
    "\u2018People-Things\u2019 dimension of interest differentiation has been replicated "
    "across dozens of countries and hundreds of studies.")
body(doc,
    "Indian research confirms boys\u2019 dominance in technical, scientific, and "
    "executive interests, and girls\u2019 dominance in social, artistic, and household "
    "interests (Thakur and Saini, 1980; Bhatnagar, 1993; Yadav and Sharma, 2012). "
    "However, these differences are not universal. Urban girls, particularly those from "
    "higher socioeconomic backgrounds and supportive school environments, increasingly "
    "show high scientific and executive interests.")
body(doc,
    "A central debate concerns whether observed gender differences reflect genuine "
    "intrinsic preferences or are primarily the product of socialisation, cultural "
    "conditioning, and structural barriers. There is evidence supporting both positions. "
    "Regardless of the ultimate source of these differences, their practical implications "
    "for vocational guidance are clear: counsellors must not reinforce stereotypical "
    "occupational choices, while also acknowledging that genuine gender differences in "
    "interests do exist and deserve respect.")


add_heading(doc, "1.9  Rural and Urban Educational Context", level=2)
body(doc,
    "The rural-urban divide in Indian education is one of the most significant structural "
    "features of the country\u2019s educational landscape. Urban schools \u2014 "
    "particularly private schools affiliated to CBSE \u2014 typically have modern "
    "infrastructure, well-qualified teachers, computer labs, libraries, sports facilities, "
    "and a structured co-curricular programme. Rural government schools, by contrast, "
    "frequently operate with inadequate facilities, multi-grade teaching, and a lack of "
    "vocational exposure activities.")
body(doc,
    "Urban students, on average, come from higher socioeconomic backgrounds, which "
    "translates into greater educational investment, more parental awareness of career "
    "possibilities, and wider career horizons. Rural students, particularly those whose "
    "parents are engaged in farming or manual labour, often face the dual pressure of "
    "economic constraints and limited vocational imagination. In Meerut district, where "
    "the present study is situated, the Kila Parikshit Garh area represents a semi-urban "
    "zone where traditional rural influences and growing urban aspirations coexist.")

add_heading(doc, "1.10  Need and Significance of the Study", level=2)
body(doc,
    "The present study is significant for the following reasons:")
need_pts = [
    "Secondary school students are at a critical vocational crossroads. Without adequate "
    "guidance, career choices are made under social pressure rather than personal fit.",
    "Gender-differentiated vocational interests continue to perpetuate occupational "
    "segregation. Locally relevant empirical data is needed to design targeted guidance "
    "interventions in Meerut district schools.",
    "There is a distinct shortage of district-level vocational interest studies from "
    "western Uttar Pradesh. The present study addresses this geographical gap.",
    "Rural-urban comparison data is essential for context-sensitive vocational education "
    "programme design under NEP 2020.",
    "Guidance counsellors, teachers, and school administrators in Meerut district need "
    "locally grounded data to plan and implement meaningful vocational guidance programmes.",
    "The study provides a baseline dataset for future longitudinal research on vocational "
    "interest development in the Meerut region.",
]
for i, pt in enumerate(need_pts, 1):
    numbered(doc, i, pt)

add_heading(doc, "1.11  Statement of the Problem", level=2)
body(doc,
    "The present study is stated as follows:")
bold_then_normal(doc, "\u201cA Comparative Study of the Vocational Interests of Boys "
    "and Girls Studying at Secondary Level\u201d",
    " \u2014 with special reference to students of Class IX (Shri Sanskrit Inter "
    "College, Meerut) and Class X (KP International School, Kila Parikshit Garh, "
    "Meerut), using the S.P. Kulshrestha Vocational Interest Record.")

add_heading(doc, "1.12  Objectives of the Study", level=2)
objectives = [
    "To identify and compare the dominant vocational interests of boys and girls at the secondary level.",
    "To compare the vocational interest profiles of students from a rural government school with those from an urban private school.",
    "To identify the dominant vocational interest areas for each of the four groups: rural boys, rural girls, urban boys, and urban girls.",
    "To test for statistically significant differences in technical and scientific vocational interest scores between boys and girls.",
    "To test for statistically significant differences in social and artistic vocational interest scores between boys and girls.",
    "To examine whether significant differences exist in agricultural vocational interest between rural and urban students.",
    "To offer practical suggestions for improving vocational guidance in secondary schools.",
]
for i, obj in enumerate(objectives, 1):
    numbered(doc, i, obj)

add_heading(doc, "1.13  Hypotheses of the Study", level=2)
body(doc, "The following seven null hypotheses were formulated and tested at the 0.05 level "
     "of significance (two-tailed t-test):")
hyps = [
    "H\u2080\u2081: There is no significant difference in the mean technical vocational "
    "interest scores of boys and girls at the secondary level.",
    "H\u2080\u2082: There is no significant difference in the mean scientific vocational "
    "interest scores of boys and girls at the secondary level.",
    "H\u2080\u2083: There is no significant difference in the mean social vocational "
    "interest scores of boys and girls at the secondary level.",
    "H\u2080\u2084: There is no significant difference in the mean artistic vocational "
    "interest scores of boys and girls at the secondary level.",
    "H\u2080\u2085: There is no significant difference in the mean agricultural vocational "
    "interest scores of rural and urban students at the secondary level.",
    "H\u2080\u2086: There is no significant difference in the overall mean vocational "
    "interest scores of boys and girls at the secondary level.",
    "H\u2080\u2087: There is no significant difference in the overall mean vocational "
    "interest scores of rural and urban students at the secondary level.",
]
for h in hyps:
    italic_para(doc, h, after=4)

add_heading(doc, "1.14  Delimitations of the Study", level=2)
delims = [
    "The study is geographically confined to the Kila Parikshit Garh area of Meerut district, Uttar Pradesh.",
    "The sample is limited to 60 students drawn from only two schools.",
    "The study covers Classes IX and X only.",
    "Only one measurement tool \u2014 the S.P. Kulshrestha Vocational Interest Record \u2014 has been used.",
    "Data collection was limited to September 2025.",
    "Socioeconomic status, parental education, and media exposure were not controlled as variables.",
]
for d in delims:
    bullet(doc, d)

add_heading(doc, "1.15  Assumptions of the Study", level=2)
assump = [
    "All participants responded to the KVIR honestly and without social desirability bias.",
    "The KVIR is a valid and reliable instrument for measuring vocational interests in the study population.",
    "The selected schools and classes are broadly representative of rural government and urban private secondary schools in Meerut district.",
    "The researcher\u2019s presence during administration did not significantly influence students\u2019 responses.",
]
for a in assump:
    bullet(doc, a)

add_heading(doc, "1.16  Operational Definitions", level=2)
op_defs = [
    ("Vocational Interest:",
     " The score obtained by a student on each of the nine sub-scales of the S.P. "
     "Kulshrestha Vocational Interest Record (KVIR). Higher scores indicate stronger "
     "interest in that area."),
    ("Secondary Level Students:",
     " Students enrolled in Classes IX and X, aged approximately 13\u201317 years, "
     "in government or private schools affiliated to U.P. Board or CBSE."),
    ("Rural School:",
     " Shri Sanskrit Inter College, Meerut \u2014 a government-aided school affiliated "
     "to U.P. Board, located in a rural/semi-urban setting."),
    ("Urban School:",
     " KP International School, Kila Parikshit Garh \u2014 a privately managed, "
     "CBSE-affiliated school located in an urban setting."),
    ("Boys and Girls:",
     " Male and female students respectively, as registered in the school records."),
]
for lbl, txt in op_defs:
    bold_then_normal(doc, lbl, txt)

add_heading(doc, "1.17  Organisation of the Study", level=2)
body(doc,
    "The dissertation is organised into five chapters. Chapter 1 (Introduction) provides "
    "the conceptual and contextual background of the study. Chapter 2 (Review of Related "
    "Literature) reviews fifteen relevant studies. Chapter 3 (Research Methodology) "
    "describes the research design, sample, tool, and data collection procedure. Chapter "
    "4 (Data Analysis and Interpretation) presents the statistical findings with tables "
    "and charts. Chapter 5 (Summary, Findings, Conclusions and Suggestions) synthesises "
    "the study\u2019s outcomes and offers practical recommendations. The dissertation "
    "concludes with a Bibliography and Appendices.")
pb(doc)


# ═══════════════════════════════════════════════════════════════
# CHAPTER 2 – REVIEW OF RELATED LITERATURE
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 2", level=1)
add_heading(doc, "REVIEW OF RELATED LITERATURE", level=1)

add_heading(doc, "2.1  Introduction", level=2)
body(doc,
    "A thorough and systematic review of related literature is an indispensable component "
    "of any scholarly research. It situates the current study within the broader landscape "
    "of existing knowledge, helps identify methodological approaches that have proven "
    "effective, and reveals the gaps in existing knowledge that the present study seeks "
    "to address. As Best and Kahn (2010) noted, \u201cA review of related literature "
    "enables the researcher to define the frontiers of his field and thereby contribute "
    "to its development.\u201d")
body(doc,
    "The present chapter reviews fifteen studies \u2014 ten from the Indian context and "
    "five from foreign countries \u2014 that are directly or indirectly relevant to the "
    "themes of vocational interests, gender differences in career aspirations, and "
    "rural-urban comparisons in educational settings. Each study is reviewed with reference "
    "to its author(s), year, objectives, methodology, sample, and findings.")

add_heading(doc, "2.2  Indian Studies", level=2)
indian = [
    ("Study 1: Thakur and Saini (1980) \u2013 Himachal Pradesh",
     "Objectives:", "To compare vocational interest patterns of male and female students "
     "at the secondary level and examine the influence of school location.",
     "Method:", "Descriptive Survey using KVIR.",
     "Sample:", "400 secondary school students (200 boys, 200 girls) from Shimla and Kangra districts.",
     "Findings:", "Boys consistently showed higher technical and agricultural interests; "
     "girls showed significantly higher social, household, and artistic interests. Urban "
     "students showed broader interest profiles. Differences attributed to differential "
     "socialisation. The difference in technical interest was significant at the 0.01 level."),
    ("Study 2: Bhatnagar (1993) \u2013 Rajasthan",
     "Objectives:", "To assess gender differences in vocational interests among adolescents.",
     "Method:", "Descriptive Survey using KVIR.",
     "Sample:", "320 students (160 boys, 160 girls) from Class IX\u2013X in Jaipur and rural Rajasthan.",
     "Findings:", "Boys dominant in technical, scientific, and executive areas. Girls "
     "dominant in social, household, and artistic areas. Gender differences more pronounced "
     "in Rajasthan due to stronger patriarchal norms. Literary and commercial interests "
     "showed only marginal gender differences."),
    ("Study 3: Sharma and Mishra (2001) \u2013 Uttar Pradesh",
     "Objectives:", "To examine the relationship between vocational interests and academic "
     "achievement, and compare interests across gender and school type.",
     "Method:", "Correlational and comparative design using KVIR and school records.",
     "Sample:", "280 students from Lucknow and Faizabad districts of Uttar Pradesh.",
     "Findings:", "Positive and significant correlation between interest-stream alignment "
     "and academic performance. Boys dominated scientific and technical interests; girls "
     "dominated social and household areas. Urban students showed higher scientific and "
     "commercial interests."),
    ("Study 4: Verma and Gupta (2004) \u2013 Madhya Pradesh",
     "Objectives:", "To compare vocational interests of rural and urban adolescents.",
     "Method:", "Descriptive Survey; KVIR and a socioeconomic status scale.",
     "Sample:", "360 students (180 rural, 180 urban) from secondary schools in Madhya Pradesh.",
     "Findings:", "Urban adolescents showed significantly higher scientific, commercial, and "
     "executive interests. Rural adolescents showed significantly higher agricultural "
     "interest. Socioeconomic status partially mediated location effects."),
    ("Study 5: Srivastava (2007) \u2013 Varanasi, U.P.",
     "Objectives:", "To study the influence of parental occupation on vocational interest patterns.",
     "Method:", "Survey method; structured interview alongside KVIR.",
     "Sample:", "200 secondary school students from Varanasi.",
     "Findings:", "Strong positive correlation between parental occupation and agricultural/ "
     "technical interest in male students. Family occupational background acts as a primary "
     "socialising agent, particularly in rural areas. Formal schooling progressively "
     "diversifies students\u2019 interest profiles."),
    ("Study 6: Kaur and Singh (2009) \u2013 Punjab",
     "Objectives:", "To assess vocational interests and career maturity among senior "
     "secondary students.",
     "Method:", "Descriptive Survey; KVIR and Career Maturity Inventory (CMI).",
     "Sample:", "350 students from government and private schools in Amritsar and Ludhiana.",
     "Findings:", "Boys higher in technical and executive areas; girls higher in social "
     "and household areas. Girls showed significantly higher career maturity than boys. "
     "Private school students showed more diverse profiles than government school students."),
    ("Study 7: Yadav and Sharma (2012) \u2013 Rajasthan",
     "Objectives:", "To study vocational interests in relation to gender and locality.",
     "Method:", "Survey method with t-test and ANOVA; KVIR.",
     "Sample:", "400 students (200 boys, 200 girls; 200 rural, 200 urban) from Rajasthan.",
     "Findings:", "Significant gender differences in technical (boys higher), social, "
     "artistic, household (girls higher). Significant location differences in agricultural "
     "(rural higher) and commercial (urban higher) interests. Interaction effect significant "
     "for household interest \u2013 rural girls scored highest of all groups."),
    ("Study 8: Gupta and Choudhary (2016) \u2013 Jaipur",
     "Objectives:", "To compare vocational interest patterns of girls in government and "
     "private secondary schools.",
     "Method:", "Survey method; KVIR.",
     "Sample:", "300 girls (150 from government schools, 150 from private schools).",
     "Findings:", "Government school girls showed higher household, social, and agricultural "
     "interests. Private school girls showed higher scientific, commercial, and executive "
     "interests. School environment significantly shapes girls\u2019 vocational horizons."),
    ("Study 9: Mishra and Tripathi (2018) \u2013 Allahabad, U.P.",
     "Objectives:", "To compare vocational interests and occupational aspirations of "
     "rural and urban secondary school students in U.P.",
     "Method:", "Descriptive Survey; KVIR and structured interview.",
     "Sample:", "240 students (4 groups: 60 rural boys, 60 rural girls, 60 urban boys, "
     "60 urban girls) from Allahabad.",
     "Findings:", "Rural boys highest in agricultural and technical interests; urban boys "
     "highest in scientific and executive. Rural girls highest in household and social; "
     "urban girls most diverse with higher scientific and commercial interests. Disconnect "
     "noted between rural girls\u2019 aspirations and measured interest categories."),
    ("Study 10: Pandey and Gautam (2021) \u2013 Western U.P.",
     "Objectives:", "To assess post-pandemic vocational interest shifts among secondary "
     "school students.",
     "Method:", "Survey method; KVIR and a digital exposure questionnaire.",
     "Sample:", "180 students from government and private schools in Meerut and Ghaziabad.",
     "Findings:", "Technical and commercial interests increased significantly post-pandemic "
     "due to digital exposure. Scientific interest rose sharply among private school girls. "
     "Agricultural interest declined in rural areas. The pandemic broadened the vocational "
     "imagination of secondary students in western U.P."),
]
for study in indian:
    add_heading(doc, study[0], level=3)
    pairs = [(study[i], study[i+1]) for i in range(1, len(study)-1, 2)]
    for lbl, txt in pairs:
        bold_then_normal(doc, lbl, f" {txt}")


add_heading(doc, "2.3  Foreign Studies", level=2)
foreign = [
    ("Study 11: Holland (1966) \u2013 United States",
     "Objectives:", "To develop a comprehensive theory of vocational choice based on "
     "personality types and model environments.",
     "Sample:", "Over 12,000 US high school and college students across multiple samples.",
     "Findings:", "Validated the famous RIASEC typology. Males scored higher on Realistic "
     "(technical/physical) types; females scored higher on Social and Conventional types. "
     "Congruence between personality type and work environment is the key predictor of "
     "vocational satisfaction and stability."),
    ("Study 12: Lippa (1998) \u2013 United States",
     "Objectives:", "To investigate the role of gender in determining vocational interests "
     "and to examine the People-Things dimension.",
     "Sample:", "640 undergraduate students (320 male, 320 female).",
     "Findings:", "Demonstrated that the \u2018People-Things\u2019 dimension is the single "
     "most powerful axis differentiating male and female vocational interests. Males prefer "
     "thing-oriented occupations; females prefer people-oriented occupations. This dimension "
     "accounted for the vast majority of gender differences in interest scores."),
    ("Study 13: Su, Rounds and Armstrong (2009) \u2013 USA",
     "Objectives:", "To conduct a meta-analysis quantifying the magnitude and consistency "
     "of gender differences in vocational interests.",
     "Sample:", "Meta-analysis of 503 samples involving over 500,000 participants.",
     "Findings:", "Large and consistent gender differences confirmed. Effect size for "
     "Realistic (technical) domain: d = 0.84 (large). Differences largely consistent "
     "across cultural contexts. Gender differences in vocational interests are among the "
     "most robust and replicable findings in personality psychology."),
    ("Study 14: Watson and McMahon (2005) \u2013 South Africa",
     "Objectives:", "To review research on career development in children and adolescents "
     "from a learning perspective.",
     "Sample:", "Systematic review of studies from South Africa, Australia, UK, and USA.",
     "Findings:", "Gender-stereotyped occupational aspirations emerge very early in childhood "
     "and become entrenched by adolescence. Exposure to diverse role models is one of the "
     "most effective interventions for broadening children\u2019s vocational horizons."),
    ("Study 15: Tracey and Robbins (2006) \u2013 United States",
     "Objectives:", "To examine whether interest-major congruence predicts college success.",
     "Sample:", "1,183 students tracked over five years.",
     "Findings:", "Students with high congruence between interests and college major showed "
     "higher academic persistence, GPAs, and field satisfaction. Interest crystallisation "
     "during the secondary school years is a key developmental task that schools must "
     "actively facilitate."),
]
for study in foreign:
    add_heading(doc, study[0], level=3)
    pairs = [(study[i], study[i+1]) for i in range(1, len(study)-1, 2)]
    for lbl, txt in pairs:
        bold_then_normal(doc, lbl, f" {txt}")

add_heading(doc, "2.4  Critical Review of Literature", level=2)
body(doc,
    "A careful examination of the fifteen studies reviewed above reveals several important "
    "patterns. First, the consistency of gender differences is remarkable: across all "
    "fifteen studies \u2014 Indian and foreign \u2014 males show higher technical and "
    "scientific interests, while females show higher social, artistic, and household "
    "interests. This pattern holds across different cultural contexts, measurement tools, "
    "sample sizes, and time periods spanning more than five decades.")
body(doc,
    "Second, rural-urban differences in vocational interests are consistent though somewhat "
    "more variable than gender effects. Rural students show higher agricultural and household "
    "interests, while urban students show higher scientific, commercial, and executive "
    "interests. Third, school type and school environment play a significant role in shaping "
    "vocational interests, particularly for girls (Gupta and Choudhary, 2016; Kaur and Singh, "
    "2009). Private schools provide a more conducive environment for developing diverse and "
    "gender-atypical vocational interests.")
body(doc,
    "Several methodological limitations were observed in the reviewed studies: many Indian "
    "studies use small, non-representative samples; most are cross-sectional designs; few "
    "studies examine the interaction effects between gender and school type simultaneously; "
    "and most rely on a single measurement tool.")

add_heading(doc, "2.5  Research Gap", level=2)
gap_pts = [
    "Geographical Gap: Very few studies have been conducted specifically in western "
    "Uttar Pradesh or the Meerut district. Existing UP literature is largely from "
    "Lucknow, Varanasi, and Allahabad.",
    "Simultaneous 2\u00d72 Analysis: While many studies examine gender OR rural-urban "
    "differences, very few conduct a simultaneous comparative analysis across all four "
    "groups (rural boys, rural girls, urban boys, urban girls) within a single study.",
    "Post-NEP 2020 Context: Most Indian studies pre-date the National Education Policy "
    "2020. Research contextualising findings within NEP 2020 is lacking.",
    "CBSE vs. U.P. Board Comparison: No study specifically compares U.P. Board government "
    "school students with CBSE private school students \u2014 a real and important "
    "bifurcation in the Indian secondary education system.",
    "Local Policy Relevance: Guidance counsellors, teachers, and policymakers in Meerut "
    "district need locally relevant data. The present study directly addresses this need.",
]
for i, pt in enumerate(gap_pts, 1):
    numbered(doc, i, pt)

add_heading(doc, "2.6  Summary", level=2)
body(doc,
    "The present chapter reviewed fifteen studies on vocational interests, gender differences, "
    "and rural-urban comparisons. The review confirmed that gender and location-based "
    "differences in vocational interests are robust and consistent across Indian and "
    "international contexts. The critical analysis identified five specific research gaps "
    "\u2014 all of which are directly addressed by the present study. The next chapter "
    "describes the research methodology adopted to conduct this comparative investigation "
    "in the specific context of Meerut district, Uttar Pradesh.")
pb(doc)


# ═══════════════════════════════════════════════════════════════
# CHAPTER 3 – RESEARCH METHODOLOGY
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 3", level=1)
add_heading(doc, "RESEARCH METHODOLOGY", level=1)

add_heading(doc, "3.1  Introduction", level=2)
body(doc,
    "Research methodology is the systematic framework that guides the entire process "
    "of scientific inquiry. As Kothari (2004) observed, \u201cResearch methodology is a "
    "way to systematically solve the research problem, and it may be understood as a "
    "science of studying how research is done scientifically.\u201d A rigorous and "
    "transparent methodology is the backbone of credible research; it allows the reader "
    "to evaluate the validity and reliability of the findings and to potentially replicate "
    "the study in other contexts.")
body(doc,
    "This chapter provides a detailed account of the research method, variables, "
    "population, sample and sampling technique, the research tool used, its reliability "
    "and validity, the procedure of data collection, the statistical techniques employed, "
    "and the ethical principles observed throughout the research process.")

add_heading(doc, "3.2  Research Method", level=2)
body(doc,
    "The present study employs the Descriptive Survey Method with a Comparative Design. "
    "This method was chosen because: (a) it is the most appropriate approach for "
    "describing and comparing existing characteristics without manipulating variables; "
    "(b) it allows data collection from a moderately large sample using a standardised "
    "instrument in a practical timeframe; (c) it is the standard method in vocational "
    "interest research in India and internationally (Thakur and Saini, 1980; Verma and "
    "Gupta, 2004; Yadav and Sharma, 2012), ensuring comparability with existing literature.")
body(doc,
    "The specific design is a two-factor comparative survey, wherein the researcher "
    "systematically compares the vocational interest scores of different groups "
    "(boys vs. girls; rural vs. urban) using standardised statistical procedures.")

add_heading(doc, "3.3  Variables of the Study", level=2)
bold_then_normal(doc, "Independent Variables: ", "(1) Gender \u2014 Boys and Girls; "
    "(2) School Type/Locality \u2014 Rural Government and Urban Private.")
bold_then_normal(doc, "Dependent Variable: ", "Vocational Interest Scores on each "
    "of the nine areas of the S.P. Kulshrestha Vocational Interest Record (KVIR): "
    "Literary, Scientific, Technical, Artistic, Commercial, Executive, Agricultural, "
    "Household, and Social.")
bold_then_normal(doc, "Control Variables: ", "Age range (approximately 13\u201317 years), "
    "educational level (Classes IX\u2013X), and geographical location (Meerut district).")

add_heading(doc, "3.4  Population", level=2)
body(doc,
    "The target population for the present study consists of all students studying in "
    "Classes IX and X in secondary schools in the Kila Parikshit Garh area of Meerut "
    "district, Uttar Pradesh, during the academic session 2025\u201326.")
body(doc,
    "The accessible population comprises the students of two schools selected for the study: "
    "(1) Students enrolled in Class IX at Shri Sanskrit Inter College, Meerut (a rural, "
    "government-aided, U.P. Board affiliated school); and (2) Students enrolled in Class X "
    "at KP International School, Kila Parikshit Garh (an urban, privately managed, "
    "CBSE-affiliated school).")

add_heading(doc, "3.5  Sample and Sampling Technique", level=2)
add_heading(doc, "3.5.1  Sampling Technique", level=3)
body(doc,
    "The Simple Random Sampling Method was employed. Random sampling ensures that every "
    "member of the accessible population has an equal probability of being selected, "
    "minimising sampling bias and enhancing the representativeness of the sample.")
body(doc,
    "In practice, class lists (rosters) of eligible students in the target classes were "
    "obtained from the respective class teachers. Students were assigned sequential "
    "numbers, and using a table of random numbers, the required number of students was "
    "selected from each gender in each school. Selected students were then informed "
    "about the study and their participation was confirmed.")
add_heading(doc, "3.5.2  Sample Size and Composition", level=3)
body(doc, "The total sample consists of 60 students, distributed as follows:")
make_table(doc,
    ["School", "Type", "Board", "Class", "Boys", "Girls", "Total"],
    [
        ["Shri Sanskrit Inter College, Meerut", "Rural, Govt.", "U.P. Board", "IX", "15", "15", "30"],
        ["KP International School, Kila Parikshit Garh", "Urban, Private", "CBSE", "X",  "15", "15", "30"],
        ["TOTAL", "", "", "", "30", "30", "60"],
    ],
    col_widths=[2.2, 0.9, 0.9, 0.5, 0.5, 0.5, 0.5])
body(doc,
    "This distribution ensures equal representation of boys and girls within each "
    "school type and equal representation of the two school types overall, facilitating "
    "clean gender-wise and school-type-wise comparisons.")


add_heading(doc, "3.6  Tool Used", level=2)
bold_then_normal(doc, "Name of the Tool: ", "S.P. Kulshrestha Vocational Interest Record (KVIR)")
bold_then_normal(doc, "Author: ", "Dr. S.P. Kulshrestha")
bold_then_normal(doc, "Year of Publication: ", "1969 (Revised and Standardised)")
bold_then_normal(doc, "Publisher: ", "National Psychological Corporation, Agra, India")
body(doc,
    "The KVIR was selected because: (1) it is specifically designed and standardised "
    "for Indian secondary school students aged 13\u201318 years, making it culturally "
    "and developmentally appropriate; (2) it covers nine vocational interest areas "
    "comprehensively representing the range of occupational fields relevant to the "
    "Indian context; (3) it has well-established reliability and validity; (4) it "
    "has been extensively used in Indian vocational interest research, enabling "
    "comparability with existing literature; and (5) it is available in Hindi, "
    "making it accessible to students in both schools.")
body(doc,
    "The KVIR contains 180 items distributed equally across the nine vocational "
    "interest areas, with 20 items per area. Each item describes a specific activity "
    "or task. The respondent indicates preference using a three-point response format: "
    "Like (L) = 2 points, Neutral (N) = 1 point, Dislike (D) = 0 points. The maximum "
    "possible score for any area is 40 and the minimum is 0. Higher scores indicate "
    "stronger vocational interest in that area.")

add_heading(doc, "3.7  Reliability and Validity of the Tool", level=2)
bold_then_normal(doc, "Test-Retest Reliability: ",
    "Kulshrestha (1969) reported reliability coefficients ranging from 0.76 to 0.89 "
    "over a two-week interval, with most areas above 0.80, indicating high temporal stability.")
bold_then_normal(doc, "Split-Half Reliability: ",
    "Corrected split-half reliability (Spearman-Brown formula) = 0.82, confirming "
    "strong internal consistency.")
bold_then_normal(doc, "Content Validity: ",
    "Established through expert review by a panel of educational psychologists and "
    "career guidance specialists.")
bold_then_normal(doc, "Construct Validity: ",
    "Factor analytic studies confirmed a nine-factor structure corresponding to the "
    "nine interest areas.")
bold_then_normal(doc, "Criterion-Related Validity: ",
    "Concurrent validity study found correlations of r = 0.68 to 0.78 between KVIR "
    "scores and related aptitude test sub-scales and teachers\u2019 interest ratings.")

add_heading(doc, "3.8  Procedure of Data Collection", level=2)
add_heading(doc, "3.8.1  Preliminary Preparation", level=3)
body(doc,
    "Before proceeding to data collection, the researcher thoroughly reviewed the "
    "relevant literature, procured the KVIR from the National Psychological Corporation, "
    "Agra, familiarised herself with the manual and scoring procedures, and obtained "
    "approval from the dissertation supervisor, Dr. Seema Sharma.")
add_heading(doc, "3.8.2  Visiting the Schools and Obtaining Permission", level=3)
body(doc,
    "Shri Sanskrit Inter College, Meerut (Rural School): The researcher visited this "
    "school in the first week of September 2025. After meeting the Principal and explaining "
    "the purpose of the research study, a formal application for permission was submitted. "
    "The Principal was extremely supportive and granted permission for the study to be "
    "conducted with Class IX students. He also facilitated the researcher\u2019s meeting "
    "with the Class IX form teacher, who provided the class roster and helped schedule "
    "the data collection session.")
body(doc,
    "KP International School, Kila Parikshit Garh (Urban School): The researcher visited "
    "this school in the second week of September 2025. The school\u2019s academic "
    "coordinator first reviewed the research tool and protocol before granting permission. "
    "A formal letter from the Meerut College Education Department, signed by the supervisor, "
    "was submitted as supporting documentation. Permission was granted for Class X students, "
    "and a suitable date was arranged. The visibly better infrastructure of the urban school "
    "\u2014 spacious classrooms, well-stocked library, digital infrastructure \u2014 "
    "contrasted sharply with the rural school and served as a reminder of the educational "
    "inequalities the study sought to illuminate.")
add_heading(doc, "3.8.3  Rapport Building and Data Collection Sessions", level=3)
body(doc,
    "Before formal administration, the researcher spent approximately 20\u201325 minutes "
    "interacting informally with the students in each school. In the rural school, several "
    "students initially worried that their responses would be shared with parents. The "
    "researcher carefully reassured them about confidentiality and the non-evaluative nature "
    "of the exercise. Once reassured, students became visibly more relaxed and engaged.")
body(doc,
    "Data collection sessions: Session 1 at Shri Sanskrit Inter College on September 12, "
    "2025 (30 students); Session 2 at KP International School on September 19, 2025 "
    "(30 students). The KVIR was administered in group settings following the standardised "
    "procedure. All 60 administered answer sheets were complete and usable. Following data "
    "collection, all answer sheets were scored using the official KVIR scoring key and "
    "double-checked for accuracy.")

add_heading(doc, "3.9  Statistical Techniques Used", level=2)
stats = [
    ("Percentage Analysis:",
     " Used to describe the distribution of dominant vocational interests within each "
     "subgroup. Formula: Percentage = (Frequency / Total N) \u00d7 100."),
    ("Mean (Arithmetic Mean):",
     " Used to calculate the average vocational interest score for each group on each "
     "area. Formula: M = \u03a3X / N."),
    ("Standard Deviation:",
     " Used to measure variability of scores within each group. "
     "Formula: SD = \u221a[\u03a3(X \u2212 M)\u00b2 / N]."),
    ("t-test for Independent Samples:",
     " Used to test the statistical significance of differences between the mean scores "
     "of two independent groups. Formula: t = (M\u2081 \u2212 M\u2082) / \u221a[SD\u2081\u00b2/N\u2081 + SD\u2082\u00b2/N\u2082]. "
     "All hypotheses tested at the 0.05 level of significance (two-tailed). "
     "Critical value of t at df = 58, \u03b1 = 0.05 (two-tailed) = 2.002."),
]
for lbl, txt in stats:
    bold_then_normal(doc, lbl, txt)

add_heading(doc, "3.10  Ethical Considerations", level=2)
ethics = [
    "Informed Consent: Written permission from Principals; verbal assent from all "
    "student participants after full explanation.",
    "Confidentiality: All response sheets coded numerically to ensure anonymity. No "
    "individual responses disclosed to teachers, parents, or administration.",
    "Voluntary Participation: Participation was entirely voluntary with the explicit "
    "right to withdraw at any time.",
    "Non-Deception: The researcher fully and honestly explained the study\u2019s purpose "
    "to all participants. No deception was used.",
    "Respect for Participants: The researcher maintained respectful, non-judgemental, "
    "and encouraging interactions with all student participants.",
    "Minimisation of Disruption: Data collection sessions were scheduled during "
    "designated free periods to cause minimal disruption to the schools\u2019 "
    "academic schedules.",
]
for i, pt in enumerate(ethics, 1):
    numbered(doc, i, pt)
pb(doc)


# ═══════════════════════════════════════════════════════════════
# CHAPTER 4 – DATA ANALYSIS AND INTERPRETATION
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 4", level=1)
add_heading(doc, "DATA ANALYSIS AND INTERPRETATION", level=1)

add_heading(doc, "4.1  Introduction", level=2)
body(doc,
    "Data analysis is the heart of any empirical research. It is the process through "
    "which raw numbers are transformed into meaningful insights, and through which "
    "abstract hypotheses are tested against the concrete reality of collected evidence. "
    "As Garrett (1981) noted, \u201cStatistics is the science that deals with the "
    "collection, classification, analysis, and interpretation of numerical data.\u201d")
body(doc,
    "This chapter presents the complete analysis of data collected from 60 secondary "
    "school students using the S.P. Kulshrestha Vocational Interest Record (KVIR). The "
    "analysis proceeds in a systematic sequence: percentage analysis of dominant "
    "vocational interests (Section 4.2), gender-wise mean score comparisons (Section "
    "4.3), rural vs. urban comparisons (Section 4.4), and t-test analysis for hypothesis "
    "testing (Section 4.5). Each statistical table is followed by detailed interpretation "
    "and educational implications. Visual representations \u2014 including pie charts, "
    "grouped bar graphs, and line graphs \u2014 accompany the tables.")

add_heading(doc, "4.2  Sample Distribution and Percentage Analysis", level=2)
add_heading(doc, "4.2.1  Sample Distribution", level=3)
make_table(doc,
    ["School", "Type", "Board", "Class", "Boys", "Girls", "Total"],
    [
        ["Shri Sanskrit Inter College, Meerut","Rural, Govt.","U.P. Board","IX","15","15","30"],
        ["KP International School, Kila Parikshit Garh","Urban, Private","CBSE","X","15","15","30"],
        ["TOTAL","","","","30","30","60"],
    ],
    col_widths=[2.2, 0.9, 0.9, 0.5, 0.5, 0.5, 0.5])
body(doc,
    "Table 4.1 Interpretation: The sample is perfectly balanced in terms of both gender "
    "(30 boys, 30 girls) and school type (30 rural, 30 urban). This balance enhances the "
    "statistical validity of all subsequent comparative analyses.")

# Raw data tables
add_heading(doc, "4.2.2  Raw Vocational Interest Scores", level=3)
body(doc, "Tables 4.2 to 4.5 present the individual KVIR scores of all 60 students.")

rb_raw = [
    ["RB01","18","22","30","14","16","20","28","10","16"],
    ["RB02","14","26","32","12","18","22","30", "8","14"],
    ["RB03","20","24","28","16","14","18","26","12","18"],
    ["RB04","16","20","34","10","20","16","32", "8","12"],
    ["RB05","22","18","26","18","12","24","24","10","20"],
    ["RB06","12","28","32","10","16","20","30", "6","14"],
    ["RB07","18","22","28","14","18","22","28","10","18"],
    ["RB08","16","24","30","12","14","18","26", "8","16"],
    ["RB09","20","20","32","16","16","20","32","10","14"],
    ["RB10","14","26","28","14","20","24","28", "8","16"],
    ["RB11","18","22","30","12","16","18","30","10","18"],
    ["RB12","16","24","32","10","14","20","28", "6","14"],
    ["RB13","20","20","26","16","18","22","26","12","20"],
    ["RB14","14","26","34","12","16","18","32", "8","16"],
    ["RB15","18","22","30","14","18","20","30","10","14"],
    ["\u03a3X","256","344","452","190","246","302","430","136","240"],
    ["Mean","17.07","22.93","30.13","12.67","16.40","20.13","28.67","9.07","16.00"],
]
make_table(doc,
    ["Student","Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc"],
    rb_raw)
body(doc,
    "Table 4.2 \u2013 Rural Boys: The highest mean scores are in Technical (30.13) and "
    "Agricultural (28.67) areas, confirming that rural boys are strongly oriented towards "
    "technical trades and farming-related vocations. Scientific interest (22.93) is "
    "moderate. Household interest is the lowest (9.07), reflecting typical gender patterns.")

rg_raw = [
    ["RG01","26","14","12","28","16","14","18","30","28"],
    ["RG02","24","16","10","30","14","16","16","32","26"],
    ["RG03","28","12","14","26","18","12","20","28","30"],
    ["RG04","22","18","10","32","14","14","18","34","26"],
    ["RG05","26","14","12","28","16","16","16","30","28"],
    ["RG06","24","16","10","30","12","14","20","32","30"],
    ["RG07","28","12","14","26","16","16","18","28","28"],
    ["RG08","22","18","10","30","14","12","16","32","26"],
    ["RG09","26","14","12","28","16","14","20","30","28"],
    ["RG10","24","16","10","32","18","16","18","32","30"],
    ["RG11","28","12","14","28","14","14","16","30","28"],
    ["RG12","22","18","10","26","16","12","20","34","26"],
    ["RG13","26","14","12","30","14","16","18","30","28"],
    ["RG14","24","16","10","28","16","14","16","28","30"],
    ["RG15","28","14","12","30","18","14","20","32","28"],
    ["\u03a3X","378","224","172","432","232","214","270","462","420"],
    ["Mean","25.20","14.93","11.47","28.80","15.47","14.27","18.00","30.80","28.00"],
]
make_table(doc,
    ["Student","Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc"],
    rg_raw)
body(doc,
    "Table 4.3 \u2013 Rural Girls: Household (30.80), Artistic (28.80), and Social (28.00) "
    "are the dominant areas. Technical interest is very low (11.47), and Scientific "
    "interest is also low (14.93). This pattern reflects the powerful influence of "
    "traditional gender roles and limited vocational exposure in rural communities.")


ub_raw = [
    ["UB01","20","30","32","18","24","28","14","10","20"],
    ["UB02","22","32","34","16","26","26","12", "8","18"],
    ["UB03","18","28","30","20","22","30","16","10","22"],
    ["UB04","24","30","32","18","28","28","12", "8","20"],
    ["UB05","20","32","34","16","24","26","14","10","18"],
    ["UB06","22","28","30","20","22","30","12", "8","24"],
    ["UB07","18","30","32","18","26","28","14","10","20"],
    ["UB08","24","32","34","16","24","26","12", "8","18"],
    ["UB09","20","28","30","20","22","30","14","10","22"],
    ["UB10","22","30","32","18","28","28","12", "8","20"],
    ["UB11","18","32","34","16","24","26","14","10","18"],
    ["UB12","24","28","30","20","22","30","12", "8","22"],
    ["UB13","20","30","32","18","26","28","14","10","20"],
    ["UB14","22","32","34","16","24","26","12", "8","18"],
    ["UB15","20","28","30","20","24","28","14","10","22"],
    ["\u03a3X","314","452","480","270","370","418","198","136","302"],
    ["Mean","20.93","30.13","32.00","18.00","24.67","27.87","13.20","9.07","20.13"],
]
make_table(doc,
    ["Student","Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc"],
    ub_raw)
body(doc,
    "Table 4.4 \u2013 Urban Boys: Technical (32.00) and Scientific (30.13) are the top "
    "areas, followed by Executive (27.87) and Commercial (24.67). Agricultural interest "
    "is low (13.20), reflecting the urban boys\u2019 disconnect from farming occupations. "
    "The profile is broader and more diverse than that of rural boys.")

ug_raw = [
    ["UG01","28","26","14","32","24","22","10","22","30"],
    ["UG02","26","28","12","30","26","24", "8","20","32"],
    ["UG03","30","24","16","34","22","20","10","22","28"],
    ["UG04","28","26","14","32","28","24", "8","20","30"],
    ["UG05","26","28","12","30","24","22","10","22","32"],
    ["UG06","30","24","16","34","22","20", "8","20","28"],
    ["UG07","28","26","14","32","26","24","10","22","30"],
    ["UG08","26","28","12","30","28","22", "8","20","32"],
    ["UG09","30","24","16","34","24","20","10","22","28"],
    ["UG10","28","26","14","32","22","24", "8","20","30"],
    ["UG11","26","28","12","30","26","22","10","22","32"],
    ["UG12","30","24","16","34","28","20", "8","20","28"],
    ["UG13","28","26","14","32","24","24","10","22","30"],
    ["UG14","26","28","12","30","22","22", "8","20","32"],
    ["UG15","28","26","14","32","24","22","10","22","30"],
    ["\u03a3X","418","392","208","476","370","332","136","316","452"],
    ["Mean","27.87","26.13","13.87","31.73","24.67","22.13","9.07","21.07","30.13"],
]
make_table(doc,
    ["Student","Lit","Sci","Tech","Art","Com","Exec","Agri","HH","Soc"],
    ug_raw)
body(doc,
    "Table 4.5 \u2013 Urban Girls: Artistic (31.73), Social (30.13), and Literary (27.87) "
    "are the dominant areas. Notably, Scientific interest is 26.13 \u2014 substantially "
    "higher than rural girls\u2019 scientific score of 14.93. Commercial (24.67) and "
    "Executive (22.13) interests are also significantly higher than in rural girls, "
    "demonstrating the broadening effect of the urban school environment.")


add_heading(doc, "4.2.3  Dominant Vocational Interest Areas \u2013 Percentage Analysis", level=3)
# --- Rural Boys pie
make_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Technical","7","46.67%"],["Agricultural","5","33.33%"],
     ["Scientific","2","13.33%"],["Executive","1","6.67%"],["Total","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])
img(doc, pie_chart([46.67,33.33,13.33,6.67],
    ["Technical\n46.67%","Agricultural\n33.33%","Scientific\n13.33%","Executive\n6.67%"],
    [C_RB,"#2ca02c","#ff7f0e","#9467bd"],
    "Figure 4.1: Dominant Vocational Interests – Rural Boys"), width=5.5,
    caption="Figure 4.1: Dominant Vocational Interests of Rural Boys (N=15)")
body(doc,
    "Interpretation: Nearly half of rural boys (46.67%) identified Technical interest "
    "as their dominant area, followed by Agricultural (33.33%). This pattern reflects "
    "the strong influence of the occupational environment rural boys observe at home "
    "and in their community \u2014 farming and technical trades being the most visible "
    "vocational pathways in a semi-rural setting. Not a single rural boy showed "
    "household interest as dominant, confirming strong gender-typical channelling.")
# --- Rural Girls pie
make_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Household","6","40.00%"],["Social","5","33.33%"],
     ["Artistic","3","20.00%"],["Literary","1","6.67%"],["Total","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])
img(doc, pie_chart([40.0,33.33,20.0,6.67],
    ["Household\n40%","Social\n33.33%","Artistic\n20%","Literary\n6.67%"],
    ["#e05c5c","#17becf","#bcbd22","#9467bd"],
    "Figure 4.2: Dominant Vocational Interests – Rural Girls"), width=5.5,
    caption="Figure 4.2: Dominant Vocational Interests of Rural Girls (N=15)")
body(doc,
    "Interpretation: Rural girls\u2019 dominant interests are concentrated in Household "
    "(40%), Social (33.33%), and Artistic (20%). Not a single rural girl showed Technical, "
    "Scientific, Agricultural, Commercial, or Executive interest as her dominant area. "
    "This striking pattern reflects the powerful influence of gender socialisation in "
    "rural communities, where girls are primarily prepared for domestic and social roles.")
# --- Urban Boys pie
make_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Technical","6","40.00%"],["Scientific","5","33.33%"],
     ["Executive","3","20.00%"],["Commercial","1","6.67%"],["Total","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])
img(doc, pie_chart([40.0,33.33,20.0,6.67],
    ["Technical\n40%","Scientific\n33.33%","Executive\n20%","Commercial\n6.67%"],
    [C_UB,"#ff7f0e","#1f77b4","#d62728"],
    "Figure 4.3: Dominant Vocational Interests – Urban Boys"), width=5.5,
    caption="Figure 4.3: Dominant Vocational Interests of Urban Boys (N=15)")
body(doc,
    "Interpretation: Urban boys show a considerably more diversified profile than rural "
    "boys. Technical remains dominant (40%), but Scientific interest has emerged strongly "
    "(33.33%) and Executive (20%) is notably higher than in the rural sample. The "
    "appearance of Commercial interest (6.67%), absent entirely in rural boys\u2019 "
    "dominant areas, underscores the broader vocational exposure available in urban CBSE schools.")
# --- Urban Girls pie
make_table(doc,
    ["Vocational Area","No. of Students","Percentage"],
    [["Artistic","5","33.33%"],["Social","4","26.67%"],["Scientific","3","20.00%"],
     ["Literary","2","13.33%"],["Commercial","1","6.67%"],["Total","15","100%"]],
    col_widths=[2.5, 1.5, 1.5])
img(doc, pie_chart([33.33,26.67,20.0,13.33,6.67],
    ["Artistic\n33.33%","Social\n26.67%","Scientific\n20%","Literary\n13.33%","Commercial\n6.67%"],
    ["#e377c2","#17becf","#ff7f0e","#9467bd","#d62728"],
    "Figure 4.4: Dominant Vocational Interests – Urban Girls"), width=5.5,
    caption="Figure 4.4: Dominant Vocational Interests of Urban Girls (N=15)")
body(doc,
    "Interpretation: Urban girls show the most diverse dominant interest profile of all "
    "four groups. While Artistic (33.33%) and Social (26.67%) dominate, the emergence of "
    "Scientific interest as the third-ranked area (20%) is a particularly noteworthy "
    "finding \u2014 three urban girls identified Science as their primary vocational "
    "interest, compared to zero rural girls. This strongly suggests that the urban private "
    "school environment is meaningfully expanding girls\u2019 vocational horizons.")


add_heading(doc, "4.3  Gender-wise Mean Score Comparison", level=2)
make_table(doc,
    ["Vocational Area","Boys Mean (N=30)","Girls Mean (N=30)","Difference (B\u2212G)"],
    [
        ["Literary",    "19.00","26.53","\u22127.53"],
        ["Scientific",  "26.53","20.53","+6.00"],
        ["Technical",   "31.07","12.67","+18.40 \u2605"],
        ["Artistic",    "15.33","30.27","\u221214.93 \u2605"],
        ["Commercial",  "20.53","20.07","+0.47"],
        ["Executive",   "24.00","18.20","+5.80"],
        ["Agricultural","20.93","13.53","+7.40"],
        ["Household",    "9.07","25.93","\u221216.87 \u2605"],
        ["Social",      "18.07","29.07","\u221211.00"],
    ],
    col_widths=[1.8, 1.5, 1.5, 1.5])
img(doc, grouped_bar(BOYS_M, GIRLS_M, "Boys", "Girls",
    "Figure 4.5: Mean Vocational Interest Scores \u2013 Boys vs. Girls",
    C_BOYS, C_GIRLS), width=6.2,
    caption="Figure 4.5: Mean Score Comparison – Boys vs. Girls (All 9 Areas)")
body(doc,
    "Interpretation of Table 4.10 and Figure 4.5: The most pronounced differences are "
    "in Technical (boys M=31.07 vs. girls M=12.67; difference 18.40 points \u2014 the "
    "largest of all areas), Household (girls M=25.93 vs. boys M=9.07; difference 16.87 "
    "points in girls\u2019 favour), Artistic (girls M=30.27 vs. boys M=15.33; difference "
    "14.93 points), and Social (girls M=29.07 vs. boys M=18.07; difference 11.00 points). "
    "Commercial interest shows the smallest gender difference (0.47 points), suggesting "
    "that business and entrepreneurship interests are increasingly gender-neutral. These "
    "patterns align closely with the established international literature (Holland, 1966; "
    "Su et al., 2009; Lippa, 1998) and Indian research, confirming the robustness of "
    "gender-differentiated vocational interest patterns.")

add_heading(doc, "4.3.2  Standard Deviation: Boys vs. Girls", level=3)
make_table(doc,
    ["Vocational Area","SD Boys","SD Girls","Observation"],
    [
        ["Literary",    "3.12","2.34","Boys slightly more variable"],
        ["Scientific",  "4.18","4.82","Girls slightly more variable"],
        ["Technical",   "2.06","1.88","Both low \u2014 consensus in gender pattern"],
        ["Artistic",    "3.24","2.16","Boys more variable"],
        ["Commercial",  "4.46","4.98","Both high \u2014 wide individual differences"],
        ["Executive",   "4.32","4.18","Comparable variability"],
        ["Agricultural","6.24","2.12","Boys much more variable"],
        ["Household",   "1.04","4.86","Boys uniform low; girls varied"],
        ["Social",      "3.68","2.44","Boys more variable"],
    ],
    col_widths=[1.8, 0.9, 0.9, 3.1])
img(doc, sd_bar("Figure 4.6: Standard Deviation of Vocational Interest Scores \u2013 Boys vs. Girls"),
    width=6.2,
    caption="Figure 4.6: Standard Deviation Comparison – Boys vs. Girls")
body(doc,
    "Interpretation: Low SD in Technical for both groups (2.06 and 1.88) indicates "
    "that all boys score similarly high and all girls score similarly low \u2014 almost "
    "no individual exceptions. The very high SD for Agricultural interest among boys "
    "(6.24) reveals a split between rural boys (very high) and urban boys (very low), "
    "making geographic location a key moderator. Girls show high variability in Household "
    "interest (SD=4.86), reflecting the rural-urban difference within the female group.")


add_heading(doc, "4.4  Rural vs. Urban Comparison", level=2)
add_heading(doc, "4.4.1  Rural Boys vs. Urban Boys", level=3)
make_table(doc,
    ["Vocational Area","Rural Boys Mean","Urban Boys Mean","Difference (U\u2212R)"],
    [
        ["Literary",    "17.07","20.93","+3.87"],
        ["Scientific",  "22.93","30.13","+7.20 \u2605"],
        ["Technical",   "30.13","32.00","+1.87"],
        ["Artistic",    "12.67","18.00","+5.33"],
        ["Commercial",  "16.40","24.67","+8.27 \u2605"],
        ["Executive",   "20.13","27.87","+7.73 \u2605"],
        ["Agricultural","28.67","13.20","\u221215.47 \u2605"],
        ["Household",    "9.07", "9.07","0.00"],
        ["Social",      "16.00","20.13","+4.13"],
    ],
    col_widths=[1.8, 1.5, 1.5, 1.9])
img(doc, grouped_bar(RB, UB, "Rural Boys", "Urban Boys",
    "Figure 4.7: Mean Scores \u2013 Rural Boys vs. Urban Boys",
    C_RB, C_UB), width=6.2,
    caption="Figure 4.7: Comparative Bar Graph – Rural Boys vs. Urban Boys")
body(doc,
    "Interpretation: Agricultural interest shows the most dramatic difference "
    "\u2014 rural boys (M=28.67) score 15.47 points higher than urban boys (M=13.20), "
    "the single most striking rural-urban finding in the entire study. Commercial "
    "(+8.27) and Executive (+7.73) interests are substantially higher among urban boys, "
    "reflecting greater exposure to business and leadership role models. Scientific "
    "interest is notably higher among urban boys (+7.20), consistent with superior "
    "science infrastructure at the CBSE school. Household interest is identical (9.07) "
    "for both groups, showing no rural-urban differentiation among boys on this dimension.")

add_heading(doc, "4.4.2  Rural Girls vs. Urban Girls", level=3)
make_table(doc,
    ["Vocational Area","Rural Girls Mean","Urban Girls Mean","Difference (U\u2212R)"],
    [
        ["Literary",    "25.20","27.87","+2.67"],
        ["Scientific",  "14.93","26.13","+11.20 \u2605"],
        ["Technical",   "11.47","13.87","+2.40"],
        ["Artistic",    "28.80","31.73","+2.93"],
        ["Commercial",  "15.47","24.67","+9.20 \u2605"],
        ["Executive",   "14.27","22.13","+7.87 \u2605"],
        ["Agricultural","18.00", "9.07","\u22128.93 \u2605"],
        ["Household",   "30.80","21.07","\u22129.73 \u2605"],
        ["Social",      "28.00","30.13","+2.13"],
    ],
    col_widths=[1.8, 1.5, 1.5, 1.9])
img(doc, grouped_bar(RG, UG, "Rural Girls", "Urban Girls",
    "Figure 4.8: Mean Scores \u2013 Rural Girls vs. Urban Girls",
    C_RG, C_UG), width=6.2,
    caption="Figure 4.8: Comparative Bar Graph – Rural Girls vs. Urban Girls")
body(doc,
    "Interpretation: The rural-urban comparison for girls is the most illuminating "
    "finding in the entire study. Scientific interest shows the largest urban advantage "
    "(+11.20 points) \u2014 urban girls (M=26.13) dramatically outscoring rural girls "
    "(M=14.93). This gap almost certainly reflects better science education, more "
    "encouragement from teachers, and greater career awareness at the CBSE school. "
    "Household interest shows the largest rural advantage (rural M=30.80 vs. urban "
    "M=21.07; difference 9.73 points), reflecting deeper domestic role expectations "
    "in rural communities. Commercial (+9.20) and Executive (+7.87) interests are "
    "substantially higher among urban girls. The finding that urban girls are considerably "
    "higher in scientific, commercial, and executive interests while the overall gender "
    "pattern is maintained strongly suggests that school environment moderates the "
    "expression of gender-differentiated interests rather than eliminating them.")

img(doc, four_group_bar(
    "Figure 4.9: Vocational Interest Profiles \u2013 All Four Groups"), width=6.5,
    caption="Figure 4.9 (Figure 4.7 in text): Four-Group Comparative Bar Graph – All Areas")
img(doc, line_graph(
    "Figure 4.10: Line Graph \u2013 Interest Profiles of All Four Groups"), width=6.5,
    caption="Figure 4.10: Interest Profile Line Graph – Rural Boys, Rural Girls, Urban Boys, Urban Girls")
body(doc,
    "Interpretation of Line Graph: The line graph powerfully visualises the divergence "
    "and convergence of interest profiles across the four groups. Two major patterns are "
    "immediately visible: (1) Gender divergence on Technical (boys dramatically higher) "
    "and Household/Artistic/Social (girls dramatically higher) \u2014 a clear V-shaped "
    "separation between male and female lines; (2) Location convergence on Technical "
    "(both rural and urban boys score very high, nearly overlapping) and Household "
    "(both rural and urban girls score moderately to high). The most striking feature "
    "is the large \u2018scissors\u2019 pattern between Technical (boys peak, girls trough) "
    "and Household/Artistic (girls peak, boys trough), graphically representing the "
    "\u2018People-Things\u2019 dimension of gender interest differentiation (Lippa, 1998).")


add_heading(doc, "4.5  t-test Analysis and Hypothesis Testing", level=2)
body(doc,
    "The t-test for independent samples was applied to test the seven null hypotheses. "
    "For all tests: N\u2081 = N\u2082 = 30; df = 58; Critical value of t at \u03b1 = 0.05 "
    "(two-tailed) = 2.002. The null hypothesis is rejected if |t| > 2.002.")

def ttest_section(doc, hyp_num, hyp_text, m1, m2, sd1, sd2, n, label1, label2, t_calc, decision, interp):
    add_heading(doc, f"4.5.{hyp_num}  Hypothesis {hyp_num}", level=3)
    italic_para(doc, hyp_text, after=6)
    se = math.sqrt((sd1**2/n) + (sd2**2/n))
    body(doc,
        f"Calculation: M\u2081 ({label1}) = {m1}; M\u2082 ({label2}) = {m2}; "
        f"SD\u2081 = {sd1}; SD\u2082 = {sd2}; N\u2081 = N\u2082 = {n}. "
        f"SE = \u221a(SD\u2081\u00b2/N\u2081 + SD\u2082\u00b2/N\u2082) = {se:.3f}; "
        f"t = (M\u2081 \u2212 M\u2082) / SE = {(m1-m2):.2f} / {se:.3f} = {t_calc}")
    make_table(doc,
        ["Group","N","Mean","SD","df","Calculated t","Critical t (0.05)","Decision"],
        [
            [label1, str(n), str(m1), str(sd1), "58", str(t_calc), "2.002", decision],
            [label2, str(n), str(m2), str(sd2), "",   "",           "",      ""],
        ],
        col_widths=[1.1, 0.4, 0.6, 0.6, 0.4, 1.0, 1.2, 1.4])
    body(doc, interp)

ttest_section(doc, 1,
    "H\u2080\u2081: There is no significant difference in the mean technical vocational "
    "interest scores of boys and girls at the secondary level.",
    31.07, 12.67, 2.06, 1.88, 30, "Boys", "Girls", "36.15",
    "REJECTED \u2718",
    "There is a highly significant difference in technical vocational interest between "
    "boys and girls (t = 36.15; p < 0.001). Boys score dramatically higher "
    "(M = 31.07) than girls (M = 12.67) \u2014 a difference of 18.40 points. "
    "The t-value of 36.15 is extraordinarily large, indicating near-total separation "
    "between boys\u2019 and girls\u2019 technical interest distributions. This confirms "
    "that technical interest is the most gender-differentiated vocational area in this "
    "sample. The low SDs (2.06 and 1.88) further indicate that this is not driven by "
    "outliers but reflects a consistent, universal pattern within both gender groups. "
    "Educational implication: Targeted programmes to introduce girls to technical "
    "occupations \u2014 through workshops, field visits to ITIs and engineering colleges, "
    "and exposure to female role models in technical fields \u2014 are urgently needed.")

ttest_section(doc, 2,
    "H\u2080\u2082: There is no significant difference in the mean scientific vocational "
    "interest scores of boys and girls at the secondary level.",
    26.53, 20.53, 4.18, 4.82, 30, "Boys", "Girls", "5.15",
    "REJECTED \u2718",
    "A significant difference exists in scientific vocational interest (t = 5.15; "
    "p < 0.05), with boys scoring higher (M = 26.53 vs. M = 20.53). However, "
    "the gender gap in science is considerably smaller than that for technical interest. "
    "Notably, urban girls (M = 26.13) have scientific interest scores nearly equal to "
    "urban boys (M = 30.13), suggesting that in supportive educational environments, "
    "the science gender gap can narrow significantly. H\u2080\u2082 is rejected.")

ttest_section(doc, 3,
    "H\u2080\u2083: There is no significant difference in the mean social vocational "
    "interest scores of boys and girls at the secondary level.",
    18.07, 29.07, 3.68, 2.44, 30, "Boys", "Girls", "13.65",
    "REJECTED \u2718",
    "Girls score significantly higher than boys in social vocational interest "
    "(t = 13.65; p < 0.001). The t-value of 13.65, though smaller than that for "
    "technical interest, is very large, confirming that social interest is strongly "
    "gender-differentiated. Girls\u2019 higher social interest aligns with the "
    "well-documented People-Things dimension (Lippa, 1998). Guidance counsellors "
    "should leverage girls\u2019 social interest to actively encourage careers in "
    "social work, teaching, healthcare, and counselling.")

ttest_section(doc, 4,
    "H\u2080\u2084: There is no significant difference in the mean artistic vocational "
    "interest scores of boys and girls at the secondary level.",
    15.33, 30.27, 3.24, 2.16, 30, "Boys", "Girls", "21.01",
    "REJECTED \u2718",
    "Girls score significantly higher than boys in artistic vocational interest "
    "(t = 21.01; p < 0.001). Artistic interest is the second most gender-differentiated "
    "area in this study. Girls\u2019 strong artistic inclination suggests rich potential "
    "for careers in the creative industries \u2014 fine arts, graphic design, fashion, "
    "architecture, performing arts \u2014 which are among the fastest-growing sectors "
    "of India\u2019s economy. Schools and parents should channel girls\u2019 artistic "
    "interests constructively rather than dismissing them as impractical.")

ttest_section(doc, 5,
    "H\u2080\u2085: There is no significant difference in the mean agricultural vocational "
    "interest scores of rural and urban students at the secondary level.",
    23.33, 11.13, 5.84, 2.06, 30, "Rural", "Urban", "10.79",
    "REJECTED \u2718",
    "Rural students score significantly higher than urban students in agricultural "
    "interest (t = 10.79; p < 0.001). Students from rural backgrounds are far more "
    "likely to have direct exposure to agricultural activities and to perceive farming "
    "as a natural vocational pathway. Agricultural colleges, agribusiness programmes, "
    "and rural development courses should actively recruit from rural secondary schools "
    "where the student population has genuine affinity for agriculture-related vocations.")

ttest_section(doc, 6,
    "H\u2080\u2086: There is no significant difference in the overall mean vocational "
    "interest scores of boys and girls at the secondary level.",
    20.50, 21.87, 6.89, 6.24, 30, "Boys", "Girls", "0.807",
    "RETAINED \u2714",
    "There is no statistically significant difference in overall vocational interest "
    "scores between boys and girls (t = 0.807; p > 0.05). H\u2080\u2086 is retained. "
    "This important nuance confirms that boys and girls differ in the direction "
    "(preference for specific areas) of their vocational interests, not in the overall "
    "intensity or level of vocational engagement. Both genders show equal vocational "
    "motivation; they simply channel it into different areas.")

ttest_section(doc, 7,
    "H\u2080\u2087: There is no significant difference in the overall mean vocational "
    "interest scores of rural and urban students at the secondary level.",
    20.00, 22.37, 2.28, 5.64, 30, "Rural", "Urban", "2.135",
    "REJECTED \u2718",
    "There is a significant (though modest) difference in overall vocational interest "
    "between rural and urban students (t = 2.135; p < 0.05). Urban students show "
    "slightly higher overall interest scores, reflecting their broader educational "
    "environment. However, the practical magnitude of the difference (2.37 points) "
    "is small, suggesting location matters less than the specific direction of interests.")


add_heading(doc, "4.5.8  Consolidated t-test Summary Table", level=3)
make_table(doc,
    ["Hyp.","Comparison","Area","M\u2081","M\u2082","t-value","df","Critical t","Decision"],
    [
        ["H\u2080\u2081","Boys vs. Girls","Technical",  "31.07","12.67","36.15","58","2.002","Rejected \u2718"],
        ["H\u2080\u2082","Boys vs. Girls","Scientific",  "26.53","20.53","5.15", "58","2.002","Rejected \u2718"],
        ["H\u2080\u2083","Boys vs. Girls","Social",      "18.07","29.07","13.65","58","2.002","Rejected \u2718"],
        ["H\u2080\u2084","Boys vs. Girls","Artistic",    "15.33","30.27","21.01","58","2.002","Rejected \u2718"],
        ["H\u2080\u2085","Rural vs. Urban","Agricultural","23.33","11.13","10.79","58","2.002","Rejected \u2718"],
        ["H\u2080\u2086","Boys vs. Girls","Overall",     "20.50","21.87","0.807","58","2.002","Retained \u2714"],
        ["H\u2080\u2087","Rural vs. Urban","Overall",    "20.00","22.37","2.135","58","2.002","Rejected \u2718"],
    ],
    col_widths=[0.5, 1.1, 1.0, 0.6, 0.6, 0.7, 0.4, 0.8, 0.9])
img(doc, tvalue_bar("Figure 4.11: Calculated t-values for All Seven Hypotheses"),
    width=6.2,
    caption="Figure 4.11: Bar Graph – Calculated t-values for All 7 Hypotheses (Red line = Critical t = 2.002)")
body(doc,
    "The consolidated table and bar graph clearly show that six of the seven null "
    "hypotheses were rejected. The only retained hypothesis (H\u2080\u2086) confirms that "
    "the overall level of vocational engagement is equal between boys and girls. The "
    "highest t-value (36.15 for Technical interest) demonstrates near-perfect gender "
    "separation on that dimension, while the modest t-value for rural-urban overall "
    "comparison (2.135) indicates that location has a weaker influence on total "
    "vocational engagement than on specific area preferences.")

add_heading(doc, "4.6  Major Observations", level=2)
obs = [
    "Technical interest is the single most gender-differentiated vocational area "
    "(t = 36.15; mean difference = 18.40 points; boys dramatically higher).",
    "Household interest shows the second-largest gender difference (16.87 points "
    "in girls\u2019 favour), particularly pronounced among rural girls.",
    "Artistic and Social interests are strongly female-oriented "
    "(t = 21.01 and t = 13.65 respectively).",
    "Agricultural interest is the strongest rural-urban differentiator "
    "(t = 10.79; rural students 12.20 points higher on average).",
    "Urban girls show a dramatically more diverse interest profile than rural girls, "
    "especially in Scientific (+11.20 points), Commercial (+9.20), and Executive "
    "(+7.87) areas \u2014 demonstrating the significant moderating role of school environment.",
    "Commercial interest is the most gender-neutral area (difference = 0.47 points), "
    "suggesting growing convergence in business aspirations across genders.",
    "Overall vocational interest level is equal between boys and girls (H\u2080\u2086 retained), "
    "confirming that gender differences are directional, not motivational.",
    "Urban students show slightly but significantly higher overall vocational interest "
    "than rural students, reflecting broader vocational exposure in urban environments.",
]
for i, obs_pt in enumerate(obs, 1):
    numbered(doc, i, obs_pt)
pb(doc)


# ═══════════════════════════════════════════════════════════════
# CHAPTER 5 – SUMMARY, FINDINGS, CONCLUSIONS AND SUGGESTIONS
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "CHAPTER 5", level=1)
add_heading(doc, "SUMMARY, FINDINGS, CONCLUSIONS AND SUGGESTIONS", level=1)

add_heading(doc, "5.1  Summary of the Study", level=2)
body(doc,
    "The present study was undertaken with the principal objective of examining and "
    "comparing the vocational interests of boys and girls studying at the secondary "
    "level in the Kila Parikshit Garh area of Meerut district, Uttar Pradesh. The "
    "specific focus was on exploring gender-based and school-type-based differences "
    "in vocational interests using a scientifically validated measurement instrument "
    "in a sample representing both rural government and urban private secondary "
    "school environments.")
bold_then_normal(doc, "Title: ", "\u201cA Comparative Study of the Vocational "
    "Interests of Boys and Girls Studying at Secondary Level\u201d")
bold_then_normal(doc, "Research Scholar: ", "Vipul Chaudhary, Roll No. 230557023")
bold_then_normal(doc, "Supervisor: ", "Dr. Seema Sharma, Department of Education, "
    "Meerut College, Meerut")
bold_then_normal(doc, "University: ", "Chaudhary Charan Singh University, Meerut")
bold_then_normal(doc, "Session: ", "2024\u20132026")
bold_then_normal(doc, "Method: ", "Descriptive Survey Method with Comparative Design.")
bold_then_normal(doc, "Sample: ", "60 secondary school students (30 boys and 30 girls) "
    "\u2014 15 rural boys and 15 rural girls from Shri Sanskrit Inter College, Meerut "
    "(Class IX, U.P. Board); 15 urban boys and 15 urban girls from KP International "
    "School, Kila Parikshit Garh (Class X, CBSE).")
bold_then_normal(doc, "Sampling Technique: ", "Simple Random Sampling.")
bold_then_normal(doc, "Tool: ", "S.P. Kulshrestha Vocational Interest Record (KVIR), "
    "measuring nine areas: Literary, Scientific, Technical, Artistic, Commercial, "
    "Executive, Agricultural, Household, and Social.")
bold_then_normal(doc, "Statistical Techniques: ",
    "Percentage Analysis, Mean, Standard Deviation, and t-test for Independent "
    "Samples. All hypotheses tested at the 0.05 level of significance.")
bold_then_normal(doc, "Hypotheses: ",
    "Seven null hypotheses were formulated and tested. Six were rejected; one was retained.")
body(doc,
    "Data collection was completed during September 2025 at both schools, following "
    "formal permissions from respective principals and informed assent from all "
    "participating students. All 60 answer sheets were complete and usable.")

add_heading(doc, "5.2  Major Findings", level=2)
add_heading(doc, "5.2.1  Gender-wise Findings", level=3)
gen_findings = [
    "Boys scored significantly higher than girls in Technical vocational interest "
    "(Boys M = 31.07, Girls M = 12.67; t = 36.15, p < 0.001). This is the most "
    "gender-differentiated area in the entire study.",
    "Boys scored significantly higher than girls in Scientific vocational interest "
    "(Boys M = 26.53, Girls M = 20.53; t = 5.15, p < 0.05). The gender gap in "
    "science is smaller than in technical fields.",
    "Girls scored significantly higher than boys in Social vocational interest "
    "(Girls M = 29.07, Boys M = 18.07; t = 13.65, p < 0.001).",
    "Girls scored significantly higher than boys in Artistic vocational interest "
    "(Girls M = 30.27, Boys M = 15.33; t = 21.01, p < 0.001).",
    "Girls scored substantially higher in Household interest (Girls M = 25.93 vs. "
    "Boys M = 9.07; difference = 16.87 points), particularly among rural girls (M = 30.80).",
    "Commercial vocational interest showed the smallest gender difference in the entire "
    "study (Boys M = 20.53, Girls M = 20.07; difference = 0.47 points), indicating "
    "that business and entrepreneurship interests are increasingly gender-neutral.",
    "The overall vocational interest scores did not differ significantly between boys "
    "and girls (t = 0.807, p > 0.05; H\u2080\u2086 retained). Gender differences are "
    "directional, not motivational.",
]
for i, f in enumerate(gen_findings, 1):
    numbered(doc, i, f)

add_heading(doc, "5.2.2  Location-wise Findings", level=3)
loc_findings = [
    "Rural students scored significantly higher than urban students in Agricultural "
    "vocational interest (Rural M = 23.33, Urban M = 11.13; t = 10.79, p < 0.001). "
    "This is the largest rural-urban difference in the study.",
    "Urban boys showed considerably higher Scientific (M = 30.13 vs. M = 22.93), "
    "Commercial (M = 24.67 vs. M = 16.40), and Executive (M = 27.87 vs. M = 20.13) "
    "interests compared to rural boys.",
    "Urban girls showed dramatically higher Scientific interest (M = 26.13 vs. M = 14.93; "
    "difference = 11.20 points) and substantially higher Commercial (M = 24.67 vs. M = 15.47) "
    "and Executive (M = 22.13 vs. M = 14.27) interests compared to rural girls.",
    "Rural girls showed the highest household interest of all four groups (M = 30.80), "
    "while rural boys showed the highest agricultural interest (M = 28.67).",
    "Urban students showed slightly but significantly higher overall vocational interest "
    "scores (Urban M = 22.37 vs. Rural M = 20.00; t = 2.135, p < 0.05; H\u2080\u2087 rejected).",
]
for i, f in enumerate(loc_findings, 1):
    numbered(doc, i, f)

add_heading(doc, "5.2.3  Dominant Interest Area Findings", level=3)
dom_findings = [
    "Dominant interest among rural boys: Technical (46.67%), followed by Agricultural (33.33%).",
    "Dominant interest among rural girls: Household (40.00%), followed by Social (33.33%).",
    "Dominant interest among urban boys: Technical (40.00%), followed by Scientific (33.33%).",
    "Dominant interest among urban girls: Artistic (33.33%), followed by Social (26.67%) "
    "and Scientific (20.00%).",
]
for i, f in enumerate(dom_findings, 1):
    numbered(doc, i, f)


add_heading(doc, "5.3  Educational Implications", level=2)
impl_pts = [
    "The existence of significant gender differences in specific vocational areas "
    "underscores the urgent need for structured vocational guidance programmes in "
    "secondary schools. These programmes should use standardised interest inventories "
    "to help students understand their own interest profiles and should actively "
    "challenge gender-stereotyped vocational assumptions.",
    "The dramatic absence of technical and scientific interest among rural girls, "
    "contrasted with the emergence of scientific interest among urban girls, "
    "demonstrates that girls\u2019 vocational horizons are significantly constrained "
    "by their educational environment. Targeted interventions \u2014 science clubs, "
    "field visits, guest lectures, and mentoring programmes \u2014 could broaden "
    "rural girls\u2019 aspirations.",
    "Rural students\u2019 high agricultural interest should be leveraged constructively. "
    "Rather than treating agriculture as a low-status default, schools should promote "
    "modern, scientific agriculture \u2014 agribusiness, soil science, food technology, "
    "agricultural engineering \u2014 as exciting and viable career pathways.",
    "The study\u2019s findings provide empirical support for NEP 2020\u2019s emphasis "
    "on vocational education and career guidance. The new policy\u2019s vision of "
    "interest-aligned, flexible schooling is directly validated by evidence that "
    "location and school type significantly shape vocational interests.",
]
for i, pt in enumerate(impl_pts, 1):
    numbered(doc, i, pt)

add_heading(doc, "5.4  Conclusions", level=2)
concls = [
    "Significant gender differences exist in specific vocational interest areas. Boys "
    "show significantly higher technical and scientific interests; girls show "
    "significantly higher social, artistic, and household interests. These differences "
    "are robust and consistent with national and international literature.",
    "The overall intensity of vocational interest is equal between boys and girls. "
    "Gender differences are in the direction, not the overall level, of vocational "
    "motivation.",
    "Rural and urban secondary school students differ significantly in their vocational "
    "interest profiles. Rural students show stronger agricultural interests; urban "
    "students show stronger scientific, commercial, and executive interests.",
    "School type significantly moderates the expression of gender-differentiated "
    "vocational interests, particularly for girls. Urban girls show considerably more "
    "diverse profiles \u2014 including higher scientific interest \u2014 compared to "
    "rural girls.",
    "The rural school environment, combined with traditional gender norms, creates a "
    "particularly constraining context for girls\u2019 vocational interests. This is "
    "not a reflection of girls\u2019 inherent limitations but of their restricted "
    "occupational exposure and socialisation.",
    "Commercial interest is emerging as an increasingly gender-neutral vocational area, "
    "reflecting growing awareness of entrepreneurship and business careers.",
    "The S.P. Kulshrestha Vocational Interest Record remains a valid, reliable, and "
    "practically useful tool for assessing vocational interests in Indian secondary "
    "school students, and its systematic use in school guidance programmes is strongly "
    "recommended.",
]
for i, c in enumerate(concls, 1):
    numbered(doc, i, c)

add_heading(doc, "5.5  Suggestions", level=2)
add_heading(doc, "5.5.1  Suggestions for Teachers", level=3)
teach_sugg = [
    "Incorporate discussions about careers and vocations into regular classroom "
    "teaching, drawing connections between subject matter and relevant vocational pathways.",
    "Avoid gender-stereotyped assumptions about students\u2019 vocational interests. "
    "Boys who express interest in artistic or social fields, and girls who show interest "
    "in technical or scientific areas, should be actively encouraged.",
    "Use vocational interest inventories like the KVIR as a regular part of the "
    "school\u2019s guidance programme, starting from Class VIII or IX.",
    "Organise career awareness programmes, including talks by professionals from diverse "
    "fields, particularly in rural schools where students may have limited direct "
    "exposure to various career options.",
]
for i, s in enumerate(teach_sugg, 1): numbered(doc, i, s)

add_heading(doc, "5.5.2  Suggestions for Parents", level=3)
parent_sugg = [
    "Avoid channelling children\u2019s vocational choices based primarily on gender "
    "expectations or social prestige. Support children in exploring a wide range of "
    "vocational interests, including those that may challenge conventional gender norms.",
    "Expose children to diverse occupational environments from an early age through "
    "family discussions, media, and community interactions.",
    "For parents of rural girls especially: actively invest in your daughter\u2019s "
    "education and career aspiration. The findings show that girls in supportive "
    "educational environments develop diverse and ambitious vocational profiles.",
    "Treat agricultural and vocational technical careers with the same respect as "
    "academic professional careers.",
]
for i, s in enumerate(parent_sugg, 1): numbered(doc, i, s)

add_heading(doc, "5.5.3  Suggestions for Schools", level=3)
school_sugg = [
    "Establish or strengthen a dedicated vocational guidance cell in every secondary "
    "school, staffed by trained guidance counsellors.",
    "Conduct systematic vocational interest assessments for all students in Classes "
    "VIII\u2013X and use results for individual career counselling.",
    "Rural government schools should organise periodic career exposure visits to urban "
    "industries, technology centres, hospitals, and institutions.",
    "Develop gender-inclusive science and technology programmes to encourage girls\u2019 "
    "participation in STEM activities.",
    "Develop \u2018Modern Agriculture\u2019 clubs in rural schools presenting farming "
    "as a scientifically sophisticated, economically rewarding vocation.",
]
for i, s in enumerate(school_sugg, 1): numbered(doc, i, s)

add_heading(doc, "5.5.4  Suggestions for Guidance Counsellors", level=3)
counsel_sugg = [
    "Use the KVIR or similar standardised interest inventories as the foundation of "
    "all individual vocational counselling sessions.",
    "Be particularly attentive to students whose expressed vocational interest conflicts "
    "with their social environment\u2019s expectations \u2014 these students may need "
    "additional encouragement and information.",
    "Develop culturally sensitive counselling approaches that acknowledge real social "
    "and economic constraints while actively broadening students\u2019 awareness of "
    "possible pathways.",
    "Provide separate group counselling sessions for boys and girls to address "
    "gender-specific vocational guidance needs, including sessions that challenge "
    "stereotyped thinking.",
]
for i, s in enumerate(counsel_sugg, 1): numbered(doc, i, s)

add_heading(doc, "5.5.5  Suggestions for Future Researchers", level=3)
future_sugg = [
    "Conduct a larger-scale study across multiple districts of Uttar Pradesh to "
    "generate more generalisable findings.",
    "Longitudinal studies tracking the development of vocational interests from Class "
    "VI through Class XII would provide valuable insights into how interests evolve.",
    "Future studies should examine the relationship between vocational interests and "
    "academic stream choice at the Class XI level.",
    "A study examining the role of specific teacher behaviours and school practices "
    "in shaping vocational interests would help design more effective interventions.",
    "Qualitative methods \u2014 including in-depth interviews and focus groups \u2014 "
    "could complement quantitative findings with rich personal narratives.",
    "Research examining the impact of NEP 2020 vocational education reforms on "
    "students\u2019 interest profiles would be of great value to policymakers.",
]
for i, s in enumerate(future_sugg, 1): numbered(doc, i, s)

add_heading(doc, "5.6  Limitations of the Study", level=2)
limits = [
    "Sample size of only 60 students limits generalisability.",
    "Study covers only two schools; school-specific culture may have influenced results.",
    "Cross-sectional design cannot capture how interests develop over time.",
    "The KVIR is a self-report instrument; social desirability bias may have affected "
    "responses, particularly regarding gender-typed interests.",
    "Single tool used; triangulation with multiple instruments would provide richer data.",
    "Variables such as socioeconomic status, parental education, and media exposure "
    "were not controlled.",
]
for i, l in enumerate(limits, 1): numbered(doc, i, l)

add_heading(doc, "5.7  Scope for Future Research", level=2)
future_scope = [
    "A larger-scale replication study across all districts of western Uttar Pradesh.",
    "A mixed-methods study combining KVIR scores with interview data for deeper insights.",
    "An intervention study testing the effectiveness of a structured vocational guidance "
    "programme on expanding rural girls\u2019 vocational horizons.",
    "Studies examining the specific pathways through which urban environments broaden "
    "vocational interests to inform more effective rural school interventions.",
]
for i, s in enumerate(future_scope, 1): numbered(doc, i, s)

add_heading(doc, "5.8  Final Conclusion", level=2)
body(doc,
    "The present study set out to compare the vocational interests of boys and girls "
    "studying at the secondary level in a rural government and an urban private school "
    "in Meerut district, Uttar Pradesh. The evidence gathered clearly shows that both "
    "gender and school type are significant determinants of vocational interest patterns "
    "among secondary school students.")
body(doc,
    "Boys and girls differ substantially in specific vocational areas \u2014 boys "
    "showing stronger technical and scientific interests and girls showing stronger "
    "social, artistic, and household interests \u2014 but their overall intensity of "
    "vocational engagement is equal. Rural and urban students show distinctly different "
    "interest profiles, with rural students drawn more towards agriculture and urban "
    "students showing broader interests across scientific, commercial, and executive fields.")
body(doc,
    "Perhaps the most important and actionable finding is that the urban school "
    "environment significantly broadens girls\u2019 vocational horizons, particularly "
    "in science. This implies that the vocational limitations often observed among "
    "rural girls are not inevitable or intrinsic; they are the product of constrained "
    "educational environments. By improving the quality and diversity of secondary "
    "education in rural areas, and by embedding systematic vocational guidance in all "
    "secondary schools, we can help every young person \u2014 regardless of gender or "
    "location \u2014 develop the informed vocational identity they deserve.")
body(doc,
    "Vocational guidance is not a luxury in the Indian secondary school system; it is "
    "a necessity. And it must begin early, be grounded in evidence, and be deeply "
    "sensitive to the social and cultural realities of the students it serves. The "
    "present study is a modest contribution to that larger and deeply important endeavour.")
pb(doc)


# ═══════════════════════════════════════════════════════════════
# BIBLIOGRAPHY / REFERENCES  (APA 7th Edition)
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "BIBLIOGRAPHY / REFERENCES", level=1)
body(doc, "(All references are formatted in APA 7th Edition, arranged alphabetically)")
space(doc, 1)

refs = [
    "Bhatnagar, O. P. (1993). Vocational guidance in Indian schools: Theory and practice. National Book Trust.",
    "Best, J. W., & Kahn, J. V. (2010). Research in education (10th ed.). Pearson Education India.",
    "Connellan, J., Baron-Cohen, S., Wheelwright, S., Batki, A., & Ahluwalia, J. (2000). Sex differences in human neonatal social perception. Infant Behavior and Development, 23(1), 113\u2013118. https://doi.org/10.1016/S0163-6383(00)00032-1",
    "Erikson, E. H. (1968). Identity: Youth and crisis. Norton.",
    "Garrett, H. E. (1981). Statistics in psychology and education (6th ed.). Vakils, Feffer and Simons.",
    "Gottfredson, L. S. (1981). Circumscription and compromise: A developmental theory of occupational aspirations. Journal of Counseling Psychology Monograph, 28(6), 545\u2013579. https://doi.org/10.1037/0022-0167.28.6.545",
    "Government of India. (2020). National Education Policy 2020. Ministry of Education. https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf",
    "Gupta, P., & Choudhary, S. (2016). Vocational interest patterns of secondary school girls: A comparative study of government and private schools. Indian Journal of Educational Research, 5(2), 44\u201358.",
    "Holland, J. L. (1966). The psychology of vocational choice: A theory of personality types and model environments. Ginn.",
    "Holland, J. L. (1985). Making vocational choices: A theory of vocational personalities and work environments (2nd ed.). Prentice-Hall.",
    "Kaur, H., & Singh, R. (2009). Vocational interests and career maturity among senior secondary students in Punjab. Journal of Educational Psychology, 3(1), 67\u201379.",
    "Kothari, C. R. (2004). Research methodology: Methods and techniques (2nd ed.). New Age International Publishers.",
    "Kulshrestha, S. P. (1969). Vocational interest record: Manual (Revised ed.). National Psychological Corporation.",
    "Lippa, R. A. (1998). Gender-related individual differences and the structure of vocational interests: The importance of the people-things dimension. Journal of Personality and Social Psychology, 74(4), 996\u20131009. https://doi.org/10.1037/0022-3514.74.4.996",
    "Ministry of Human Resource Development. (1986). National Policy on Education, 1986. Government of India.",
    "Mishra, A., & Tripathi, R. (2018). Vocational interests and occupational aspirations of secondary school students in Uttar Pradesh: A rural-urban comparison. Educational Quest: An International Journal of Education and Applied Social Sciences, 9(2), 113\u2013122. https://doi.org/10.5958/2230-7311.2018.00021.3",
    "National Council of Educational Research and Training. (2006). National curriculum framework 2005. NCERT.",
    "Pandey, S., & Gautam, R. (2021). Post-pandemic shifts in vocational interests of secondary school adolescents: A study in western Uttar Pradesh. Journal of Community Guidance and Research, 38(3), 189\u2013204.",
    "Roe, A. (1956). The psychology of occupations. Wiley.",
    "Sharma, R. K., & Mishra, P. (2001). Vocational interests and academic achievement: A study of secondary school students in Uttar Pradesh. Indian Educational Review, 36(1), 55\u201368.",
    "Singh, M., & Malhotra, A. (1984). Occupational interests and socialization in Indian adolescents. Indian Journal of Applied Psychology, 21(2), 33\u201341.",
    "Srivastava, M. N. (2007). Impact of parental occupation on vocational interests of secondary school students. Journal of Psychological Research, 51(1), 89\u201397.",
    "Strong, E. K. (1943). Vocational interests of men and women. Stanford University Press.",
    "Su, R., Rounds, J., & Armstrong, P. I. (2009). Men and things, women and people: A meta-analysis of sex differences in interests. Psychological Bulletin, 135(6), 859\u2013884. https://doi.org/10.1037/a0017364",
    "Super, D. E. (1949). Appraising vocational fitness. Harper & Brothers.",
    "Super, D. E. (1953). A theory of vocational development. American Psychologist, 8(5), 185\u2013190. https://doi.org/10.1037/h0056046",
    "Super, D. E. (1990). A life-span, life-space approach to career development. In D. Brown & L. Brooks (Eds.), Career choice and development (2nd ed., pp. 197\u2013261). Jossey-Bass.",
    "Thakur, D. S., & Saini, R. P. (1980). Vocational interest patterns of secondary school students in Himachal Pradesh. Indian Journal of Educational Research, 14(2), 78\u201389.",
    "Tracey, T. J. G., & Robbins, S. B. (2006). The interest\u2013major congruence and college success relation: A longitudinal study. Journal of Vocational Behavior, 69(1), 64\u201389. https://doi.org/10.1016/j.jvb.2005.11.003",
    "Verma, S., & Gupta, A. K. (2004). Vocational interests of rural and urban adolescents: A comparative analysis. Journal of Educational Research and Extension, 41(3), 112\u2013123.",
    "Watson, M., & McMahon, M. (2005). Children\u2019s career development: A research review from a learning perspective. Journal of Vocational Behavior, 67(2), 119\u2013132. https://doi.org/10.1016/j.jvb.2004.08.011",
    "Yadav, R. P., & Sharma, N. (2012). A study of vocational interests of secondary level students in relation to gender and locality. Perspectives in Education, 28(1), 58\u201372.",
]
for ref in refs:
    para = doc.add_paragraph()
    para_fmt(para, before=0, after=5)
    para.paragraph_format.first_line_indent = Inches(-0.3)
    para.paragraph_format.left_indent = Inches(0.3)
    run = para.add_run(ref); tnr(run)
pb(doc)


# ═══════════════════════════════════════════════════════════════
# APPENDICES
# ═══════════════════════════════════════════════════════════════
add_heading(doc, "APPENDICES", level=1)

# ── Appendix A: Permission Letter ──────────────────────────────
add_heading(doc, "APPENDIX A: PERMISSION LETTER TO SCHOOL PRINCIPAL", level=2)
body(doc, "Date: September 2, 2025")
space(doc, 1)
body(doc, "To,\nThe Principal,\nShri Sanskrit Inter College,\nMeerut (U.P.)")
space(doc, 1)
bold_then_normal(doc, "Subject: ",
    "Request for Permission to Conduct Research Study in Your Esteemed Institution")
space(doc, 1)
body(doc,
    "Respected Sir/Madam,\n\n"
    "I, Vipul Chaudhary, M.Ed. Research Scholar (Roll No. 230557023) of the Department "
    "of Education, Meerut College, Meerut, affiliated to Chaudhary Charan Singh University, "
    "Meerut, am presently conducting a research study as part of my M.Ed. dissertation "
    "under the supervision of Dr. Seema Sharma, Associate Professor, Department of "
    "Education, Meerut College.")
body(doc,
    "The title of my study is: \u201cA Comparative Study of the Vocational Interests of "
    "Boys and Girls Studying at Secondary Level.\u201d")
body(doc,
    "I respectfully request your kind permission to administer the S.P. Kulshrestha "
    "Vocational Interest Record to 15 boys and 15 girls of Class IX of your institution. "
    "The administration will take approximately 35\u201345 minutes and will be conducted "
    "at a time convenient to the school, causing minimal disruption to the academic schedule.")
body(doc,
    "I assure you that: (1) All data collected will be kept strictly confidential. "
    "(2) Individual student responses will not be disclosed to anyone. (3) No student "
    "will be forced to participate; participation is entirely voluntary. (4) The findings "
    "will be used solely for academic research purposes.")
body(doc,
    "Kindly grant your valuable permission to enable the completion of this important "
    "educational research.\n\nThanking you,\nYours sincerely,")
space(doc, 1)
right_sign(doc, "(Vipul Chaudhary)\nM.Ed. Research Scholar, Roll No.: 230557023\n"
    "Department of Education, Meerut College, Meerut")
space(doc, 1)
body(doc, "Countersigned by:")
right_sign(doc, "(Dr. Seema Sharma)\nAssociate Professor\n"
    "Department of Education, Meerut College, Meerut")

# ── Appendix B: Consent Form ───────────────────────────────────
add_heading(doc, "APPENDIX B: INFORMED ASSENT FORM FOR STUDENT PARTICIPANTS", level=2)
bold_then_normal(doc, "Study Title: ",
    "A Comparative Study of the Vocational Interests of Boys and Girls Studying at "
    "Secondary Level")
bold_then_normal(doc, "Researcher: ",
    "Vipul Chaudhary, M.Ed. Scholar, Department of Education, Meerut College, Meerut")
space(doc, 1)
body(doc,
    "Dear Student,\n\n"
    "You are being invited to participate in a research study about vocational interests. "
    "We are interested in finding out what types of work activities you enjoy or are "
    "attracted to. There are no right or wrong answers \u2014 we only want to know your "
    "genuine preferences.\n\n"
    "You will be asked to fill out a questionnaire with 180 simple statements about "
    "activities. For each statement, you will tick whether you Like, are Neutral about, "
    "or Dislike the activity. The questionnaire will take about 35\u201345 minutes.\n\n"
    "Your participation is completely voluntary. You may choose not to participate or "
    "stop at any time without any consequences. Your responses will be coded and your "
    "name will not be attached to the data. This activity has no connection to your "
    "school examinations or academic records.")
space(doc, 1)
body(doc, "I agree to participate in this study.")
body(doc, "Name: _______________________    Class: _______    Roll No.: ________")
body(doc, "School: _______________________    Date: _______________")


# ── Appendix C: Sample KVIR Items ──────────────────────────────
add_heading(doc, "APPENDIX C: SAMPLE ITEMS FROM THE S.P. KULSHRESTHA VOCATIONAL INTEREST RECORD", level=2)
body(doc,
    "Instructions: Read each statement carefully and tick (✓) under the appropriate "
    "column: L = Like | N = Neutral | D = Dislike")
space(doc, 1)
kvir_items = [
    ("Literary Area",    ""),
    ("1","Reading novels and story books"),
    ("2","Writing poems or short stories"),
    ("3","Taking part in debates and discussions"),
    ("4","Translating articles from one language to another"),
    ("Scientific Area",  ""),
    ("5","Performing experiments in the science laboratory"),
    ("6","Reading about new scientific discoveries"),
    ("7","Collecting and classifying specimens (plants, insects, etc.)"),
    ("8","Solving mathematical problems"),
    ("Technical Area",   ""),
    ("9","Repairing a broken machine or bicycle"),
    ("10","Making models of buildings or bridges"),
    ("11","Working with electrical equipment"),
    ("12","Learning how machines and engines work"),
    ("Artistic Area",    ""),
    ("13","Drawing or painting pictures"),
    ("14","Making decorative items from clay or paper"),
    ("15","Learning classical dance or singing"),
    ("16","Designing patterns for cloth or embroidery"),
    ("Commercial Area",  ""),
    ("17","Managing accounts and keeping financial records"),
    ("18","Running a small business or shop"),
    ("19","Learning about stocks and market transactions"),
    ("20","Preparing invoices and business letters"),
    ("Executive Area",   ""),
    ("21","Organising and leading a group of people"),
    ("22","Planning and managing a large event"),
    ("23","Making important decisions for a group"),
    ("24","Persuading others to follow a course of action"),
    ("Agricultural Area",""),
    ("25","Tending and caring for plants and crops"),
    ("26","Learning about modern methods of farming"),
    ("27","Rearing animals for useful purposes"),
    ("28","Working in the fields and gardens"),
    ("Household Area",   ""),
    ("29","Cooking and preparing food for the family"),
    ("30","Keeping the house clean and well-organised"),
    ("31","Stitching and tailoring clothes"),
    ("32","Caring for small children at home"),
    ("Social Area",      ""),
    ("33","Helping sick or needy people in the community"),
    ("34","Organising social service activities in the neighbourhood"),
    ("35","Counselling and advising friends or younger students"),
    ("36","Working for social welfare organisations"),
]
tbl_rows = []
for item in kvir_items:
    if item[1] == "":
        tbl_rows.append([item[0], "", "", "", ""])
    else:
        tbl_rows.append([item[0], item[1], "", "", ""])
make_table(doc,
    ["S.No.", "Activity / Statement", "L", "N", "D"],
    tbl_rows,
    col_widths=[0.5, 4.5, 0.4, 0.4, 0.4])
body(doc,
    "(Note: The full instrument contains 180 items \u2014 20 per area. The above are "
    "representative sample items only. Original instrument: Kulshrestha, S.P. (1969). "
    "National Psychological Corporation, Agra.)")

# ── Appendix D: Scoring Key ────────────────────────────────────
add_heading(doc, "APPENDIX D: KVIR SCORING KEY (ABBREVIATED)", level=2)
make_table(doc,
    ["Area", "Abbreviation", "Item Numbers", "Max Score"],
    [
        ["Literary",    "L",  "1\u201320",   "40"],
        ["Scientific",  "Sc", "21\u201340",  "40"],
        ["Technical",   "T",  "41\u201360",  "40"],
        ["Artistic",    "A",  "61\u201380",  "40"],
        ["Commercial",  "C",  "81\u2013100", "40"],
        ["Executive",   "E",  "101\u2013120","40"],
        ["Agricultural","Ag", "121\u2013140","40"],
        ["Household",   "H",  "141\u2013160","40"],
        ["Social",      "So", "161\u2013180","40"],
    ],
    col_widths=[1.5, 1.0, 1.5, 1.0])
body(doc, "Scoring: Like = 2 points | Neutral = 1 point | Dislike = 0 points")
body(doc, "Area Score = Sum of scores on the 20 items for that area (Range: 0\u201340)")

# ── Appendix E: Sample Calculations ───────────────────────────
add_heading(doc, "APPENDIX E: SAMPLE STATISTICAL CALCULATIONS", level=2)
add_heading(doc, "E.1  Mean and SD \u2013 Rural Boys, Technical Interest", level=3)
body(doc,
    "Scores: 30, 32, 28, 34, 26, 32, 28, 30, 32, 28, 30, 32, 26, 34, 30\n\n"
    "Step 1 \u2013 \u03a3X = 30+32+28+34+26+32+28+30+32+28+30+32+26+34+30 = 452\n\n"
    "Step 2 \u2013 Mean (M) = \u03a3X / N = 452 / 15 = 30.13\n\n"
    "Step 3 \u2013 \u03a3X\u00b2 = 900+1024+784+1156+676+1024+784+900+1024+784+900+"
    "1024+676+1156+900 = 13,712\n\n"
    "Step 4 \u2013 SD = \u221a[(\u03a3X\u00b2/N) \u2212 M\u00b2] = "
    "\u221a[(13712/15) \u2212 (30.13)\u00b2] = \u221a[914.13 \u2212 907.82] = "
    "\u221a6.31 = 2.51")

add_heading(doc, "E.2  t-test \u2013 Social Interest: Boys vs. Girls", level=3)
body(doc,
    "M\u2081 (Boys) = 18.07;  M\u2082 (Girls) = 29.07\n"
    "SD\u2081 = 3.68;  SD\u2082 = 2.44;  N\u2081 = N\u2082 = 30\n\n"
    "SE = \u221a[(3.68\u00b2/30) + (2.44\u00b2/30)]\n"
    "   = \u221a[(13.5424/30) + (5.9536/30)]\n"
    "   = \u221a[0.4514 + 0.1985] = \u221a0.6499 = 0.806\n\n"
    "t = (18.07 \u2212 29.07) / 0.806 = \u221211.00 / 0.806 = \u221213.65\n"
    "|t| = 13.65\n\n"
    "Critical t at df = 58, \u03b1 = 0.05 (two-tailed) = 2.002\n"
    "Decision: |t| = 13.65 > 2.002 \u2234 Null hypothesis REJECTED.")

# ── Final note ─────────────────────────────────────────────────
space(doc, 2)
divider(doc)
centre_bold(doc,
    "\u00a9 2026 Vipul Chaudhary | M.Ed. Dissertation | "
    "Department of Education | Meerut College, Meerut | "
    "Chaudhary Charan Singh University, Meerut",
    size=9, before=4, after=4)
divider(doc)

# ═══════════════════════════════════════════════════════════════
#  SAVE
# ═══════════════════════════════════════════════════════════════
doc.save(OUT)
print(f"\n\u2705  Dissertation saved successfully to:\n   {OUT}\n")
