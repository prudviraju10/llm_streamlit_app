from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI


# llm = ChatGoogleGenerativeAI(model="gemini-pro")
model = ChatGroq(model="llama-3.1-70b-versatile",
                 api_key=st.secrets["GROQ_API_KEY"])

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model
