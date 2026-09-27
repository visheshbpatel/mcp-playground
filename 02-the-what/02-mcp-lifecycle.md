# MCP Lifecycle

The **MCP Lifecycle** defines how an MCP Client and MCP Server establish a connection, communicate during normal operation, and eventually terminate that connection.

For the lifecycle model covered by your outline, there are **three main phases**:

```text
                         ┌──────────────────────┐
                         │     MCP LIFECYCLE    │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │INITIALIZATION│    │   OPERATION  │    │  SHUT DOWN   │
        └──────────────┘    └──────────────┘    └──────────────┘
                │                   │                   │
                ▼                   ▼                   ▼
          Establish             Normal              Terminate
          connection             usage              connection
          + negotiate            + requests          gracefully
          capabilities
```

The lifecycle is essentially:

**Initialize → Negotiate → Operate → Shut Down**

For the session-based MCP protocol covered by this material, initialization establishes protocol version compatibility and capabilities before normal operations begin. ([MCP Protocol][1])

---

# 1. MCP Lifecycle

An MCP connection passes through three phases:

| Phase              | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| **Initialization** | Establish compatibility and negotiate capabilities |
| **Operation**      | Perform normal MCP communication                   |
| **Shutdown**       | Gracefully terminate the connection                |

A useful mental model:

```text
Client                                      Server
  │                                           │
  │          INITIALIZATION                   │
  │ ────────────────────────────────────────► │
  │          "Can we communicate?"            │
  │                                           │
  │          OPERATION                        │
  │ ◄──────────────────────────────────────►  │
  │          "Let's do the work."             │
  │                                           │
  │          SHUTDOWN                         │
  │ ────────────────────────────────────────► │
  │          "We're finished."                │
  │                                           │
```

---

# 2. Initialization Phase

The **Initialization Phase** is the handshake between the MCP Client and MCP Server.

Its main purposes are:

1. Establish a compatible **MCP protocol version**
2. Exchange **capabilities**
3. Exchange **implementation information**
4. Prepare both sides for normal operation

In the session-based lifecycle, initialization must happen before normal protocol operations. ([MCP Protocol][1])

### Simple idea

Before using a server, the client first asks:

> "Which MCP version do you support, and what can you do?"

The server responds:

> "This is the version we'll use, and these are the capabilities I provide."

---

# 3. Step 1 - Client Sends `initialize`

The **Client starts the initialization**.

It sends an `initialize` request containing information such as:

* `protocolVersion`
* Client `capabilities`
* `clientInfo`

Conceptually:

```text
┌────────────────────┐
│    MCP CLIENT      │
└─────────┬──────────┘
          │
          │ initialize
          │
          │ protocolVersion
          │ client capabilities
          │ clientInfo
          ▼
┌────────────────────┐
│    MCP SERVER      │
└────────────────────┘
```

Example:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {
      "name": "MyClient",
      "version": "1.0.0"
    }
  }
}
```

### Important

The `initialize` request is not an ordinary tool request.

It is the request that **starts the MCP session/handshake**.

---

# 4. Step 2 - Server Sends `initialize` Response

The server receives the `initialize` request and responds with:

* The **selected protocol version**
* Server **capabilities**
* Server `serverInfo`

```text
┌────────────────────┐
│    MCP CLIENT      │
└─────────┬──────────┘
          │
          │  initialize
          ├────────────────────────►
          │
          │  initialize response
          │  selected version
          │  server capabilities
          │  serverInfo
          ◄────────────────────────┤
┌─────────┴──────────┐
│    MCP SERVER      │
└────────────────────┘
```

Example:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "serverInfo": {
      "name": "MyServer",
      "version": "1.0.0"
    }
  }
}
```

The client now knows:

> "This is the protocol version we will use, and these are the features this server supports."

---

# 5. Step 3 - Client Sends `initialized`

After successfully processing the server's response, the client sends:

```text
notifications/initialized
```

