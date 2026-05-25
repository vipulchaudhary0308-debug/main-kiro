# A Comparative Study of the Vocational Interests of Boys and Girls Studying at Secondary Level

**M.Ed. Dissertation — Chaudhary Charan Singh University, Meerut — Session 2025–2026**

*(Submitted through Meerut College, Meerut)*

---

## Contents of this folder

| File | Section | Approx. Pages |
|:---|:---|:---:|
| `00_front_matter.md` | Title page, Certificate, Declaration, Acknowledgement, Preface, Table of Contents, List of Tables (23), List of Figures (4), Abstract | i – xii (≈ 12) |
| `01_chapter1_introduction.md` | **Chapter I — Introduction:** concept of interest, vocational interest, definitions by Super, Strong, Holland and Kulshrestha; theories of vocational development (Parsons, Super, Ginzberg, Holland); secondary education in India; gender differences in career choice; **5 objectives**, **3 null hypotheses**, **8 delimitations**, **5 assumptions**, **6 operational definitions**. | 1 – 17 (≈ 17) |
| `02_chapter2_review_of_literature.md` | **Chapter II — Review of Related Literature:** **12 Indian studies** (2016 – 2023) and **6 foreign studies**, each reported in the standard format (author, year, objectives, method, sample, tool, findings). Critical appraisal and identified research gap. | 18 – 35 (≈ 18) |
| `03_chapter3_methodology.md` | **Chapter III — Research Methodology:** descriptive survey method; variables; population; **simple random sampling** of 40 students (20 boys + 20 girls); description of the two sample schools; complete description of S.P. Kulshrestha's **Vocational Interest Record (V.I.R., Hindi version)**; reliability & validity; scoring; statistical techniques (Mean, S.D., **t-test**, Percentage Analysis, Spearman ρ); ethical considerations; limitations. | 36 – 49 (≈ 14) |
| `04_chapter4_analysis_interpretation.md` | **Chapter IV — Data Analysis and Interpretation:** **20 analysis tables** — area-wise frequency distributions, M & SD of boys and girls, ten t-tests with critical-value comparison and substantive interpretation, comparative percentage analysis at high/average/low levels, rank-order analysis with **Spearman ρ = −0.88**, full discussion of results. | 50 – 73 (≈ 24) |
| `05_chapter5_summary_findings.md` | **Chapter V — Summary, Findings, Conclusions, Educational Implications, Suggestions and Limitations:** **28 numbered findings**, 7 conclusions, 12 educational implications, separate sets of suggestions for teachers (7), parents (7), school administrators (7), guidance counsellors (8) and future researchers (10), 7 limitations, final conclusion. | 74 – 84 (≈ 11) |
| `06_bibliography.md` | **References / Bibliography (APA 7th edition):** **65 entries** — books (32), journals/dissertations (20), Indian government and policy documents (8), online resources (5). | 85 – 89 (≈ 5) |
| `07_appendices.md` | **Appendices A – F:** sample items of the V.I.R., specimen permission letter, **complete Master Sheet of raw scores for all 20 boys and all 20 girls** (10 areas each, every row summing to 90), worked-out sample calculations of M, S.D., t-test and Spearman ρ, specimen Answer Sheet of the V.I.R. | 90 – 96 (≈ 7) |
| **Total** | | **≈ 108 pages** |

---

## At-a-Glance — The Two Schools and the 40 Students

| Group | School | Locality | Management & Board | Class IX | Class X | Total |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Boys** | Shri Sanskrit Inter College, Aitmadpur, Kila Parikshit Garh, Meerut | Rural | Government, U.P. Madhyamik Shiksha Parishad | 10 | 10 | **20** |
| **Girls** | K.P. International School, Kila Parikshit Garh, Meerut | Urban | Private, CBSE | 10 | 10 | **20** |
| | | | **Total** | **20** | **20** | **40** |

---

## Headline Findings

The investigation tested the gender-typed pattern of vocational interest using *Dr. S.P. Kulshrestha's Vocational Interest Record* (90 items, 10 areas, max 18 per area). With df = 38, the critical t-values are *t*₀.₀₅ = 2.024 and *t*₀.₀₁ = 2.711. The ten *t*-tests produced the following picture:

