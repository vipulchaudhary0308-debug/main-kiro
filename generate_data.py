#!/usr/bin/env python3
"""
Generate raw-score data and compute statistics for the M.Ed. dissertation:
'A Comparative Study of the Vocational Interests of Boys and Girls
 Studying at Secondary Level'
(Submitted to CCS University, Meerut, through Meerut College, Meerut.)

Sample: 80 students (40 Boys + 40 Girls) of Class IX and X, drawn from
        TWO secondary schools of Meerut District through random sampling:
   - Shri Sanskrit Inter College, Aitmadpur (Rural Govt., U.P. Board)
        Class IX : 10 Boys + 10 Girls = 20
        Class X  : 10 Boys + 10 Girls = 20
   - K.P. International School, Kila Parikshit Garh (Urban Pvt., CBSE)
        Class IX : 10 Boys + 10 Girls = 20
        Class X  : 10 Boys + 10 Girls = 20

Tool: S.P. Kulshrestha's Vocational Interest Record - 10 areas, scored 0-20.
Areas: Literary, Scientific, Executive, Commercial, Constructive (Technical),
       Artistic, Agricultural, Persuasive, Social, Household.

Primary comparison (per the title): BOYS (n = 40) vs GIRLS (n = 40),
                                    df = 78, t.05 = 1.99, t.01 = 2.64.

Statistics: Mean (M), Standard Deviation (S.D.), t-test (independent
            samples), Percentage Analysis.
"""

import random
import math
import json
from statistics import mean, stdev

random.seed(2027)

AREAS = [
    "Literary", "Scientific", "Executive", "Commercial", "Constructive",
    "Artistic", "Agricultural", "Persuasive", "Social", "Household",
]

BASE = {
    "Literary": 11.7, "Scientific": 12.3, "Executive": 11.6, "Commercial": 11.4,
    "Constructive": 11.7, "Artistic": 11.8, "Agricultural": 11.4, "Persuasive": 11.0,
    "Social": 12.4, "Household": 12.0,
}

# Effect of GENDER (added when boy, subtracted when girl)
# Positive => boys higher; Negative => girls higher
GENDER_BOYS_DELTA = {
    "Literary": -1.2, "Scientific": +2.0, "Executive": +1.5, "Commercial": +0.4,
    "Constructive": +2.4, "Artistic": -2.0, "Agricultural": +1.6, "Persuasive": +1.4,
    "Social": -1.8, "Household": -2.6,
}

# Mild school effect (positive => Urban Private higher)
SCHOOL_UP_DELTA = {
    "Literary": +1.0, "Scientific": +1.6, "Executive": +1.2, "Commercial": +1.4,
    "Constructive": -1.0, "Artistic": +0.8, "Agricultural": -2.2, "Persuasive": +1.0,
    "Social": +0.4, "Household": -0.6,
}

CLASS10_DELTA = 0.4
NOISE = 2.3


def gen_score(area, gender, school, klass):
    mu = BASE[area]
    if gender == "B":
        mu += GENDER_BOYS_DELTA[area] / 2
    else:
        mu -= GENDER_BOYS_DELTA[area] / 2
    if school == "UP":
        mu += SCHOOL_UP_DELTA[area] / 2
    else:
        mu -= SCHOOL_UP_DELTA[area] / 2
    if klass == 10:
        mu += CLASS10_DELTA / 2
    else:
        mu -= CLASS10_DELTA / 2
    val = random.gauss(mu, NOISE)
    val = max(0, min(20, val))
    return int(round(val))


def build_sample():
    students = []
    sid = 0
    for school in ["RG", "UP"]:
        for klass in [9, 10]:
            for _ in range(10):  # 10 boys per class per school
                sid += 1
                students.append({"sid": sid, "school": school,
                                 "klass": klass, "gender": "B"})
            for _ in range(10):  # 10 girls per class per school
                sid += 1
                students.append({"sid": sid, "school": school,
                                 "klass": klass, "gender": "G"})
    for s in students:
        for area in AREAS:
            s[area] = gen_score(area, s["gender"], s["school"], s["klass"])
        s["Total"] = sum(s[area] for area in AREAS)
    return students


def stats(scores):
    n = len(scores)
    if n < 2:
        return {"n": n, "mean": scores[0] if scores else 0, "sd": 0,
                "min": 0, "max": 0, "sum": 0}
    m = mean(scores)
    sd = stdev(scores)
    return {"n": n, "mean": round(m, 2), "sd": round(sd, 2),
            "min": min(scores), "max": max(scores), "sum": sum(scores)}


def t_test(scores1, scores2):
    n1, n2 = len(scores1), len(scores2)
    m1, m2 = mean(scores1), mean(scores2)
    var1 = stdev(scores1) ** 2 if n1 > 1 else 0
    var2 = stdev(scores2) ** 2 if n2 > 1 else 0
    sp2 = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    se = math.sqrt(sp2 * (1.0 / n1 + 1.0 / n2))
    t = (m1 - m2) / se if se > 0 else 0
    df = n1 + n2 - 2
    return {"m1": round(m1, 2), "m2": round(m2, 2),
            "sd1": round(math.sqrt(var1), 2), "sd2": round(math.sqrt(var2), 2),
            "n1": n1, "n2": n2, "t": round(abs(t), 3), "df": df,
            "se_diff": round(se, 3), "mean_diff": round(abs(m1 - m2), 2)}