This is a **notification**, not a request.

Therefore, the server does **not** send a response.

```text
┌────────────────────┐
│    MCP CLIENT      │
└─────────┬──────────┘
          │
          │ notifications/initialized
          │
          └────────────────────────►
                                     
                              ┌───────────────┐
                              │ MCP SERVER    │
                              │               │
                              │ Ready for     │
                              │ normal        │
                              │ operation     │
                              └───────────────┘
```

This effectively tells the server:

> "Initialization is complete. We can now start normal MCP communication."

The standard initialization sequence is therefore:

```text
CLIENT                                      SERVER
  │                                           │
  │──── initialize  ─────────────────────────►│
  │                                           │
  │◄─── initialize response  ─────────────────│
  │                                           │
  │──── notifications/initialized  ──────────►│
  │                                           │
  │          NORMAL OPERATION                 │
  │◄─────────────────────────────────────────►│
```

This three-step sequence is the core of the session-based MCP lifecycle. ([MCP Protocol][1])

---

# 6. Important Rules

Initialization has strict ordering rules.

### Rule 1 - Client initializes first

The client must initiate initialization.

### Rule 2 - No normal requests before initialization

Before receiving the `initialize` response, the client should not send normal requests.

`ping` is an exception in the older/session-based protocol.

### Rule 3 - Server waits for `initialized`

The server should not start normal request processing until it receives:

```text
notifications/initialized
```

### Rule 4 - Capabilities must be respected

After negotiation, both sides should use only capabilities that were successfully negotiated.

([MCP Protocol][1])

### Core flow

```text
       CLIENT                                      SERVER
         │                                           │
         │            initialize                     │
         ├──────────────────────────────────────────►│
         │                                           │
         │            response                       │
         │◄──────────────────────────────────────────┤
         │                                           │
         │            initialized                    │
         ├──────────────────────────────────────────►│
         │                                           │
         │              READY                        │
         │◄─────────────────────────────────────────►│
```

---

# 7. Practical Demo

Imagine an MCP Client connecting to a **GitHub MCP Server**.

The client might do:

```text
MCP Client
    │
    │  1. initialize
    │     "I support version X"
    │
    ▼
GitHub MCP Server
    │
    │  2. response
    │     "We'll use version X"
    │     "I support tools"
    │
    ▼
MCP Client
    │
    │  3. initialized
    │
    ▼
GitHub MCP Server
    │
    │
    │  Now normal operations
    ▼
tools/list
tools/call
resources/read
...
```

The important point is that **tool calling happens only after the initialization phase has successfully completed**.

---

# 8. Version Negotiation

Both client and server may support different MCP protocol versions.

The initialization phase determines which version will be used.

```text
CLIENT                                      SERVER
  │                                           │
  │ Supported:                                │
  │ 2025-11-25                                │
  │ 2025-06-18                                │
  │                                           │
  │──── initialize ─────────────────────────► │
  │     protocolVersion: 2025-11-25           │
  │                                           │
  │◄──── response ─────────────────────────── │
  │      protocolVersion: 2025-11-25          │
  │                                           │
  ▼                                           ▼
          AGREED VERSION
           2025-11-25
```

### If the server supports the requested version

It responds with that version.

### If it does not

It can respond with another version that it supports.

The client must then determine whether it supports the version selected by the server. If it does not, it should disconnect. ([MCP Protocol][1])

### Why version negotiation?

Because MCP evolves.

Different versions may introduce:

* New capabilities
* New methods
* Changed behavior
* Deprecated features

So both sides need a common protocol version.

---

# 9. Capability Negotiation

**Capabilities** tell the other side which optional MCP features are supported.

Think of capabilities as a feature declaration:

```text
CLIENT
 ├── roots
 ├── sampling
 └── experimental

SERVER
 ├── tools
 ├── resources
 ├── prompts
 ├── logging
 └── experimental
```

Conceptually:

