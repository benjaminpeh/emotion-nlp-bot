# app.py
import streamlit as st
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="SafeSpace: Scam Alert for Seniors", layout="centered")

# --- Title and Welcome Message ---
st.markdown("<h1 style='font-size: 50px;'>🛡️ SafeSpace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 28px;'>Helping our seniors detect and report scams with ease</h3>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Main Navigation ---
st.write("### What would you like to do?")
choice = st.selectbox("Navigate:", ["👀 Learn to Detect Scams (Quiz)", "📢 Report a Scam", "📞 Scam Help & Resources"])

# --- Redirect based on choice ---
if choice == "👀 Learn to Detect Scams (Quiz)":
    st.switch_page("pages/2_Scam_Quiz.py")
elif choice == "📢 Report a Scam":
    st.switch_page("pages/1_Report_Scam.py")
elif choice == "📞 Scam Help & Resources":
    st.switch_page("pages/3_Help_Resources.py")
