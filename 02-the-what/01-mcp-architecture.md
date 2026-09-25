# MCP Architecture

## 1. Architecture

MCP follows a **Host–Client–Server architecture**.

* **Host** → The AI application used by the user.
* **MCP Client** → Connects the Host to an MCP Server.
* **MCP Server** → Provides tools, resources, and prompts.
* **External System** → The actual service or data source being accessed.

```text
                         ┌──────────────────────────────────────┐
                         │                 HOST                 │
                         │                                      │
                         │   ┌────────────┐    ┌────────────┐   │
                         │   │    LLM     │    │ MCP Client │   │
                         │   └────────────┘    └──────┬─────┘   │
                         └────────────────────────────┼─────────┘
                                                      │
                                                MCP Protocol
                                                      │
                                                      ▼
                                      ┌──────────────────────────┐
                                      │       MCP SERVER         │
                                      │                          │
                                      │ Tools / Resources /      │
                                      │ Prompts                  │
                                      └────────────┬─────────────┘
                                                   │
                                                   ▼
                                      ┌──────────────────────────┐
                                      │     EXTERNAL SYSTEM      │
                                      │                          │
                                      │ GitHub / Slack / DB etc. │
                                      └──────────────────────────┘
```

### Example

```text
User
 ↓
AI Application
 ↓
MCP Client
 ↓
GitHub MCP Server
 ↓
GitHub API
 ↓
GitHub
```

**Core Concept:**

> The **Host** provides the AI experience, the **Client** handles MCP communication, and the **Server** provides external capabilities.

---

# 2. Multiple MCP Clients

A Host can connect to **multiple MCP Servers**.

Each MCP Client manages communication with an MCP Server.

```text
    ┌───────────────────────────────────────────────────┐
    │                       ┌──────────────┐            │      ┌─────────────┐   
    │                       │ MCP Client 1 │────────────┼────► |GitHub Server|
    │                       └──────────────┘            │      └─────────────┘
    │                                                   │
    │                       ┌──────────────┐            │      ┌─────────────┐
    │    HOST               │ MCP Client 2 │────────────┼────► | Slack Server|
    │                       └──────────────┘            │      └─────────────┘
    │                                                   │
    │                       ┌──────────────┐            │     ┌────────────────┐
    │                       │ MCP Client 3 │────────────┼────►| Database Server|
    │                       └──────────────┘            │     └────────────────┘
    └───────────────────────────────────────────────────┘
```

For example:

```text
AI Application
 ├── MCP Client → GitHub MCP Server
 ├── MCP Client → Slack MCP Server
 └── MCP Client → PostgreSQL MCP Server
```

**Core Concept:**

> One Host can communicate with multiple MCP Servers through multiple MCP Clients.

---

# 3. Benefits of MCP Architecture

### 1. Separation of Concerns

Each component has a specific responsibility.

```text
Host
→ AI application

Client
→ MCP communication

Server
→ External capabilities
```

### 2. Modularity

Servers can be added or removed without changing the entire AI application.

### 3. Reusability

An MCP Server can be used by multiple MCP-compatible applications.

### 4. Standardization

Different AI applications can communicate with external systems using the same protocol.

**Core Concept:**

> MCP separates the AI application from the implementation details of external systems.

---

# 4. MCP Primitives

An MCP Server exposes **primitives** that provide capabilities to the AI application.

The three main server primitives are:

```text
                         ┌──────────────────┐
                         │    MCP SERVER    │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌────────────┐      ┌────────────┐      ┌────────────┐
       │   TOOLS    │      │ RESOURCES  │      │  PROMPTS   │
       └──────┬─────┘      └──────┬─────┘      └──────┬─────┘
              │                   │                   │
              ▼                   ▼                   ▼
           Actions             Context            Templates
```

### Tools

Used to **perform actions**.

Examples:

```text
search_github()
create_issue()
query_database()
```

### Resources