```text
                  MCP INITIALIZATION
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
        CLIENT CAPABILITIES     SERVER CAPABILITIES
             │                       │
             │                       │
             ▼                       ▼
          "I support..."          "I support..."
             │                       │
             └───────────┬───────────┘
                         ▼
                 NEGOTIATED FEATURES
```

### Common server capabilities

* `tools`
* `resources`
* `prompts`
* `logging`

### Common client capabilities

* `roots`
* `sampling`
* `experimental`

Some capabilities also contain sub-capabilities such as:

```text
listChanged
subscribe
```

([MCP Protocol][1])

### Important concept

**Capability negotiation prevents assumptions.**

The client should not assume:

> "The server definitely supports this."

Instead:

> "The server advertised this capability, so I can use it."

---

# 10. Operation Phase

After initialization is complete, MCP enters the **Operation Phase**.

This is where normal MCP communication happens.

```text
                    OPERATION PHASE

       ┌─────────────────┐
       │   MCP CLIENT    │
       └────────┬────────┘
                │
       ┌────────┼───────────────┐
       │        │               │
       ▼        ▼               ▼
   tools/list tools/call   resources/read
       │        │               │
       └────────┼───────────────┘
                │
                ▼
       ┌─────────────────┐
       │   MCP SERVER    │
       └─────────────────┘
```

During this phase:

* Client discovers capabilities
* Client calls tools
* Client reads resources
* Client gets prompts
* Notifications may be exchanged
* Errors, cancellations and progress updates may occur

The exact operations depend on the capabilities negotiated during initialization.

---

# 11. Capability Discovery

After initialization, the client can discover what the server actually provides.

For example:

```text
                  MCP SERVER
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       TOOLS       RESOURCES      PROMPTS
          │            │            │
          ▼            ▼            ▼
       tools/list  resources/list prompts/list
```

### Tool discovery

```text
tools/list
```

returns the tools available from the server.

For example:

```text
tools/list
     │
     ▼
┌─────────────────────────────┐
│ search_github               │
│ create_issue                │
│ get_repository              │
│ list_pull_requests          │
└─────────────────────────────┘
```

The client can then understand:

* Tool name
* Description
* Input schema
* Other tool metadata

This allows an AI application to know **what actions are available before attempting to call them**.

---

# 12. Tool Calling

Once the client discovers a tool, it can call it using:

```text
tools/call
```

Example:

```text
                 MCP CLIENT
                      │
                      │ tools/call
                      │
                      │ name: search_github
                      │ arguments: {"query": "MCP"}
                      ▼
                 MCP SERVER
                      │
                      │ Executes actual operation
                      ▼
                 GitHub API
                      │
                      ▼
                 Result
                      │
                      ▼
                 MCP SERVER
                      │
                      │ result
                      ▼
                 MCP CLIENT
```

### Important distinction

The MCP Client does not necessarily implement the actual GitHub logic.

The **MCP Server performs the integration work**.

```text
AI Application
      │
      ▼
MCP Client
      │
      │ MCP
      ▼
MCP Server
      │
      │ API / SDK / Database
      ▼
External System
```

This is one of the major benefits of MCP.

---

# 13. Shutdown Phase

When the client no longer needs the connection, the lifecycle enters the **Shutdown Phase**.

The goal is to terminate the connection cleanly.

```text
          OPERATION
              │
              │ finished
              ▼
       ┌──────────────┐
       │   SHUTDOWN   │
       └──────┬───────┘
              │
              ▼
       Close transport
              │
              ▼
       Connection closed
```

Unlike initialization, the older MCP lifecycle does **not define a dedicated `shutdown` MCP message**.

Shutdown is handled by the underlying transport. ([MCP Protocol][1])

---

# 14. Shutdown in STDIO

With **STDIO**, the MCP Server usually runs as a local process.

The client/host is responsible for managing that process.

