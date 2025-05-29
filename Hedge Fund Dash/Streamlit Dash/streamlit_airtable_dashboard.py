import streamlit as st
import pandas as pd

st.set_page_config(page_title="Legends Never Die Hedge Fund", layout="wide")
st.title("💼 Legends Never Die Hedge Fund")

# Load CSV exported from Airtable
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/Dan/Desktop/Hedge Fund Dash/Forward Testing Results/Strategies-👁️ Watch List.csv")

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Status
    df["status"] = df["Live Trades"].apply(lambda x: "Live trades" if x >= 1 else "Backtest")

    # Level (based on timeframe)
    def map_level(tf):
        tf = str(tf).lower().strip()
        if any(x in tf for x in ["1", "3", "5", "15"]) and "min" in tf:
            return "Aggressive"
        elif any(x in tf for x in ["30", "45"]) and "min" in tf:
            return "Moderate"
        elif "1h" in tf or "60" in tf:
            return "Conservative"
        else:
            return "Unknown"

    df["Level"] = df["TIMEFRAME"].apply(map_level)
    df["instrument"] = df["COIN PAIR"]
    df["journal"] = ""
    df["Settings"] = df["TIMEFRAME"]
    df["P&L"] = ""
    df["Win Rate"] = df["WIN RATE - LIVE"]
    df["Total Trades"] = df["TRADES - LIVE"]
    df["Winning Trades"] = df["NUMBER WINNING TRADES"]
    df["PF"] = df["PROFIT FACTOR - LIVE"]
    df["Net Profit $"] = df["NET PROFIT % - LIVE"]
    df["FIRST TRADED DATE"] = pd.to_datetime(df["FIRST TRADED DATE"], errors="coerce")
    df["LAST TRADED DATE"] = pd.to_datetime(df["LAST TRADED DATE"], errors="coerce")
    df["Years"] = (df["LAST TRADED DATE"] - df["FIRST TRADED DATE"]).dt.days / 365
    df["Avg Annual Return"] = df["Net Profit $"] / df["Years"]
    df["Max Drawdown%"] = df["MAX DRAWDOWN - LIVE"]
    df["Max Drawdown$"] = ""
    df["Reward-to-Risk Ratio"] = df["Avg Annual Return"] / df["Max Drawdown%"]
    df["RMD > 2"] = df["Reward-to-Risk Ratio"].apply(lambda x: "Yes" if x > 2 else "No")
    df["IMG"] = ""

    final_columns = [
        "instrument", "journal", "status", "Level", "Settings", "P&L", "Win Rate", "Total Trades",
        "Winning Trades", "PF", "Net Profit $", "Years", "Avg Annual Return",
        "Max Drawdown%", "Max Drawdown$", "Reward-to-Risk Ratio", "RMD > 2", "IMG"
    ]

    return df[final_columns]

df = load_data()

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Instruments", df["instrument"].nunique())
col2.metric("Avg Profit Factor", round(df["PF"].mean(), 2))
top = df.loc[df["PF"].idxmax()]
col3.metric("Top Performer", top["instrument"], round(top["PF"], 2))

st.markdown("---")

# Filter by Instrument
instruments = df["instrument"].dropna().unique()
selected_instruments = st.multiselect("🎯 Filter by Instrument", instruments, default=instruments)
filtered_df = df[df["instrument"].isin(selected_instruments)]

# Display the table
st.dataframe(filtered_df, use_container_width=True)
