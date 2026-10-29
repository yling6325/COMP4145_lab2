import streamlit as st

from trading_strategy import run_strategy

st.set_page_config(page_title="Detailed Trades", layout="wide")

st.title("Detailed Trades Record")

data, positions = run_strategy("MSFT")

if positions.empty:
    st.warning("No trades were generated.")
    st.stop()

st.dataframe(positions.reset_index(drop=True), use_container_width=True)
