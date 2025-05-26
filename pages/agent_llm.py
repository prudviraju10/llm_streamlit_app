from langchain_groq import ChatGroq
import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from llm.agent import agent
from src.functions import messages_print

st.title("CHAT WITH AN AI AGENT")
st.text("with tools websearch, arxiv, wikipedia")


def response_generator_agent(lst):
    if len(lst) != 1:
        lst = lst[-3:]
    result = agent.invoke({"messages": lst})
    print(result)
    # print(result["messages"][-1])
    # print(result["messages"][-1].content)
    return result["messages"][-1].content


if "messages_chat_agent" not in st.session_state:
    st.session_state.messages_chat_agent = []

lst = messages_print(st.session_state.messages_chat_agent)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages_chat_agent.append(
        {"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        lst.append(HumanMessage(content=prompt))
    with st.chat_message("assistant"):
        response = response_generator_agent(lst)
        response_st = st.write(response)
    st.session_state.messages_chat_agent.append(
        {"role": "assistant", "content": response})

print(st.session_state.messages_chat_agent)
