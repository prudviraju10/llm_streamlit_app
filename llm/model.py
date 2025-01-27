from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# llm = ChatGoogleGenerativeAI(model="gemini-pro")
model = ChatGroq(model="llama-3.3-70b-versatile",
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

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=st.secrets["GOOGLE_API_KEY"])

prompt_pdf = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        ("user", """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:)"""),
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain_pdf = prompt_pdf | model

# prompt_pdf.invoke(
#     {"messages": [], "question": "What is up?", "context": "None"})
