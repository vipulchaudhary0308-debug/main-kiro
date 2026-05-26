#!/usr/bin/env python3
"""
Build the complete M.Ed. Dissertation DOCX for Vipul Chaudhary.
Chaudhary Charan Singh University — CCSU Pattern.

Produces: Dissertation_Final.docx
Steps:
  1. Concatenate all markdown chapters
  2. Convert via pypandoc → raw .docx
  3. Post-process with python-docx:
       • Times New Roman throughout
       • Headings bold (H1=16pt, H2=14pt, H3=13pt, body=12pt)
       • 1.5 line spacing body, 1.15 for tables
       • Justified body text
       • 1.5" left / 1" other margins
       • Centered page numbers in footer
  4. Inject real matplotlib charts as embedded images
     (Gender Bar, Rural-Urban Bar, Boys Pie, Girls Pie,
      Comparative Bar, 3D-style grouped bar, Line chart)
"""

import os, io, math, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── paths ─────────────────────────────────────────────────────────────────────
BASE    = os.path.dirname(os.path.abspath(__file__))
DISS    = os.path.join(BASE, "dissertation")
CHARTS  = os.path.join(DISS, "_charts")
COMBINED= os.path.join(DISS, "_combined.md")
OUT     = os.path.join(BASE, "Dissertation_Final.docx")
os.makedirs(CHARTS, exist_ok=True)

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

# ── DATA ──────────────────────────────────────────────────────────────────────
AREAS = ["Literary","Scientific","Technical","Artistic",
         "Commercial","Executive","Agricultural","Household","Social"]
SHORT = ["LIT","SCI","TEC","ART","COM","EXE","AGR","HOU","SOC"]

boys_mean  = [12.17, 15.13, 16.47, 10.27, 12.20, 12.87, 13.67,  5.57, 12.87]
girls_mean = [15.10, 11.67,  8.60, 15.80, 11.60, 12.60, 11.10, 14.40, 16.20]
rural_mean = [13.17, 12.70, 11.77, 11.77, 10.20, 10.87, 15.17, 10.77, 13.77]
urban_mean = [14.10, 14.10, 13.30, 14.30, 13.60, 14.60,  9.60,  9.20, 15.30]

rb_mean    = [11.73, 14.67, 15.93,  8.93, 10.80, 11.13, 16.73,  5.33, 12.13]
rg_mean    = [14.60, 10.73,  7.60, 14.60,  9.60, 10.60, 13.60, 16.20, 15.40]
ub_mean    = [12.60, 15.60, 17.00, 11.60, 13.60, 14.60, 10.60,  5.80, 13.60]
ug_mean    = [15.60, 12.60,  9.60, 17.00, 13.60, 14.60,  8.60, 12.60, 17.00]

boys_hi_pct  = [13.3, 73.3, 93.3, 10.0, 16.7, 23.3, 80.0,  0.0, 20.0]
girls_hi_pct = [80.0, 10.0,  0.0, 90.0, 13.3, 20.0, 26.7, 86.7, 96.7]

