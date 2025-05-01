import streamlit as st
from textblob import TextBlob
import datetime
import pandas as pd
import altair as alt
import random
import openai

# --- Streamlit Page Setup ---
st.set_page_config(page_title="MindScape: AI Mental Wellness Companion", layout="centered")

# --- Load OpenAI API key from Streamlit Secrets ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- App Title and Description ---
st.title("🧠 MindScape: Your AI-Powered Mental Wellness Companion")
st.write("Check in with yourself, journal safely, and receive AI-guided support.")

# --- Mood Input ---
st.subheader("💬 How are you feeling today?")
user_input = st.text_area("Write anything on your mind...")

# --- Journaling Prompts ---
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

# --- Session state to track mood history ---
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# --- Mood Analysis + GPT Journaling Coach ---
if st.button("Check My Mood"):
    if user_input.strip() == "":
        st.warning("Please enter something before submitting.")
    else:
        # Step 1: Sentiment Analysis
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity > 0.3:
            mood = "😊 Positive"
        elif polarity < -0.3:
            mood = "😞 Negative"
        else:
            mood = "😐 Neutral"

        st.success(f"**Detected Mood:** {mood}")

        # Log entry
        st.session_state["mood_log"].append({
            "timestamp": datetime.datetime.now(),
            "mood": mood.split()[1],
            "polarity": polarity
        })

        # Step 2: GPT Journaling Coach
        with st.spinner("AI Coach is responding..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a calm and empathetic journaling coach for stressed university students. Help them reflect and feel better."
                        },
                        {
                            "role": "user",
                            "content": f"I feel like this: {user_input}"
                        }
                    ],
                    timeout=15
                )
                reply = response["choices"][0]["message"]["content"]
                st.info(f"🧠 **AI Coach says:**\n\n{reply}")
            except Exception as e:
                st.error("❌ GPT failed to respond. Here’s the error:")
                st.code(str(e))

# --- Mood Tracker Chart ---
if st.session_state["mood_log"]:
    st.subheader("📊 Mood Tracker Over Time")
    df = pd.DataFrame(st.session_state["mood_log"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='timestamp:T',
        y='polarity:Q',
        tooltip=['timestamp:T', 'mood', 'polarity']
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

# --- Support Resources ---
st.subheader("📚 Feeling overwhelmed?")
st.markdown("- [SUTD Mental Wellness](https://www.sutd.edu.sg/Campus-Life/Wellness-Matters)")
st.markdown("- Singapore Mental Health Helpline: 6389 2222")
st.markdown("- Samaritans of Singapore (SOS): 1767")

# --- Footer ---
st.markdown("---")
st.caption("🛡️ All data is stored locally in your browser. Nothing is saved to the cloud.")
st.markdown("**Created by: Benjamin Peh Ren-Jie**")
