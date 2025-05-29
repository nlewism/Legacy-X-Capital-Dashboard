
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Legends Never Die Hedge Fund", layout="wide")

st.markdown("## 💼 Legends Never Die Hedge Fund")

# Header Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Instruments", "20")
col2.metric("Avg Base Hit Profit", "2.07")
col3.metric("Top Performer", "XAU/USD", delta="2.44")

st.markdown("---")

# Define all the required columns
columns = [
    "Instrument", "Journal", "Status", "Settings", "P&L", "Win Rate", "Total Trades", 
    "Winning Trades", "PF - ALL USD", "PF - Long USD", "PF - Short USD", "Stop Loss on 5",
    "Starting Value", "Net Profit $", "Ending Value", "Years", "Avg Annual Return", 
    "Max Drawdown (%)", "Max Drawdown ($)", "Reward-to-Risk Ratio", "RMD > 2", "IMG"
]

# Create an empty dataframe with those columns
#df = pd.DataFrame(columns=columns)
df = pd.read_csv("/Users/Dan/Desktop/Hedge Fund Dash/Forward Testing Results/Strategies-👁️ Watch List.csv")  # ✅ Your real data
df.columns = [col.strip() for col in df.columns] 

# Optional: Add this before displaying the table
# Get unique instruments (will be empty initially, but works when data is added)
instruments = df["Instrument"].dropna().unique()

# Filter selector (change to st.selectbox if you want single selection)
selected_instruments = st.multiselect("🎯 Filter by Instrument", options=instruments, default=instruments)

# Apply filter
filtered_df = df[df["Instrument"].isin(selected_instruments)]

# Display the filtered table
st.dataframe(filtered_df, use_container_width=True)
