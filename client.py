import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports.stdio import UvxStdioTransport
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

async def run_client():
    # Define the SQLite database path from env or default
    db_path = os.getenv("LOCAL_DB_PATH", "test.db")
    db_path = os.path.abspath(db_path)
    
    console.print(Panel(f"[bold blue]FastMCP Client Demo[/bold blue]\nConnecting to: [cyan]mcp-server-sqlite[/cyan]\nDatabase: [cyan]{db_path}[/cyan]", expand=False))

    # Initialize the UvxStdioTransport
    # This transport knows how to run tools via 'uvx'
    transport = UvxStdioTransport(
        tool_name="mcp-server-sqlite",
        tool_args=["--db-path", db_path]
    )

    try:
        # Initialize the FastMCP Client with the explicit transport
        async with Client(transport) as client:
            console.print("[bold green]✓ Connected to MCP Server successfully![/bold green]\n")

            # 1. List available tools
            tools = await client.list_tools()
            tool_table = Table(title="Available Tools")
            tool_table.add_column("Tool Name", style="magenta")
            tool_table.add_column("Description", style="white")
            
            for tool in tools:
                tool_table.add_row(tool.name, tool.description)
            
            console.print(tool_table)
            console.print("\n")

            # 2. List tables using the 'list_tables' tool
            console.print("[yellow]Querying database tables...[/yellow]")
            tables_result = await client.call_tool("list_tables")
            console.print(f"Tables found: [bold cyan]{tables_result}[/bold cyan]\n")

            # 3. Read data using 'read_query' tool
            query = "SELECT * FROM users"
            console.print(f"[yellow]Running query:[/yellow] [bold white]{query}[/bold white]")
            
            # The tool result is usually a string or a list of Content objects
            query_result = await client.call_tool("read_query", arguments={"query": query})
            
            console.print(Panel(str(query_result), title="Query Result", border_style="green"))

            console.print("\n[bold green]Validation Complete![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    asyncio.run(run_client())
