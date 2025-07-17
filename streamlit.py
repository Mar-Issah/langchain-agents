import streamlit as st
from weather_info import *
from langsmith import traceable
import os
from dotenv import load_dotenv

load_dotenv()


# I added the project name to the .env file but this took precedence
@traceable(name="streamlit_agents_1")
def main():
    pages = {
        "LANGCHAIN AGENTS": [
            st.Page("basic_calculator.py", title="Basic Calculator : +  -  *  /  ^"),
            st.Page("weather_info.py", title="Weather Information"),
            st.Page("manage_account.py", title="Manage your account"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
