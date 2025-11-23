import streamlit as st
import pandas as pd
import time
from pathlib import Path

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700&display=swap');

/* 
   🔥 Alle Headline-Tags überschreiben,
   egal welche emotion/cache Klasse Streamlit erzeugt
*/
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter Tight', sans-serif !important;
}

/* 
   🔥 Auch WENN Streamlit eine hochspezifische dynamische Klasse generiert
   → diese Version schlägt alles
*/
[class^="st-emotion-cache"] h1,
[class^="st-emotion-cache"] h2,
[class^="st-emotion-cache"] h3,
[class^="st-emotion-cache"] h4,
[class^="st-emotion-cache"] h5,
[class^="st-emotion-cache"] h6 {
    font-family: 'Inter', sans-serif !important;
}

</style>
""", unsafe_allow_html=True)

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "stock_prices.csv"
st.title("Live Aktien Dashboard")
st.write("Daten werden live aus Kafka → Consumer → CSV geladen.")

refreshrate = st.slider("Aktualisierungs-Intervall (Sekunden)", 1, 10, 3)
placeholder = st.empty()

while True:
    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["timestamp"].dt.strftime("%H:%M")
        df["time_full"] = df["timestamp"].dt.strftime("%d.%m.%y %H:%M")
        
        latest = df.tail(200)
        with placeholder.container():
            st.subheader("Live Stock Prices")
            chart_df = latest.pivot(index="timestamp", columns="symbol", values="price")
            st.line_chart(chart_df)

            st.subheader("Letzte Datenpunkte")
            st.dataframe(df[["time_full", "symbol", "price"]].tail(10))
    else:
        st.warning("CSV existiert noch nicht. Starte Producer & Consumer.")

    time.sleep(refreshrate)
