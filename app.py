import streamlit as st
from textblob import TextBlob
import datetime
import pandas as pd
import altair as alt
import random

# --- Streamlit Page Setup ---
st.set_page_config(page_title="MindScape: Personalised Mental Wellness Companion", layout="centered")

# --- Title ---
st.title("🧠 MindScape: Your Personalised Mental Wellness Companion")
st.write("Check in with yourself, journal safely, and receive supportive reflection prompts.")

# --- Mood Input ---
st.subheader("💬 How are you feeling today?")
user_input = st.text_area("Write anything on your mind...")

# --- Journaling Prompts ---
st.markdown("✍️ *Need inspiration?*")
if st.button("Give me a journaling prompt"):
    prompts = [
        "Describe a moment you felt truly at peace.",
        "Write a letter to your future self.",
        "What's something small you're grateful for today?",
        "Imagine your ideal calm space — what does it look like?"
    ]
    st.info(random.choice(prompts))

# --- Session state to track mood history ---
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# --- Function: Basic NLP Response Engine ---
def generate_personalised_response(text):
    text_lower = text.lower()

    if any(word in text_lower for word in ["anxious", "nervous", "worried", "overthinking"]):
        return "It sounds like you're feeling anxious. Try writing down 3 things that are within your control right now."
    elif any(word in text_lower for word in ["tired", "burnt out", "exhausted", "drained"]):
        return "You might be experiencing burnout. Consider reflecting on what you could let go of or say no to today."
    elif any(word in text_lower for word in ["lonely", "alone", "isolated"]):
        return "Feeling alone can be heavy. Try journaling about someone who made you feel seen in the past."
    elif any(word in text_lower for word in ["happy", "grateful", "excited"]):
        return "That's wonderful! Would you like to write a gratitude letter or reflect on what brought that joy?"
    elif any(word in text_lower for word in ["sad", "down", "depressed"]):
        return "Thanks for opening up. Consider writing about one small act of kindness you've experienced."
    else:
        return "Thanks for sharing. Try journaling about what triggered that feeling — or what you need more of right now."

# --- Mood + AI Coach ---
if st.button("Check My Mood"):
    if user_input.strip() == "":
        st.warning("Please enter something before submitting.")
    else:
        # Sentiment
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity > 0.3:
            mood = "😊 Positive"
        elif polarity < -0.3:
            mood = "😞 Negative"
        else:
            mood = "😐 Neutral"

        st.success(f"**Detected Mood:** {mood}")

        # Log mood
        st.session_state["mood_log"].append({
            "timestamp": datetime.datetime.now(),
            "mood": mood.split()[1],
            "polarity": polarity
        })

        # Local rule-based personalised response
        with st.spinner("AI Coach is thinking..."):
            reply = generate_personalised_response(user_input)
            st.info(f"🧠 **Personalised Coach says:**\n\n{reply}")

# --- Mood Tracker Chart ---
if st.session_state["mood_log"]:
    st.subheader("📊 Mood Tracker Over Time")
    df = pd.DataFrame(st.session_state["mood_log"])
    df
