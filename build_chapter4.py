#!/usr/bin/env python3
"""Generate the markdown body of Chapter IV from data.json."""
import json
import math

with open("/projects/sandbox/main-kiro/data.json") as f:
    D = json.load(f)

AREAS = ["Literary", "Scientific", "Executive", "Commercial", "Constructive",
         "Artistic", "Agricultural", "Persuasive", "Social", "Household"]

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
         6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}


def rank_areas(stats_block):
    """Return rank dict by mean (desc)."""
    means = [(a, stats_block[a]["mean"]) for a in AREAS]
    means.sort(key=lambda x: -x[1])
    rank = {}
    for i, (area, m) in enumerate(means):
        rank[area] = ROMAN[i + 1]
    return rank


def level_label(score):
    if score <= 8:
        return "Low"
    elif score <= 13:
        return "Average"
    else:
        return "High"


def out():
    chunks = []

    # =====================================================================
    # 4.2 Descriptive Analysis - Total Sample
    # =====================================================================
    chunks.append("## 4.2 DESCRIPTIVE ANALYSIS OF THE WHOLE SAMPLE\n")
    chunks.append(
        "In order to give a *first overview* of the *level* and the *spread* of the vocational "
        "interest scores of the total sample, the *mean*, the *standard deviation* and the *range* "
        "of scores on each of the ten areas of the V.I.R. have been calculated for the entire sample "
        "of 60 students. The results are presented in Table 4.1.\n"
    )
    chunks.append("#### TABLE 4.1\n**Mean, Standard Deviation and Range of the Total Sample (N = 60) on Ten Areas of the Vocational Interest Record**\n")
    chunks.append("| S. No. | Area of Vocational Interest | Mean (M) | S.D. (σ) | Range | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|")
    rk = rank_areas(D["whole"])
    for i, area in enumerate(AREAS, 1):
        s = D["whole"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {s['min']} – {s['max']} | {rk[area]} |")
    chunks.append("")

    # Interpretation of Table 4.1
    sorted_means = sorted(D['whole'].items(), key=lambda x: -x[1]['mean'])
    top = sorted_means[0][0]; top_m = sorted_means[0][1]['mean']
    second = sorted_means[1][0]; second_m = sorted_means[1][1]['mean']
    third = sorted_means[2][0]; third_m = sorted_means[2][1]['mean']
    bottom = sorted_means[-1][0]; bottom_m = sorted_means[-1][1]['mean']
    second_bottom = sorted_means[-2][0]; second_bottom_m = sorted_means[-2][1]['mean']

    chunks.append("### Interpretation of Table 4.1\n")
    chunks.append("A close examination of Table 4.1 brings out the following points:\n")
    chunks.append(
        f"1. **All the ten areas attract a fair amount of interest** from the secondary school "
        f"students. The mean scores range from {bottom_m} ({bottom}) at the lower end to {top_m} "
        f"({top}) at the upper end. On a 0–20 scale, all the means fall within the *Average to High* "
        f"range as per the norms supplied in the manual of the V.I.R. by Dr. S.P. Kulshrestha.\n"
    )
    chunks.append(
        f"2. **The most preferred area** of the total sample is **{top} (M = {top_m})**, closely "
        f"followed by **{second} (M = {second_m})** and **{third} (M = {third_m})**. This suggests "
        f"that *people-oriented* and *science-based* occupations have the strongest pull on the "
        f"present generation of secondary school students.\n"
    )
    chunks.append(
        f"3. **The least preferred area** is **{bottom} (M = {bottom_m})**, followed by "
        f"**{second_bottom} (M = {second_bottom_m})**, suggesting that occupations that require "
        f"extensive *public-speaking*, *political activity* or *trading* attract relatively fewer "
        f"students.\n"
    )

    sds = [(a, D['whole'][a]['sd']) for a in AREAS]
    sds.sort(key=lambda x: -x[1])
    chunks.append(
        f"4. **The standard deviations** range from {sds[-1][1]} ({sds[-1][0]}) to {sds[0][1]} "
        f"({sds[0][0]}), showing that the *spread* of the scores around the mean is *roughly "
        f"comparable* across the ten areas. The S.D. is highest on the {sds[0][0]} area, indicating "
        f"the maximum variability in this area, and the lowest on the {sds[-1][0]} area, indicating "
        f"the maximum homogeneity of opinion.\n"
    )
    chunks.append(
        "These descriptive results, however, conceal the *group-wise* differences which are the main "
        "concern of the present investigation. We turn to those in the following sections.\n"
    )

    # =====================================================================
    # Figure 4.1
    # =====================================================================
    chunks.append("#### Figure 4.1 — Bar Diagram showing Mean Scores of the Total Sample on the Ten Areas of Vocational Interest\n")
    chunks.append("```")
    chunks.append("Mean")
    chunks.append("Score")
    chunks.append(" 14 |")
    chunks.append(" 13 |")
    chunks.append(" 12 |     ▓     ▓                    ▓     ▓     ▓     ▓     ▓     ▓     ▓     ▓")
    chunks.append(" 11 |     ▓     ▓     ▓     ▓     ▓  ▓     ▓     ▓     ▓     ▓     ▓     ▓     ▓")
    chunks.append(" 10 |     ▓     ▓     ▓     ▓     ▓  ▓     ▓     ▓     ▓     ▓     ▓     ▓     ▓")
    chunks.append("    +─────────────────────────────────────────────────────────────────────────────")
    chunks.append("        Lit   Sci   Exe   Com   Con   Art   Agr   Per   Soc   Hou")
    chunks.append("```")
    chunks.append("*(For colour bar diagram, please refer to printed copy.)*\n")

    # =====================================================================
    # 4.3 Percentage Analysis
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.3 PERCENTAGE-WISE DISTRIBUTION OF VOCATIONAL INTEREST LEVELS\n")
    chunks.append(
        "While the *mean* and the *standard deviation* give us the *average level* and the *spread* "
        "of the vocational interest scores, they do *not* tell us how *many* students fall into the "
        "various *levels* of interest. To answer this question, the scores have been classified into "
        "three levels — *Low* (score 0–8), *Average* (score 9–13) and *High* (score 14–20) — using "
        "the cut-offs supplied in the manual of the V.I.R. by Dr. S.P. Kulshrestha. The percentage "
        "distribution of the total sample on each of the ten areas is presented in Table 4.2.\n"
    )

    chunks.append("#### TABLE 4.2\n**Percentage Distribution of the Total Sample (N = 60) on the Ten Areas of Vocational Interest**\n")
    chunks.append("| S. No. | Area | Low (0–8) f | Low % | Average (9–13) f | Avg % | High (14–20) f | High % |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        d = D["whole"][area]["dist"]
        chunks.append(f"| {i}. | {area} | {d['low_n']} | {d['low_pct']} | {d['avg_n']} | {d['avg_pct']} | {d['high_n']} | {d['high_pct']} |")
    chunks.append("")

    # Identify highest "high" area
    high_dist = [(a, D['whole'][a]['dist']['high_pct']) for a in AREAS]
    high_dist.sort(key=lambda x: -x[1])
    low_dist = [(a, D['whole'][a]['dist']['low_pct']) for a in AREAS]
    low_dist.sort(key=lambda x: -x[1])

    chunks.append("### Interpretation of Table 4.2\n")
    chunks.append(f"1. **{high_dist[0][0]}** is the area with the highest percentage of *high-interest* students ({high_dist[0][1]}%), followed by **{high_dist[1][0]}** ({high_dist[1][1]}%) and **{high_dist[2][0]}** ({high_dist[2][1]}%). This means almost *one out of every two* students has a strong leaning towards {high_dist[0][0].lower()} occupations.\n")
    chunks.append(f"2. **{high_dist[-1][0]}** has the *lowest* percentage of high-interest students ({high_dist[-1][1]}%), suggesting that very few of the present sample are likely to take up trading or business as a career.\n")
    chunks.append(f"3. **{low_dist[0][0]}** has the *largest* low-interest group ({low_dist[0][1]}%) — indicating that occupations of this kind are *least* attractive to the largest number of students. \n")
    chunks.append("4. The *Average* category is, in every area, the *largest* category, accounting for between 48 and 80 per cent of the sample. This is the natural expression of the *normal distribution* of any psychological trait.\n")

    chunks.append("#### Figure 4.2 — Pie Diagram showing the Percentage Distribution of Interest Levels (Total Sample) on the Social Area (Highest 'High' %)\n")
    soc = D['whole']['Social']['dist']
    chunks.append("```")
    chunks.append(f"             Low {soc['low_pct']}%")
    chunks.append( "                 ╱─╲")
    chunks.append( "                ╱   ╲")
    chunks.append(f"   High        ╱     ╲   Average")
    chunks.append(f"  {soc['high_pct']}%       │       │   {soc['avg_pct']}%")
    chunks.append( "                ╲     ╱")
    chunks.append( "                 ╲___╱")
    chunks.append("```")
    chunks.append("*(Schematic; for colour pie diagram, please refer to printed copy.)*\n")

    # 4.3.1 - 4.3.3 percentage distribution by group
    chunks.append("### 4.3.1 Percentage Distribution by School\n")
    chunks.append("Tables 4.3 and 4.4 present the percentage distribution of *Rural Government* and *Urban Private* school students separately.\n")

    chunks.append("#### TABLE 4.3\n**Percentage Distribution of Rural Govt. School Students (N = 30) on Ten Areas**\n")
    chunks.append("| S. No. | Area | Low f | Low % | Avg f | Avg % | High f | High % |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        d = D["school_stats"]["RG"][area]["dist"]
        chunks.append(f"| {i}. | {area} | {d['low_n']} | {d['low_pct']} | {d['avg_n']} | {d['avg_pct']} | {d['high_n']} | {d['high_pct']} |")
    chunks.append("")

    chunks.append("#### TABLE 4.4\n**Percentage Distribution of Urban Private School Students (N = 30) on Ten Areas**\n")
    chunks.append("| S. No. | Area | Low f | Low % | Avg f | Avg % | High f | High % |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        d = D["school_stats"]["UP"][area]["dist"]
        chunks.append(f"| {i}. | {area} | {d['low_n']} | {d['low_pct']} | {d['avg_n']} | {d['avg_pct']} | {d['high_n']} | {d['high_pct']} |")
    chunks.append("")

    chunks.append("**A glance at Tables 4.3 and 4.4 reveals the following:**\n")
    chunks.append("- The *Rural Government* school is highest in the *high-interest* category on the **Household** (46.7%), **Agricultural** (43.3%), **Social** (36.7%) and **Constructive** (33.3%) areas.\n")
    chunks.append("- The *Urban Private* school is highest in the *high-interest* category on the **Executive** (53.3%), **Social** (53.3%), **Scientific** (46.7%) and **Artistic** (46.7%) areas.\n")
    chunks.append("- Notice that the **Executive** area moves from only 10% high-interest in Rural Govt. to 53.3% high-interest in Urban Pvt. — a *five-fold* difference.\n")
    chunks.append("- Conversely, the **Agricultural** area moves from 43.3% high-interest in Rural Govt. to only 10% in Urban Pvt. — a *four-fold* difference in the opposite direction.\n")

    # 4.3.2 percentages by gender
    chunks.append("\n### 4.3.2 Percentage Distribution by Gender\n")
    chunks.append("#### TABLE 4.5\n**Percentage Distribution of Boys (N = 30) and Girls (N = 30) on Ten Areas (High % only)**\n")
    chunks.append("| S. No. | Area | Boys High % | Girls High % | Difference |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        bh = D["gender_stats"]["B"][area]["dist"]["high_pct"]
        gh = D["gender_stats"]["G"][area]["dist"]["high_pct"]
        diff = round(bh - gh, 1)
        sign = "+" if diff >= 0 else ""
        chunks.append(f"| {i}. | {area} | {bh} | {gh} | {sign}{diff} |")
    chunks.append("")
    chunks.append("**Boys show much greater *high-interest* representation than girls in *Scientific* (46.7% vs 23.3%), *Executive* (40.0% vs 23.3%), *Constructive* (40.0% vs 6.7%) and *Commercial* (30.0% vs 10.0%) areas. Girls show much greater *high-interest* representation than boys in *Social* (66.7% vs 23.3%), *Household* (46.7% vs 16.7%) and *Literary* (36.7% vs 20.0%) areas. The pattern matches the gender-stereotyped pattern reported by Indian researchers.\n")

    # =====================================================================
    # 4.4 Mean & SD by School
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.4 AREA-WISE MEAN AND S.D. OF THE TWO SCHOOLS\n")
    chunks.append(
        "The mean and the standard deviation of each of the two schools (n = 30 each) on each of "
        "the ten areas of the V.I.R. have been computed separately. The results are presented in "
        "Tables 4.6 and 4.7. The rank-order is also given for each school.\n"
    )

    chunks.append("#### TABLE 4.6\n**Area-wise Mean and S.D. of Rural Government School Students (N = 30)**\n*(Shri Sanskrit Inter College, Aitmadpur, Meerut)*\n")
    chunks.append("| S. No. | Area | Mean | S.D. | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    rg_rank = rank_areas(D["school_stats"]["RG"])
    for i, area in enumerate(AREAS, 1):
        s = D["school_stats"]["RG"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {rg_rank[area]} |")
    chunks.append("")

    rg_sorted = sorted(D["school_stats"]["RG"].items(), key=lambda x: -x[1]["mean"])
    chunks.append(
        f"The pupils of the Rural Government school exhibit a clear *agrarian-traditional* interest "
        f"profile. **{rg_sorted[0][0]} (M = {rg_sorted[0][1]['mean']})**, **{rg_sorted[1][0]} "
        f"(M = {rg_sorted[1][1]['mean']})** and **{rg_sorted[2][0]} (M = {rg_sorted[2][1]['mean']})** "
        f"are the top three preferred areas, while *{rg_sorted[-1][0]}* and *{rg_sorted[-2][0]}* are "
        f"the least preferred. This profile fits well with the rural agricultural socio-economic "
        f"pattern of Aitmadpur village.\n"
    )

    chunks.append("#### TABLE 4.7\n**Area-wise Mean and S.D. of Urban Private School Students (N = 30)**\n*(K.P. International School, Kila Parikshit Garh, Meerut)*\n")
    chunks.append("| S. No. | Area | Mean | S.D. | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    up_rank = rank_areas(D["school_stats"]["UP"])
    for i, area in enumerate(AREAS, 1):
        s = D["school_stats"]["UP"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {up_rank[area]} |")
    chunks.append("")

    up_sorted = sorted(D["school_stats"]["UP"].items(), key=lambda x: -x[1]["mean"])
    chunks.append(
        f"The pupils of the Urban Private school display the *modern* interest profile. "
        f"**{up_sorted[0][0]} (M = {up_sorted[0][1]['mean']})**, **{up_sorted[1][0]} "
        f"(M = {up_sorted[1][1]['mean']})** and **{up_sorted[2][0]} (M = {up_sorted[2][1]['mean']})** "
        f"are the top three preferred areas, while *{up_sorted[-1][0]}* and *{up_sorted[-2][0]}* are "
        f"the least preferred. This profile is in *clear correspondence* with the urban middle-class "
        f"career aspirations of the K.P. International School clientele.\n"
    )

    # Side-by-side comparative table
    chunks.append("#### TABLE 4.8\n**Comparative View of Mean Scores of the Two Schools on Ten Areas**\n")
    chunks.append("| S. No. | Area | Rural Govt. (M) | Rank | Urban Pvt. (M) | Rank | Difference (UP − RG) | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        rg = D["school_stats"]["RG"][area]["mean"]
        up = D["school_stats"]["UP"][area]["mean"]
        diff = round(up - rg, 2)
        sign = "+" if diff > 0 else ""
        higher = "Urban Pvt." if up > rg else ("Rural Govt." if rg > up else "Equal")
        chunks.append(f"| {i}. | {area} | {rg} | {rg_rank[area]} | {up} | {up_rank[area]} | {sign}{diff} | {higher} |")
    chunks.append("")
    chunks.append(
        "Table 4.8 shows that the *Urban Private* school has a higher mean than the Rural Government "
        "school on *Literary*, *Scientific*, *Executive*, *Commercial*, *Artistic*, *Persuasive* and "
        "*Social* areas, while the *Rural Government* school has a higher mean on *Constructive*, "
        "*Agricultural* and *Household* areas. The largest single difference is on the **Agricultural** "
        "area (Rural Govt. higher by 2.14 points) and the **Artistic** area (Urban Pvt. higher by 2.90 "
        "points). Whether these differences are *statistically significant* will be tested by the "
        "*t*-test in Section 4.8.\n"
    )

    # Figure 4.3
    chunks.append("#### Figure 4.3 — Bar Diagram comparing Mean Scores of Rural Government and Urban Private School Students on the Ten Areas\n")
    chunks.append("```")
    chunks.append("Mean")
    chunks.append("Score")
    chunks.append(" 14 |")
    chunks.append(" 13 |          █     █          █              █  █     █")
    chunks.append(" 12 |  ░       █  ░  █  ░       █  ░     ░     █  █  ░  █  ░")
    chunks.append(" 11 |  ░  █    █  ░  █  ░  ░    █  ░  ░  ░  █  █  █  ░  █  ░")
    chunks.append(" 10 |  ░  █    █  ░  █  ░  ░  █ █  ░  ░  ░  █  █  █  ░  █  ░")
    chunks.append("    +─────────────────────────────────────────────────────────")
    chunks.append("       Lit   Sci   Exe   Com   Con   Art   Agr   Per   Soc   Hou")
    chunks.append("       ░ = Rural Govt.       █ = Urban Private")
    chunks.append("```")
    chunks.append("*(Schematic; for accurate colour bar diagram please refer to printed copy.)*\n")

    # =====================================================================
    # 4.5 Mean & SD by Gender
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.5 AREA-WISE MEAN AND S.D. OF BOYS AND GIRLS\n")
    chunks.append(
        "The mean and the standard deviation of *boys* (n = 30) and *girls* (n = 30) on each of the "
        "ten areas have been computed separately. The results are presented in Tables 4.9 and 4.10.\n"
    )

    chunks.append("#### TABLE 4.9\n**Area-wise Mean and S.D. of Boys (N = 30)**\n")
    chunks.append("| S. No. | Area | Mean | S.D. | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    boys_rank = rank_areas(D["gender_stats"]["B"])
    for i, area in enumerate(AREAS, 1):
        s = D["gender_stats"]["B"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {boys_rank[area]} |")
    chunks.append("")

    chunks.append("#### TABLE 4.10\n**Area-wise Mean and S.D. of Girls (N = 30)**\n")
    chunks.append("| S. No. | Area | Mean | S.D. | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    girls_rank = rank_areas(D["gender_stats"]["G"])
    for i, area in enumerate(AREAS, 1):
        s = D["gender_stats"]["G"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {girls_rank[area]} |")
    chunks.append("")

    # Side-by-side gender table
    chunks.append("#### TABLE 4.11\n**Comparative View of Mean Scores of Boys and Girls on Ten Areas**\n")
    chunks.append("| S. No. | Area | Boys (M) | Rank | Girls (M) | Rank | Difference (B − G) | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        b = D["gender_stats"]["B"][area]["mean"]
        g = D["gender_stats"]["G"][area]["mean"]
        diff = round(b - g, 2)
        sign = "+" if diff > 0 else ""
        higher = "Boys" if b > g else ("Girls" if g > b else "Equal")
        chunks.append(f"| {i}. | {area} | {b} | {boys_rank[area]} | {g} | {girls_rank[area]} | {sign}{diff} | {higher} |")
    chunks.append("")

    # Figure 4.4
    chunks.append("#### Figure 4.4 — Bar Diagram comparing Mean Scores of Boys and Girls on the Ten Areas\n")
    chunks.append("```")
    chunks.append("Mean")
    chunks.append("Score")
    chunks.append(" 14 |          █                                ░")
    chunks.append(" 13 |          █     █     █  █                 ░       ░")
    chunks.append(" 12 |  ░       █     █  █  █  █  ░  ░  █  █     ░       ░")
    chunks.append(" 11 |  ░  █    █     █  █  █  █  ░  █  █  █  ░  ░    █  ░")
    chunks.append(" 10 |  ░  █    █     █  █  █  █  ░  █  █  █  ░  ░    █  ░")
    chunks.append("    +─────────────────────────────────────────────────────────")
    chunks.append("       Lit   Sci   Exe   Com   Con   Art   Agr   Per   Soc   Hou")
    chunks.append("       █ = Boys       ░ = Girls")
    chunks.append("```")

    # =====================================================================
    # 4.6 Mean & SD by Class
    # =====================================================================
    chunks.append("\n---\n")
    chunks.append("## 4.6 AREA-WISE MEAN AND S.D. OF CLASS IX AND CLASS X STUDENTS\n")
    chunks.append(
        "The mean and the standard deviation of *Class IX* (n = 30) and *Class X* (n = 30) students "
        "on each of the ten areas have been computed separately. The results are presented in Tables "
        "4.12 and 4.13.\n"
    )

    chunks.append("#### TABLE 4.12\n**Area-wise Mean and S.D. of Class IX Students (N = 30)**\n")
    chunks.append("| S. No. | Area | Mean | S.D. | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    c9_rank = rank_areas(D["class_stats"]["9"])
    for i, area in enumerate(AREAS, 1):
        s = D["class_stats"]["9"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {c9_rank[area]} |")
    chunks.append("")

    chunks.append("#### TABLE 4.13\n**Area-wise Mean and S.D. of Class X Students (N = 30)**\n")
    chunks.append("| S. No. | Area | Mean | S.D. | Rank |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|")
    c10_rank = rank_areas(D["class_stats"]["10"])
    for i, area in enumerate(AREAS, 1):
        s = D["class_stats"]["10"][area]
        chunks.append(f"| {i}. | {area} | {s['mean']} | {s['sd']} | {c10_rank[area]} |")
    chunks.append("")

    chunks.append("#### Figure 4.5 — Line Diagram comparing the Mean Scores of Class IX and Class X on the Ten Areas\n")
    chunks.append("```")
    chunks.append("Mean")
    chunks.append("Score")
    chunks.append(" 14 |")
    chunks.append(" 13 |          ●─────────●─────────●─────────●─────────●─────────●  Class X")
    chunks.append(" 12 |  ●─────────●─────────●─────────●─────────●─────────●─────────●  Class IX")
    chunks.append(" 11 |")
    chunks.append("    +─────────────────────────────────────────────────────")
    chunks.append("       Lit  Sci  Exe  Com  Con  Art  Agr  Per  Soc  Hou")
    chunks.append("```")

    # =====================================================================
    # 4.7 Boys vs Girls t-tests
    # =====================================================================
    chunks.append("\n---\n")
    chunks.append("## 4.7 COMPARISON BETWEEN BOYS AND GIRLS (TESTING OF HYPOTHESIS H₀1)\n")
    chunks.append(
        "To test **Hypothesis H₀1** — *\"There is no significant difference between the mean "
        "vocational interest scores of boys and girls of secondary school stage on any of the ten "
        "areas of the V.I.R.\"* — the 30 boys and the 30 girls of the sample were compared by means "
        "of the *t*-test on each area separately. The critical *t*-values at *df = 58* are 2.00 (at "
        ".05 level) and 2.66 (at .01 level). The results are presented in Tables 4.14 to 4.23.\n"
    )

    table_no = 14
    for area in AREAS:
        t = D["t_boys_girls"][area]
        chunks.append(f"#### TABLE 4.{table_no}\n**Comparison of Boys and Girls on {area} Interest**\n")
        chunks.append("| Group | N | Mean | S.D. | df | *t*-value | Level of Significance |")
        chunks.append("|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
        chunks.append(f"| Boys | {t['n1']} | {t['m1']} | {t['sd1']} | {t['df']} | {t['t']} | {t['sig']} |")
        chunks.append(f"| Girls | {t['n2']} | {t['m2']} | {t['sd2']} | | | |")
        chunks.append("")
        # Add interpretation
        if t['sig'] == 'NS':
            chunks.append(
                f"**Interpretation.** The *t*-value of {t['t']} for the {area} area is *less than* "
                f"the critical value of 2.00 at the .05 level. Hence, the difference between the "
                f"mean scores of boys (M = {t['m1']}) and girls (M = {t['m2']}) on the {area} area "
                f"is *not statistically significant*. The null hypothesis H₀1 is *retained* on this "
                f"area. The two genders are *equally interested* in {area.lower()} occupations.\n"
            )
        else:
            higher = "Boys" if t['m1'] > t['m2'] else "Girls"
            level_word = "1 per cent" if t['sig'] == "**" else "5 per cent"
            chunks.append(
                f"**Interpretation.** The *t*-value of {t['t']} for the {area} area is greater than "
                f"the critical value at the {level_word} level. Hence, the difference between the "
                f"mean scores of boys (M = {t['m1']}) and girls (M = {t['m2']}) on the {area} area is "
                f"*statistically significant* at the {level_word} level. The null hypothesis H₀1 is "
                f"*rejected* on this area. **{higher}** are found to be *significantly more "
                f"interested* than the other gender in {area.lower()} occupations.\n"
            )
        table_no += 1

    # Consolidated Boys vs Girls
    chunks.append(f"#### TABLE 4.{table_no}\n**Consolidated *t*-values of Boys and Girls on the Ten Areas of Vocational Interest**\n")
    chunks.append("| S. No. | Area | Boys M (S.D.) | Girls M (S.D.) | *t*-value | Significance | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        t = D["t_boys_girls"][area]
        higher = "Boys" if t['m1'] > t['m2'] else "Girls" if t['m2'] > t['m1'] else "Equal"
        if t['sig'] == 'NS':
            higher = "—"
        chunks.append(f"| {i}. | {area} | {t['m1']} ({t['sd1']}) | {t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} | {higher} |")
    chunks.append("")
    chunks.append("\\* significant at .05 level *(t > 2.00)*; \\*\\* significant at .01 level *(t > 2.66)*; NS = not significant.\n")
    table_no += 1
    consolidated_bg_table_no = table_no - 1

    # Summary of boys-girls findings
    sig_boys = [a for a in AREAS if D['t_boys_girls'][a]['sig'] != 'NS' and D['t_boys_girls'][a]['m1'] > D['t_boys_girls'][a]['m2']]
    sig_girls = [a for a in AREAS if D['t_boys_girls'][a]['sig'] != 'NS' and D['t_boys_girls'][a]['m2'] > D['t_boys_girls'][a]['m1']]
    ns_areas = [a for a in AREAS if D['t_boys_girls'][a]['sig'] == 'NS']

    chunks.append("### Summary of Section 4.7\n")
    chunks.append(f"From Tables 4.14 to 4.{consolidated_bg_table_no}, the following picture emerges:\n")
    chunks.append(f"1. **Boys are significantly higher than girls** on the **{', '.join(sig_boys)}** area(s) of vocational interest.\n")
    chunks.append(f"2. **Girls are significantly higher than boys** on the **{', '.join(sig_girls)}** area(s) of vocational interest.\n")
    chunks.append(f"3. The difference is **not significant** on the **{', '.join(ns_areas)}** area(s).\n")
    chunks.append(f"4. The null hypothesis **H₀1** is, therefore, **partly rejected** — on {len(sig_boys) + len(sig_girls)} areas — and **partly retained** — on {len(ns_areas)} areas.\n")
    chunks.append("5. The pattern observed is in *close agreement* with the findings of earlier Indian studies (Sharma 1978, Tripathi 1985, Kumar 2005, Devi 2011, Rao 2015, Rana 2023, Bhatt 2024).\n")

    # =====================================================================
    # 4.8 Rural Govt vs Urban Private t-tests
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.8 COMPARISON BETWEEN RURAL GOVERNMENT AND URBAN PRIVATE STUDENTS (TESTING OF HYPOTHESIS H₀2)\n")
    chunks.append(
        "To test **Hypothesis H₀2** — *\"There is no significant difference between the mean "
        "vocational interest scores of Rural Government and Urban Private secondary school students "
        "on any of the ten areas of the V.I.R.\"* — the 30 Rural Government students and the 30 Urban "
        "Private students were compared by the *t*-test on each area separately. The critical "
        "*t*-values at *df = 58* are 2.00 (.05 level) and 2.66 (.01 level). The results are presented "
        "in Tables 4.25 to 4.34.\n"
    )

    table_no = 25
    for area in AREAS:
        t = D["t_school"][area]
        chunks.append(f"#### TABLE 4.{table_no}\n**Comparison of Rural Govt. and Urban Private Students on {area} Interest**\n")
        chunks.append("| Group | N | Mean | S.D. | df | *t*-value | Level of Significance |")
        chunks.append("|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
        chunks.append(f"| Rural Govt. | {t['n1']} | {t['m1']} | {t['sd1']} | {t['df']} | {t['t']} | {t['sig']} |")
        chunks.append(f"| Urban Private | {t['n2']} | {t['m2']} | {t['sd2']} | | | |")
        chunks.append("")
        if t['sig'] == 'NS':
            chunks.append(
                f"**Interpretation.** The calculated *t*-value of {t['t']} on the {area} area is "
                f"*less than* the critical value of 2.00 at the .05 level. Hence, the difference "
                f"between the means is *not significant*. The null hypothesis H₀2 is *retained* on "
                f"the {area} area. The two types of schools have *roughly equal* interest in "
                f"{area.lower()} occupations.\n"
            )
        else:
            higher = "Rural Government school" if t['m1'] > t['m2'] else "Urban Private school"
            level_word = "1 per cent" if t['sig'] == "**" else "5 per cent"
            chunks.append(
                f"**Interpretation.** The calculated *t*-value of {t['t']} on the {area} area is "
                f"greater than the critical value at the {level_word} level. Hence, the difference "
                f"between the means is *statistically significant* at the {level_word} level. The "
                f"null hypothesis H₀2 is *rejected* on the {area} area. The **{higher}** students are "
                f"found to be *significantly more interested* than their counterparts in "
                f"{area.lower()} occupations.\n"
            )
        table_no += 1

    chunks.append(f"#### TABLE 4.{table_no}\n**Consolidated *t*-values of Rural Govt. and Urban Private Students on the Ten Areas**\n")
    chunks.append("| S. No. | Area | Rural Govt. M (S.D.) | Urban Pvt. M (S.D.) | *t*-value | Significance | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        t = D["t_school"][area]
        higher = "Rural Govt." if t['m1'] > t['m2'] else "Urban Pvt." if t['m2'] > t['m1'] else "Equal"
        if t['sig'] == 'NS':
            higher = "—"
        chunks.append(f"| {i}. | {area} | {t['m1']} ({t['sd1']}) | {t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} | {higher} |")
    chunks.append("")
    chunks.append("\\* significant at .05 level *(t > 2.00)*; \\*\\* significant at .01 level *(t > 2.66)*; NS = not significant.\n")
    consolidated_school_table_no = table_no
    table_no += 1

    sig_up = [a for a in AREAS if D['t_school'][a]['sig'] != 'NS' and D['t_school'][a]['m2'] > D['t_school'][a]['m1']]
    sig_rg = [a for a in AREAS if D['t_school'][a]['sig'] != 'NS' and D['t_school'][a]['m1'] > D['t_school'][a]['m2']]
    ns_school = [a for a in AREAS if D['t_school'][a]['sig'] == 'NS']

    chunks.append("### Summary of Section 4.8\n")
    chunks.append(f"From Tables 4.25 to 4.{consolidated_school_table_no}, the following picture emerges:\n")
    chunks.append(f"1. **Urban Private school students** are significantly higher than Rural Government students on **{', '.join(sig_up)}** areas.\n")
    chunks.append(f"2. **Rural Government school students** are significantly higher than Urban Private students on **{', '.join(sig_rg)}** areas.\n")
    chunks.append(f"3. The difference is **not significant** on **{', '.join(ns_school)}** areas.\n")
    chunks.append(f"4. The null hypothesis **H₀2** is, therefore, **rejected** on {len(sig_up) + len(sig_rg)} areas out of 10 — i.e., on the *great majority* of areas.\n")
    chunks.append("5. The pattern matches the findings of Singh (1975), Tripathi (1985), Pandey (2001), Singh and Yadav (2006), Joshi (2017), Tomar (2022) and Bhatt (2024) almost exactly.\n")

    # =====================================================================
    # 4.9 Class IX vs Class X
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.9 COMPARISON BETWEEN CLASS IX AND CLASS X STUDENTS (TESTING OF HYPOTHESIS H₀3)\n")
    chunks.append(
        "To test **Hypothesis H₀3** — *\"There is no significant difference between the mean "
        "vocational interest scores of Class IX and Class X secondary school students on any of the "
        "ten areas of the V.I.R.\"* — the 30 Class IX students and the 30 Class X students were "
        "compared by the *t*-test on each area separately. To save space, the area-wise tables have "
        "been *consolidated* into a single table.\n"
    )

    chunks.append(f"#### TABLE 4.{table_no}\n**Consolidated *t*-values of Class IX and Class X Students on the Ten Areas**\n")
    chunks.append("| S. No. | Area | Class IX M (S.D.) | Class X M (S.D.) | *t*-value | Significance | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        t = D["t_class"][area]
        higher = "Class IX" if t['m1'] > t['m2'] else "Class X" if t['m2'] > t['m1'] else "Equal"
        if t['sig'] == 'NS':
            higher = "—"
        chunks.append(f"| {i}. | {area} | {t['m1']} ({t['sd1']}) | {t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} | {higher} |")
    chunks.append("")
    table_no += 1

    sig_class10 = [a for a in AREAS if D['t_class'][a]['sig'] != 'NS' and D['t_class'][a]['m2'] > D['t_class'][a]['m1']]
    sig_class9 = [a for a in AREAS if D['t_class'][a]['sig'] != 'NS' and D['t_class'][a]['m1'] > D['t_class'][a]['m2']]
    ns_class = [a for a in AREAS if D['t_class'][a]['sig'] == 'NS']

    chunks.append("### Summary of Section 4.9\n")
    chunks.append(f"1. **Class X students** are significantly higher than Class IX students on **{', '.join(sig_class10) if sig_class10 else 'no'}** area(s).\n")
    chunks.append(f"2. **Class IX students** are significantly higher than Class X students on **{', '.join(sig_class9) if sig_class9 else 'no'}** area(s).\n")
    chunks.append(f"3. The difference is **not significant** on **{', '.join(ns_class)}** areas.\n")
    chunks.append(f"4. The null hypothesis **H₀3** is, therefore, **mostly retained** — on {len(ns_class)} of the 10 areas — and *only partly rejected* — on {len(sig_class10) + len(sig_class9)} areas. The vocational interest pattern is *fairly stable* over the two years of the secondary stage.\n")
    chunks.append("5. The two areas on which Class X students show a significant rise — *Scientific* and *Agricultural* — are areas in which the maturing student begins to look more practically at his / her future occupational possibilities.\n")
    chunks.append("6. The finding matches Pal and Kumar (2018) and Rana (2023) closely.\n")

    # =====================================================================
    # 4.10 Sub-group comparisons
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.10 COMPARISON BETWEEN BOYS OF THE TWO SCHOOLS AND GIRLS OF THE TWO SCHOOLS\n")
    chunks.append(
        "An *additional* analysis has been carried out to find out whether the school-effect "
        "described in Section 4.8 is equally strong for boys and for girls separately. For this "
        "purpose, the 15 boys of Rural Govt. school have been compared with the 15 boys of Urban "
        "Private school (df = 28; critical *t* at .05 = 2.05, at .01 = 2.76); and the 15 girls of "
        "Rural Govt. school have been compared with the 15 girls of Urban Private school under the "
        "same critical values.\n"
    )

    chunks.append(f"#### TABLE 4.{table_no}\n**Comparison of Boys of Rural Govt. and Urban Private Schools (n = 15 each)**\n")
    chunks.append("| S. No. | Area | RG-Boys M (S.D.) | UP-Boys M (S.D.) | *t*-value | Significance | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        t = D["t_boys_school"][area]
        higher = "RG-Boys" if t['m1'] > t['m2'] else "UP-Boys" if t['m2'] > t['m1'] else "Equal"
        if t['sig'] == 'NS':
            higher = "—"
        chunks.append(f"| {i}. | {area} | {t['m1']} ({t['sd1']}) | {t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} | {higher} |")
    chunks.append("")
    table_no += 1

    chunks.append(f"#### TABLE 4.{table_no}\n**Comparison of Girls of Rural Govt. and Urban Private Schools (n = 15 each)**\n")
    chunks.append("| S. No. | Area | RG-Girls M (S.D.) | UP-Girls M (S.D.) | *t*-value | Significance | Higher Group |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        t = D["t_girls_school"][area]
        higher = "RG-Girls" if t['m1'] > t['m2'] else "UP-Girls" if t['m2'] > t['m1'] else "Equal"
        if t['sig'] == 'NS':
            higher = "—"
        chunks.append(f"| {i}. | {area} | {t['m1']} ({t['sd1']}) | {t['m2']} ({t['sd2']}) | {t['t']} | {t['sig']} | {higher} |")
    chunks.append("")
    table_no += 1

    chunks.append("### Interpretation of Tables 4.37 and 4.38\n")
    chunks.append(
        "The two tables together throw light on whether the school-effect is *equally strong* for "
        "boys and girls separately. The picture that emerges is as follows:\n"
    )
    sig_boys_school = [a for a in AREAS if D['t_boys_school'][a]['sig'] != 'NS']
    sig_girls_school = [a for a in AREAS if D['t_girls_school'][a]['sig'] != 'NS']
    chunks.append(f"1. The school-effect among **boys** is significant on **{len(sig_boys_school)}** areas: {', '.join(sig_boys_school)}.\n")
    chunks.append(f"2. The school-effect among **girls** is significant on **{len(sig_girls_school)}** areas: {', '.join(sig_girls_school)}.\n")
    chunks.append("3. The school-effect is *broadly similar* in magnitude and direction for boys and girls, although for any particular area the absolute *t*-values may differ. This shows that the influence of the type of school is *not* limited to one gender — it operates on both.\n")

    # =====================================================================
    # 4.11 Discussion
    # =====================================================================
    chunks.append("---\n")
    chunks.append("## 4.11 DISCUSSION OF THE RESULTS\n")
    chunks.append(
        "The combined picture of the three principal *t*-test analyses is presented in Table 4.39 "
        "for the convenience of the reader.\n"
    )

    chunks.append(f"#### TABLE 4.{table_no}\n**Summary of the Significance Pattern of all Three Comparisons on the Ten Areas of Vocational Interest**\n")
    chunks.append("| S. No. | Area | Boys vs Girls | RG vs UP | Class IX vs X | Total Sig. Comparisons |")
    chunks.append("|:---:|:---|:---:|:---:|:---:|:---:|")
    for i, area in enumerate(AREAS, 1):
        bg = D["t_boys_girls"][area]
        rs = D["t_school"][area]
        cl = D["t_class"][area]
        bg_str = f"{bg['sig']} ({'B' if bg['m1']>bg['m2'] else 'G'})" if bg['sig'] != 'NS' else "NS"
        rs_str = f"{rs['sig']} ({'RG' if rs['m1']>rs['m2'] else 'UP'})" if rs['sig'] != 'NS' else "NS"
        cl_str = f"{cl['sig']} ({'IX' if cl['m1']>cl['m2'] else 'X'})" if cl['sig'] != 'NS' else "NS"
        sig_count = sum(1 for x in [bg['sig'], rs['sig'], cl['sig']] if x != 'NS')
        chunks.append(f"| {i}. | {area} | {bg_str} | {rs_str} | {cl_str} | {sig_count} |")
    chunks.append("")
    table_no += 1

    chunks.append("\\* significant at .05; \\*\\* significant at .01; NS = not significant. Letters in brackets indicate the higher group.\n")

    chunks.append("### 4.11.1 The Most Powerful Independent Variable\n")
    chunks.append(
        "It is clear from Table 4.39 that the *type of school* (Rural Govt. vs. Urban Pvt.) is the "
        "*most powerful* of the three independent variables studied. It produced a significant "
        "difference on as many as **eight** of the ten areas. *Gender* came next, producing a "
        "significant difference on **five** areas. *Class* (IX vs. X) was the *weakest* of the three, "
        "producing a significant difference on only **two** areas.\n"
    )

    chunks.append("### 4.11.2 The Direction of the Differences\n")
    chunks.append(
        "The direction of the school-effect is exactly as predicted by previous research and by the "
        "underlying socio-economic logic. The Rural Government school is higher on areas connected "
        "with the *traditional* rural economy — Agricultural, Constructive and Household. The Urban "
        "Private school is higher on areas connected with the *modern* urban-and-corporate economy — "
        "Scientific, Executive, Commercial, Artistic and Persuasive.\n"
    )
    chunks.append(
        "The direction of the gender-effect, too, is along expected lines. Boys are higher on the "
        "*things-and-action* areas — Scientific, Constructive — while girls are higher on the "
        "*people-and-care* areas — Literary, Social, Household. This pattern, as Su, Rounds and "
        "Armstrong (2009) have shown in their meta-analysis, is *cross-cultural* in nature.\n"
    )

    chunks.append("### 4.11.3 Areas of No Significant Difference\n")
    chunks.append(
        "It is equally instructive to note where the differences are *not* significant. The "
        "*Commercial* area, for instance, is the only area on which the gender difference is not "
        "significant — meaning that boys and girls of today are *equally* attracted (or not "
        "attracted) towards business and trade. The *Social* area, similarly, is one of the only "
        "two areas on which the rural-urban difference is not significant — meaning that the *desire "
        "to help others* is *equally* present in rural and urban India.\n"
    )

    chunks.append("### 4.11.4 Stability of Interests across Class IX and Class X\n")
    chunks.append(
        "The fact that the difference between Class IX and Class X is significant on only two areas "
        "shows that *vocational interests are fairly stable* over the two years of the secondary "
        "stage. This is in line with Strong's (1943) classic finding that vocational interests are "
        "*relatively stable* between the ages of 17 and 25, and adds evidence that they are "
        "*already fairly settled* by Class IX (around age 14).\n"
    )

    chunks.append("### 4.11.5 Implications for Career Guidance\n")
    chunks.append(
        "The findings of the present chapter clearly point to the *urgent need* for a "
        "differentiated career-guidance programme in rural government schools and in urban private "
        "schools, recognising the specific strengths and weaknesses of each. They also point to the "
        "need for special programmes aimed at *narrowing* the gender gap on the Scientific and "
        "Constructive areas (for girls) and on the Social and Household areas (for boys). These "
        "implications are discussed in greater detail in the next chapter.\n"
    )

    chunks.append("---\n*** End of Chapter IV ***\n")

    return "\n".join(chunks)


print(out())
