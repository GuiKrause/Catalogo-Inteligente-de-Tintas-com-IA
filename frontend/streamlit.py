import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AGENT_API_URL = os.getenv("AGENT_API_URL")

def question_api(question: str) -> str:
    response = requests.post(
        f'{AGENT_API_URL}/ask',
        json={"question": question},
        timeout=60
    )
    return response.json()["answer"]


st.set_page_config(page_title="Catálogo de Tintas", page_icon="🎨")

st.title("Catálogo Inteligente de Tintas")
st.subheader("Tire suas dúvidas sobre as tintas do nosso catálogo")

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