```text
             SAME MACHINE

      ┌─────────────────────────┐
      │          HOST           │
      │                         │
      │      MCP CLIENT         │
      └───────────┬─────────────┘
                  │
                STDIO
                  │
                  ▼
      ┌─────────────────────────┐
      │       MCP SERVER        │
      │       Process           │
      └─────────────────────────┘
```

A graceful shutdown generally follows:

```text
CLIENT
  │
  │ Close server input stream
  ▼
SERVER
  │
  │ Try to exit
  ▼
Process exits
```

If the server does not exit within a reasonable period:

```text
Close stdin
    │
    ▼
Wait
    │
    ├── Server exits → DONE
    │
    └── Server hangs
            │
            ▼
         SIGTERM
            │
            ▼
          Wait
            │
            └── Still running
                    │
                    ▼
                  SIGKILL
```

This escalation behavior is specified for the session-based STDIO lifecycle. ([MCP Protocol][1])

---

# 15. Shutdown in HTTP

For HTTP-based MCP transports, shutdown is handled through the HTTP connection.

Conceptually:

```text
        MCP CLIENT
             │
             │ HTTP
             ▼
        MCP SERVER
             │
             │
       Connection closed
             │
             ▼
          SHUTDOWN
```

There isn't a special MCP `shutdown` request that must be sent.

The underlying HTTP connection is closed to indicate termination. ([MCP Protocol][1])

---

# 16. Special Cases

MCP communication can encounter situations that are not part of the normal:

```text
initialize → operation → shutdown
```

flow.

Important special cases include:

* `ping`
* Errors
* Timeout
* Cancellation
* Progress notifications
* Connection failure
* Version mismatch
* Capability mismatch

A useful picture:

```text
                         MCP OPERATION
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
           PING             ERROR          CANCELLATION
             │                │                │
             ▼                ▼                ▼
        "Are you alive?"  "Something       "Stop this
                           went wrong."      request."
                              │
                              ▼
                         PROGRESS
                              │
                              ▼
                       "Still working..."
```

---

# 17. Pings

A **ping** is a lightweight message used to check whether the other side is still responsive.

Conceptually:

```text
CLIENT                                      SERVER
  │                                           │
  │────────────── ping ─────────────────────►│
  │                                           │
  │◄────────────── response ────────────────│
  │                                           │
  ▼                                           ▼
Alive / responsive
```

It is similar to asking:

> "Are you still there?"

In the session-based MCP protocol, both client and server could initiate pings. ([MCP Go SDK][2])

---

# 18. When is Ping Used?

Ping can be useful when:

### 1. Checking connection health

```text
Client ── ping ──► Server
       ◄─ response
```

### 2. Detecting a dead connection

If the other side doesn't respond within the expected period, the connection may be considered unhealthy.

### 3. Keep-alive behavior

An implementation can periodically ping its peer to check whether the connection is still alive.

```text
CLIENT
  │
  │ ping
  ▼
SERVER
  │
  │ response
  ▼
CLIENT
  │
  │ ... time ...
  │
  │ ping
  ▼
SERVER
```

**Important current-spec note:** `ping` was removed from the MCP protocol core in the `2026-07-28` specification. It remains relevant when studying older/session-based MCP implementations, which is the lifecycle model used by this outline. ([MCP Go SDK][2])

---

# 19. Error Handling

Errors are an expected part of distributed systems.

MCP uses **JSON-RPC error responses** to communicate protocol-level failures.

Instead of:

```text
Request
   │
   ▼
Success
```

we may have:

```text
Request
   │
   ▼
MCP Server
   │
   ├──────────────► SUCCESS
   │
   └──────────────► ERROR
```

Example:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params"
  }
}
```

### Common causes

* Invalid request
* Unknown method
* Invalid parameters
* Unsupported operation
* Internal server error
* Protocol/version mismatch
* Capability not available

A robust MCP implementation should also use appropriate **timeouts**, particularly to avoid indefinitely hung requests. ([MCP Protocol][1])

---

# 20. Error Object Structure

A JSON-RPC error generally contains:

```text
┌─────────────────────────────┐
│          ERROR              │
├─────────────────────────────┤
│ code                        │
│ message                     │
│ data (optional)             │
└─────────────────────────────┘
```

Example:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "field": "repository"
    }
  }
}
```

