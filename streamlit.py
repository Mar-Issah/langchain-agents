import streamlit as st
from websearch_agent import *
from langsmith import traceable
import os
from dotenv import load_dotenv

load_dotenv()


# I added the project name to the .env file but this took precedence
@traceable(name="streamlit_agents_1", project_name="Langchain Agents")
def main():
    pages = {
        "LANGCHAIN AGENTS": [
            st.Page("basic_calculator.py", title="Basic Calculator : +  -  *  /  ^"),
            st.Page("websearch_agent.py", title="Web Search Agent"),
            st.Page("manage_account.py", title="Manage your account"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
