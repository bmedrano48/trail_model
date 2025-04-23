# simulation.py
import numpy as np
import pandas as pd
from scipy.stats import beta

def pert_random(min_val, mode, max_val, size=1):
    alpha = 1 + 4 * (mode - min_val) / (max_val - min_val)
    beta_param = 1 + 4 * (max_val - mode) / (max_val - min_val)
    return beta.rvs(alpha, beta_param, size=size) * (max_val - min_val) + min_val

def run_income_statement_simulation(start_revenue, growth_input, gross_margin, sga_pct, pert=True, num_simulations=1000):
    simulations = []

    for _ in range(num_simulations if pert else 1):
        revenue = [start_revenue]
        growth_rates = []

        for year in range(9):
            if pert:
                if year == 0:
                    growth = pert_random(*growth_input)[0]
                else:
                    prev_growth = growth_rates[-1]
                    growth = np.clip(np.random.normal(loc=prev_growth, scale=0.05), 0, 1)
            else:
                growth = growth_input

            growth_rates.append(growth)
            revenue.append(revenue[-1] * (1 + growth))

        cogs = [r * (1 - gross_margin) for r in revenue]
        gm = [r - c for r, c in zip(revenue, cogs)]
        sga = [r * sga_pct for r in revenue]
        ebitda = [g - s for g, s in zip(gm, sga)]

        df = pd.DataFrame({
            "Year": list(range(1, 11)),
            "Revenue": revenue,
            "Growth Rate": [None] + growth_rates,
            "COGS": cogs,
            "Gross Margin": gm,
            "SG&A": sga,
            "EBITDA": ebitda
        })
        simulations.append(df)

    return simulations

def calculate_exit_value(revenue, exit_year, exit_multiple):
    return revenue[exit_year - 1] * exit_multiple