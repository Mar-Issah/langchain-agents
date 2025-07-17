import streamlit as st
from main import calculator


st.subheader("Basic Calculator Agent")
query = st.text_input("Enter your query:")
if st.button("Submit"):
    response = calculator(query)
    st.success("Response:", response)
