import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_openai import ChatOpenAI
from tools import get_current_datetime, get_location_from_ip
from langchain_community.agent_toolkits.load_tools import load_tools


os.environ.get("SERPAPI_API_KEY")
os.environ.get("OPENAI_API_KEY")

st.subheader("Weather Information")


def weather(query: str):
    """Sample function to demonstrate the agent's functionality."""

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.0,
    )
    toolbox = load_tools(tool_names=["serpapi"], llm=llm)

    # we are not including the chat history in the agent's input
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you're a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    tools = toolbox + [get_current_datetime, get_location_from_ip]
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # for step in agent_executor.stream({"input": [query]}):
    #     response = step["messages"][-1]

    response = agent_executor.invoke(
        {
            "input": query,
            # "chat_history": memory,
        }
    )

    return response


query = st.text_input(
    "Enter a text: ", placeholder="What is the current weather here in NYC?"
)
if st.button("Submit"):
    if not query:
        st.warning("Please enter a query to get the weather information.")
        st.stop()
    with st.spinner("Fetching weather information..."):
        # Call the weather function with the user's query
        response = weather(query)
        st.success(response.get("output"))
