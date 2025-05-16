from typing import Annotated, Literal
from typing_extensions import TypedDict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableSerializable, Runnable
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from agent_ai.database import get_vector_store
from agent_ai.environment import Environment
from agent_ai.travel_tools import recommend_destinations, suggest_budget, suggest_transport

class TravelState(TypedDict):
    messages: Annotated[list, add_messages]
    interests: str
    transport: str
    budget_min: int
    budget_max: int
    travel_days: int
    start_location: str

Destinations = Literal["Barcelona", "Prague", "Rome", "Athens", "Slovenia", "Norway"]

class TravelAgent:
    def __init__(self) -> None:
        self.environment = Environment()
        self.tools = self.get_tools()
        self.llm = self.get_llm()
        self.embeddings = self.get_embeddings()
        self.retriever = self.get_retriever()
        self.prompt = self.get_prompt()
        self.chain = self.get_chain()
        self.graph = self.get_empty_compiled_graph()

    def get_chain(self) -> RunnableSerializable:
        chain: RunnableSerializable = (
            {
                "context": RunnableLambda(lambda x: x["messages"][-1].content),
                "messages": lambda x: x["messages"],
                "interests": lambda x: x["interests"],
                "transport": lambda x: x["transport"],
                "budget_min": lambda x: x["budget_min"],
                "budget_max": lambda x: x["budget_max"],
                "travel_days": lambda x: x["travel_days"],
                "start_location": lambda x: x["start_location"],
            }
            | self.prompt
            | self.llm
        )
        return chain

    def get_prompt(self) -> ChatPromptTemplate:
        system_prompt = """
            You are an AI travel assistant named TravelAgent.
            Your task is to help the user plan their perfect trip.
            Ask for preferences, suggest two destinations, and create a day-by-day travel itinerary.

            Below are knowledge base details (about cities, attractions, etc.):
            {context}

            User preferences:
            - Interests: {interests}
            - Transport: {transport}
            - Budget: from {budget_min} to {budget_max} PLN
            - Number of travel days: {travel_days}
            - Starting location: {start_location}
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])

    def get_embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            api_key=self.environment.openai_api_key.get_secret_value(),
            model="text-embedding-3-small"
        )

    def get_retriever(self):
        return get_vector_store(
            embeddings=self.embeddings,
            qdrant_url=self.environment.qdrant_url,
            qdrant_api_key=self.environment.qdrant_api_key
        ).as_retriever()

    def get_tools(self) -> list:
        return [recommend_destinations, suggest_transport, suggest_budget]

    def get_llm(self) -> Runnable:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)
        llm_with_tools = llm.bind_tools(self.tools)
        return llm_with_tools

    def agent(self, state: TravelState) -> dict[str, list]:
        return {"messages": [self.chain.invoke(state)]}

    def get_empty_compiled_graph(self) -> CompiledStateGraph:
        memory = MemorySaver()
        graph_builder = StateGraph(TravelState)

        tool_node = ToolNode(tools=self.tools)
        graph_builder.add_node("agent", self.agent)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge(START, "agent")

        return graph_builder.compile(checkpointer=memory)


travel_agent = TravelAgent()
