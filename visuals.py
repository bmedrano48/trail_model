# visuals.py

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_distributions(values, title, xlabel=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(values, kde=True, ax=ax, bins=30, color="skyblue")
    ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Show summary stats
    summary = pd.Series(values).describe(percentiles=[0.25, 0.5, 0.75])
    st.write("Summary Statistics")
    st.dataframe(summary.to_frame(name=title))