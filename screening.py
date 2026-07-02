import pandas as pd

df = pd.read_csv('benchmarks/normad_etiquette_final_data.csv')

target_subaxes = [

    "gift_giving",

    "visiting",

    "offering_and_complimenting_items",

    "direct_manners",

    "religious_dietary_laws",

    "‘taarof’_(politeness_and_mutual_respect)"

]

candidates = df[df["Subaxis"].isin(target_subaxes)]

sample = candidates.sample(n=20, random_state=42)

sample.to_csv("screening_candidates.csv", index=False)