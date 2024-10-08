import streamlit as st
import json
import uuid
import requests
import pandas as pd

def get_random_question(file_path):
    df = pd.read_csv(file_path)
    return df.sample(n=1).iloc[0]["question"]

def ask_question(url, question):
    data = {"question": question}
    response = requests.post(url, json=data)
    return response.json()

def send_feedback(url, conversation_id, feedback):
    feedback_data = {"conversation_id": conversation_id, "feedback": feedback}
    response = requests.post(f"{url}/feedback", json=feedback_data)
    return response.status_code

st.set_page_config(page_title="Find an HR surgeon", page_icon="❓", layout="wide")
st.title("Find an HR surgeon")

base_url = "http://localhost:5000"
csv_file = "Find-a-Doctor/data/ground-truth-retrieval.csv"

# Sidebar
st.sidebar.title("Settings")
use_random_questions = st.sidebar.checkbox("Use random questions from our data set")

# Initialize session state
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'answer' not in st.session_state:
    st.session_state.answer = ""
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = ""

# Main content
if use_random_questions:
    if st.button("Get Random Question"):
        st.session_state.question = get_random_question(csv_file)
    st.info(f"Random question: {st.session_state.question}")
else:
    st.session_state.question = st.text_input("Enter your question:", value=st.session_state.question)

if st.button("Get Answer"):
    if st.session_state.question:
        with st.spinner("Getting answer..."):
            response = ask_question(f"{base_url}/question", st.session_state.question)

        st.session_state.answer = response.get("answer", "No answer provided")
        st.session_state.conversation_id = response.get("conversation_id", str(uuid.uuid4()))

if st.session_state.answer:
    st.subheader("Answer:")
    st.write(st.session_state.answer)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Positive"):
            status = send_feedback(base_url, st.session_state.conversation_id, 1)
            st.success(f"Positive feedback sent. Status code: {status}")
    with col2:
        if st.button("👎 Negative"):
            status = send_feedback(base_url, st.session_state.conversation_id, -1)
            st.error(f"Negative feedback sent. Status code: {status}")
    with col3:
        if st.button("⏭️ Skip feedback"):
            st.info("Feedback skipped.")
else:
    st.warning("Please enter a question or use a random question, then click 'Get Answer'.")
