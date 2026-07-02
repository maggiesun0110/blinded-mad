import pandas as pd

df = pd.read_csv("data/normad_eti.csv")

already = pd.read_json("results/screening_results.json")
already_ids = set(already["id"])

target_subaxes = [
    "gift_giving",
    "visiting",
    "offering_and_complimenting_items",
]

candidates = df[
    df["subaxis"].isin(target_subaxes)
    & ~df["id"].isin(already_ids)
]

keywords = [
    "gift", "offer", "decline", "accept", "host", "guest",
    "visit", "unannounced", "shoes", "left hand", "both hands",
    "open", "compliment", "elder", "respect"
]

mask = candidates["story"].str.contains("|".join(keywords), case=False, na=False) | \
       candidates["rule-of-thumb"].str.contains("|".join(keywords), case=False, na=False)

candidates = candidates[mask]

batch2 = candidates.sample(n=20, random_state=43)

batch2.to_csv("data/screening_candidates_2.csv", index=False)
print(batch2[["id", "country", "subaxis", "rule-of-thumb", "story"]])