# ── CHART HELPERS ─────────────────────────────────────────────────────────────
def save(fig, name):
    p = os.path.join(CHARTS, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p

def bar_chart_gender():
    x = np.arange(len(SHORT)); w = 0.35
    fig, ax = plt.subplots(figsize=(13, 5.5))
    b1 = ax.bar(x - w/2, boys_mean,  w, label="Boys",  color="#4472C4", edgecolor="white", linewidth=0.5)
    b2 = ax.bar(x + w/2, girls_mean, w, label="Girls", color="#FF6B6B", edgecolor="white", linewidth=0.5)
    ax.set_xticks(x); ax.set_xticklabels(SHORT, fontsize=10, fontweight="bold")
    ax.set_ylabel("Mean Score (Max = 20)", fontsize=11)
    ax.set_ylim(0, 22)
    ax.set_title("Figure 4.1 — Mean Vocational Interest Scores: Boys vs. Girls\n(S.P. Kulshrestha VIR, N=60)",
                 fontsize=12, fontweight="bold", pad=10)
    ax.legend(fontsize=11, framealpha=0.9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    for bar in list(b1) + list(b2):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    fig.tight_layout()
    return save(fig, "fig4_1_gender_bar.png")

def bar_chart_rural_urban():
    x = np.arange(len(SHORT)); w = 0.35
    fig, ax = plt.subplots(figsize=(13, 5.5))
    b1 = ax.bar(x - w/2, rural_mean, w, label="Rural Govt. School",  color="#70AD47", edgecolor="white")
    b2 = ax.bar(x + w/2, urban_mean, w, label="Urban Private School", color="#ED7D31", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(SHORT, fontsize=10, fontweight="bold")
    ax.set_ylabel("Mean Score (Max = 20)", fontsize=11)
    ax.set_ylim(0, 22)
    ax.set_title("Figure 4.2 — Mean Vocational Interest Scores: Rural vs. Urban\n(S.P. Kulshrestha VIR, N=60)",
                 fontsize=12, fontweight="bold", pad=10)
    ax.legend(fontsize=11, framealpha=0.9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5); ax.set_axisbelow(True)
    for bar in list(b1)+list(b2):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    fig.tight_layout()
    return save(fig, "fig4_2_rural_urban_bar.png")

def pie_chart_boys():
    # Only areas with >0 high interest
    labels = [a for a, p in zip(AREAS, boys_hi_pct) if p > 0]
    sizes  = [p for p in boys_hi_pct if p > 0]
    colors = ["#4472C4","#5B9BD5","#70AD47","#ED7D31","#FFC000",
              "#FF0000","#7030A0","#00B0F0","#92D050"][:len(labels)]
    explode = [0.04]*len(labels)
    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=140,
        colors=colors, explode=explode,
        textprops={"fontsize": 9}, pctdistance=0.78)
    for at in autotexts: at.set_fontweight("bold"); at.set_fontsize(8)
    ax.set_title("Figure 4.3 — Boys: Percentage with High Interest (Score ≥ 15)\nby Vocational Area",
                 fontsize=11, fontweight="bold", pad=12)
    fig.tight_layout()
    return save(fig, "fig4_3_boys_pie.png")

def pie_chart_girls():
    labels = [a for a, p in zip(AREAS, girls_hi_pct) if p > 0]
    sizes  = [p for p in girls_hi_pct if p > 0]
    colors = ["#FF6B6B","#C55A11","#FF0000","#7030A0","#FFC000",
              "#92D050","#00B050","#FF7C80","#F4B942"][:len(labels)]
    explode = [0.04]*len(labels)
    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=140,
        colors=colors, explode=explode,
        textprops={"fontsize": 9}, pctdistance=0.78)
    for at in autotexts: at.set_fontweight("bold"); at.set_fontsize(8)
    ax.set_title("Figure 4.4 — Girls: Percentage with High Interest (Score ≥ 15)\nby Vocational Area",
                 fontsize=11, fontweight="bold", pad=12)
    fig.tight_layout()
    return save(fig, "fig4_4_girls_pie.png")

def comparative_bar_pct():
    rural_pct = [46.7, 33.3, 46.7, 36.7,  6.7, 10.0, 80.0, 46.7, 56.7]
    urban_pct = [60.0, 56.7, 53.3, 70.0, 56.7, 66.7, 26.7, 36.7, 73.3]
    x = np.arange(len(SHORT)); w = 0.35
    fig, ax = plt.subplots(figsize=(13, 5.5))
    b1 = ax.bar(x-w/2, rural_pct, w, label="Rural Govt.",   color="#548235", edgecolor="white")
    b2 = ax.bar(x+w/2, urban_pct, w, label="Urban Private", color="#C55A11", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(SHORT, fontsize=10, fontweight="bold")
    ax.set_ylabel("% Students with High Interest", fontsize=11)
    ax.set_ylim(0, 100)
    ax.set_title("Figure 4.5 — Percentage of Students with High Interest: Rural vs. Urban",
                 fontsize=12, fontweight="bold", pad=10)
    ax.legend(fontsize=11); ax.yaxis.grid(True, linestyle="--", alpha=0.5); ax.set_axisbelow(True)
    for bar in list(b1)+list(b2):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                f"{bar.get_height():.0f}%", ha="center", va="bottom", fontsize=8, fontweight="bold")
    fig.tight_layout()
    return save(fig, "fig4_5_rural_urban_pct.png")

def grouped_bar_4groups():
    x = np.arange(len(SHORT)); w = 0.2
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = ["#003087","#FF1493","#4472C4","#FF69B4"]
    labels = ["Rural Boys","Rural Girls","Urban Boys","Urban Girls"]
    data   = [rb_mean, rg_mean, ub_mean, ug_mean]
    offsets= [-1.5*w, -0.5*w, 0.5*w, 1.5*w]
    bars_list = []
    for d, c, l, off in zip(data, colors, labels, offsets):
        b = ax.bar(x+off, d, w, label=l, color=c, edgecolor="white", linewidth=0.4)
        bars_list.append(b)
    ax.set_xticks(x); ax.set_xticklabels(SHORT, fontsize=9, fontweight="bold")
    ax.set_ylabel("Mean Score (Max = 20)", fontsize=11)
    ax.set_ylim(0, 22)
    ax.set_title("Figure 4.6 — Mean Vocational Scores: Rural Boys / Rural Girls / Urban Boys / Urban Girls\n(Gender × School Type Comparison)",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(fontsize=9, ncol=2, framealpha=0.9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4); ax.set_axisbelow(True)
    fig.tight_layout()
    return save(fig, "fig4_6_4group_bar.png")

def rural_urban_3d_bar():
    x = np.arange(len(SHORT)); w = 0.35
    fig, ax = plt.subplots(figsize=(13, 5.5))
    for xi, (rv, uv) in enumerate(zip(rural_mean, urban_mean)):
        ax.bar(xi-w/2, rv, w, color="#70AD47", edgecolor="white", zorder=3)
        ax.bar(xi+w/2, uv, w, color="#ED7D31", edgecolor="white", zorder=3)
        # shadow for "3D" feel
        ax.bar(xi-w/2+0.06, rv, w, color="#4E7A31", edgecolor="none", alpha=0.35, zorder=2)
        ax.bar(xi+w/2+0.06, uv, w, color="#A85A20", edgecolor="none", alpha=0.35, zorder=2)
    ax.set_xticks(x); ax.set_xticklabels(SHORT, fontsize=10, fontweight="bold")
    ax.set_ylabel("Mean Score (Max = 20)", fontsize=11)
    ax.set_ylim(0, 22)
    ax.set_title("Figure 4.7 — Mean Vocational Interest: Rural Govt. vs. Urban Private (3D Style)",
                 fontsize=12, fontweight="bold", pad=10)
    p1 = mpatches.Patch(color="#70AD47", label="Rural Govt. School")
    p2 = mpatches.Patch(color="#ED7D31", label="Urban Private School")
    ax.legend(handles=[p1,p2], fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5); ax.set_axisbelow(True)
    fig.tight_layout()
    return save(fig, "fig4_7_rural_urban_3d.png")

def line_chart_4groups():
    x = np.arange(len(SHORT))
    fig, ax = plt.subplots(figsize=(13, 6))
    styles = [
        (rb_mean, "Rural Boys",  "#003087", "o-",  2.2),
        (rg_mean, "Rural Girls", "#C0006A", "s-",  2.2),
        (ub_mean, "Urban Boys",  "#4472C4", "^--", 2.0),
        (ug_mean, "Urban Girls", "#FF69B4", "D--", 2.0),
    ]
    for data, label, color, style, lw in styles:
        ax.plot(x, data, style, label=label, color=color, linewidth=lw,
                markersize=7, markerfacecolor="white", markeredgewidth=2)
    ax.set_xticks(x); ax.set_xticklabels(SHORT, fontsize=10, fontweight="bold")
    ax.set_ylabel("Mean Score (Max = 20)", fontsize=11)
    ax.set_ylim(0, 21)
    ax.set_title("Figure 4.8 — Vocational Interest Trend Lines: Gender × School Type\n(Rural Boys, Rural Girls, Urban Boys, Urban Girls)",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(fontsize=10, ncol=2, framealpha=0.9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.45); ax.set_axisbelow(True)
    # annotate crossing zone at COM/EXE
    ax.axvspan(3.5, 5.5, alpha=0.06, color="gold", label="_nolegend_")
    ax.text(4.5, 20.2, "Gender gap narrows\n(COM & EXE)", ha="center", fontsize=8,
            color="goldenrod", fontweight="bold")
    fig.tight_layout()
    return save(fig, "fig4_8_line_chart.png")

# ── GENERATE ALL CHARTS ────────────────────────────────────────────────────────
print("Generating charts …")
chart_paths = {
    "fig4_1": bar_chart_gender(),
    "fig4_2": bar_chart_rural_urban(),
    "fig4_3": pie_chart_boys(),
    "fig4_4": pie_chart_girls(),
    "fig4_5": comparative_bar_pct(),
    "fig4_6": grouped_bar_4groups(),
    "fig4_7": rural_urban_3d_bar(),
    "fig4_8": line_chart_4groups(),
}
print(f"  {len(chart_paths)} charts saved to {CHARTS}")

# ── COMBINE MARKDOWN ──────────────────────────────────────────────────────────
print("Combining markdown …")
PAGE_BREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
with open(COMBINED, "w", encoding="utf-8") as out:
    for i, fn in enumerate(FILES):
        with open(os.path.join(DISS, fn), "r", encoding="utf-8") as src:
            out.write(src.read())
        if i < len(FILES) - 1:
            out.write(PAGE_BREAK)
print(f"  Combined markdown: {COMBINED}")

# ── PANDOC → DOCX ─────────────────────────────────────────────────────────────
print("Running pandoc …")
import pypandoc
pypandoc.convert_file(
    COMBINED,
    "docx",
    format="markdown-yaml_metadata_block+pipe_tables+raw_attribute",
    outputfile=OUT,
    extra_args=["--standalone"],
)
print(f"  Raw docx: {OUT}")

# ── POST-PROCESS WITH PYTHON-DOCX ─────────────────────────────────────────────
print("Applying CCSU formatting …")
doc = Document(OUT)

# margins
for section in doc.sections:
    section.left_margin   = Inches(1.5)
    section.right_margin  = Inches(1.0)
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)

HEADING_PT = {"Heading 1":16,"Heading 2":14,"Heading 3":13,
              "Heading 4":12,"Heading 5":12,"Heading 6":12}

def set_tnr(run, pt):
    run.font.name = "Times New Roman"
    run.font.size = Pt(pt)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.insert(0, rFonts)
    for attr in ("w:ascii","w:hAnsi","w:cs","w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")

for para in doc.paragraphs:
    sname = para.style.name if para.style else ""
    if sname in HEADING_PT:
        pt = HEADING_PT[sname]
        if sname in ("Heading 1","Heading 2"):
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after  = Pt(6)
        for run in para.runs:
            set_tnr(run, pt); run.bold = True
    else:
        pt = 12
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_after = Pt(6)
        for run in para.runs:
            set_tnr(run, pt)

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
                para.paragraph_format.line_spacing = 1.15
                for run in para.runs:
                    set_tnr(run, 11)

# page numbers
def add_page_num(footer):
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    for tag, txt in [("w:fldChar","begin"),("w:instrText","PAGE"),("w:fldChar","end")]:
        el = OxmlElement(tag)
        if tag == "w:fldChar":
            el.set(qn("w:fldCharType"), txt)
        else:
            el.set(qn("xml:space"), "preserve"); el.text = txt
        run._r.append(el)
    set_tnr(run, 11)

for section in doc.sections:
    add_page_num(section.footer)

doc.save(OUT)
print("  Formatting applied.")

# ── INJECT CHARTS ─────────────────────────────────────────────────────────────
print("Injecting charts into docx …")
doc = Document(OUT)

# Map placeholder text → chart path & caption
CHART_MAP = [
    ("fig4_1", "fig4_1_gender_bar.png",
     "Figure 4.1 — Mean Vocational Interest Scores: Boys vs. Girls"),
    ("fig4_2", "fig4_2_rural_urban_bar.png",
     "Figure 4.2 — Mean Vocational Interest Scores: Rural vs. Urban"),
    ("fig4_3", "fig4_3_boys_pie.png",
     "Figure 4.3 — Boys: Percentage with High Interest by Vocational Area"),
    ("fig4_4", "fig4_4_girls_pie.png",
     "Figure 4.4 — Girls: Percentage with High Interest by Vocational Area"),
    ("fig4_5", "fig4_5_rural_urban_pct.png",
     "Figure 4.5 — Comparative: % High Interest Rural vs. Urban"),
    ("fig4_6", "fig4_6_4group_bar.png",
     "Figure 4.6 — Mean Scores: Rural Boys / Rural Girls / Urban Boys / Urban Girls"),
    ("fig4_7", "fig4_7_rural_urban_3d.png",
     "Figure 4.7 — Rural vs. Urban Vocational Interest (3D Style)"),
    ("fig4_8", "fig4_8_line_chart.png",
     "Figure 4.8 — Vocational Interest Trend Lines: Gender × School Type"),
]

def insert_image_after(para, img_path, caption_text):
    """Insert an image paragraph + caption paragraph immediately after 'para'."""
    from docx.oxml import OxmlElement as OE
    from copy import deepcopy

    body = doc.element.body
    para_idx = list(body).index(para._element)

    # image paragraph
    img_para = doc.add_paragraph()
    img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = img_para.add_run()
    run.add_picture(img_path, width=Inches(6.0))
    body.remove(img_para._element)
    body.insert(para_idx + 1, img_para._element)

    # caption paragraph
    cap_para = doc.add_paragraph()
    cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_run = cap_para.add_run(caption_text)
    set_tnr(cap_run, 11)
    cap_run.bold = True
    body.remove(cap_para._element)
    body.insert(para_idx + 2, cap_para._element)

    # blank line after
    blank = doc.add_paragraph()
    body.remove(blank._element)
    body.insert(para_idx + 3, blank._element)

inserted = set()
for para in doc.paragraphs:
    text_lower = para.text.lower()
    for key, fname, caption in CHART_MAP:
        if key in inserted:
            continue
        fig_num = key.replace("fig4_","fig4.")  # "fig4_1" → look for "figure 4.1"
        fig_label = "figure " + key.split("_")[1].replace("fig4_","4.")
        # match lines like "NOTE FOR MS WORD" or the figure reference line
        if ("note for ms word" in text_lower and fig_num.replace("_",".") in text_lower) \
           or ("figure " + key.split("_")[1] in text_lower and "insert" in text_lower):
            img_path = os.path.join(CHARTS, fname)
            if os.path.exists(img_path):
                insert_image_after(para, img_path, caption)
                inserted.add(key)
                break

# Also insert charts in order after Section 4.3, 4.5, 4.6, 4.7 headings
# by finding paragraphs with placeholder ASCII art blocks
remaining = [k for k, _, _ in CHART_MAP if k not in inserted]
if remaining:
    for para in doc.paragraphs:
        txt = para.text
        for key, fname, caption in CHART_MAP:
            if key in inserted: continue
            tag = key  # e.g. "fig4_1"
            if tag in txt or (fname.replace("_charts/","") in txt):
                img_path = os.path.join(CHARTS, fname)
                if os.path.exists(img_path):
                    insert_image_after(para, img_path, caption)
                    inserted.add(key)

# Final pass: append any still-not-inserted charts at end of Chapter 4
# (find the last paragraph of Chapter 4 content)
if len(inserted) < len(CHART_MAP):
    for key, fname, caption in CHART_MAP:
        if key in inserted: continue
        img_path = os.path.join(CHARTS, fname)
        if os.path.exists(img_path):
            # Find "Summary of Analysis" heading to insert before it
            for para in doc.paragraphs:
                if "summary of analysis" in para.text.lower():
                    insert_image_after(para, img_path, caption)
                    inserted.add(key)
                    break
            else:
                # absolute fallback: append to document
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run().add_picture(img_path, width=Inches(6.0))
                cap = doc.add_paragraph(caption)
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in cap.runs: set_tnr(r, 11); r.bold = True
                inserted.add(key)

print(f"  Charts injected: {len(inserted)}/{len(CHART_MAP)}")

doc.save(OUT)
size_kb = os.path.getsize(OUT) / 1024
print(f"\n✅  DONE → {OUT}  ({size_kb:.1f} KB)")
print(f"   Total charts embedded: {len(inserted)}")

# cleanup
if os.path.exists(COMBINED):
    os.remove(COMBINED)
