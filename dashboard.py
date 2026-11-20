# import sqlite3, pandas as pd, streamlit as st
# from llm import analyze

# st.set_page_config(page_title="Equipment Monitor", layout="wide")
# st.title("⚡ GenAI Equipment Monitoring Assistant")

# LIMITS = {"temperature": (0, 70), "voltage": (22, 26), "current": (0, 6)}
# UNITS = {"temperature": "°C", "voltage": "V", "current": "A"}

# def load():
#     with sqlite3.connect("readings.db") as c:
#         return pd.read_sql("SELECT * FROM readings ORDER BY rowid", c)

# @st.fragment(run_every=3)
# def live():
#     df = load()
#     if df.empty:
#         st.info("Waiting for data...")
#         return
#     last = df.iloc[-1]

#     cols = st.columns(3)
#     faults = []
#     for col, k in zip(cols, LIMITS):
#         lo, hi = LIMITS[k]
#         ok = lo <= last[k] <= hi
#         if not ok:
#             faults.append(k)
#         col.metric(k.title(), f"{last[k]:.1f} {UNITS[k]}",
#                    "OK" if ok else "OUT OF RANGE",
#                    delta_color="normal" if ok else "inverse")

#     if faults:
#         st.error("⚠️ Out of range: " + ", ".join(faults))
#     else:
#         st.success("✅ All readings normal")

#     st.line_chart(df[["temperature", "voltage", "current"]].tail(100))

# live()

# st.subheader("🤖 AI Diagnosis")
# if st.button("Analyze current readings"):
#     df = load()
#     if df.empty:
#         st.warning("No data yet.")
#     else:
#         with st.spinner("AI is analyzing... (can take 10-60 seconds on a local model)"):
#             st.markdown(analyze(df))


import sqlite3
import pandas as pd
import streamlit as st
from llm import analyze

st.set_page_config(page_title="Equipment Monitor", layout="wide")
st.title("⚡ GenAI Equipment Monitoring Assistant")

LIMITS = {"temperature": (0, 70), "voltage": (22, 26), "current": (0, 6)}
UNITS = {"temperature": "°C", "voltage": "V", "current": "A"}


def load():
    with sqlite3.connect("readings.db") as c:
        return pd.read_sql("SELECT * FROM readings ORDER BY rowid", c)


@st.fragment(run_every=3)
def live():
    df = load()
    if df.empty:
        st.info("Waiting for data...")
        return
    last = df.iloc[-1]

    cols = st.columns(3)
    faults = []
    for col, k in zip(cols, LIMITS):
        lo, hi = LIMITS[k]
        ok = lo <= last[k] <= hi
        if not ok:
            faults.append(k)
        col.metric(k.title(), f"{last[k]:.1f} {UNITS[k]}",
                   "OK" if ok else "OUT OF RANGE",
                   delta_color="normal" if ok else "inverse")

    if faults:
        st.error("⚠️ Out of range: " + ", ".join(faults))
    else:
        st.success("✅ All readings normal")

    c1, c2, c3 = st.columns(3)
    c1.caption("Temperature (°C)")
    c1.line_chart(df["temperature"].tail(100))
    c2.caption("Voltage (V)")
    c2.line_chart(df["voltage"].tail(100))
    c3.caption("Current (A)")
    c3.line_chart(df["current"].tail(100))


live()

st.subheader("🤖 AI Diagnosis")
if st.button("Analyze current readings"):
    df = load()
    if df.empty:
        st.warning("No data yet.")
    else:
        with st.spinner("AI is analyzing..."):
            try:
                st.markdown(analyze(df))
            except Exception as e:
                st.error(f"AI request failed: {e}")