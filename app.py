import streamlit as st
from textblob import TextBlob
import datetime
import pandas as pd
import altair as alt
import random

st.set_page_config(page_title="MindScape: Mental Wellness Companion", layout="centered")

# --- Theme Toggle ---
theme = st.sidebar.selectbox("🌙 Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """<style>body { background-color: #121212; color: white; }</style>""",
        unsafe_allow_html=True,
    )

# --- Title ---
st.title("🧠 MindScape: Your Mental Wellness Companion")
st.write("A simple, private space to reflect and receive support.")

# --- Mood Input ---
st.subheader("💬 How are you feeling today?")
user_input = st.text_area("Write anything on your mind...")

# Journaling prompts
st.markdown("✍️ *Need inspiration?*")
if st.button("Give me a journaling prompt"):
    prompts = [
        "Describe a moment you felt truly at peace.",
        "Write a letter to your future self.",
        "What would you tell a friend who feels how you do?",
        "What's something small you're grateful for today?",
        "Imagine your ideal calm space — what does it look like?"
    ]
    st.info(random.choice(prompts))

# Mood log storage
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# --- Sentiment Analysis ---
if st.button("Check My Mood"):
    if user_input.strip() == "":
        st.warning("Please enter something before submitting.")
    else:
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity > 0.3:
            mood = "😊 Positive"
            suggestion = "Great! Keep it up. Maybe journal or take a walk outside."
        elif polarity < -0.3:
            mood = "😞 Negative"
            suggestion = "It's okay to feel this way. Consider breathing exercises or calling a friend."
        else:
            mood = "😐 Neutral"
            suggestion = "Try to engage with something relaxing like music or stretching."

        st.success(f"**Detected Mood:** {mood}")
        st.info(f"**Suggestion:** {suggestion}")

        st.session_state.mood_log.append({
            "timestamp": datetime.datetime.now(),
            "mood": mood.split()[1],
            "polarity": polarity
        })

# --- Mood Trend Chart ---
if st.session_state["mood_log"]:
    st.subheader("📊 Mood Tracker Over Time")
    df = pd.DataFrame(st.session_state["mood_log"])
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='timestamp:T',
        y='polarity:Q',
        color=alt.value("#1f77b4"),
        tooltip=['timestamp:T', 'mood', 'polarity']
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

# --- Resources ---
st.subheader("📚 Feeling overwhelmed?")
st.markdown("- [SUTD Mental Wellness](https://www.sutd.edu.sg/Campus-Life/Wellness-Matters)")
st.markdown("- Singapore Mental Health Helpline: 6389 2222")
st.markdown("- Samaritans of Singapore (SOS): 1767")

st.caption("🛡️ All data is stored locally in your browser. Nothing is saved to the cloud.")
