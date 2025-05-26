import sys
import streamlit as st
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

home_p = st.Page("pages/home.py", title="home")
llm_on_documents_p = st.Page(
    "pages/document_query.py", title="llm_on_documents")
agent_llm_p = st.Page("pages/agent_llm.py", title="agent_llm")

pg = st.navigation(
    {
        "Navigation": [home_p, llm_on_documents_p, agent_llm_p],
    })

st.set_page_config(page_title="LLM Interviewer")
pg.run()