Used to provide **information or context**.

Examples:

```text
files
documents
database schemas
application data
```

### Prompts

Used to provide **reusable interaction templates**.

Examples:

```text
code_review
summarize_document
explain_commit
```

### Easy way to remember

```text
Tools      → Actions
Resources  → Information
Prompts    → Templates
```

---

# 5. The Prompt Primitive

A **Prompt** is a reusable interaction template provided by an MCP Server.

For example:

```text
MCP Server
    │
    └── Prompts
         ├── review_code
         ├── summarize_issue
         └── explain_commit
```

A user can select a predefined prompt instead of creating the entire interaction manually.

### Example

```text
User
 ↓
Select "review_code"
 ↓
MCP Prompt
 ↓
AI
```

### Important

A Prompt is different from a Tool.

```text
Tool
→ Performs an action

Prompt
→ Provides a reusable interaction template
```

**Core Concept:**

> Prompts make common interactions reusable and easier for users to invoke.

---

# 6. Primitives — Standard Operations

MCP provides standard operations for interacting with its primitives.

```text
Tools
 ├── tools/list
 └── tools/call

Resources
 ├── resources/list
 └── resources/read

Prompts
 ├── prompts/list
 └── prompts/get
```

### `tools/list`

Returns the tools available from the server.

```text
Client
   │
   │ tools/list
   ▼
Server
   │
   ▼
Available tools
```

### `tools/call`

Executes a specific tool.

```text
Client
   │
   │ tools/call
   ▼
Server
   │
   ▼
Tool execution
```

### `resources/list`

Returns available resources.

### `resources/read`

Reads a specific resource.

### `prompts/list`

Returns available prompts.

### `prompts/get`

Retrieves a specific prompt.

### Simple pattern

```text
/list
→ Discover what is available

/call
→ Execute a tool

/read
→ Read a resource

/get
→ Retrieve a prompt
```

---

# 7. Quick Summary

At this point, the basic MCP structure is:

```text
                         MCP SERVER
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
            TOOLS         RESOURCES         PROMPTS
              │               │               │
              ▼               ▼               ▼
           Actions         Context         Templates
```

Standard operations:

```text
TOOLS
 ├── tools/list
 └── tools/call

RESOURCES
 ├── resources/list
 └── resources/read

PROMPTS
 ├── prompts/list
 └── prompts/get
```

### Core Concept

> MCP defines standard ways to **discover and use** the capabilities provided by a server.

---

# 8. MCP Data Layer

Now we need to understand how the Client and Server exchange messages.

MCP can be viewed in layers:

```text
┌─────────────────────────────────────────────┐
│                  MCP                        │
├─────────────────────────────────────────────┤
│              Primitives                     │
│       Tools / Resources / Prompts           │
├─────────────────────────────────────────────┤
│              Data Layer                     │
│              JSON-RPC 2.0                   │
├─────────────────────────────────────────────┤
│            Transport Layer                  │
│             STDIO / HTTP                    │
└─────────────────────────────────────────────┘
```

### Data Layer

Defines:

> **What messages are exchanged and what they mean.**

MCP uses **JSON-RPC 2.0** for this.

### Transport Layer

Defines:

> **How those messages travel between Client and Server.**

---

# 9. JSON-RPC 2.0

**JSON-RPC** stands for **JSON Remote Procedure Call**.

It provides a standard format for sending requests and receiving responses between applications.

The basic idea:

```text
Client
   │
   │ Request
   ▼
Server
   │
   │ Response
   ▼
Client
```

For example:

```text
Client
   │
   │ "Call add(2, 3)"
   ▼
Server
   │
   │ "Result = 5"
   ▼
Client
```

A JSON-RPC request looks like:

```json
{
  "jsonrpc": "2.0",
  "method": "add",
  "params": [2, 3],
  "id": 1
}
```

---

# 10. JSON-RPC Request and Response

A request commonly contains:

