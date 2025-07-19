import streamlit as st
from complex_chabot import ChatGraphAgent

# Run the chatbot
query = st.text_input("Enter your query:")
if st.button("Submit"):
    if not query:
        st.warning("Please enter a query to get a response.")
    else:
        with st.spinner("Generating response..."):
            initial_state = {"messages": [], "message_type": None}
            initial_state["messages"].append({"role": "user", "content": query})
            agent = ChatGraphAgent()

            for chunk in agent.stream_responses(initial_state):
                # print(chunk)  # Debugging output
                if chunk is None:
                    continue  # Skip if no update

                if "messages" in chunk:
                    last_msg = chunk["messages"][-1]  # get latest message
                    if last_msg["role"] == "assistant":
                        st.success(last_msg["content"])

                if "message_type" in chunk:
                    st.badge(f"From your {chunk['message_type']} Therapist")

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
