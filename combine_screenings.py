import json
import pandas as pd

with open("results/screening_results.json") as f:
    batch1 = json.load(f)

with open("results/screening_results_2.json") as f:
    batch2 = json.load(f)

all_results = batch1 + batch2

rows = []

for s in all_results:
    if s["disagreement_score"] > 1:

        rows.append({
            "id": s["id"],
            "country": s["country"],
            "subaxis": s["subaxis"],
            "story": s["story"],

            "Western": s["judgments"].get("Western"),
            "East Asian": s["judgments"].get("East Asian"),
            "African": s["judgments"].get("African"),
            "Middle Eastern": s["judgments"].get("Middle Eastern"),
            "South/SE Asian": s["judgments"].get("South/SE Asian"),

            "disagreement_score": s["disagreement_score"],
        })

df = pd.DataFrame(rows)

df.to_csv(
    "results/disagreement_scenarios.csv",
    index=False
)

print(df)
print(f"\nFound {len(df)} disagreement scenarios")