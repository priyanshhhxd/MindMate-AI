import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_ai_response
import matplotlib.pyplot as plt
import os  # ✅ Needed to safely check file

# Set up page config
st.set_page_config(page_title="MindMate AI", page_icon="🧠", layout="centered")

# App Title
st.title("🧠 MindMate AI")
st.markdown("Your personal mental health companion powered by AI")

# Create all 3 tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat with AI", "📓 Mood Journal", "📈 Mood Insights"])

# ================================
# 💬 Tab 1: Chat with MindMate AI
# ================================
with tab1:
    st.subheader("How are you feeling today?")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None
    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []

    user_input = st.text_area("Share anything that's on your mind...", height=150, key="chat_input")

    if st.button("🧠 Talk to MindMate"):
        if user_input.strip() == "":
            st.warning("Please write something before submitting.")
        else:
            with st.spinner("MindMate is listening..."):
                try:
                    response, chat_history = get_ai_response(user_input, st.session_state.chat_history)
                    st.session_state.chat_history = chat_history
                    st.session_state.chat_log.append(("🧑 You", user_input))
                    st.session_state.chat_log.append(("🧠 MindMate", response))
                except Exception as e:
                    st.error(f"❌ Error generating response: {e}")

    for sender, msg in st.session_state.chat_log:
        st.markdown(f"**{sender}:** {msg}")

# ================================
# 📓 Tab 2: Mood Journal
# ================================
with tab2:
    st.subheader("Daily Mood Tracker")

    mood = st.selectbox("Select your mood today:", [
        "😊 Happy", "😢 Sad", "😡 Angry", "😰 Anxious", "😌 Calm", "😴 Tired"
    ])
    note = st.text_area("Write a short note about your mood", key="mood_note")

    if st.button("📝 Save Mood"):
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mood": mood,
            "note": note
        }

        try:
            df = pd.read_csv("mood_log.csv")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=["date", "mood", "note"])

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv("mood_log.csv", index=False)
        st.success("✅ Mood saved successfully!")

# ================================
# 📈 Tab 3: Mood Insights
# ================================
with tab3:
    st.subheader("📈 Your Mood Trends Over Time")

    try:
        if os.path.exists("mood_log.csv") and os.path.getsize("mood_log.csv") > 0:
            df = pd.read_csv("mood_log.csv")

            if df.empty:
                st.info("Mood log is empty. Start tracking to see trends.")
            else:
                df["date"] = pd.to_datetime(df["date"])
                mood_counts = df.groupby(["date", "mood"]).size().unstack(fill_value=0)
                st.line_chart(mood_counts)
        else:
            st.info("No mood data available yet. Start tracking to visualize your mood.")
    except Exception as e:
        st.error(f"⚠️ Error loading mood log: {e}")
