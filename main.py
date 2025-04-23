# main.py
import streamlit as st
import pandas as pd
from simulation import run_income_statement_simulation, calculate_exit_value
from waterfall import calculate_waterfall
from visuals import plot_distributions

st.set_page_config(layout="wide")
st.title("10-Year Financial Forecast & Investment Return Model")

# User Inputs
st.sidebar.header("Revenue & Cost Inputs")
start_revenue = st.sidebar.number_input("Year 1 ARR ($)", value=1000000)
input_type = st.sidebar.radio("Growth Rate Input Type", ["Static", "PERT"])

gross_margin_pct = st.sidebar.slider("Gross Margin %", 0.0, 1.0, 0.7)
sga_pct = st.sidebar.slider("SG&A as % of Revenue", 0.0, 1.0, 0.3)

if input_type == "Static":
    static_growth = st.sidebar.slider("Static Annual Growth Rate %", 0.0, 1.0, 0.1)
else:
    min_growth = st.sidebar.number_input("PERT Min Growth %", value=0.05)
    mode_growth = st.sidebar.number_input("PERT Mode Growth %", value=0.10)
    max_growth = st.sidebar.number_input("PERT Max Growth %", value=0.20)
    num_simulations = st.sidebar.number_input("Number of Simulations", value=1000)

# Exit Inputs
st.sidebar.header("Exit Inputs")
exit_year = st.sidebar.slider("Exit Year", 1, 10, 10)
exit_type = st.sidebar.radio("Exit Multiple Type", ["Static", "PERT"])
if exit_type == "Static":
    exit_multiple = st.sidebar.number_input("Exit Multiple", value=5.0)
else:
    min_exit = st.sidebar.number_input("PERT Min Exit Multiple", value=3.0)
    mode_exit = st.sidebar.number_input("PERT Mode Exit Multiple", value=5.0)
    max_exit = st.sidebar.number_input("PERT Max Exit Multiple", value=7.0)

run_button = st.sidebar.button("Run Simulation")

if run_button:
    if input_type == "Static":
        simulations = run_income_statement_simulation(start_revenue, static_growth, gross_margin_pct, sga_pct, pert=False)
    else:
        simulations = run_income_statement_simulation(
            start_revenue, (min_growth, mode_growth, max_growth), gross_margin_pct, sga_pct, pert=True, num_simulations=num_simulations
        )

    st.subheader("Income Statement (First Simulation)")
    st.dataframe(simulations[0])

    exit_values, ebitda_values = [], []
    for sim in simulations:
        revenue_series = sim["Revenue"].tolist()
        ebitda_series = sim["EBITDA"].tolist()
        if exit_type == "Static":
            multiple = exit_multiple
        else:
            from simulation import pert_random
            multiple = pert_random(min_exit, mode_exit, max_exit, 1)[0]

        tev = calculate_exit_value(revenue_series, exit_year, multiple)
        exit_values.append(tev)
        ebitda_values.append(ebitda_series[exit_year - 1])

    st.subheader("Exit Value Distribution")
    plot_distributions(exit_values, "Total Enterprise Value")

    st.subheader("Waterfall Outputs (First Simulation)")
    proceeds_table, shareholder_proceeds = calculate_waterfall(exit_values[0], exit_year)
    st.dataframe(proceeds_table)
    st.markdown(f"**Key Shareholder Proceeds:** ${shareholder_proceeds:,.2f}")