### Fields

**`code`**

Machine-readable error code.

**`message`**

Human-readable explanation.

**`data`**

Optional additional information.

### Important

Do not confuse:

```text
JSON-RPC error
```

with:

```text
Tool execution result
```

A tool can also return a result indicating that the tool's underlying operation failed, while the JSON-RPC layer itself successfully processed the request.

---

# 21. Common Error Codes

The common JSON-RPC error codes are:

|     Code | Meaning          |
| -------: | ---------------- |
| `-32700` | Parse Error      |
| `-32600` | Invalid Request  |
| `-32601` | Method Not Found |
| `-32602` | Invalid Params   |
| `-32603` | Internal Error   |

### Easy way to remember

```text
-32700  → Can't parse the message
-32600  → Request itself is invalid
-32601  → Method doesn't exist
-32602  → Parameters are wrong
-32603  → Server-side internal problem
```

MCP can also define/use additional application or protocol-specific errors depending on the specification version and feature involved. For example, current MCP revisions have changed some custom error handling over time. ([Model Context Protocol Blog][3])

---

# 22. Timeout

A **timeout** occurs when a response does not arrive within an acceptable amount of time.

```text
CLIENT                                      SERVER
  │                                           │
  │──────── request ────────────────────────► │
  │                                           │
  │              processing...                │
  │                                           │
  │              processing...                │
  │                                           │
  │              TIMEOUT                      │
  X                                           │
```

Instead of waiting forever:

```text
Request
   │
   ▼
Wait
   │
   ├── Response arrives → SUCCESS
   │
   └── Time exceeded → TIMEOUT
```

### Why timeout matters

Without timeouts:

```text
Request
   │
   ▼
Server hangs
   │
   ▼
Client waits forever
   │
   ▼
Resources remain occupied
```

Timeouts help prevent:

* Hung connections
* Resource exhaustion
* Indefinitely blocked requests

The MCP lifecycle specification explicitly recommends appropriate timeouts for requests. ([MCP Protocol][1])

---

# 23. Cancellation

**Cancellation** means:

> "Stop processing this request because I no longer need the result."

This is different from shutting down the entire connection.

### Example

Suppose the client calls a slow tool:

```text
Client
   │
   │ tools/call
   ▼
Server
   │
   │──── Processing ────
   │──── Processing ────
   │
```

The user changes their mind.

The client can send a cancellation notification:

```text
Client
   │
   │ notifications/cancelled
   ▼
Server
   │
   ▼
Stop processing request
```

### Important distinction

```text
CANCELLATION
    │
    └── Stop ONE request

SHUTDOWN
    │
    └── End the connection/session
```

Cancellation therefore does **not necessarily mean disconnecting the MCP connection**.

The MCP SDK documentation describes cancellation as terminating an individual RPC while the session itself can remain available. ([MCP Go SDK][2])

---

# 24. Progress Notification

Some operations take time.

For example:

```text
Generate a large report
Process 10,000 files
Run a long database operation
```

Instead of making the client wait without information, the server can send **progress notifications**.

```text
CLIENT                                      SERVER
  │                                           │
  │──────── request ─────────────────────────►│
  │                                           │
  │◄──── progress: 20% ───────────────────────│
  │                                           │
  │◄──── progress: 40% ───────────────────────│
  │                                           │
  │◄──── progress: 70% ───────────────────────│
  │                                           │
  │◄──── progress: 100% ──────────────────────│
  │                                           │
  │◄──── final result ────────────────────────│
```

### Why progress notifications?

They allow the client to know:

> "The operation is still running."

rather than:

> "Nothing is happening."

---

# Complete MCP Lifecycle

Now combine everything:

