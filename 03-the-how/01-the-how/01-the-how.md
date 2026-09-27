# MCP Connections & Connectors

## 1. Types of Connections

An MCP connection is simply **how an AI application communicates with an MCP server**.

The two main transport options in current MCP are:

```text
                    MCP CONNECTION
                          │
              ┌───────────┴───────────┐
              │                       │
            STDIO              Streamable HTTP
              │                       │
          Local server            Remote server
          Same machine             Over network
```

### STDIO

Used when the MCP server runs locally.

```text
MCP Client ── stdin/stdout ──► MCP Server
                              (local process)
```

It is simple and has no network overhead. ([GitHub][1])

### Streamable HTTP

Used mainly for **remote MCP servers**.

```text
MCP Client ───── HTTP ─────► MCP Server
                             (remote)
```

It allows the server to be hosted separately and accessed over a network. ([GitHub][1])

---

# 2. What Are Connectors?

A **connector** is a pre-built way for an AI application to connect to an external service.

For example:

```text
              AI APPLICATION
                     │
             ┌───────┼────────┐
             │       │        │
             ▼       ▼        ▼
           Gmail   GitHub   Dropbox
         Connector Connector Connector
```

Instead of building the complete integration yourself, the connector provides the connection and exposes the service's capabilities to the AI.

For example, an application might provide a connector that allows the model to:

* Read emails
* Search files
* Access calendar information
* Interact with another service

OpenAI's API documentation describes connectors as built-in integrations to third-party services, while remote MCP servers provide a more general way to connect to external tools and data. ([OpenAI Developers][2])

### Simple distinction

```text
Connector
   ↓
Pre-built integration

MCP Server
   ↓
A server implementing the MCP protocol
   ↓
Can expose custom tools, resources and prompts
```

A connector can therefore be thought of as a **ready-made integration**, while an MCP server gives you a more general and programmable integration mechanism.

---

# 3. Why Not Use Connectors Always?

Because **connectors are not suitable for every situation**.

### 1. Limited availability

A platform may only provide connectors for certain services.

```text
Connector available?
       │
   ┌───┴───┐
  YES      NO
   │        │
   ▼        ▼
Use it    MCP server /
           custom integration
```

MCP allows developers to build their own servers for services that don't have a ready-made connector. ([Claude Help Center][3])

### 2. Less control

With a ready-made connector, you generally use the functionality that the provider exposes.

With your own MCP server, you control:

* Which tools exist
* Tool descriptions
* Input/output schemas
* Authentication/integration logic
* How the external API is used

### 3. Custom workflows

Suppose you want:

```text
GitHub
   ↓
Your database
   ↓
Custom processing
   ↓
AI result
```

A simple connector may not provide this exact workflow.

You can build an MCP server that handles the entire workflow.

### 4. Tool/context overhead

Giving an AI too many connectors/tools can make tool selection harder and consume additional context. Keeping only relevant integrations available can improve efficiency. ([ConnectorZone][4])

---

# The Simple Mental Model

```text
                 AI APPLICATION
                       │
             ┌─────────┴─────────┐
             │                   │
       CONNECTOR            MCP SERVER
             │                   │
       Ready-made            Custom / flexible
       integration           integration
             │                   │
             └─────────┬─────────┘
                       ▼
                EXTERNAL SERVICE
```

### Remember

**Connector = ready-made connection**

**MCP Server = programmable MCP-based integration**

**Use connectors when the ready-made integration is sufficient. Use an MCP server when you need more control, custom tools, or a service/workflow that isn't covered by an existing connector.**
