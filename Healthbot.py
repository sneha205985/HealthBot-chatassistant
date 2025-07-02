import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import time


# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Initialize HealthBot Chat Assistant heading
#st.markdown(
#    """
#    <div style='position: relative; top: 0px; left: 0px; padding-left: 10px; padding-top: 5px; text-align: left;'>
#        <span style='font-size: 28px; font-weight: bold; color: red; font-family: Arial;'>
#            HealthBot Chat Assistant
#        </span>
#    </div>
#    """,
#    unsafe_allow_html=True
#)

# Create a placeholder
title_placeholder = st.empty()

# Inject HTML & CSS for top-left positioning
with title_placeholder:
    st.markdown(
        """
        <div id="temp-title" style="
            position: fixed;
            top: 40px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 38px;
            font-weight: bold;
            color: red;
            font-family: 'Arial', sans-serif;
            background-color: white;
            padding: 10px 20px;
            z-index: 9999;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        ">
            HealthBot Chat Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

# Wait 10 seconds
time.sleep(3)

# Clear the placeholder
title_placeholder.empty()

# Initialize HealthBot Chat Assistant heading
st.markdown(
    """
    <div style='position: relative; top: 0px; left: 0px; padding-left: 10px; padding-top: 5px; text-align: left;'>
        <span style='font-size: 28px; font-weight: bold; color: red; font-family: Arial;'>
            HealthBot Chat Assistant
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


# --- Welcome and Instructions ---
st.markdown(
    """
    <div style='text-align: center;'>
        <div style='font-size: 37px; font-weight: bold; font-family: Arial; margin-top: 60px;'>
            WELCOME! HOPE YOU ARE DOING WELL.
        </div>
        <p style='font-size: 16px; font-family: Arial; margin-top: 20px;'>
            This HealthBot will help you identify diseases based on symptoms.<br>
            Please enter your symptoms below, and then ask health-related follow-up questions.<br><br>
            <strong>Note:</strong> This is for informational use only. Always consult a real doctor.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Session state setup ---
if "symptoms" not in st.session_state:
    st.session_state.symptoms = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step 1: Enter Patient Symptoms
st.markdown("### Step 1: Enter Patient's Symptoms")
st.caption("Submit Symptoms")

# Text input box for symptoms
symptoms_input = st.text_input("Example: fever, sore throat, fatigue", key="symptom_input")

# Submit button
if st.button("Submit Symptoms"):
    if symptoms_input.strip() != "":
        st.session_state.symptoms = symptoms_input.strip()
        st.success("✅ Symptoms submitted successfully.")
        st.markdown("**✅ Symptoms received. Now you can ask your health-related question below:**")
    else:
        st.warning("⚠️ Please enter some symptoms.")

# --- Show message to proceed ---
if st.session_state.symptoms:
    st.markdown("**✅ Symptoms received. Now you can ask your health-related question below:**")
else:
    st.warning("⚠️ Please enter patient’s symptoms to begin diagnosis.")

# --- Step 2: Follow-up Chat Input ---
user_query = st.chat_input("Ask your health-related question...")

# --- Step 3: Handle Input & Response ---
if user_query:
    if st.session_state.symptoms == "":
        bot_reply = "⚠️ Please enter the patient's symptoms first."
    else:
        user_query_lower = user_query.lower()
        prompt = ""

        if "disease" in user_query_lower and not any(w in user_query_lower for w in ["cure", "remedy", "treatment"]):
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY predict the most likely disease(s).
DO NOT include causes, remedies, or any other information.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif any(w in user_query_lower for w in ["cure", "remedy", "treatment"]):
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY provide remedies, treatments, or cures.
DO NOT mention disease names unless asked.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif "symptom" in user_query_lower:
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY explain the likely symptoms or how they relate.
DO NOT include disease name, remedies, or causes.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif "cause" in user_query_lower:
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY describe the possible causes of the condition.
DO NOT include symptoms, disease name, or remedies.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif "doctor" in user_query_lower or "consult" in user_query_lower:
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY provide doctor consultation advice.
DO NOT include disease name, causes, or remedies.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif "prevention" in user_query_lower:
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY suggest general prevention tips related to the suspected condition.
DO NOT include disease names or medications.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif any(w in user_query_lower for w in ["diet", "nutrition"]):
            prompt = f"""
You are a medical assistant. Based on the symptoms below, ONLY suggest healthy diet and nutritional habits
that may help the user stay fit or recover better. Avoid giving any medicine names or diagnosis.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        elif "medicine" in user_query_lower or "medication" in user_query_lower:
            prompt = f"""
You are a medical assistant. Based on the symptoms below, provide some basic over-the-counter medications
that are commonly used, but always include a warning: "**If symptoms persist or worsen, consult a doctor.**"

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        else:
            prompt = f"""
You are a medical assistant. Help the user based on the symptoms and the query.

Symptoms: {st.session_state.symptoms}
User Question: {user_query}
"""

        # Get response from model
        response = model.generate_content(prompt)
        bot_reply = response.text

    # Save to history
    st.session_state.chat_history.append(("user", user_query))
    st.session_state.chat_history.append(("assistant", bot_reply))

# --- Display Chat History ---
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").markdown(message)

# --- Reset Button ---
if st.button("🔁 Reset Conversation"):
    st.session_state.symptoms = ""
    st.session_state.chat_history = []
    st.success("Chat reset successfully.")
