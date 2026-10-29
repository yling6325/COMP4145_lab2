import streamlit as st
import pandas as pd

from trading_strategy import run_strategy

st.set_page_config(page_title="Trade Statistics", layout="wide")

st.title("Overall Trade Statistics")

data, positions = run_strategy("MSFT")

if positions.empty:
    st.warning("No trades were generated for the strategy.")
    st.stop()

summary = {
    "Total Trades": len(positions),
    "Winning Trades": int((positions["ProfitPct"] > 0).sum()),
    "Losing Trades": int((positions["ProfitPct"] <= 0).sum()),
    "Win Rate (%)": round((positions["ProfitPct"] > 0).mean() * 100, 2),
    "Average Profit (%)": round(positions["ProfitPct"].mean(), 2),
    "Average Holding Days": round(positions["HoldingDays"].mean(), 2),
    "Target Reached": int((positions["SellReason"] == "Target reached").sum()),
    "Max Holding Period": int((positions["SellReason"] == "Max holding period").sum()),
}

for key, value in summary.items():
    st.write(f"{key}: {value}")

st.dataframe(pd.DataFrame([summary]).T.rename(columns={0: "Value"}), use_container_width=True)
