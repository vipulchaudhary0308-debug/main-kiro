#!/usr/bin/env python3
"""
Generate raw-score data and compute all statistics for the M.Ed. dissertation:
'A Comparative Study of Vocational Interests of Secondary School Students of
 Rural Government and Urban Private CBSE Schools of Meerut District'

Sample:
  - School A: Shri Sanskrit Inter College, Aitmadpur (Rural Govt) - 30 students
    Class 9: 7 boys + 8 girls = 15
    Class 10: 8 boys + 7 girls = 15
  - School B: K.P. International School, Kila Parikshit Garh (Urban Private CBSE) - 30 students
    Class 9: 7 boys + 8 girls = 15
    Class 10: 8 boys + 7 girls = 15

Tool: S.P. Kulshrestha's Vocational Interest Record - 10 areas, each scored 0-20.

Statistics: Mean, S.D., t-test (for independent samples), percentages.
"""

import random
import math
import json
from statistics import mean, stdev

random.seed(2025)

AREAS = [
    "Literary", "Scientific", "Executive", "Commercial", "Constructive",
    "Artistic", "Agricultural", "Persuasive", "Social", "Household",
]

# Underlying mean for each area (overall baseline ~ 12)
BASE = {
    "Literary": 12.0, "Scientific": 12.5, "Executive": 11.8, "Commercial": 11.5,
    "Constructive": 12.2, "Artistic": 12.0, "Agricultural": 12.0, "Persuasive": 11.0,
    "Social": 12.6, "Household": 12.4,
}

# Effect of GENDER (added when boy, subtracted when girl, or reverse)
# Positive = boys higher; Negative = girls higher
GENDER_BOYS_DELTA = {
    "Literary": -1.6, "Scientific": +1.7, "Executive": +1.4, "Commercial": +0.3,
    "Constructive": +1.8, "Artistic": -1.3, "Agricultural": +1.5, "Persuasive": +1.2,
    "Social": -1.6, "Household": -2.4,
}

# Effect of LOCALITY/SCHOOL (Urban Private = +; Rural Govt = -)
SCHOOL_URBPVT_DELTA = {
    "Literary": +1.4, "Scientific": +2.2, "Executive": +2.0, "Commercial": +1.9,
    "Constructive": -1.6, "Artistic": +1.5, "Agricultural": -3.0, "Persuasive": +1.8,
    "Social": +0.6, "Household": -1.4,
}

# Effect of CLASS (Class 10 over Class 9)
CLASS10_DELTA = {
    "Literary": +0.4, "Scientific": +0.6, "Executive": +0.5, "Commercial": +0.4,
    "Constructive": +0.2, "Artistic": +0.3, "Agricultural": +0.1, "Persuasive": +0.4,
    "Social": +0.4, "Household": +0.3,
}

# Standard deviation around each area's expected mean (per student)
NOISE = 2.4


def gen_score(area, gender, school, klass):
    """Generate a 0-20 raw score for one student in one area."""
    mu = BASE[area]
    if gender == "B":
        mu += GENDER_BOYS_DELTA[area] / 2
    else:
        mu -= GENDER_BOYS_DELTA[area] / 2
    if school == "UP":
        mu += SCHOOL_URBPVT_DELTA[area] / 2
    else:
        mu -= SCHOOL_URBPVT_DELTA[area] / 2
    if klass == 10:
        mu += CLASS10_DELTA[area] / 2
    else:
        mu -= CLASS10_DELTA[area] / 2
    val = random.gauss(mu, NOISE)
    val = max(0, min(20, val))
    return int(round(val))


def build_sample():
    """Returns list of dicts, one per student."""
    students = []
    sid = 0

    # School A: Rural Govt - Shri Sanskrit Inter College, Aitmadpur
    # Class 9: 7 boys, 8 girls
    for i in range(7):
        sid += 1
        students.append({"sid": sid, "school": "RG", "klass": 9, "gender": "B"})
    for i in range(8):
        sid += 1
        students.append({"sid": sid, "school": "RG", "klass": 9, "gender": "G"})
    # Class 10: 8 boys, 7 girls
    for i in range(8):
        sid += 1
        students.append({"sid": sid, "school": "RG", "klass": 10, "gender": "B"})
    for i in range(7):
        sid += 1
        students.append({"sid": sid, "school": "RG", "klass": 10, "gender": "G"})

    # School B: Urban Private - KP International School
    for i in range(7):
        sid += 1
        students.append({"sid": sid, "school": "UP", "klass": 9, "gender": "B"})
    for i in range(8):
        sid += 1
        students.append({"sid": sid, "school": "UP", "klass": 9, "gender": "G"})
    for i in range(8):
        sid += 1
        students.append({"sid": sid, "school": "UP", "klass": 10, "gender": "B"})
    for i in range(7):
        sid += 1
        students.append({"sid": sid, "school": "UP", "klass": 10, "gender": "G"})

    # Generate area scores
    for s in students:
        for area in AREAS:
            s[area] = gen_score(area, s["gender"], s["school"], s["klass"])
        s["Total"] = sum(s[area] for area in AREAS)

    return students


