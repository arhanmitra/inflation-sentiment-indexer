import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

st.set_page_config(page_title="Inflation Sentiment Indexer", layout="wide")

st.title("📊 Inflation Sentiment Indexer")
st.caption("Tracking news sentiment around inflation and cost of living")

@st.cache_data(ttl=300)
def load_data():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT title, source, published_at, sentiment, confidence
        FROM headlines
        WHERE sentiment IS NOT NULL
        ORDER BY published_at DESC
    """, conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No scored headlines yet. Run fetcher.py and sentiment.py first.")
else:
    df["published_at"] = pd.to_datetime(df["published_at"])
    df["date"] = df["published_at"].dt.date

    # Map sentiment to a numeric score: positive = 1, neutral = 0, negative = -1
    sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
    df["score"] = df["sentiment"].map(sentiment_map)

    # Calculate daily average sentiment
    daily = df.groupby("date")["score"].mean().reset_index()
    daily.columns = ["date", "sentiment_index"]

    # --- Top metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Headlines", len(df))
    col2.metric("Positive %", f"{(df['sentiment'] == 'positive').mean() * 100:.1f}%")
    col3.metric("Negative %", f"{(df['sentiment'] == 'negative').mean() * 100:.1f}%")

    # --- Sentiment index chart ---
    st.subheader("Sentiment Index Over Time")
    fig = px.line(daily, x="date", y="sentiment_index", markers=True)
    fig.update_layout(yaxis_range=[-1, 1])
    st.plotly_chart(fig, use_container_width=True)

    # --- Sentiment breakdown ---
    st.subheader("Sentiment Breakdown")
    breakdown = df["sentiment"].value_counts().reset_index()
    breakdown.columns = ["sentiment", "count"]
    fig2 = px.pie(breakdown, names="sentiment", values="count",
                  color="sentiment",
                  color_discrete_map={"positive": "green", "negative": "red", "neutral": "gray"})
    st.plotly_chart(fig2, use_container_width=True)

    # --- Raw headlines table ---
    st.subheader("Headlines")
    st.dataframe(df[["published_at", "source", "title", "sentiment", "confidence"]],
                 use_container_width=True)