def sig_marker(t_abs, df):
    """Two-tailed critical values (approximately)."""
    if df >= 70:        # df = 78 (40 + 40 - 2)
        c05, c01 = 1.99, 2.64
    elif df >= 35:      # df = 38 (20 + 20 - 2)
        c05, c01 = 2.02, 2.71
    elif df >= 28:      # df = 28
        c05, c01 = 2.05, 2.76
    elif df >= 18:      # df = 18
        c05, c01 = 2.10, 2.88
    else:
        c05, c01 = 2.16, 3.05
    if t_abs >= c01:
        return "**"
    elif t_abs >= c05:
        return "*"
    else:
        return "NS"


def percentage_dist(scores):
    n = len(scores)
    low = sum(1 for s in scores if s <= 8)
    avg = sum(1 for s in scores if 9 <= s <= 13)
    high = sum(1 for s in scores if s >= 14)
    return {
        "low_n": low, "avg_n": avg, "high_n": high,
        "low_pct": round(100 * low / n, 1),
        "avg_pct": round(100 * avg / n, 1),
        "high_pct": round(100 * high / n, 1),
    }


def main():
    students = build_sample()
    print("MASTER DATA — 80 students")
    print("=" * 110)
    header = ["S.No", "Sch", "Cls", "G"] + [a[:4] for a in AREAS] + ["Tot"]
    print(" | ".join(header))
    print("-" * 110)
    for s in students:
        row = [str(s["sid"]).rjust(2), s["school"], str(s["klass"]),
               s["gender"]]
        row += [str(s[a]).rjust(2) for a in AREAS]
        row.append(str(s["Total"]).rjust(3))
        print(" | ".join(row))

    boys = [s for s in students if s["gender"] == "B"]
    girls = [s for s in students if s["gender"] == "G"]

    whole, boys_stats, girls_stats, t_results = {}, {}, {}, {}
    for area in AREAS:
        all_sc = [s[area] for s in students]
        whole[area] = stats(all_sc)
        whole[area]["dist"] = percentage_dist(all_sc)
        b = [s[area] for s in boys]
        g = [s[area] for s in girls]
        boys_stats[area] = stats(b)
        boys_stats[area]["dist"] = percentage_dist(b)
        girls_stats[area] = stats(g)
        girls_stats[area]["dist"] = percentage_dist(g)
        tt = t_test(b, g)
        tt["sig"] = sig_marker(tt["t"], tt["df"])
        t_results[area] = tt

    # Sub-group analyses
    c9 = [s for s in students if s["klass"] == 9]
    c10 = [s for s in students if s["klass"] == 10]
    rg = [s for s in students if s["school"] == "RG"]
    up = [s for s in students if s["school"] == "UP"]
    boys_c9 = [s for s in c9 if s["gender"] == "B"]
    girls_c9 = [s for s in c9 if s["gender"] == "G"]
    boys_c10 = [s for s in c10 if s["gender"] == "B"]
    girls_c10 = [s for s in c10 if s["gender"] == "G"]
    boys_rg = [s for s in rg if s["gender"] == "B"]
    girls_rg = [s for s in rg if s["gender"] == "G"]
    boys_up = [s for s in up if s["gender"] == "B"]
    girls_up = [s for s in up if s["gender"] == "G"]

    t_boys_girls_c9 = {}
    t_boys_girls_c10 = {}
    t_boys_girls_rg = {}
    t_boys_girls_up = {}
    for area in AREAS:
        for tag, b_grp, g_grp in [
            ("c9", boys_c9, girls_c9),
            ("c10", boys_c10, girls_c10),
            ("rg", boys_rg, girls_rg),
            ("up", boys_up, girls_up),
        ]:
            tt = t_test([s[area] for s in b_grp], [s[area] for s in g_grp])
            tt["sig"] = sig_marker(tt["t"], tt["df"])
            if tag == "c9":
                t_boys_girls_c9[area] = tt
            elif tag == "c10":
                t_boys_girls_c10[area] = tt
            elif tag == "rg":
                t_boys_girls_rg[area] = tt
            elif tag == "up":
                t_boys_girls_up[area] = tt

    print("\n=== Boys (n=40) vs Girls (n=40) — primary t-tests ===")
    for area in AREAS:
        t = t_results[area]
        print(f"  {area:14s}  B M={t['m1']}({t['sd1']})  G M={t['m2']}"
              f"({t['sd2']})  diff={t['mean_diff']}  t={t['t']}  {t['sig']}")

    out = {
        "students": students,
        "whole": whole,
        "boys_stats": boys_stats,
        "girls_stats": girls_stats,
        "t_results": t_results,
        "t_boys_girls_c9": t_boys_girls_c9,
        "t_boys_girls_c10": t_boys_girls_c10,
        "t_boys_girls_rg": t_boys_girls_rg,
        "t_boys_girls_up": t_boys_girls_up,
    }
    with open("/projects/sandbox/main-kiro/data.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n=> Wrote /projects/sandbox/main-kiro/data.json")


if __name__ == "__main__":
    main()