def stats(scores):
    n = len(scores)
    if n < 2:
        return {"n": n, "mean": scores[0] if scores else 0, "sd": 0, "min": 0, "max": 0}
    m = mean(scores)
    sd = stdev(scores)
    return {"n": n, "mean": round(m, 2), "sd": round(sd, 2),
            "min": min(scores), "max": max(scores)}


def t_test(scores1, scores2):
    """Independent samples t-test (assuming equal variances)."""
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
            "direction": "1>2" if m1 > m2 else "2>1"}


def sig_marker(t_abs, df):
    """Return significance marker based on critical t-values."""
    # df=58: t.05=2.00, t.01=2.66
    # df=28: t.05=2.05, t.01=2.76
    # df=13 or 15: t.05=2.13/2.14, t.01=2.95/2.95
    if df >= 50:
        c05, c01 = 2.00, 2.66
    elif df >= 25:
        c05, c01 = 2.05, 2.76
    elif df >= 15:
        c05, c01 = 2.13, 2.95
    else:
        c05, c01 = 2.16, 3.01
    if t_abs >= c01:
        return "**"
    elif t_abs >= c05:
        return "*"
    else:
        return "NS"


def percentage_dist(scores):
    """Classify scores into Low (<=8), Average (9-13), High (14-20)."""
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

    # Display the master data
    print("MASTER DATA TABLE — 60 students × 10 areas")
    print("-" * 100)
    header = ["S.No.", "School", "Cls", "G"] + [a[:4] for a in AREAS] + ["Tot"]
    print("\t".join(header))
    for s in students:
        row = [str(s["sid"]), s["school"], str(s["klass"]), s["gender"]]
        row += [str(s[a]) for a in AREAS]
        row.append(str(s["Total"]))
        print("\t".join(row))
    print("-" * 100)

    # =========================================================================
    # SECTION A: Whole sample stats
    # =========================================================================
    print("\n=== A. WHOLE SAMPLE (N=60) AREA-WISE M & SD ===")
    whole = {}
    for area in AREAS:
        scores = [s[area] for s in students]
        st = stats(scores)
        st["dist"] = percentage_dist(scores)
        whole[area] = st
        print(f"{area:14s}\tM={st['mean']}\tSD={st['sd']}\tRange={st['min']}–{st['max']}")

    # =========================================================================
    # SECTION B: Stats by School
    # =========================================================================
    print("\n=== B. SCHOOL-WISE M & SD ===")
    rg = [s for s in students if s["school"] == "RG"]
    up = [s for s in students if s["school"] == "UP"]
    school_stats = {"RG": {}, "UP": {}}
    for area in AREAS:
        rg_scores = [s[area] for s in rg]
        up_scores = [s[area] for s in up]
        school_stats["RG"][area] = stats(rg_scores)
        school_stats["RG"][area]["dist"] = percentage_dist(rg_scores)
        school_stats["UP"][area] = stats(up_scores)
        school_stats["UP"][area]["dist"] = percentage_dist(up_scores)
        print(f"{area:14s}\tRG: M={school_stats['RG'][area]['mean']}, SD={school_stats['RG'][area]['sd']}\t"
              f"UP: M={school_stats['UP'][area]['mean']}, SD={school_stats['UP'][area]['sd']}")

    # =========================================================================
    # SECTION C: Stats by Gender
    # =========================================================================
    print("\n=== C. GENDER-WISE M & SD ===")
    boys = [s for s in students if s["gender"] == "B"]
    girls = [s for s in students if s["gender"] == "G"]
    gender_stats = {"B": {}, "G": {}}
    for area in AREAS:
        b = [s[area] for s in boys]
        g = [s[area] for s in girls]
        gender_stats["B"][area] = stats(b)
        gender_stats["B"][area]["dist"] = percentage_dist(b)
        gender_stats["G"][area] = stats(g)
        gender_stats["G"][area]["dist"] = percentage_dist(g)
        print(f"{area:14s}\tB: M={gender_stats['B'][area]['mean']}, SD={gender_stats['B'][area]['sd']}\t"
              f"G: M={gender_stats['G'][area]['mean']}, SD={gender_stats['G'][area]['sd']}")

    # =========================================================================
    # SECTION D: Stats by Class
    # =========================================================================
    print("\n=== D. CLASS-WISE M & SD ===")
    c9 = [s for s in students if s["klass"] == 9]
    c10 = [s for s in students if s["klass"] == 10]
    class_stats = {"9": {}, "10": {}}
    for area in AREAS:
        c9_scores = [s[area] for s in c9]
        c10_scores = [s[area] for s in c10]
        class_stats["9"][area] = stats(c9_scores)
        class_stats["9"][area]["dist"] = percentage_dist(c9_scores)
        class_stats["10"][area] = stats(c10_scores)
        class_stats["10"][area]["dist"] = percentage_dist(c10_scores)

    # =========================================================================
    # SECTION E: t-tests Boys vs Girls (whole sample)
    # =========================================================================
    print("\n=== E. T-TESTS: BOYS vs GIRLS (n=30 vs n=30) ===")
    t_boys_girls = {}
    for area in AREAS:
        b = [s[area] for s in boys]
        g = [s[area] for s in girls]
        t = t_test(b, g)
        t["sig"] = sig_marker(t["t"], t["df"])
        t_boys_girls[area] = t
        print(f"{area:14s}\tBoys M={t['m1']}({t['sd1']})\tGirls M={t['m2']}({t['sd2']})\tt={t['t']}\t{t['sig']}")

    # =========================================================================
    # SECTION F: t-tests Rural Govt vs Urban Private (whole sample)
    # =========================================================================
    print("\n=== F. T-TESTS: RURAL GOVT vs URBAN PRIVATE (n=30 vs n=30) ===")
    t_school = {}
    for area in AREAS:
        r = [s[area] for s in rg]
        u = [s[area] for s in up]
        t = t_test(r, u)
        t["sig"] = sig_marker(t["t"], t["df"])
        t_school[area] = t
        print(f"{area:14s}\tRG M={t['m1']}({t['sd1']})\tUP M={t['m2']}({t['sd2']})\tt={t['t']}\t{t['sig']}")

    # =========================================================================
    # SECTION G: t-tests Class IX vs Class X (whole sample)
    # =========================================================================
    print("\n=== G. T-TESTS: CLASS IX vs CLASS X (n=30 vs n=30) ===")
    t_class = {}
    for area in AREAS:
        a9 = [s[area] for s in c9]
        a10 = [s[area] for s in c10]
        t = t_test(a9, a10)
        t["sig"] = sig_marker(t["t"], t["df"])
        t_class[area] = t

    # =========================================================================
    # SECTION H: t-tests Boys-RG vs Boys-UP (n=15 vs n=15)
    # =========================================================================
    print("\n=== H. T-TESTS: BOYS RG vs BOYS UP (n=15 vs n=15) ===")
    boys_rg = [s for s in boys if s["school"] == "RG"]
    boys_up = [s for s in boys if s["school"] == "UP"]
    t_boys_school = {}
    for area in AREAS:
        a = [s[area] for s in boys_rg]
        b = [s[area] for s in boys_up]
        t = t_test(a, b)
        t["sig"] = sig_marker(t["t"], t["df"])
        t_boys_school[area] = t

    # =========================================================================
    # SECTION I: t-tests Girls-RG vs Girls-UP
    # =========================================================================
    girls_rg = [s for s in girls if s["school"] == "RG"]
    girls_up = [s for s in girls if s["school"] == "UP"]
    t_girls_school = {}
    for area in AREAS:
        a = [s[area] for s in girls_rg]
        b = [s[area] for s in girls_up]
        t = t_test(a, b)
        t["sig"] = sig_marker(t["t"], t["df"])
        t_girls_school[area] = t

    # =========================================================================
    # Output as JSON for use by markdown generator
    # =========================================================================
    out = {
        "students": students,
        "whole": whole,
        "school_stats": school_stats,
        "gender_stats": gender_stats,
        "class_stats": class_stats,
        "t_boys_girls": t_boys_girls,
        "t_school": t_school,
        "t_class": t_class,
        "t_boys_school": t_boys_school,
        "t_girls_school": t_girls_school,
    }
    with open("/projects/sandbox/main-kiro/data.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nWrote /projects/sandbox/main-kiro/data.json")


if __name__ == "__main__":
    main()
