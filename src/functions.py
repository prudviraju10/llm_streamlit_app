import fitz
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage


def extract_text_from_pdf(file):
    # Open the PDF file
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    # Iterate over each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def messages_print(messages_list):
    lst = []
    for message in messages_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "user":
                lst.append(HumanMessage(content=message["content"]))
            if message["role"] == "assistant":
                lst.append(SystemMessage(content=message["content"]))
    return lst
