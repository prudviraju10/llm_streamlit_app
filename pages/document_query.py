from langchain_groq import ChatGroq
import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from llm.model import chain_pdf, embeddings, format_docs
from src.functions import extract_text_from_pdf, messages_print
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

st.title("Chat With Your data")


def response_generator_pdf(lst, question):
    retriever = st.session_state.chroma_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 5})
    chain_temp = retriever | format_docs
    context = chain_temp.invoke(question)
    for r in chain_pdf.stream({"messages": lst, "question": question, "context": context}):
        yield r.content


if "chroma_store" not in st.session_state:
    st.session_state.chroma_store = Chroma(embedding_function=embeddings)
if "doc_name" not in st.session_state:
    st.session_state.doc_name = []
if "messages_pdf" not in st.session_state:
    st.session_state.messages_pdf = []

uploaded_files = st.file_uploader("Upload your documents", type=[
                                  "pdf"], accept_multiple_files=True)


if uploaded_files:
    for uploaded_file in uploaded_files:
        document_name = uploaded_file.name
        if document_name not in st.session_state.doc_name:
            st.session_state.doc_name.append(document_name)
            text = extract_text_from_pdf(uploaded_file)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(text)

            documents = [Document(page_content=chunk) for chunk in chunks]

            st.session_state.chroma_store.add_documents(documents=documents)

lst = messages_print(st.session_state.messages_pdf)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages_pdf.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        lst.append(HumanMessage(content=prompt))
    with st.chat_message("assistant"):
        response = st.write_stream(
            response_generator_pdf(lst=lst, question=prompt))
    st.session_state.messages_pdf.append(
        {"role": "assistant", "content": response})
