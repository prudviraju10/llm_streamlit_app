from langchain_groq import ChatGroq
import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from llm.model import chain
from src.functions import messages_print

st.title("CHAT WITH LLAMA MODEL")


def response_generator(lst):
    for r in chain.stream({"messages": lst, }):
        yield r.content


if "messages_chat" not in st.session_state:
    st.session_state.messages_chat = []

lst = messages_print(st.session_state.messages_chat)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        lst.append(HumanMessage(content=prompt))
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(lst))
    st.session_state.messages_chat.append(
        {"role": "assistant", "content": response})
