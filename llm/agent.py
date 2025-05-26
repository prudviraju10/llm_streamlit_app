from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.utilities import ArxivAPIWrapper
from langchain_core.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import streamlit as st

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]


model = init_chat_model(
    "qwen-qwq-32b", model_provider="groq")

# model.invoke("Hello, how are you?")
# model.invoke("what is 30 times 20 and then add 230")

# print(model.invoke(
#     "given a question only give the final answer. question: what is 3 times 2 and then add 2."))


tavily_search_tool = TavilySearch(
    max_results=2,
    topic="general",
)

# tool_arxiv = load_tools(
#     ["arxiv"],
# )

tool_arxiv_wrapper = ArxivAPIWrapper()

tool_arxiv = Tool(
    name="arxiv",
    func=tool_arxiv_wrapper.run,
    description="useful for when you need to answer questions about arxiv papers",
)

api_wrapper_wiki = WikipediaAPIWrapper(
    top_k_results=1, doc_content_chars_max=100000)
wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}, with tempratrues at 35 degrees celsius!"


agent = create_react_agent(
    model=model,
    tools=[get_weather, tavily_search_tool, tool_arxiv, wikipedia],
    prompt="You are a helpful assistant"
)

# Run the agent
# agent.invoke(
# {"messages": [{"role": "user", "content": "what is team india and england squads selected for 2025 india tour of england test series"}]})
# agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the paper 1605.08386 about?"}]})

# agent.invoke(
#     {"messages": [{"role": "user", "content": "when is birthdate of rahul gandhi "}]})
