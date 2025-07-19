import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model


# -----------------------------
# State Definition
# -----------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]


# -----------------------------
# Chat Agent Class
# -----------------------------
class ChatGraphAgent:
    def __init__(self):
        self.llm = self._init_llm()
        self.graph = self._build_graph()

    def _init_llm(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not set in environment variables."
            )
        return init_chat_model("anthropic:claude-3-5-sonnet-latest")

    def _chatbot_node(self, state: State) -> dict:
        """Single LLM step: Takes a state and returns a new state with LLM output."""
        return {"messages": [self.llm.invoke(state["messages"])]}

    def _build_graph(self):
        """Builds and compiles the LangGraph graph."""
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self._chatbot_node)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)
        return graph_builder.compile()

    def stream_responses(self, messages: list):
        """Yields streamed chatbot responses (if graph has multiple steps)."""
        initial_state = {"messages": messages}
        for step in self.graph.stream(initial_state):
            for value in step.values():
                yield value["messages"][-1].content

    def get_response(self, messages: list) -> str:
        """Returns only the final chatbot message (non-streaming)."""
        return next(self.stream_responses(messages))


if __name__ == "__main__":
    agent = ChatGraphAgent()

    # Example conversation history
    user_messages = [
        {"role": "user", "content": "What is LangGraph and how does it work?"}
    ]

    # For final response
    response = agent.get_response(user_messages)
    print("Final response:", response)

    # For streaming (if needed)
    # for chunk in agent.stream_responses(user_messages):
    #     print("Streamed chunk:", chunk)
