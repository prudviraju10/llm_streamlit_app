import streamlit as st

home_p = st.Page("pages/home.py", title="home")
llm_on_documents_p = st.Page(
    "pages/document_query.py", title="llm_on_documents")

pg = st.navigation(
    {
        "Navigation": [home_p, llm_on_documents_p],
    })

st.set_page_config(page_title="LLM Interviewer")
pg.run()
