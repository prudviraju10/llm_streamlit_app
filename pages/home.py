from langchain_groq import ChatGroq
import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from llm.model import chain

st.title("CHAT WITH LLAMA MODEL")


def response_generator(lst):
    for r in chain.stream({"messages": lst, }):
        yield r.content


if "messages" not in st.session_state:
    st.session_state.messages = []

lst = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "user":
            lst.append(HumanMessage(content=message["content"]))
        if message["role"] == "assistant":
            lst.append(SystemMessage(content=message["content"]))

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        lst.append(HumanMessage(content=prompt))
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(lst))
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
