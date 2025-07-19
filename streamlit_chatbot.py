import streamlit as st
from simple_chatbot import ChatGraphAgent

# Run the chatbot
query = st.text_input("Enter your query:")
if st.button("Submit"):
    if not query:
        st.warning("Please enter a query to get a response.")
    else:
        with st.spinner("Generating response..."):
            # initial_state = {"messages": [{"role": "user", "content": query}]}
            initial_state = [{"role": "user", "content": query}]
            agent = ChatGraphAgent()
            st.write_stream(agent.stream_responses(initial_state))
            for chunk in agent.stream_responses(initial_state):
                st.success(chunk)

    # Chat input
    # prompt: str = st.chat_input("Enter a prompt here")

    # if prompt:
    #     model_response = get_response(prompt)

    #     if model_response:
    #         st.sidebar.write("Summary of your chat.")
    #         # summarise_btn = st.sidebar.button("Summarise the conversation", key="summarise", type="secondary")
    #         st.sidebar.write(summarize_conversation(st.session_state["previous_chat"]))

    #       #   if summarise_btn:
    #       #      st.sidebar.write(summarize_conversation(st.session_state["previous_chat"]))

    #         with st.container():
    #             for msg in model_response.messages:
    #                 if isinstance(msg, HumanMessage):
    #                     st.chat_message("user").write(msg.content)
    #                 elif isinstance(msg, AIMessage):
    #                     st.chat_message("assistant").write(msg.content)
