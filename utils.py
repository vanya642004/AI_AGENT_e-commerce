import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def display_chart(df: pd.DataFrame, title: str = None):
    if df.empty:
        return
    fig, ax = plt.subplots()
    df.select_dtypes(include=["number"]).plot(ax=ax)
    if title:
        ax.set_title(title)
    st.pyplot(fig)