```text
jsonrpc
→ JSON-RPC version

method
→ Operation to perform

params
→ Arguments

id
→ Request identifier
```

Example:

```json
{
  "jsonrpc": "2.0",
  "method": "add",
  "params": [2, 3],
  "id": 1
}
```

The server can return:

```json
{
  "jsonrpc": "2.0",
  "result": 5,
  "id": 1
}
```

The `id` allows the Client to match the response with the original request.

### Error response

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```

**Core Concept:**

> **JSON-RPC provides a standard structure for MCP requests, responses, and errors.**

---

# 11. Why RPC for the Data Layer?

MCP performs many remote operations:

```text
tools/list
tools/call
resources/list
resources/read
prompts/list
prompts/get
```

These are essentially **operations requested from another system**.

RPC is designed for this type of communication.

```text
Client
   │
   │ Remote operation
   ▼
Server
   │
   │ Result
   ▼
Client
```

Therefore:

```text
JSON-RPC
→ Defines the structure of messages

MCP
→ Defines the meaning of the operations
```

### Simple example

```text
tools/list
```

is an MCP operation.

JSON-RPC provides the structure in which that operation is sent.

**Core Concept:**

> **JSON-RPC tells us how to structure the message; MCP tells us what the message means.**

---

# 12. MCP Transport Layer

After creating a JSON-RPC message, we need a way to send it from the Client to the Server.

This is the job of the **Transport Layer**.

```text
Client
   │
   │ JSON-RPC message
   ▼
Transport
   │
   ▼
Server
```

The Transport Layer answers:

> **How does the message travel?**

The message itself is still an MCP/JSON-RPC message.

Common transport approaches include:

```text
Local
→ STDIO

Remote
→ HTTP-based transport
```

---

# 13. Types of MCP Servers

MCP Servers can be broadly classified based on where they run.

```text
                         MCP SERVERS
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
                LOCAL                   REMOTE
                  │                       │
                STDIO              HTTP-based transport
```

### Local Server

Runs on the same machine as the Host.

```text
Host
 ↓
MCP Client
 ↓
STDIO
 ↓
MCP Server
```

### Remote Server

Runs on another machine or server.

```text
Host
 ↓
MCP Client
 ↓
HTTP
 ↓
Remote MCP Server
```

---

# 14. Local Servers — STDIO

**STDIO** stands for:

> **Standard Input / Standard Output**

STDIO is commonly used for **local MCP Servers**.

The Host starts the MCP Server as a local process and communicates with it using:

```text
stdin
stdout
```

Architecture:

```text
                  SAME MACHINE

        ┌───────────────────────────┐
        │           HOST            │
        │                           │
        │       MCP Client          │
        └─────────────┬─────────────┘
                      │
                   STDIO
                stdin / stdout
                      │
                      ▼
        ┌───────────────────────────┐
        │        MCP Server         │
        └───────────────────────────┘
```

---

# 15. How Does STDIO Work?

The Client communicates with the Server process through standard input and output.

### Client → Server

The Client writes the JSON-RPC message to the Server's:

```text
stdin
```

### Server → Client

The Server writes the response to:

```text
stdout
```

So the flow is:

```text
┌──────────────┐
│ MCP Client   │
└──────┬───────┘
       │
       │ JSON-RPC request
       ▼
     stdin
       │
       ▼
┌──────────────┐
│ MCP Server   │
└──────┬───────┘
       │
       │ JSON-RPC response
       ▼
    stdout
       │
       ▼
┌──────────────┐
│ MCP Client   │
└──────────────┘
```

### Example

The Client sends:

```text
tools/list
```

through STDIO.

The Server processes it and returns:

```text
Available tools
```

through STDIO.

### Core Concept

> **STDIO allows a local MCP Client and Server to communicate through the Server process's standard input and output streams.**

---

# 16. Demo Flow

Consider a local GitHub MCP Server.

The complete flow is:

```text
User
  │
  ▼