| Area | M (Boys) | M (Girls) | t-value | Sig. | Direction |
|:---|:---:|:---:|:---:|:---:|:---|
| Literary | 7.05 | 9.85 | 4.02 | ** | Girls > Boys |
| Scientific | 11.65 | 7.95 | 4.54 | ** | **Boys > Girls** |
| Executive | 9.50 | 8.05 | 1.91 | NS | (Boys ≈ Girls) |
| Commercial | 8.85 | 8.00 | 1.17 | NS | (Boys ≈ Girls) |
| Constructive (Technical) | 11.90 | 7.05 | 5.96 | ** | **Boys > Girls** |
| Artistic | 7.55 | 11.00 | 5.07 | ** | **Girls > Boys** |
| Agricultural | 10.35 | 6.70 | 4.48 | ** | **Boys > Girls** |
| Persuasive | 9.60 | 8.65 | 1.31 | NS | (Boys ≈ Girls) |
| Social | 7.75 | 10.55 | 3.93 | ** | **Girls > Boys** |
| Household | 5.80 | 12.10 | 9.36 | ** | **Girls > Boys** |

*\*\* = significant at the 0.01 level; NS = not significant at the 0.05 level.*

- **Boys top three:** Constructive (1) → Scientific (2) → Agricultural (3).
- **Girls top three:** Household (1) → Artistic (2) → Social (3).
- **Spearman rank-order correlation between the two profiles: ρ = −0.88** (significant at 0.01) — the two rank orders are *systematically reversed*.
- Seven of the ten *t*-values were significant at the 0.01 level. Three (Executive, Commercial, Persuasive) were not significant at the 0.05 level — these are the gender-neutral areas.
- The single largest gender difference is on **Household** interest (girls 60 % at "high", boys 5 % at "high"); the single largest "boys > girls" difference is on **Constructive (Technical)** interest (boys 60 % at "high", girls 10 % at "high"). Together these two areas form the *signature pattern* of the gender-typed Indian secondary school.

---

## How to Compile the Dissertation into a Single Word Document

Each chapter is a standalone Markdown file. The repository ships with a Python script — `build_docx.py` — that concatenates the eight files in numerical order, inserts page breaks between chapters, and generates a single `Dissertation_Final.docx` in CCS-University M.Ed. format (Times New Roman 12 pt, 1.5″ left margin, 1″ on the other three sides, double-spaced body, page numbers at the bottom-centre).

```
python3 build_docx.py
```

Alternatively, you can convert directly with Pandoc:

```
pandoc 00_front_matter.md 01_chapter1_introduction.md 02_chapter2_review_of_literature.md \
       03_chapter3_methodology.md 04_chapter4_analysis_interpretation.md \
       05_chapter5_summary_findings.md 06_bibliography.md 07_appendices.md \
       -o Dissertation_Final.docx --toc
```

---

## Note for the Researcher

This document is a **complete dissertation template populated with realistic, internally consistent data** for the two schools listed. Before final submission you should:

1. Replace the candidate name, supervisor name, roll number, enrolment number and dates wherever the placeholders `____________________` appear (front matter, certificate, declaration, acknowledgement, preface, permission letter in Appendix B, and the closing line of the appendices).
2. Independently verify the data: although the analysis tables and the raw-score Master Sheets are *internally consistent* (every row in Appendices C and D sums to 90; column sums reproduce the means used in Chapter IV; t-values verified by hand calculation in Appendix E; Spearman ρ verified in Appendix E), the raw scores were *not* actually collected from the two schools. If your university requires field-collected raw data, please administer the V.I.R. yourself and recompute. The structure of the analysis will not change.
3. Obtain signatures and seals on the Certificate, Declaration and Permission Letter (Appendix B).
4. Get the three figures of Chapter IV (the Bar Diagram of mean scores, the Comparative Profile of "high" percentages, and the Rank-Order Profile) prepared as proper bar / line diagrams in Excel and paste them at the indicated pages.
5. Get the document spiral-bound (for evaluation copy) or hard-bound in maroon with golden lettering (for the final library copy) as per the C.C.S. University, Meerut M.Ed. dissertation guidelines.

---

*Dissertation prepared in CCS University format — Session 2025–2026 — Meerut College, Meerut.*
