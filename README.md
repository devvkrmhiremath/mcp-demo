# FastMCP Client Demo 🚀

A comprehensive demonstration of building and running **Model Context Protocol (MCP)** clients using the **FastMCP** framework. This repository includes examples for both local and cloud-based MCP servers.

## ✨ Features

- **Local SQLite Client**: Connects to a local SQLite database via `uvx mcp-server-sqlite`.
- **Seismic Cloud Client**: Connects to the official **Seismic.com** MCP server using **OAuth 2.1** (Client ID & Secret).
- **Modern Tooling**: Built with `uv` for fast, reproducible dependency management.
- **Beautiful UI**: Uses `rich` for formatted terminal output.

---

## 🛠️ Setup

1. **Install uv** (if you haven't):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and Install Dependencies**:
   ```bash
   cd fastmcp-client-demo
   uv sync
   ```

3. **Configure Environment Variables**:
   Copy the example file and fill in your Seismic credentials:
   ```bash
   cp .env.example .env
   ```

---

## 🚀 Running the Clients

### 1. Local SQLite Demo
This client launches a local MCP server that provides tools to query an SQLite database.

```bash
uv run client.py
```
*Note: This will create a `test.db` file locally and populate it with sample data.*

### 2. Seismic Cloud Client
This client connects to the Seismic platform to access tools like Generative Search.

```bash
uv run seismic_client.py
```
*Requires `SEISMIC_CLIENT_ID` and `SEISMIC_CLIENT_SECRET` in your `.env`.*

---

## 📂 Project Structure

- `client.py`: Demo for local subprocess-based MCP servers.
- `seismic_client.py`: Demo for remote SSE-based MCP servers with OAuth.
- `.env.example`: Template for required credentials.
- `pyproject.toml`: Dependency and project configuration.

---

## 🧪 Requirements

- Python 3.10+
- `fastmcp`
- `python-dotenv`
- `rich`