┌──────────────┐
│     Host     │
│     + LLM    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ MCP Client   │
└──────┬───────┘
       │
      STDIO
       │
       ▼
┌──────────────┐
│ GitHub MCP   │
│    Server    │
└──────┬───────┘
       │
       ▼
   GitHub API
       │
       ▼
     GitHub
```

If the user asks:

> "Show me the latest commits."

The LLM can decide to use an appropriate GitHub tool.

```text
User
 ↓
LLM
 ↓
Tool selection
 ↓
MCP Client
 ↓
tools/call
 ↓
GitHub MCP Server
 ↓
GitHub API
 ↓
Result
 ↓
LLM
 ↓
User
```

---

# 17. Benefits of STDIO Transport

### Simple

No separate HTTP server is required.

### Local

The MCP Server runs on the same machine.

### Lightweight

Communication happens through process streams.

### Easy to manage

The Host can start and stop the Server process.

### Useful for local tools

Examples:

```text
Local Files
Git
Local Database
Development Tools
```

**Core Concept:**

> **STDIO is simple and suitable when the MCP Server runs locally with the Host.**

---

# 18. Remote Servers - HTTP + SSE

Remote MCP Servers need network communication.

An older remote transport approach used:

**HTTP + SSE**

### HTTP

Used for Client → Server communication.

```text
Client
  │
  │ HTTP
  ▼
Server
```

### SSE

**Server-Sent Events (SSE)** allows the Server to send events back to the Client over an HTTP connection.

```text
Client
  │
  │ HTTP
  ▼
Server
  │
  │ SSE
  ▼
Client
```

Overall:

```text
                 REMOTE SERVER

┌──────────────┐
│ MCP Client   │
└──────┬───────┘
       │
       │ HTTP
       ▼
┌──────────────┐
│ MCP Server   │
└──────┬───────┘
       │
       │ SSE
       ▼
     Client
```

### Important

**HTTP + SSE is the older remote transport approach.**

Modern MCP uses **Streamable HTTP** for new remote-server implementations.

So for understanding the architecture:

```text
Older:
Remote MCP Server → HTTP + SSE

Current:
Remote MCP Server → Streamable HTTP
```

---

# Final MCP Architecture

Put everything together:

```text
                              USER
                                │
                                ▼
                     ┌─────────────────────┐
                     │        HOST         │
                     │                     │
                     │        LLM          │
                     │                     │
                     │     MCP Client      │
                     └──────────┬──────────┘
                                │
                                │ MCP
                                ▼
                     ┌─────────────────────┐
                     │     DATA LAYER      │
                     │                     │
                     │    JSON-RPC 2.0     │
                     └──────────┬──────────┘
                                │
                                │
                     ┌──────────▼──────────┐
                     │   TRANSPORT LAYER   │
                     │                     │
                     │   STDIO / HTTP      │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     MCP SERVER      │
                     │                     │
                     │ Tools / Resources / │
                     │ Prompts             │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  EXTERNAL SYSTEM    │
                     │                     │
                     │ GitHub / DB / Slack │
                     │ Files / APIs        │
                     └─────────────────────┘
```

# Core Concepts to Remember

### Architecture

```text
Host
 ↓
MCP Client
 ↓
MCP Server
 ↓
External System
```

### Primitives

```text
Tools
→ Actions

Resources
→ Information / Context

Prompts
→ Reusable Templates
```

### Data Layer

```text
JSON-RPC 2.0
→ Structure of MCP messages
```

### Transport Layer

```text
STDIO
→ Local communication

HTTP-based transport
→ Remote communication
```

### The complete idea

> **MCP provides a standardized way for an AI application to communicate with external capabilities. The Host contains the AI and MCP Client, the Server provides Tools, Resources, and Prompts, JSON-RPC defines the message structure, and the Transport Layer carries those messages between Client and Server.**
