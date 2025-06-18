import os
from dotenv import load_dotenv
from typing import TypedDict, List, Union

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import Tool, initialize_agent

from langgraph.graph import StateGraph, END
import gradio as gr

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Step 1: Embedding and Chroma setup
embedding_model = OpenAIEmbeddings(openai_api_key=openai_key)
vectorstore = Chroma(persist_directory="chroma_store", embedding_function=embedding_model)
retriever = vectorstore.as_retriever()

# Step 2: RetrievalQA tool
retrieval_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(openai_api_key=openai_key, temperature=0),
    retriever=retriever,
)

tools = [
    Tool(
        name="JazzCashDocs",
        func=retrieval_chain.run,
        description="Use this tool to answer questions using JazzCash internal documents."
    )
]

# Step 3: Initialize the agent properly
llm = ChatOpenAI(openai_api_key=openai_key, temperature=0)
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    handle_parsing_errors=True,
    verbose=True,
)

# Step 4: Define LangGraph nodes
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

def input_node(state: AgentState) -> AgentState:
    return {"messages": state["messages"]}  # ✅ Ensure dict return

def agent_node(state: AgentState) -> AgentState:
    user_message = state["messages"][-1]
    try:
        result = agent_executor.invoke({"input": user_message.content})
        response_text = result["output"]
    except Exception as e:
        response_text = f"⚠️ Error: {str(e)}"
    updated_messages = state["messages"] + [AIMessage(content=response_text)]
    return {"messages": updated_messages}  # ✅ Ensure dict return

def output_node(state: AgentState) -> AgentState:
    return {"messages": state["messages"]}  # ✅ Ensure dict return

# Step 5: LangGraph build
builder = StateGraph(AgentState)
builder.add_node("input", input_node)
builder.add_node("agent", agent_node)
builder.add_node("output", output_node)
builder.set_entry_point("input")
builder.add_edge("input", "agent")
builder.add_edge("agent", "output")
builder.add_edge("output", END)

graph = builder.compile()

# Step 6: Gradio app
chat_history: List[Union[HumanMessage, AIMessage]] = []

def chat_fn(user_input, history):
    global chat_history
    chat_history.append(HumanMessage(content=user_input))
    state = {"messages": chat_history}
    updated_state = graph.invoke(state)
    final_response = updated_state["messages"][-1].content
    chat_history.append(AIMessage(content=final_response))
    return final_response  # Just return the final assistant message


gr.ChatInterface(chat_fn, title="JazzCash RAG Agent (LangGraph + ChromaDB)").launch()

