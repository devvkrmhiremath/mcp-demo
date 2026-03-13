import asyncio
import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from fastmcp import Client
from fastmcp.client.auth import OAuth

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

# Define the state of our graph
class AgentState(TypedDict):
    query: str
    mcp_results: str
    summary: str

async def call_seismic_mcp(state: AgentState) -> AgentState:
    """Node to call the Seismic MCP server"""
    server_url = os.getenv("SEISMIC_MCP_URL", "https://mcp.seismic.com")
    client_id = os.getenv("SEISMIC_CLIENT_ID")
    client_secret = os.getenv("SEISMIC_CLIENT_SECRET")
    
    query = state["query"]
    
    if not client_id or not client_secret:
        console.print("[yellow]Warning: Seismic credentials missing. Using mock data for demo.[/yellow]")
        return {**state, "mcp_results": f"Mock results for query: '{query}'. In a real scenario, this would contain content from Seismic platform regarding {query}."}

    try:
        auth = OAuth(client_id=client_id, client_secret=client_secret)
        async with Client(server_url, auth=auth) as client:
            console.print(f"[dim]Connected to Seismic MCP for query: {query}[/dim]")
            
            # For demo, we'll try to use generative_search if it exists, otherwise list_tools
            tools = await client.list_tools()
            if any(t.name == "generative_search" for t in tools):
                result = await client.call_tool("generative_search", arguments={"query": query})
                mcp_data = str(result)
            else:
                mcp_data = f"Tool 'generative_search' not found. Available tools: {[t.name for t in tools]}"
                
            return {**state, "mcp_results": mcp_data}
    except Exception as e:
        console.print(f"[red]MCP Error: {e}[/red]")
        return {**state, "mcp_results": f"Error calling MCP: {str(e)}"}

async def summarize_results(state: AgentState) -> AgentState:
    """Node to summarize the MCP results using GPT"""
    mcp_results = state["mcp_results"]
    
    llm = ChatOpenAI(model="gpt-4o") # Assumes OPENAI_API_KEY is in .env
    
    messages = [
        SystemMessage(content="You are a helpful assistant that summarizes technical or business data fetched from external systems via MCP."),
        HumanMessage(content=f"Please summarize the following data fetched from the Seismic platform for the user query '{state['query']}':\n\n{mcp_results}")
    ]
    
    try:
        response = await llm.ainvoke(messages)
        return {**state, "summary": response.content}
    except Exception as e:
        console.print(f"[red]LLM Error: {e}[/red]")
        return {**state, "summary": f"Could not generate summary: {str(e)}"}

# Define the LangGraph workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("fetch_mcp", call_seismic_mcp)
workflow.add_node("summarize", summarize_results)

# Define edges
workflow.set_entry_point("fetch_mcp")
workflow.add_edge("fetch_mcp", "summarize")
workflow.add_edge("summarize", END)

# Compile the graph
app = workflow.compile()

async def run_flow(user_query: str):
    console.print(Panel(f"[bold blue]LangGraph x FastMCP Flow[/bold blue]\nUser Query: [cyan]{user_query}[/cyan]", expand=False))
    
    inputs = {"query": user_query}
    
    async for event in app.astream(inputs):
        for node_name, state_update in event.items():
            console.print(f"[bold green]Node '{node_name}' completed[/bold green]")
            if "summary" in state_update:
                console.print(Panel(state_update["summary"], title="Final GPT Summary", border_style="purple"))

if __name__ == "__main__":
    # Example usage
    query = "Standard sales pitch for cloud services"
    asyncio.run(run_flow(query))
