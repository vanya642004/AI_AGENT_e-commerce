import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def display_chart(df: pd.DataFrame, title: str = None):
    """
    Simple line chart wrapper: plots numeric columns vs index.
    """
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    if title:
        ax.set_title(title)
    st.pyplot(fig)
