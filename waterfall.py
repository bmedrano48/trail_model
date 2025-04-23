# waterfall.py

import pandas as pd

def calculate_waterfall(tev, exit_year):
    # Define share class inputs
    class_f = {
        "name": "Class F",
        "capital": 11_564_321,
        "pik_rate": 0.08,
        "ownership": 0.194
    }
    class_e = {
        "name": "Class E/E.1",
        "capital": 12_853_311,
        "pik_rate": 0.0,
        "ownership": 0.283
    }
    class_b = {
        "name": "Class B/D",
        "capital": 4_888_997,
        "pik_rate": 0.0,
        "ownership": 0.191
    }
    class_a = {
        "name": "Class A/C",
        "capital": 2_000_000,
        "pik_rate": 0.0,
        "ownership": 0.332
    }

    classes = [class_f, class_e, class_b, class_a]

    # Compute PIK accruals
    class_f_accrued = class_f["capital"] * ((1 + class_f["pik_rate"]) ** exit_year - 1)
    class_f_total = class_f["capital"] + class_f_accrued

    proceeds = tev
    dist = {}

    # Step 1: Pay Class F total (capital + PIK)
    dist["Class F"] = min(proceeds, class_f_total)
    proceeds -= dist["Class F"]

    # Step 2: Return capital to E, B, A
    for cls in [class_e, class_b, class_a]:
        name = cls["name"]
        dist[name] = min(proceeds, cls["capital"])
        proceeds -= dist[name]

    # Step 3: Pro-rata remaining based on ownership
    if proceeds > 0:
        for cls in classes:
            name = cls["name"]
            share = proceeds * cls["ownership"]
            dist[name] += share

    # Create output DataFrame
    df = pd.DataFrame({
        "Class": dist.keys(),
        "Proceeds": dist.values()
    })

    # Add Invested Capital and ROI
    df["Invested Capital"] = [class_f["capital"], class_e["capital"], class_b["capital"], class_a["capital"]]
    df["ROI"] = df["Proceeds"] / df["Invested Capital"]

    # Shareholder Ownership
    key_shareholder = {
        "Class F": 0.301,
        "Class E/E.1": 0.246,
        "Class A/C": 0.448
    }

    shareholder_proceeds = sum(
        dist.get(cls, 0) * pct for cls, pct in key_shareholder.items()
    )

    return df, shareholder_proceeds