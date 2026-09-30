# MCP Playground

A hands-on repository for exploring and building with the **Model Context Protocol (MCP)**.

The repository covers MCP from its fundamentals to practical implementations, including protocol architecture, lifecycle, transports, servers, clients, tools, resources, and remote integrations.

## Contents

### 01: The Why

Understanding the problems MCP addresses and the need for a standardized protocol for connecting AI applications with external tools and data.

### 02: The What

Core MCP concepts and protocol architecture:

- MCP Architecture
- Host, Client & Server
- Tools, Resources & Prompts
- JSON-RPC 2.0
- Data & Transport Layers
- STDIO & HTTP
- MCP Lifecycle
- Initialization & Capability Negotiation
- Operation & Shutdown
- Errors, Cancellation & Progress

### 03: The How

Practical MCP implementations:

- MCP server development with FastMCP
- Local MCP servers
- Remote MCP servers
- Expense Tracker MCP
- MCP Math Server
- MCP client development
- Multi-server client connections
- Streamable HTTP & STDIO
- LangChain MCP integration
- Streamlit MCP chatbot

## Stack

- Python
- FastMCP
- MCP SDK
- LangChain
- LangChain MCP Adapters
- OpenAI-compatible LLMs
- Streamlit
- uv

## Repository Flow

```text
WHY
 │
 ▼
WHAT
 │
 ▼
HOW
 │
 ├── Local MCP Servers
 ├── Remote MCP Servers
 └── MCP Clients
````

## Resource

MCP Playlist: [https://www.youtube.com/playlist?list=PLKnIA16_Rmva_oZ9F4ayUu9qcWgF7Fyc0](https://www.youtube.com/playlist?list=PLKnIA16_Rmva_oZ9F4ayUu9qcWgF7Fyc0)

