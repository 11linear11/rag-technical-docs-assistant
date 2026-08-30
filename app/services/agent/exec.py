# # pyrefly: ignore [missing-import]
from app.services.tools.retriever_tool import retriever_tool
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.agent.prompt import agent_prompt,SYSTEM_PROMPT
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
import asyncio


tools = [retriever_tool]

llm = ChatOpenAI(
    base_url=settings.llm_base_url,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
    max_tokens=settings.llm_max_tokens,
    api_key=settings.api_key,
)



class State(TypedDict):
    messages: Annotated[list,add_messages]
    

tool_node = ToolNode(tools)

def call_llm_node(state: State):
    messages = state["messages"]

    system_instruction = SystemMessage(
        content=SYSTEM_PROMPT
    )
    full_message = [system_instruction] + messages

    llm_with_tool = llm.bind_tools(tools)

    response = llm_with_tool.invoke(full_message)
    
    return {"messages": [response]}




flow = StateGraph(State)

flow.add_node("agent",call_llm_node)
flow.add_node("tools",tool_node)

flow.add_edge(START, "agent")
flow.add_conditional_edges(
    "agent",
    tools_condition 
)

flow.add_edge("tools","agent")

memory = MemorySaver()
agent_app = flow.compile(checkpointer=memory)

async def chat_with_agent(query: str, thread_id: str = "default_session"):
    config = {"configurable": {"thread_id": thread_id}}
    response = await agent_app.ainvoke(
        {"messages": [("human", query)]},
        config=config
    )
    return response["messages"][-1].content

    

async def main():
    session_id = "test_user_session"
    
    # ۱. ارسال سوال تستی
    query = "How to handle exceptions in FastAPI?"
    print(f"\n[User]: {query}\n" + "-"*40)
    
    # فراخوانی اولیه
    result = await chat_with_agent(query=query, thread_id=session_id)
    print(result)

if __name__== "__main__":
    asyncio.run(main())