import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Legacy X Capital", layout="wide")
st.title("💵 Legacy X Capital")
st.markdown("### Base Hit Algorithms (Forex & Futures)")

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

    # Map crypto coins to Forex instruments
    coin_to_forex = {
        "BTC": "EUR/USD",
        "ETH": "AUD/USD",
        "SOL": "GBP/USD",
        "LINK": "NZD/USD",
        "AVAX": "USD/CAD",
        "NEAR": "USD/JPY",
        "RUNE": "USD/CHF"
    }
    df["Instrument"] = df["COIN PAIR"].str.strip().map(coin_to_forex)

    # Determine type: Forex vs Futures
    df["Market"] = df["Instrument"].apply(lambda x: "Forex" if pd.notna(x) else "Futures")

    # Filter only Forex mapped instruments
    forex_df = df[df["Instrument"].notna()].copy()

    # Manual addition of a futures strategy (CHF/JPY)
    new_row = {
        "Instrument": "CHF/JPY",
        "Status": "Backtest",
        "Level": "Moderate",
        "Settings": "30 minutes",
        "Win Rate": 41.59,
        "Total Trades": 743,
        "Winning Trades": 309,
        "PF": 1.314,
        "Net Profit $": 6237.97,
        "Years": 2,
        "Avg Annual Return": 6237.97 / 2,
        "Max Drawdown%": 37.85,
        "Reward-to-Risk Ratio": (6237.97 / 2) / 37.85,
        "RMD > 2": "No",
        "IMG": "/mnt/data/image (6).png",
        "Market": "Futures"
    }

    # Append to dataframe
    forex_df = pd.concat([forex_df, pd.DataFrame([new_row])], ignore_index=True)

    # Timeframe classification
    def map_level(Settings):
        s = str(Settings).lower().strip()
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

    forex_df["Level"] = forex_df["Settings"].apply(map_level)

    final_columns = [
        "Instrument", "Status", "Level", "Settings", "Win Rate", "Total Trades",
        "Winning Trades", "PF", "Net Profit $", "Years", "Avg Annual Return",
        "Max Drawdown%", "Reward-to-Risk Ratio", "RMD > 2", "IMG", "Market"
    ]

    return forex_df[final_columns]

# Load data and split by market
df = load_data()
forex_df = df[df["Market"] == "Forex"].copy()
futures_df = df[df["Market"] == "Futures"].copy()

# Forex Section
st.subheader("📊 Forex Algorithms (Goal: 9 Active)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Forex Instruments", forex_df["Instrument"].nunique())
col2.metric("Avg PF (Forex)", round(forex_df["PF"].mean(), 2))
top_forex = forex_df.loc[forex_df["PF"].idxmax()]
col3.metric("Top Forex Performer", top_forex["Instrument"], round(top_forex["PF"], 2))

selected_forex = st.multiselect("🎯 Filter Forex Instruments", forex_df["Instrument"].unique(), default=forex_df["Instrument"].unique())
filtered_forex = forex_df[forex_df["Instrument"].isin(selected_forex)]
st.dataframe(filtered_forex.drop(columns=["Market"]), use_container_width=True)

st.markdown("---")

# Futures Section
st.subheader("📈 Futures Algorithms (Goal: 3 Active)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Futures Instruments", futures_df["Instrument"].nunique())
col2.metric("Avg PF (Futures)", round(futures_df["PF"].mean(), 2))
top_futures = futures_df.loc[futures_df["PF"].idxmax()]
col3.metric("Top Futures Performer", top_futures["Instrument"], round(top_futures["PF"], 2))

selected_futures = st.multiselect("🎯 Filter Futures Instruments", futures_df["Instrument"].unique(), default=futures_df["Instrument"].unique())
filtered_futures = futures_df[futures_df["Instrument"].isin(selected_futures)]
st.dataframe(filtered_futures.drop(columns=["Market"]), use_container_width=True)

# Optional: Display equity curves for each instrument
# st.markdown("## Equity Curves")
# for _, row in df.iterrows():
#     if pd.notna(row["IMG"]):
#         st.markdown(f"### {row['Instrument']}")
#         st.image(row["IMG"], width=700)