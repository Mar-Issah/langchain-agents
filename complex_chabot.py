import os
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field


# -----------------------------
# THINK OF THIS LIKE AN OUTPUTPARSER
# Pydantic Model for Message Classification. This is used to classify messages from user as either emotional or logical. Lieteral is used to ensure that the message type is either EMOTIONAL or LOGICAL  only.
# -----------------------------
class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical"] = Field(
        ...,
        description="Classify if the message requires an emotional (therapist) or logical response.",  # DESCRIPTION ensures that the field is doing what it is supposed to do.
    )


# Pydantic Model for Person if needed. This is used to define the person object with name, age and message_type.
# class Person(BaseModel):
#     name: str = Field(..., description="Name of the person.")
# 	age: int = Field(..., description="Age of the person.")
# 	message_type: Literal["emotional", "logical"] = Field(
# 		...,
# 		description="Classify if the message requires an emotional (therapist) or logical response.",
# # -----------------------------
# State Definition
# -----------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None


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

    # def _chatbot_node(self, state: State) -> dict:
    #     """Single LLM step: Takes a state and returns a new state with LLM output."""
    #     return {"messages": [self.llm.invoke(state["messages"])]}

    def _classify_message_node(self, state: State):
        """Classify the last message in the state as emotional or logical. Prompting the llm with the system and user message giving it the user query to classify the message type."""
        last_message = state["messages"][-1]
        # Classify the message type from the using the llm structured output model i.e llm comes with a structured output model.
        # Invoke the classifier LLM with the last message content to retrieve the message type.
        classifier_llm = self.llm.with_structured_output(MessageClassifier)
        result = classifier_llm.invoke(
            [
                {
                    "role": "system",
                    "content": """Classify the user message as either:
				- 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems
				- 'logical': if it asks for facts, information, logical analysis, or practical solutions
				""",
                },
                {"role": "user", "content": last_message.content},
            ]
        )
        # Because the llm is a structured output model, we can access the message_type attribute directly.and update the state with the message type.
        return {"message_type": result.message_type}

    def _router_node(self, state: State):
        """Route the conversation based on the message type to either the therapist or logical agent node"""
        message_type = state.get("message_type", "logical")
        if message_type == "emotional":
            return {"next": "therapist"}
        return {"next": "logical"}

    def _therapist_agent_node(self, state: State):
        """Therapist agent: Handles emotional messages.
        Just prompting eng. the node with relevant instructions to the llm to act as a therapist.

                Returns a new state with the LLM's response
        """
        last_message = state["messages"][-1]
        messages = [
            {
                "role": "system",
                "content": """You are a compassionate therapist. Focus on the emotional aspects of the user's message.
							Show empathy, validate their feelings, and help them process their emotions.
							Ask thoughtful questions to help them explore their feelings more deeply.
							Avoid giving logical solutions unless explicitly asked.""",
            },
            {"role": "user", "content": last_message.content},
        ]
        reply = self.llm.invoke(messages)
        return {"messages": [{"role": "assistant", "content": reply.content}]}

    def _logical_agent_(self, state: State):
        """Logical agent: Handles logical messages.
        Promt eng the llm with relevant instructions to act as a logical agent.

                Returns a new state with the LLM's response.
        """
        last_message = state["messages"][-1]
        messages = [
            {
                "role": "system",
                "content": """You are a purely logical assistant. Focus only on facts and information.
				Provide clear, concise answers based on logic and evidence.
				Do not address emotions or provide emotional support.
				Be direct and straightforward in your responses.""",
            },
            {"role": "user", "content": last_message.content},
        ]
        reply = self.llm.invoke(messages)
        return {"messages": [{"role": "assistant", "content": reply.content}]}

    def _build_graph(self):
        """Builds and compiles the LangGraph graph.
        The StateGraph StateGraph Engine:
                When you compile and run the graph, LangGraph automatically manages the state.
                It starts with your initial state (e.g., {"messages": [...]}).
                After each node executes, LangGraph merges the returned dictionary into the current state.
                The updated state is passed to the next node according to the graph's edges.
        """
        graph_builder = StateGraph(State)
        graph_builder.add_node("classifier", self._classify_message_node)
        graph_builder.add_node("router", self._router_node)
        graph_builder.add_node("therapist", self._therapist_agent_node)
        graph_builder.add_node("logical", self._logical_agent_)

        # Add edges to connect the nodes. We aare diagraming the graph here.
        graph_builder.add_edge(START, "classifier")
        graph_builder.add_edge("classifier", "router")
        graph_builder.add_conditional_edges(
            "router",
            lambda state: state.get("next"),
            {"therapist": "therapist", "logical": "logical"},
            # good thing we defined the next in the state when we were creating the router node
        )  # Beacuse the router can move to either the therapist or logical agent node based on the message type.we are using conditional edges to connect the router node to the therapist and logical agent nodes.
        graph_builder.add_edge("therapist", END)
        graph_builder.add_edge("logical", END)
        return graph_builder.compile()

    def stream_responses(self, initial_state: list):
        """Yields streamed chatbot responses (if graph has multiple steps)."""
        # initial_state = {"messages": messages}
        for step in self.graph.stream(initial_state):
            for value in step.values():
                yield value
                # yield value["messages"][-1].content

    def get_response(self, messages: list) -> str:
        """Returns only the final chatbot message (non-streaming)."""
        return next(self.stream_responses(messages))
