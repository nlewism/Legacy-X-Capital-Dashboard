import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Legacy X Capital", layout="wide")
st.title("💵 Legacy X Capital")

# Load CSV exported from Airtable
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/Dan/Desktop/Legacy-X-Capital-Dashboard/Hedge Fund Dash/Forward Testing Results/Strategies-👁️ Watch List.csv")

    # Drop unwanted rows based on their original position in the CSV
    rows_to_drop = [0, 1, 3, 5, 6, 7, 9, 12, 14, 15, 20, 22]
    df = df.drop(index=rows_to_drop, errors="ignore").reset_index(drop=True)

    # Clean column names
    df.columns = [col.strip() for col in df.columns]


    # Status
    df["Status"] = df["Live Trades"].apply(lambda x: "Live trades" if x >= 1 else "Backtest")

    

    #df["instrument"] = df["COIN PAIR"]
    coin_to_forex = {
    "BTC": "EUR/USD",
    "ETH": "AUD/USD",
    "SOL": "GBP/USD",
    "LINK": "NZD/USD",
    "AVAX": "USD/CAD",
    "NEAR": "USD/JPY",
    "RUNE":"USD/CHF"
}
    df["Instrument"] = df["COIN PAIR"].str.strip().map(coin_to_forex)
# Filter only instruments that were mapped (i.e., non-NaN)
    df = df[df["Instrument"].notna()]
               
    #df["journal"] = ""
    df["Settings"] = df["TIMEFRAME"]
    #df["P&L"] = ""
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
    #df["Max Drawdown$"] = ""
    df["Reward-to-Risk Ratio"] = df["Avg Annual Return"] / df["Max Drawdown%"]
    df["RMD > 2"] = df["Reward-to-Risk Ratio"].apply(lambda x: "Yes" if x > 2 else "No")
    df["IMG"] = ""
    #df["IMG"] = df["Equity Curve TV URL"]
    #df["IMG"] = df["Equity Curve TV URL"].apply(lambda url: f"[View]({url})" if pd.notna(url) else "")
    new_row = {
    "instrument": "CAD/CHF",
    "status": "Backtest",
    "Level": "Moderate",  # or based on your logic
    "Settings": "30 minutes",
    "P&L": "",
    "Win Rate": 41.59,
    "Total Trades": 743,
    "Winning Trades": 309,
    "PF": 1.314,
    "Net Profit $": 6237.97,
    "Years": 2,  # Estimate if not clear
    "Avg Annual Return": 6237.97 / 2,
    "Max Drawdown%": 37.85,
    "Max Drawdown$": "",
    "Reward-to-Risk Ratio": (6237.97 / 2) / 37.85,
    "RMD > 2": "No",
    "IMG": "/mnt/data/image (6).png"  # Optional if you want to show an image
}
    df.loc[len(df)] = new_row








# Level (based on timeframe)
    def map_level(Settings):
        s = str(Settings).lower().strip()

        # Look for time in minutes or hours
        match = re.search(r"(\d+)", s)
        if not match:
            return "Unknown"

        time_val = int(match.group(1))

        if "min" in s:
            if time_val <= 15:
                return "Aggressive"
            elif 30 <= time_val <= 45:
                return "Moderate"
            elif time_val >= 60:
                return "Conservative"
        elif "hour" in s or "hr" in s or "h" in s:
            return "Conservative"

        return "Unknown"

    df["Level"] = df["Settings"].apply(map_level)

    final_columns = [
        "Instrument", "Status", "Level", "Settings", "Win Rate", "Total Trades",
        "Winning Trades", "PF", "Net Profit $", "Years", "Avg Annual Return",
        "Max Drawdown%", "Reward-to-Risk Ratio", "RMD > 2", "IMG"
    ]

    return df[final_columns]

df = load_data()

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Instruments", df["Instrument"].nunique())
col2.metric("Avg Profit Factor", round(df["PF"].mean(), 2))
top = df.loc[df["PF"].idxmax()]
col3.metric("Top Performer", top["Instrument"], round(top["PF"], 2))

st.markdown("---")

# Filter by Instrument
instruments = df["Instrument"].dropna().unique()
selected_instruments = st.multiselect("🎯 Filter by Instrument", instruments, default=instruments)
filtered_df = df[df["Instrument"].isin(selected_instruments)]

# Display the table
st.dataframe(filtered_df, use_container_width=True)

#st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)

#st.markdown("## 📈 Equity Curves")

#for _, row in filtered_df.iterrows():
#    if pd.notna(row["IMG"]):
#        st.markdown(f"### {row['Instrument']}")
#        st.image(row["IMG"], width=700)