```text
                         ┌─────────────────────────┐
                         │      MCP LIFECYCLE      │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     INITIALIZATION      │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
             ┌────────────┐   ┌────────────┐   ┌──────────────┐
             │ initialize │   │  Version   │   │ Capabilities │
             │  request   │   │ Negotiation│   │ Negotiation  │
             └─────┬──────┘   └────────────┘   └──────────────┘
                   │
                   ▼
             ┌────────────┐
             │ initialize │
             │  response  │
             └─────┬──────┘
                   │
                   ▼
             ┌─────────────────────┐
             │ notifications/      │
             │ initialized         │
             └─────────┬───────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    OPERATION     │
              └────────┬─────────┘
                       │
          ┌────────────┼─────────────┐
          │            │             │
          ▼            ▼             ▼
      tools/list   tools/call   resources/read
          │            │             │
          └────────────┼─────────────┘
                       │
             ┌─────────┼─────────┐
             │         │         │
             ▼         ▼         ▼
           Ping      Errors   Progress
                       │
                       ▼
                  Cancellation
                       │
                       ▼
              ┌──────────────────┐
              │     SHUTDOWN     │
              └────────┬─────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
          STDIO                  HTTP
       close stream         close connection
             │                   │
             └─────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │    DISCONNECTED  │
              └──────────────────┘
```

## Core Concept / Flow

The easiest way to remember the whole topic is:

```text
INITIALIZATION
      │
      ├── Agree on VERSION
      ├── Exchange CAPABILITIES
      └── Confirm initialization
              │
              ▼
          OPERATION
              │
              ├── Discover tools
              ├── Call tools
              ├── Read resources
              ├── Get prompts
              ├── Handle errors
              ├── Track progress
              └── Cancel requests
              │
              ▼
           SHUTDOWN
              │
              └── Close transport
```

### The three most important messages in the session-based lifecycle

```text
1. initialize
        ↓
   "Let's establish the connection."

2. initialize response
        ↓
   "This is the version and these are my capabilities."

3. notifications/initialized
        ↓
   "Initialization is complete. Start normal operation."
```

---

## Important Current MCP Note

There is one **very important version distinction** to keep in mind while studying this material.

The lifecycle above describes the **session-based MCP model** used by earlier MCP specifications and the `2025-11-25` era: `initialize → initialize response → notifications/initialized → operation`. ([MCP Protocol][1])

MCP **2026-07-28** introduced a major change: the protocol core became **stateless**, and the `initialize`/`initialized` handshake and protocol-level sessions were removed. Clients can use `server/discover` when they want capability discovery before making requests. The same release also removed `ping` from the protocol core and deprecated the legacy HTTP+SSE transport. ([Model Context Protocol Blog][4])

So for your learning:

```text
OLDER / SESSION-BASED MCP
─────────────────────────
initialize
     ↓
version + capabilities
     ↓
initialized
     ↓
operation
     ↓
shutdown


CURRENT 2026-07-28 MCP
──────────────────────
request carries relevant context
     ↓
optional server/discover
     ↓
stateless operation
     ↓
no protocol-level initialize handshake
```

**For understanding the concepts in this set of notes, learn the first flow thoroughly first.** Then the newer stateless model will make much more sense as an evolution of the same underlying problem. ([Model Context Protocol Blog][4])

[1]: https://modelcontextprotocol.info/specification/2024-11-05/basic/lifecycle/?utm_source=chatgpt.com "Lifecycle – Model Context Protocol （MCP）"
[2]: https://go.sdk.modelcontextprotocol.io/protocol/?utm_source=chatgpt.com "LifeCycle - MCP Go SDK"
[3]: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/?utm_source=chatgpt.com "The 2026-07-28 MCP Specification Release Candidate | Model Context Protocol Blog"
[4]: https://blog.modelcontextprotocol.io/posts/2026-07-28/?utm_source=chatgpt.com "The 2026-07-28 Specification | Model Context Protocol Blog"
