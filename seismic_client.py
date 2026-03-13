import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.auth import OAuth
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

console = Console()

async def run_seismic_client():
    # 1. Configuration from environment variables
    # For Seismic, the default global URL is https://mcp.seismic.com
    # If using a tenant-specific URL, it would be https://mcp.seismic.com/tenants/{tenant}
    server_url = os.getenv("SEISMIC_MCP_URL", "https://mcp.seismic.com")
    client_id = os.getenv("SEISMIC_CLIENT_ID")
    client_secret = os.getenv("SEISMIC_CLIENT_SECRET")

    if not client_id or not client_secret:
        console.print("[bold red]Error: SEISMIC_CLIENT_ID and SEISMIC_CLIENT_SECRET must be set in .env[/bold red]")
        console.print("Please copy .env.example to .env and fill in your credentials.")
        return

    console.print(Panel(
        f"[bold blue]FastMCP Seismic Client[/bold blue]\n"
        f"Server: [cyan]{server_url}[/cyan]\n"
        f"Client ID: [cyan]{client_id}[/cyan]", 
        expand=False
    ))

    try:
        # 2. Configure OAuth authentication
        auth = OAuth(
            client_id=client_id,
            client_secret=client_secret
        )

        # 3. Initialize the FastMCP Client with OAuth
        # FastMCP will handle the OAuth handshake and session automatically
        async with Client(server_url, auth=auth) as client:
            console.print("[bold green]✓ Authenticated and connected to Seismic MCP successfully![/bold green]\n")

            # 4. Discover capabilities (Tools)
            tools = await client.list_tools()
            tool_table = Table(title="Available Seismic Tools")
            tool_table.add_column("Tool Name", style="magenta")
            tool_table.add_column("Description", style="white")
            
            for tool in tools:
                tool_table.add_row(tool.name, tool.description)
            
            console.print(tool_table)

            # 5. Example Tool Call (e.g., 'generative_search')
            # Note: Available tools depend on your Seismic app scopes
            if any(t.name == "generative_search" for t in tools):
                console.print("\n[yellow]Testing Generative Search...[/yellow]")
                query = "What is our company strategy for 2026?"
                result = await client.call_tool("generative_search", arguments={"query": query})
                console.print(Panel(str(result), title="Search Result", border_style="green"))
            else:
                console.print("\n[yellow]Note: 'generative_search' tool not found. Check your app scopes.[/yellow]")

            console.print("\n[bold green]Seismic Client Validation Complete![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")
        console.print("[dim]Hint: Ensure your Client ID and Secret are valid and your Seismic tenant has the app enabled.[/dim]")

if __name__ == "__main__":
    asyncio.run(run_seismic_client())
