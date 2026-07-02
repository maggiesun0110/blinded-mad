import pandas as pd

df = pd.read_csv("benchmarks/normad_etiquette_final_data.csv")

already = pd.read_json("results/screening_results.json")
already_ids = set(already["id"])

target_subaxes = [
    "gift_giving",
    "visiting",
    "offering_and_complimenting_items",
]

candidates = df[
    df["Subaxis"].isin(target_subaxes)
    & ~df["ID"].isin(already_ids)
]

keywords = [
    "gift", "offer", "decline", "accept", "host", "guest",
    "visit", "unannounced", "shoes", "left hand", "both hands",
    "open", "compliment", "elder", "respect"
]

mask = candidates["Story"].str.contains("|".join(keywords), case=False, na=False) | \
       candidates["Rule-of-Thumb"].str.contains("|".join(keywords), case=False, na=False)

candidates = candidates[mask]

batch2 = candidates.sample(n=20, random_state=43)

batch2.to_csv("benchmarks/screening_candidates_2.csv", index=False)
print(batch2[["ID", "Country", "Subaxis", "Rule-of-Thumb", "Story"]])