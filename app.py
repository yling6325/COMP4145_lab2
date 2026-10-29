import streamlit as st
import pandas as pd
import altair as alt

from trading_strategy import run_strategy

st.set_page_config(page_title="Trading Strategy Dashboard", layout="wide")


def make_chart_data():
    data, positions = run_strategy("MSFT")
    chart_data = data.reset_index().rename(columns={"index": "Date"})
    chart_data["Date"] = pd.to_datetime(chart_data["Date"])

    buy_df = pd.DataFrame({
        "Date": pd.to_datetime(positions["BuyDate"]),
        "BuyPrice": positions["BuyPrice"].astype(float)
    }) if not positions.empty else pd.DataFrame(columns=["Date", "BuyPrice"])

    sell_df = pd.DataFrame({
        "Date": pd.to_datetime(positions["SellDate"]),
        "SellPrice": positions["SellPrice"].astype(float)
    }) if not positions.empty else pd.DataFrame(columns=["Date", "SellPrice"])

    return chart_data, buy_df, sell_df, positions


st.title("MSFT Trading Strategy Dashboard")

chart_data, buy_df, sell_df, positions = make_chart_data()

st.caption("Price chart with stock price, MA50, MA200, and buy/sell markers")

base = alt.Chart(chart_data).encode(x=alt.X("Date:T", title="Date"))

close_line = base.mark_line(color="#1f77b4", strokeWidth=2).encode(
    y=alt.Y("Close:Q", title="Price")
)

ma50_line = base.mark_line(color="#ff7f0e", strokeWidth=2).encode(
    y=alt.Y("MA50:Q", title="MA50")
)

ma200_line = base.mark_line(color="#2ca02c", strokeWidth=2).encode(
    y=alt.Y("MA200:Q", title="MA200")
)

buy_points = alt.Chart(buy_df).mark_circle(size=80, color="green", opacity=0.9).encode(
    x="Date:T",
    y="BuyPrice:Q",
    tooltip=["Date:T", "BuyPrice:Q"]
)

sell_points = alt.Chart(sell_df).mark_circle(size=80, color="red", opacity=0.9).encode(
    x="Date:T",
    y="SellPrice:Q",
    tooltip=["Date:T", "SellPrice:Q"]
)

chart = (close_line + ma50_line + ma200_line + buy_points + sell_points).properties(
    width=1200,
    height=600,
    title="MSFT Price and Moving Averages"
).interactive()

st.altair_chart(chart, use_container_width=True)

st.subheader("Trade Summary")

if positions.empty:
    st.warning("No trades were generated for the current strategy settings.")
else:
    total_trades = len(positions)
    win_trades = int((positions["ProfitPct"] > 0).sum())
    loss_trades = total_trades - win_trades
    win_rate = (win_trades / total_trades * 100) if total_trades else 0
    avg_profit = positions["ProfitPct"].mean() if total_trades else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Trades", total_trades)
    col2.metric("Winning Trades", win_trades)
    col3.metric("Losing Trades", loss_trades)
    col4.metric("Win Rate", f"{win_rate:.2f}%")
    col5.metric("Avg Profit %", f"{avg_profit:.2f}%")

    st.subheader("Detailed Trades")
    st.dataframe(positions.reset_index(drop=True), use_container_width=True)
