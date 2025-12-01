import streamlit as st
import pandas as pd
import altair as alt
import time
from pathlib import Path
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Live Aktien Dashboard", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700&display=swap');
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter Tight', sans-serif !important;
}
[class^="st-emotion-cache"] h1,
[class^="st-emotion-cache"] h2,
[class^="st-emotion-cache"] h3,
[class^="st-emotion-cache"] h4,
[class^="st-emotion-cache"] h5,
[class^="st-emotion-cache"] h6 {
    font-family: 'Inter', sans-serif !important;
}
</style>
""", 
unsafe_allow_html=True)

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "stock_prices.csv"
REFRESH_DEFAULT = 5                 
OLD_DATA_THRESHOLD = 60        
SHOW_OLD_DATA = 300          
MAX_POINTS_TO_PLOT = 200            
STOCKS = ["AAPL", "TSLA", "NVDA", "MSFT"]

st.title("Aktien im Vergleich")

refreshrate = 5
placeholder = st.empty()

symbols = ["AAPL", "TSLA", "NVDA", "MSFT"]
symbol_titles = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "NVDA": "Nvidia",
    "MSFT": "Microsoft"
}

while True:
    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["time_full"] = df["timestamp"].dt.strftime("%d.%m.%y %H:%M")

        latest = df.tail(300)

        with placeholder.container():

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            cols = [col1, col2, col3, col4]

            for col, sym in zip(cols, symbols):
                stock_df = latest[latest["symbol"] == sym]
                if not stock_df.empty:
                    col.write(f"### {symbol_titles[sym]}")

                    chart = (
                        alt.Chart(stock_df)
                        .mark_line()
                        .encode(
                            x=alt.X("timestamp:T", title="Zeit"),
                            y=alt.Y(
                                "price:Q",
                                title="Preis",
                                scale=alt.Scale(zero=False)  
                            ),
                            tooltip=["time_full", "symbol", "price"]
                        )
                        .properties(height=220)
                    )

                    col.altair_chart(chart, width='stretch')

                else:
                    col.write(f"{sym} – noch keine Daten")       
    else:
        st.warning("CSV existiert noch nicht. Starte Producer & Consumer.")
    time.sleep(REFRESH_DEFAULT)