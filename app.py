app.py
import streamlit as st
from textblob import TextBlob
import datetime
import pandas as pd
import altair as alt

st.set_page_config(page_title="MindScape: Mental Wellness Companion", layout="centered")

# --- Title ---
st.title("🧠 MindScape: Your Mental Wellness Companion")
st.write("A simple, private space to reflect and receive support.")

# --- Mood Input ---
st.subheader("💬 How are you feeling today?")
user_input = st.text_area("Write anything on your mind...")

# Initialize mood log
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# --- Analyze Sentiment ---
if st.button("Check My Mood"):
    if user_input.strip() == "":
        st.warning("Please enter something before submitting.")
    else:
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity > 0.3:
            mood = "😊 Positive"
            suggestion = "Keep it up! Try journaling or share your happiness with someone."
        elif polarity < -0.3:
            mood = "😞 Negative"
            suggestion = "You seem down. Consider taking deep breaths or reaching out to a friend."
        else:
            mood = "😐 Neutral"
            suggestion = "Stay balanced. Maybe a short walk or break will help."

        st.success(f"**Detected Mood:** {mood}")
        st.info(f"**Suggestion:** {suggestion}")

        st.session_state.mood_log.append({
            "timestamp": datetime.datetime.now(),
            "mood": mood.split()[1],
            "polarity": polarity
        })

# --- Mood History Chart ---
if st.session_state["mood_log"]:
    st.subheader("📊 Mood Tracker")
    df = pd.DataFrame(st.session_state["mood_log"])
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='timestamp:T',
        y='polarity:Q',
        tooltip=['timestamp:T', 'mood', 'polarity']
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

# --- Resources ---
st.subheader("📚 Feeling overwhelmed?")
st.write("- [SUTD Mental Wellness](https://www.sutd.edu.sg/Campus-Life/Wellness-Matters)")
st.write("- Singapore Mental Health Helpline: 6389 2222")
st.write("- Samaritans of Singapore (SOS): 1767")

st.caption("🛡️ All data is stored locally in your browser. Nothing is saved to the cloud.")
