import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import altair as alt
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STOCKS_DATA = ROOT / "data" / "stock_prices.csv"

st.set_page_config(page_title="Live Aktien Dashboard", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700&display=swap');
* {
    font-family: 'Inter Tight', sans-serif !important;
}
</style>
""", 
unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime, time as dtime
import pytz


st_autorefresh(interval=5000, key="refresh")

SYMBOLS = ["AAPL", "TSLA", "NVDA", "MSFT"]
NAMES = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "MSFT": "Microsoft"
}

# ---------- Fallback: hole historische Daten ----------
def fetch_last_yahoo(symbol, n=300):
    df = yf.download(symbol, period="5d", interval="1m")
    df = df.tail(n)
    df = df.reset_index()
    df["timestamp"] = pd.to_datetime(df["Datetime"])
    df["symbol"] = symbol
    df["price"] = df["Close"]
    return df[["timestamp", "symbol", "price"]]


# ---------- Hole Daten aus CSV oder Yahoo ----------
def load_data():
    if STOCKS_DATA.exists():
        df = pd.read_csv(STOCKS_DATA)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df, True

    # Markt geschlossen → fallback
    frames = [fetch_last_yahoo(sym) for sym in SYMBOLS]
    df = pd.concat(frames)
    return df, False


# ---------------- UI -------------------
st.title("Aktienkurse im Vergleich")
df, live_mode = load_data()

if live_mode:
    st.info("Live-Modus aktiv – Daten kommen von Kafka (alle 5 Sekunden).")

else:
    st.warning("Fallback-Modus – Börse geschlossen. Zeige letzte Kurse von Yahoo.")

# Aktuelle Werte (pro Symbol)

latest = df.sort_values("timestamp").groupby("symbol").tail(500)

row = st.container()
with row:
    colA, colB = st.columns(2)
    colC, colD = st.columns(2)
    columns = [colA, colB, colC, colD]

    for sym, col in zip(SYMBOLS, columns):

        d = latest[latest["symbol"] == sym].sort_values("timestamp")

        if len(d) < 2:
            col.metric(NAMES[sym], "—", delta="—")
            continue

        current = d["price"].iloc[-1]
        prev = d["price"].iloc[-2]
        delta = round(current - prev, 3)
        pct = round((delta / prev) * 100, 2)

        col.metric(
            label=f"{NAMES[sym]} ({sym})",
            value=f"${current:.2f}",
            delta=f"{delta:+.2f} ({pct:+.2f}%)",
            chart_data=d["price"],
            chart_type="line",
            border=True
        )
        






# import streamlit as st
# import pandas as pd
# import altair as alt
# import time
# from pathlib import Path
# from datetime import datetime, timedelta, timezone

# st.set_page_config(page_title="Live Aktien Dashboard", layout="wide")
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700&display=swap');
# h1, h2, h3, h4, h5, h6 {
#     font-family: 'Inter Tight', sans-serif !important;
# }
# [class^="st-emotion-cache"] h1,
# [class^="st-emotion-cache"] h2,
# [class^="st-emotion-cache"] h3,
# [class^="st-emotion-cache"] h4,
# [class^="st-emotion-cache"] h5,
# [class^="st-emotion-cache"] h6 {
#     font-family: 'Inter', sans-serif !important;
# }
# </style>
# """, 
# unsafe_allow_html=True)

# CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "stock_prices.csv"
# REFRESH_DEFAULT = 5                 
# OLD_DATA_THRESHOLD = 60        
# SHOW_OLD_DATA = 300          
# MAX_POINTS_TO_PLOT = 200            
# STOCKS = ["AAPL", "TSLA", "NVDA", "MSFT"]

# st.title("Aktienkurse im Vergleich")

# refreshrate = 5
# placeholder = st.empty()

# symbols = ["AAPL", "TSLA", "NVDA", "MSFT"]
# symbol_titles = {
#     "AAPL": "Apple",
#     "TSLA": "Tesla",
#     "NVDA": "Nvidia",
#     "MSFT": "Microsoft"
# }

# while True:
#     if CSV_PATH.exists():
#         df = pd.read_csv(CSV_PATH)

#         df["timestamp"] = pd.to_datetime(df["timestamp"])
#         df["time_full"] = df["timestamp"].dt.strftime("%d.%m.%y %H:%M")

#         latest = df.tail(300)

#         with placeholder.container():

#             col1, col2 = st.columns(2)
#             col3, col4 = st.columns(2)
#             cols = [col1, col2, col3, col4]

#             for col, sym in zip(cols, symbols):
#                 stock_df = latest[latest["symbol"] == sym]
#                 if not stock_df.empty:
#                     col.write(f"#### {symbol_titles[sym]}")
#                     col.metric("", "425", "1.2%")

#                     chart = (
#                         alt.Chart(stock_df)
#                         .mark_line()
#                         .encode(
#                             x=alt.X("timestamp:T", title=""),
#                             y=alt.Y(
#                                 "price:Q",
#                                 title="Preis",
#                                 scale=alt.Scale(zero=False)  
#                             ),
#                             tooltip=["time_full", "symbol", "price"]
#                         )
#                         .properties(height=220)
#                     )

#                     col.altair_chart(chart, width='stretch')

#                 else:
#                     col.write(f"{sym} – noch keine Daten")       
#     else:
#         st.warning("CSV existiert noch nicht. Starte Producer & Consumer.")
#     time.sleep(REFRESH_DEFAULT)

