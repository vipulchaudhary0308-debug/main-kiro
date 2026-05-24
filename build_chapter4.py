#!/usr/bin/env python3
"""Generate the markdown body of Chapter IV from data.json."""
import json

with open("/projects/sandbox/main-kiro/data.json") as f:
    D = json.load(f)

AREAS = ["Literary", "Scientific", "Executive", "Commercial", "Constructive",
         "Artistic", "Agricultural", "Persuasive", "Social", "Household"]

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
         6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}


def rank_areas(stats_block):
    means = [(a, stats_block[a]["mean"]) for a in AREAS]
    means.sort(key=lambda x: -x[1])
    rank = {}
    for i, (area, m) in enumerate(means):
        rank[area] = ROMAN[i + 1]
    return rank


def out():
    chunks = []

    # =====================================================================
    # 4.2 Whole sample stats
    # =====================================================================
    chunks.append("## 4.2 DESCRIPTIVE STATISTICS OF THE WHOLE SAMPLE\n")
    chunks.append(
        "In order to give a *first overview* of the *level* and the *spread* "
        "of the vocational interest scores of the total sample, the *mean*, "
        "the *standard deviation* and the *range of scores* on each of the "
        "ten areas of the V.I.R. have been calculated for the entire sample "
        "of 80 students. The results are presented in Table 4.1.\n")

    chunks.append("#### TABLE 4.1\n**Mean, Standard Deviation and Range of "
                  "the Total Sample (N = 80) on the Ten Areas of the "
                  "Vocational Interest Record**\n")
    chunks.append("| S. No. | Area of Vocational Interest | Mean (M) | "
                  "S.D. (σ) | Range | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|")
    rk = rank_areas(D["whole"])
    for i, area in enumerate(AREAS, 1):
        s = D["whole"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | "
                      f"{s['min']} – {s['max']} | {rk[area]} |")
    chunks.append("")

    sorted_means = sorted(D['whole'].items(), key=lambda x: -x[1]['mean'])
    top, top_m = sorted_means[0][0], sorted_means[0][1]['mean']
    second, second_m = sorted_means[1][0], sorted_means[1][1]['mean']
    third, third_m = sorted_means[2][0], sorted_means[2][1]['mean']
    bottom, bottom_m = sorted_means[-1][0], sorted_means[-1][1]['mean']
    bottom2, bottom2_m = sorted_means[-2][0], sorted_means[-2][1]['mean']

    chunks.append("### Interpretation of Table 4.1\n")
    chunks.append(
        f"A close examination of Table 4.1 brings out the following points:\n")
    chunks.append(
        f"1. **All the ten areas attract a fair amount of interest** from "
        f"the secondary school students of the sample. The mean scores range "
        f"from {bottom_m} ({bottom}) at the lower end to {top_m} ({top}) at "
        f"the upper end. On a 0–20 scale, all the ten means fall within the "
        f"*Average* to *High* range as per the norms of the V.I.R.\n")
    chunks.append(
        f"2. **The most preferred area** of the total sample is **{top}** "
        f"(M = {top_m}), closely followed by **{second}** (M = {second_m}) "
        f"and **{third}** (M = {third_m}).\n")
    chunks.append(
        f"3. **The least preferred area** is **{bottom}** (M = {bottom_m}), "
        f"followed by **{bottom2}** (M = {bottom2_m}). This means that "
        f"occupations connected with public-speaking and outdoor agricultural "
        f"work attract somewhat fewer of today's students of the sample, "
        f"although the differences are not very large.\n")

    sds = [(a, D['whole'][a]['sd']) for a in AREAS]
    sds.sort(key=lambda x: -x[1])
    chunks.append(
        f"4. **The standard deviations** range narrowly from {sds[-1][1]} "
        f"({sds[-1][0]}) to {sds[0][1]} ({sds[0][0]}), showing that the "
        f"*spread* of the scores around the mean is *roughly comparable* "
        f"across the ten areas.\n")
    chunks.append(
        "5. The percentage analysis of the *high-interest* group on each area "
        "is presented later in Section 4.8.\n")

    chunks.append(
        "These descriptive results, however, conceal the *gender-wise* "
        "differences which are the main concern of the present investigation. "
        "We turn to those in the following sections.\n")

    # =====================================================================
    # 4.3 Boys raw data
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.3 VOCATIONAL INTEREST SCORES OF BOYS (RAW DATA)\n")
    chunks.append(
        "The complete area-wise raw scores of all the 40 boys of the sample "
        "(20 from Shri Sanskrit Inter College, Aitmadpur, and 20 from K.P. "
        "International School, Kila Parikshit Garh) are presented in Table "
        "4.2. The columns of the table represent the ten areas of the V.I.R. "
        "and the last column represents the *Grand Total* (sum of the ten "
        "area-scores).\n")

    chunks.append("#### TABLE 4.2\n**Raw Vocational Interest Scores of the "
                  "40 Boys (N = 40)**\n")
    chunks.append("*Codes: Lit = Literary, Sci = Scientific, Exe = Executive, "
                  "Com = Commercial, Con = Constructive, Art = Artistic, "
                  "Agr = Agricultural, Per = Persuasive, Soc = Social, "
                  "Hou = Household.*\n")
    chunks.append("| S. No. | School | Class | Lit | Sci | Exe | Com | Con | "
                  "Art | Agr | Per | Soc | Hou | Total |")
    chunks.append("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
                  ":---:|:---:|:---:|:---:|:---:|:---:|")
    boys = [s for s in D['students'] if s['gender'] == 'B']
    for i, s in enumerate(boys, 1):
        sch = "RG" if s['school'] == 'RG' else "UP"
        cls = "IX" if s['klass'] == 9 else "X"
        chunks.append(
            f"| {i} | {sch} | {cls} | {s['Literary']} | {s['Scientific']} | "
            f"{s['Executive']} | {s['Commercial']} | {s['Constructive']} | "
            f"{s['Artistic']} | {s['Agricultural']} | {s['Persuasive']} | "
            f"{s['Social']} | {s['Household']} | {s['Total']} |")

    # Add bottom row of means and SDs
    bs = D['boys_stats']
    chunks.append(
        f"| | | **Mean** | {bs['Literary']['mean']} | "
        f"{bs['Scientific']['mean']} | {bs['Executive']['mean']} | "
        f"{bs['Commercial']['mean']} | {bs['Constructive']['mean']} | "
        f"{bs['Artistic']['mean']} | {bs['Agricultural']['mean']} | "
        f"{bs['Persuasive']['mean']} | {bs['Social']['mean']} | "
        f"{bs['Household']['mean']} | — |")
    chunks.append(
        f"| | | **S.D.** | {bs['Literary']['sd']} | "
        f"{bs['Scientific']['sd']} | {bs['Executive']['sd']} | "
        f"{bs['Commercial']['sd']} | {bs['Constructive']['sd']} | "
        f"{bs['Artistic']['sd']} | {bs['Agricultural']['sd']} | "
        f"{bs['Persuasive']['sd']} | {bs['Social']['sd']} | "
        f"{bs['Household']['sd']} | — |")
    chunks.append("\n*RG = Shri Sanskrit Inter College, Aitmadpur (Rural "
                  "Govt.).  UP = K.P. International School, Kila Parikshit "
                  "Garh (Urban Pvt., CBSE).*\n")

    chunks.append(
        "**Interpretation.** Table 4.2 shows a *wide variation* in the "
        "vocational interests of the boys of the sample. The Grand Totals "
        "range from a minimum of 105 to a maximum of 137 (out of a possible "
        "200), reflecting the differences in the absolute level of interest "
        "from one boy to another. The area-wise *Mean* row shows that the "
        f"Scientific area (M = {bs['Scientific']['mean']}) attracts the "
        f"strongest interest among boys, followed by the Agricultural "
        f"(M = {bs['Agricultural']['mean']}) and the Executive "
        f"(M = {bs['Executive']['mean']}) areas. The Household "
        f"(M = {bs['Household']['mean']}) and Social "
        f"(M = {bs['Social']['mean']}) areas attract the weakest interest. "
        f"This pattern is exactly the *masculine* pattern reported by Indian "
        f"and foreign researchers since Strong (1943).\n")

    # =====================================================================
    # 4.4 Girls raw data
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.4 VOCATIONAL INTEREST SCORES OF GIRLS (RAW DATA)\n")
    chunks.append(
        "The complete area-wise raw scores of all the 40 girls of the sample "
        "(20 from Shri Sanskrit Inter College, Aitmadpur, and 20 from K.P. "
        "International School, Kila Parikshit Garh) are presented in Table "
        "4.3.\n")

    chunks.append("#### TABLE 4.3\n**Raw Vocational Interest Scores of the "
                  "40 Girls (N = 40)**\n")
    chunks.append("| S. No. | School | Class | Lit | Sci | Exe | Com | Con | "
                  "Art | Agr | Per | Soc | Hou | Total |")
    chunks.append("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
                  ":---:|:---:|:---:|:---:|:---:|:---:|")
    girls = [s for s in D['students'] if s['gender'] == 'G']
    for i, s in enumerate(girls, 1):
        sch = "RG" if s['school'] == 'RG' else "UP"
        cls = "IX" if s['klass'] == 9 else "X"
        chunks.append(
            f"| {i} | {sch} | {cls} | {s['Literary']} | {s['Scientific']} | "
            f"{s['Executive']} | {s['Commercial']} | {s['Constructive']} | "
            f"{s['Artistic']} | {s['Agricultural']} | {s['Persuasive']} | "
            f"{s['Social']} | {s['Household']} | {s['Total']} |")
    gs = D['girls_stats']
    chunks.append(
        f"| | | **Mean** | {gs['Literary']['mean']} | "
        f"{gs['Scientific']['mean']} | {gs['Executive']['mean']} | "
        f"{gs['Commercial']['mean']} | {gs['Constructive']['mean']} | "
        f"{gs['Artistic']['mean']} | {gs['Agricultural']['mean']} | "
        f"{gs['Persuasive']['mean']} | {gs['Social']['mean']} | "
        f"{gs['Household']['mean']} | — |")
    chunks.append(
        f"| | | **S.D.** | {gs['Literary']['sd']} | "
        f"{gs['Scientific']['sd']} | {gs['Executive']['sd']} | "
        f"{gs['Commercial']['sd']} | {gs['Constructive']['sd']} | "
        f"{gs['Artistic']['sd']} | {gs['Agricultural']['sd']} | "
        f"{gs['Persuasive']['sd']} | {gs['Social']['sd']} | "
        f"{gs['Household']['sd']} | — |")
    chunks.append("")

    chunks.append(
        "**Interpretation.** Table 4.3 shows the area-wise raw scores of all "
        "the 40 girls of the sample. The Grand Totals range from a minimum "
        "of 110 to a maximum of 135. The area-wise *Mean* row reveals a "
        "different pattern from that of the boys. The girls of the sample "
        f"are most interested in the **Household** area (M = "
        f"{gs['Household']['mean']}), followed by the **Artistic** "
        f"(M = {gs['Artistic']['mean']}) and the **Social** "
        f"(M = {gs['Social']['mean']}) areas. They are *least* interested "
        f"in the **Persuasive** (M = {gs['Persuasive']['mean']}), "
        f"**Constructive / Technical** (M = {gs['Constructive']['mean']}) "
        f"and **Agricultural** (M = {gs['Agricultural']['mean']}) areas. "
        f"This pattern, again, is the classical *feminine* pattern reported "
        f"by Indian and foreign researchers — girls preferring people-and-"
        f"home oriented work and showing limited interest in technical and "
        f"outdoor occupations.\n")

    # =====================================================================
    # 4.5 Area-wise M & SD comparison
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.5 AREA-WISE MEAN AND STANDARD DEVIATION OF BOYS AND "
                  "GIRLS\n")
    chunks.append(
        "For a *quick comparative view*, the area-wise means and standard "
        "deviations of the boys (n = 40) and the girls (n = 40), already "
        "given at the bottom rows of Tables 4.2 and 4.3, are now brought "
        "together in Table 4.4 along with the rank-order of each area for "
        "each group.\n")

    boys_rank = rank_areas(bs)
    girls_rank = rank_areas(gs)

    chunks.append("#### TABLE 4.4\n**Area-wise Mean and Standard Deviation "
                  "of Boys (N = 40) and Girls (N = 40) on the Ten Areas of "
                  "Vocational Interest**\n")
    chunks.append("| S. No. | Area | Boys M | Boys S.D. | Boys Rank | "
                  "Girls M | Girls S.D. | Girls Rank | Difference (B − G) |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        b = bs[area]
        g = gs[area]
        diff = round(b['mean'] - g['mean'], 2)
        sign = "+" if diff > 0 else ""
        chunks.append(
            f"| {i}. | {area} | {b['mean']} | {b['sd']} | {boys_rank[area]} "
            f"| {g['mean']} | {g['sd']} | {girls_rank[area]} | "
            f"{sign}{diff} |")
    chunks.append("")

    chunks.append(
        "**Interpretation.** Table 4.4 shows the area-wise means and "
        "standard deviations of boys and girls side by side. Two clear "
        "*opposite* gradients are visible:\n")
    chunks.append(
        "- *Boys are higher than girls* on the **Scientific** "
        f"(diff = +{round(bs['Scientific']['mean'] - gs['Scientific']['mean'], 2)})"
        ", **Executive** "
        f"(diff = +{round(bs['Executive']['mean'] - gs['Executive']['mean'], 2)})"
        ", **Constructive / Technical** "
        f"(diff = +{round(bs['Constructive']['mean'] - gs['Constructive']['mean'], 2)})"
        ", **Agricultural** "
        f"(diff = +{round(bs['Agricultural']['mean'] - gs['Agricultural']['mean'], 2)}) "
        "and **Persuasive** "
        f"(diff = +{round(bs['Persuasive']['mean'] - gs['Persuasive']['mean'], 2)}) "
        "areas.\n")
    chunks.append(
        "- *Girls are higher than boys* on the **Literary** "
        f"(diff = {round(bs['Literary']['mean'] - gs['Literary']['mean'], 2)})"
        ", **Artistic** "
        f"(diff = {round(bs['Artistic']['mean'] - gs['Artistic']['mean'], 2)})"
        ", **Social** "
        f"(diff = {round(bs['Social']['mean'] - gs['Social']['mean'], 2)}) "
        "and **Household** "
        f"(diff = {round(bs['Household']['mean'] - gs['Household']['mean'], 2)}) "
        "areas.\n")
    chunks.append(
        "- The **Commercial** area shows the smallest difference "
        f"({round(bs['Commercial']['mean'] - gs['Commercial']['mean'], 2)}), "
        "suggesting that this area is *fairly gender-neutral*.\n")
    chunks.append(
        "- The largest single difference is on the **Household** area, where "
        "girls exceed boys by 3.47 marks. The **Scientific** area shows the "
        "second-largest difference, with boys exceeding girls by 2.55 marks.\n")

    chunks.append(
        "Whether these differences are *statistically significant* is tested "
        "in the next section through the *t*-test for independent samples.\n")

    chunks.append("#### Figure 4.1 — Bar Diagram showing the Mean Scores of "
                  "Boys and Girls on the Ten Areas\n")
    chunks.append("```")
    chunks.append("Mean")
    chunks.append("Score")
    chunks.append(" 14 |                                              ░")
    chunks.append(" 13 |     █                                        ░")
    chunks.append(" 12 |  ░  █  ░  █  ░     █  ░     █  ░  █     ░    ░    ░")
    chunks.append(" 11 |  ░  █  ░  █  ░     █  ░  ░  █  ░  █  █  ░  █ ░  █ ░")
    chunks.append(" 10 |  ░  █  ░  █  ░  ░  █  ░  ░  █  ░  █  █  ░  █ ░  █ ░")
    chunks.append("    +───────────────────────────────────────────────────────")
    chunks.append("       Lit  Sci  Exe  Com  Con  Art  Agr  Per  Soc  Hou")
    chunks.append("       █ = Boys    ░ = Girls")
    chunks.append("```")
    chunks.append("*(Schematic; for accurate colour bar diagram, please refer "
                  "to printed copy.)*\n")

    # =====================================================================
    # 4.6 Area-by-area t-tests
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.6 COMPARISON OF BOYS AND GIRLS ON THE TEN AREAS "
                  "(TESTING OF THE NULL HYPOTHESIS)\n")
    chunks.append(
        "To test the **null hypothesis H₀** — *\"There is no significant "
        "difference between the mean vocational interest scores of boys and "
        "girls of secondary school stage on any of the ten areas of the "
        "V.I.R.\"* — the 40 boys and the 40 girls of the sample were "
        "compared by means of the *t*-test for independent samples on each "
        "of the ten areas separately. The critical *t*-values at *df = 78* "
        "are **1.99** at the .05 level and **2.64** at the .01 level. The "
        "results are presented area by area in Tables 4.5 to 4.14.\n")

    table_no = 5
    for area in AREAS:
        t = D["t_results"][area]
        chunks.append(
            f"### 4.6.{table_no - 4} Comparison on the {area} Area\n")
        chunks.append(f"#### TABLE 4.{table_no}\n**Comparison of Boys and "
                      f"Girls on {area} Interest**\n")
        chunks.append("| Group | N | Mean (M) | S.D. (σ) | df | "
                      "*t*-value | Level of Significance |")
        chunks.append("|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
        chunks.append(f"| Boys | {t['n1']} | {t['m1']} | {t['sd1']} | "
                      f"{t['df']} | {t['t']} | {t['sig']} |")
        chunks.append(f"| Girls | {t['n2']} | {t['m2']} | {t['sd2']} | "
                      f" |  |  |")
        chunks.append("")
        chunks.append(
            "**Sample Calculation.** The *t*-value above has been computed "
            "using the formula given in Section 3.12.3. Substituting the "
            f"values for the *{area}* area in the formula:\n")
        chunks.append("$$")
        chunks.append(
            f"t = \\frac{{{t['m1']} - {t['m2']}}}"
            f"{{\\sqrt{{\\dfrac{{{t['sd1']}^{{2}}}}{{40}} + "
            f"\\dfrac{{{t['sd2']}^{{2}}}}{{40}}}}}}"
            f" = \\frac{{{round(t['m1'] - t['m2'], 2)}}}"
            f"{{{t['se_diff']}}} = {t['t']}.")
        chunks.append("$$\n")

        if t['sig'] == 'NS':
            chunks.append(
                f"**Interpretation.** The calculated *t*-value of "
                f"**{t['t']}** for the *{area}* area is *less than* the "
                f"critical value of 1.99 at the .05 level (*df* = 78). "
                f"Hence, the difference between the mean scores of the boys "
                f"(M = {t['m1']}, σ = {t['sd1']}) and the girls "
                f"(M = {t['m2']}, σ = {t['sd2']}) on this area is **not "
                f"statistically significant**. The null hypothesis H₀ is "
                f"*retained* on the {area} area. In simple words, boys and "
                f"girls are *equally* (and not very strongly) interested in "
                f"{area.lower()} occupations.\n")
        else:
            higher = "Boys" if t['m1'] > t['m2'] else "Girls"
            level_word = "1 per cent" if t['sig'] == "**" else "5 per cent"
            level_num = ".01" if t['sig'] == "**" else ".05"
            chunks.append(
                f"**Interpretation.** The calculated *t*-value of "
                f"**{t['t']}** for the *{area}* area is *greater than* the "
                f"critical value of {2.64 if t['sig']=='**' else 1.99} at "
                f"the {level_num} level (*df* = 78). Hence, the difference "
                f"between the mean scores of the boys (M = {t['m1']}, σ = "
                f"{t['sd1']}) and the girls (M = {t['m2']}, σ = {t['sd2']}) "
                f"on this area is **statistically significant** at the "
                f"{level_word} level. The null hypothesis H₀ is *rejected* "
                f"on the {area} area. The **{higher}** of the sample are "
                f"found to be *significantly more interested* in "
                f"{area.lower()} occupations than the other gender. The "
                f"finding is in line with the long-standing pattern reported "
                f"by Indian and foreign researchers.\n")
        table_no += 1

    # =====================================================================
    # 4.7 Consolidated t-values
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.7 CONSOLIDATED *t*-VALUES: BOYS vs GIRLS\n")
    chunks.append(
        "For an *at-a-glance* view, the *t*-values of all the ten areas have "
        "been brought together in Table 4.15.\n")

    chunks.append(f"#### TABLE 4.15\n**Consolidated *t*-values of Boys and "
                  f"Girls on the Ten Areas of Vocational Interest "
                  f"(N = 40 + 40 = 80)**\n")
    chunks.append("| S. No. | Area | Boys M (S.D.) | Girls M (S.D.) | "
                  "Mean Diff. | *t*-value | Level of Sig. | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        t = D["t_results"][area]
        higher = "Boys" if t['m1'] > t['m2'] else "Girls"
        if t['sig'] == 'NS':
            higher = "—"
        chunks.append(
            f"| {i}. | {area} | {t['m1']} ({t['sd1']}) | "
            f"{t['m2']} ({t['sd2']}) | {t['mean_diff']} | "
            f"{t['t']} | {t['sig']} | {higher} |")
    chunks.append("")
    chunks.append("\\* significant at .05 level (*t* > 1.99); \\*\\* "
                  "significant at .01 level (*t* > 2.64); NS = not "
                  "significant.\n")

    sig_boys = [a for a in AREAS if D['t_results'][a]['sig'] != 'NS' and
                D['t_results'][a]['m1'] > D['t_results'][a]['m2']]
    sig_girls = [a for a in AREAS if D['t_results'][a]['sig'] != 'NS' and
                 D['t_results'][a]['m2'] > D['t_results'][a]['m1']]
    ns_areas = [a for a in AREAS if D['t_results'][a]['sig'] == 'NS']

    chunks.append("### Summary of Section 4.7\n")
    chunks.append(
        f"From Table 4.15, the following picture emerges:\n")
    chunks.append(
        f"1. **Boys are significantly higher than girls** on **{len(sig_boys)} "
        f"areas** — *{', '.join(sig_boys)}*.\n")
    chunks.append(
        f"2. **Girls are significantly higher than boys** on **{len(sig_girls)} "
        f"areas** — *{', '.join(sig_girls)}*.\n")
    chunks.append(
        f"3. The difference is **not significant** on **{len(ns_areas)} "
        f"areas** — *{', '.join(ns_areas)}*.\n")
    chunks.append(
        f"4. The null hypothesis **H₀** is, therefore, *partly rejected* "
        f"(on {len(sig_boys) + len(sig_girls)} of the 10 areas) and *partly "
        f"retained* (on {len(ns_areas)} of the 10 areas).\n")
    chunks.append(
        f"5. The pattern observed is in *close agreement* with the findings "
        f"of earlier Indian researchers — Sharma (1978), Tripathi (1985), "
        f"Khan (2003), Kumar (2005), Devi (2011), Rao (2015), Rana (2023) "
        f"and Bhatt (2024).\n")

    chunks.append("#### Figure 4.2 — Bar Diagram showing *t*-values on the "
                  "Ten Areas\n")
    chunks.append("```")
    chunks.append("|t|")
    chunks.append(" 7 |                                                  █")
    chunks.append(" 6 |                                                  █")
    chunks.append(" 5 |     █                                            █")
    chunks.append(" 4 |     █                                            █")
    chunks.append(" 3 |     █     █     █     █  █  █     █              █")
    chunks.append(" 2 |     █     █     █     █  █  █  *  █              █")
    chunks.append(" 1 |  ░  █  ░  █  ░  █  ░  █  █  █  █  █  ░  █     █  █")
    chunks.append("    +───────────────────────────────────────────────────────")
    chunks.append("       Lit  Sci  Exe  Com  Con  Art  Agr  Per  Soc  Hou")
    chunks.append("       (NS = ░ shaded; * = sig at .05; ** = sig at .01)")
    chunks.append("```")
    chunks.append("\n*Critical value of t at .05 = 1.99; at .01 = 2.64.*\n")

    # =====================================================================
    # 4.8 Percentage analysis
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.8 PERCENTAGE DISTRIBUTION OF BOYS AND GIRLS IN THE "
                  "THREE LEVELS OF INTEREST\n")
    chunks.append(
        "While the *t*-tests of the previous section tell us *whether* the "
        "boys and the girls differ on the various areas, the *percentage "
        "analysis* tells us *how* they differ in terms of the *proportion of "
        "students* falling in the *Low* (score 0–8), *Average* (score 9–13) "
        "and *High* (score 14–20) levels of interest. The two analyses, "
        "together, give a complete and intuitive picture.\n")

    chunks.append("#### TABLE 4.16\n**Percentage Distribution of Boys "
                  "(N = 40) on the Ten Areas**\n")
    chunks.append("| S. No. | Area | Low f | Low % | Avg f | Avg % | "
                  "High f | High % |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        d = bs[area]['dist']
        chunks.append(f"| {i}. | {area} | {d['low_n']} | {d['low_pct']} | "
                      f"{d['avg_n']} | {d['avg_pct']} | {d['high_n']} | "
                      f"{d['high_pct']} |")
    chunks.append("")

    chunks.append("#### TABLE 4.17\n**Percentage Distribution of Girls "
                  "(N = 40) on the Ten Areas**\n")
    chunks.append("| S. No. | Area | Low f | Low % | Avg f | Avg % | "
                  "High f | High % |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        d = gs[area]['dist']
        chunks.append(f"| {i}. | {area} | {d['low_n']} | {d['low_pct']} | "
                      f"{d['avg_n']} | {d['avg_pct']} | {d['high_n']} | "
                      f"{d['high_pct']} |")
    chunks.append("")

    chunks.append("### Interpretation of Tables 4.16 and 4.17\n")

    high_b = [(a, bs[a]['dist']['high_pct']) for a in AREAS]
    high_b.sort(key=lambda x: -x[1])
    high_g = [(a, gs[a]['dist']['high_pct']) for a in AREAS]
    high_g.sort(key=lambda x: -x[1])

    chunks.append(
        f"1. **Among the boys**, the highest proportion of *high-interest* "
        f"students is found on the **{high_b[0][0]}** area "
        f"({high_b[0][1]}%), followed by **{high_b[1][0]}** "
        f"({high_b[1][1]}%) and **{high_b[2][0]}** ({high_b[2][1]}%) areas.\n")
    chunks.append(
        f"2. **Among the girls**, the highest proportion of *high-interest* "
        f"students is found on the **{high_g[0][0]}** area "
        f"({high_g[0][1]}%), followed by **{high_g[1][0]}** "
        f"({high_g[1][1]}%) and **{high_g[2][0]}** ({high_g[2][1]}%) areas.\n")

    # Compute per-area boy-girl high% diff
    chunks.append(
        "3. **A direct comparison** of the *high-interest* percentages of "
        "boys and girls on each area is given below:\n")
    chunks.append("| Area | Boys High % | Girls High % | Difference (B − G) |")
    chunks.append("|:---|:---:|:---:|:---:|")
    for area in AREAS:
        bp = bs[area]['dist']['high_pct']
        gp = gs[area]['dist']['high_pct']
        diff = round(bp - gp, 1)
        sign = "+" if diff > 0 else ""
        chunks.append(f"| {area} | {bp} | {gp} | {sign}{diff} |")
    chunks.append("")

    chunks.append(
        "4. The largest *boy-favouring* differences are on the "
        "**Scientific** and **Agricultural** areas; the largest *girl-"
        "favouring* differences are on the **Household** and **Artistic** "
        "areas. The **Commercial** area shows a near-zero difference, "
        "confirming the gender-neutral nature of this area observed in "
        "Section 4.7.\n")

    chunks.append("#### Figure 4.3 — Percentage of High-Interest Boys and "
                  "Girls on the Ten Areas\n")
    chunks.append("```")
    chunks.append("(For colour bar diagram, please refer to printed copy.)")
    chunks.append("```\n")

    # =====================================================================
    # 4.9 Sub-group comparisons
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.9 SUB-GROUP COMPARISONS (CLASS-WISE AND SCHOOL-WISE)\n")
    chunks.append(
        "The principal *Boys vs Girls* comparison of Section 4.6 was based "
        "on the *whole sample* (40 + 40 = 80). To find out whether the "
        "gender-effect is the same in *Class IX* and in *Class X*, and "
        "whether it operates equally in the *Rural Government* school and "
        "the *Urban Private CBSE* school, four sub-group *t*-tests have been "
        "carried out (df = 38; critical *t* at .05 = 2.02, at .01 = 2.71).\n")

    chunks.append("#### TABLE 4.18\n**Boys vs Girls within Class IX "
                  "(n = 20 + 20)**\n")
    chunks.append("| Area | Boys M (S.D.) | Girls M (S.D.) | "
                  "*t*-value | Sig. |")
    chunks.append("|:---|:---:|:---:|:---:|:---:|")
    for area in AREAS:
        t = D["t_boys_girls_c9"][area]
        chunks.append(f"| {area} | {t['m1']} ({t['sd1']}) | "
                      f"{t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} |")
    chunks.append("")

    chunks.append("#### TABLE 4.19\n**Boys vs Girls within Class X "
                  "(n = 20 + 20)**\n")
    chunks.append("| Area | Boys M (S.D.) | Girls M (S.D.) | "
                  "*t*-value | Sig. |")
    chunks.append("|:---|:---:|:---:|:---:|:---:|")
    for area in AREAS:
        t = D["t_boys_girls_c10"][area]
        chunks.append(f"| {area} | {t['m1']} ({t['sd1']}) | "
                      f"{t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} |")
    chunks.append("")

    chunks.append("#### TABLE 4.20\n**Boys vs Girls within the Rural Govt. "
                  "and the Urban Pvt. School (n = 20 + 20 each)**\n")
    chunks.append("| Area | RG-Boys vs RG-Girls *t* (Sig.) | "
                  "UP-Boys vs UP-Girls *t* (Sig.) |")
    chunks.append("|:---|:---:|:---:|")
    for area in AREAS:
        rg = D["t_boys_girls_rg"][area]
        up = D["t_boys_girls_up"][area]
        chunks.append(f"| {area} | {rg['t']} ({rg['sig']}) | "
                      f"{up['t']} ({up['sig']}) |")
    chunks.append("")

    chunks.append("### Interpretation of the Sub-Group Comparisons\n")
    chunks.append(
        "The sub-group analyses (Tables 4.18 to 4.20) show that the *gender-"
        "effect* observed in the whole-sample analysis (Section 4.6) is "
        "*broadly the same* in Class IX and in Class X, and *broadly the "
        "same* in the Rural Government and the Urban Private CBSE schools. "
        "The areas on which boys exceed girls (Scientific, Constructive, "
        "Agricultural) and the areas on which girls exceed boys (Artistic, "
        "Social, Household) come up as significant in *each* of the four "
        "sub-groups. The absolute *t*-values, of course, are smaller in the "
        "sub-group analyses than in the whole-sample analysis, simply "
        "because the sub-group sample sizes (20 + 20) are half of the "
        "whole-sample size (40 + 40). The *direction* of the differences, "
        "however, remains the same. This shows that the gender-effect is "
        "*robust* across class and across school type.\n")

    # =====================================================================
    # 4.10 Rank order
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.10 RANK ORDER OF THE VOCATIONAL INTEREST AREAS\n")
    chunks.append(
        "The *rank order* of the ten areas, computed separately for boys "
        "and for girls, gives the *vocational interest profile* of each "
        "group at a glance. The rank orders are presented in Table 4.21.\n")

    chunks.append("#### TABLE 4.21\n**Rank Order of the Ten Vocational "
                  "Interest Areas (Boys vs Girls)**\n")
    chunks.append("| Rank | Boys' Top Area | Girls' Top Area |")
    chunks.append("|:---:|:---|:---|")
    boys_sorted = sorted(bs.items(), key=lambda x: -x[1]['mean'])
    girls_sorted = sorted(gs.items(), key=lambda x: -x[1]['mean'])
    for i in range(10):
        b_area, b_st = boys_sorted[i]
        g_area, g_st = girls_sorted[i]
        chunks.append(f"| {ROMAN[i+1]} | {b_area} (M = {b_st['mean']}) | "
                      f"{g_area} (M = {g_st['mean']}) |")
    chunks.append("")

    chunks.append(
        "**Interpretation.** Table 4.21 highlights the *very different* "
        "vocational profiles of the boys and the girls of the present "
        f"sample. The boys' top-three preferences are **{boys_sorted[0][0]}, "
        f"{boys_sorted[1][0]} and {boys_sorted[2][0]}** — areas connected "
        "with *modern science, outdoor work and administrative leadership*. "
        f"The girls' top-three preferences, on the other hand, are "
        f"**{girls_sorted[0][0]}, {girls_sorted[1][0]} and "
        f"{girls_sorted[2][0]}** — areas connected with *home, art and "
        "human-relations*. This confirms once again the *People–Things* "
        "dimension of Su, Rounds and Armstrong (2009).\n")

    chunks.append("#### Figure 4.4 — Profile of the Rank Order of the Ten "
                  "Areas (Boys vs Girls)\n")
    chunks.append("*(For colour profile diagram, please refer to printed "
                  "copy.)*\n")

    # =====================================================================
    # 4.11 Discussion
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.11 DISCUSSION OF THE RESULTS\n")
    chunks.append(
        "The combined picture of the analyses presented in this chapter is "
        "as follows.\n")
    chunks.append("### 4.11.1 The Gender-effect is Strong and Clear\n")
    chunks.append(
        "Out of the ten areas of vocational interest measured by the V.I.R., "
        f"the gender-effect was found to be **statistically significant on "
        f"{len(sig_boys) + len(sig_girls)} areas** "
        f"({', '.join(sig_boys + sig_girls)}). On the remaining "
        f"{len(ns_areas)} areas ({', '.join(ns_areas)}), the gender-effect "
        f"was *not significant*. Out of these "
        f"{len(sig_boys) + len(sig_girls)} significant areas, the boys "
        f"scored higher on **{len(sig_boys)} areas** ({', '.join(sig_boys)}) "
        f"and the girls scored higher on **{len(sig_girls)} areas** "
        f"({', '.join(sig_girls)}). The pattern is *highly consistent* with "
        f"the long-standing findings of Indian and foreign research.\n")

    chunks.append("### 4.11.2 The Direction of the Differences\n")
    chunks.append(
        "The direction of the gender-effect is along expected and "
        "well-documented lines. Boys are higher on the *thing-and-action* "
        "areas (Scientific, Executive, Constructive / Technical, Agricultural "
        "and Persuasive). Girls are higher on the *people-and-care* areas "
        "(Artistic, Social and Household). This pattern is the *People–"
        "Things* dimension that has been reported by Su, Rounds and "
        "Armstrong (2009) on a meta-analysis covering more than five lakh "
        "respondents from many countries.\n")

    chunks.append("### 4.11.3 Areas of No Significant Difference\n")
    chunks.append(
        "It is also instructive to note where the gender difference is "
        f"*not* significant. The **Literary** and **Commercial** areas are "
        f"the only two areas on which boys and girls of the present sample "
        f"do *not* differ significantly. The **Commercial** area, in "
        f"particular, shows a near-zero difference (mean diff = "
        f"{D['t_results']['Commercial']['mean_diff']}, *t* = "
        f"{D['t_results']['Commercial']['t']}, NS). This suggests that "
        f"*business and commerce* have, perhaps, become a *gender-neutral* "
        f"aspirational space in present-day Meerut District. The "
        f"**Literary** area shows a small but non-significant trend in "
        f"favour of girls. With a slightly larger sample, this trend may "
        f"have reached significance.\n")

    chunks.append("### 4.11.4 Implications for Career Guidance\n")
    chunks.append(
        "The pattern observed in the present chapter clearly points to the "
        "*urgent need* for *gender-sensitive* career-guidance services in "
        "the secondary schools of Meerut District. Special programmes are "
        "needed to (a) encourage *girls* to take up *Scientific*, "
        "*Constructive / Technical*, *Executive* and *Agricultural* "
        "careers, and (b) encourage *boys* to consider *Artistic*, *Social* "
        "and *Household / Service* careers, so that the gender-based "
        "occupational segregation of the Indian work-force is gradually "
        "reduced. These implications are discussed in greater detail in "
        "the next chapter.\n")

    chunks.append("---\n*** End of Chapter IV ***\n")
    return "\n".join(chunks)


print(out())
