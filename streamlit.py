import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL")

def question_api(question: str) -> str:
    response = requests.post(
        API_URL,
        json={"question": question},
        timeout=60
    )
    return response.json()["answer"]


st.set_page_config(page_title="Chatbot de Tintas", page_icon="🎨")

st.title("Chatbot de Tintas")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Digite sua pergunta sobre tintas...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            answer = question_api(user_input)
            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
