import streamlit as st
from typing import Annotated
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from tools import add, subtract, multiply, exponentiate, divide
from langsmith import traceable


os.environ.get("LANGCHAIN_API_KEY")
os.environ.get("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = (
    "true"  # THis mean that the entire app will be trace when we execute the code
)

st.subheader("Basic Calculator Agent")


@traceable(name="basic_calculator_agent")
def calculator(query: str):
    """Sample function to demonstrate the agent's functionality."""

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.0,
    )

    # This is now deprecated
    # memory = ConversationBufferMemory(
    #     memory_key="chat_history",  # must align with MessagesPlaceholder variable_name
    #     return_messages=True,  # to return Message objects
    # )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            ("human", "{input}"),
            # Placeholders fill up a **list** of messages
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [add, subtract, multiply, exponentiate, divide]

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = agent_executor.invoke(
        {
            "input": query,
            # "chat_history": memory,
        }
    )
    return response


query = st.text_input("Enter your query:")
if st.button("Submit"):
    response = calculator(query)
    st.success(response["output"])
