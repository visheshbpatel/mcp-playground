# WHY MCP?

## 1. Arrival of LLMs

### What it means

Large Language Models (LLMs) changed how we interact with software.

Instead of explicitly telling a computer **how** to perform a task, we can describe **what we want** in natural language.

```text
User
 ↓
Natural Language
 ↓
LLM
 ↓
Response
```

For example:

> "Explain this Python error."

The LLM can understand the request and generate an answer.

### The limitation

An LLM by itself mainly **generates information**.

It does not automatically have access to:

* your files
* your database
* GitHub
* Slack
* external APIs
* real-time information

This creates the need to connect LLMs with external systems.

### Key idea

> **LLMs can understand and generate information, but they need additional mechanisms to access external data and perform actions.**

---

# 2. Waves of Adoption

As LLMs became more capable, developers started adding more capabilities around them.

A simplified evolution is:

```text
LLM
 ↓
Prompt Engineering
 ↓
RAG
 ↓
Tool Calling
 ↓
Agents
 ↓
MCP
```

Each step tries to solve a limitation.

### Example

An LLM may know:

> "What is RAG?"

But if you ask:

> "What is inside my company's RAG documentation?"

the model needs access to external information.

That's where **RAG, tools, and external integrations** become important.

### Key idea

> **The evolution of AI systems has been largely about giving LLMs better access to information and capabilities.**

---

# 3. The Problem of Fragmentation

As AI applications became more capable, they started connecting to many external systems.

For example:

```text
AI Application
 ├── GitHub
 ├── Slack
 ├── PostgreSQL
 ├── Google Drive
 ├── Jira
 └── AWS
```

The problem is that each integration may require its own:

* API
* authentication
* tool definitions
* implementation
* error handling
* maintenance

Now imagine **100 AI applications** doing this independently.

You get a huge amount of duplicated integration work.

This is called **fragmentation**.

### Key idea

> **Different AI applications were building separate integrations for the same external systems, creating duplicated and inconsistent implementations.**

---

# 4. Vision vs Reality

The vision of AI agents is:

> "Give AI access to the tools and information it needs, and let it perform tasks."

But the reality is:

```text
AI Application
      ↓
Many custom integrations
      ↓
Many APIs
      ↓
Many authentication systems
      ↓
Many different implementations
```

The AI may be intelligent, but the surrounding infrastructure becomes complicated.

### Vision

```text
AI
 ↓
Access everything it needs
```

### Reality

```text
AI
 ↓
GitHub integration
Slack integration
Database integration
Jira integration
...
```

### Key idea

> **The intelligence of the AI is increasing faster than the simplicity of connecting that AI to external systems.**

---

# 5. What Is Context?

This is one of the most important concepts for understanding MCP.

**Context** is the information available to an AI system that helps it understand a task and produce an appropriate response or action.

For example, suppose you ask:

> "Fix this bug."

The LLM needs context such as:

```text
Source code
Error logs
Configuration
Database schema
Documentation
Previous messages
```

Without this information:

```text
LLM
 ↓
"I don't know enough."
```

With the information:

```text
Context
 ↓
LLM
 ↓
Better understanding
 ↓
Better response/action
```

### Important point

Context is not limited to text.

It can include:

* documents
* files
* databases
* APIs
* application state
* tool results
* conversation history

### Key idea

> **Context is the information and capabilities an AI system can access to understand and complete a task.**

---

# 6. Example: Software Engineering

Consider an AI coding assistant.

You ask:

> "Find why my `/chat` endpoint is failing."

For the AI to solve this properly, it may need:

```text
Source code
      ↓
API routes
      ↓
Service layer
      ↓
Configuration
      ↓
Error logs
      ↓
Database
```

The AI therefore needs access to the **development environment**, not just the user's question.

This changes the role of the LLM.

It goes from:

```text
Question
 ↓
Generate answer
```

to:

```text
Understand task
 ↓
Get relevant context
 ↓
Use tools
 ↓
Observe results
 ↓
Take next action
```

### Key idea

> **Real-world AI applications need access to both information and actions.**

---

# 7. Workflow with AI

Traditional software development might look like:

```text
Developer
 ↓
Open file
 ↓
Read code
 ↓
Open terminal
 ↓
Run command
 ↓
Read error
 ↓
Search documentation
 ↓
Fix code
```

With an AI agent:

```text
Developer
 ↓
"Find and fix the error."
 ↓
AI Agent
 ↓
Read files
 ↓
Run commands
 ↓
Inspect results
 ↓
Search documentation
 ↓
Modify code
```

The AI is no longer only answering questions.

It is participating in the **workflow**.

### Key idea

> **AI becomes more useful when it can access the same tools and information that humans use to complete a task.**

---

# 8. Copy-Paste Hell

Before AI applications could directly access external information, humans often had to manually provide context.

For example:

```text
Open file
 ↓
Copy code
 ↓
Paste into AI
 ↓
AI asks for another file
 ↓
Open another file
 ↓
Copy
 ↓
Paste
```

This creates **copy-paste hell**.

The human becomes the bridge between the AI and the external system.

```text
GitHub
   ↓
Human
   ↓
Copy/Paste
   ↓
AI
```

What we really want is:

```text
GitHub
   ↑
   │
AI ────────────
```

The AI should be able to retrieve the necessary context itself.

### Key idea

> **Manual transfer of context creates friction. AI systems should be able to access relevant information directly.**

---

# 9. Function Calling

One solution was **Function Calling**.

Developers define functions that the LLM can use.

For example:

```python
def get_weather(city):
    ...

def search_github(query):
    ...

def read_file(path):
    ...
```

The model can decide:

> "I need to use `read_file`."

The flow becomes:

```text
User
 ↓
LLM
 ↓
Select Tool
 ↓
Function Calling
 ↓
Function executes
 ↓
Result
 ↓
LLM
 ↓
Response
```

### Important distinction

The LLM usually does **not directly execute the function**.

It produces a structured request describing which tool should be called and with what arguments. The surrounding application executes it and gives the result back to the model.

### Key idea

> **Function Calling allows an LLM to request the execution of predefined functions or tools.**

---

# 10. Rise of Tools

Once Function Calling became common, developers started giving LLMs many different tools.

For example:

```text
LLM
 │
 ├── Web Search
 ├── Calculator
 ├── Database
 ├── Filesystem
 ├── GitHub
 ├── Weather
 ├── Email
 └── Code Execution
```

Now the LLM can do more than generate text.

It can:

```text
Understand
 ↓
Decide
 ↓
Use Tool
 ↓
Observe Result
 ↓
Decide Again
```

This is an important foundation for **AI Agents**.

### Key idea

> **Tools extend an LLM's capabilities by allowing it to interact with external systems and perform actions.**

---

# 11. Implication of Tools

Tools solve one problem but create another.

Suppose we have:

```text
100 AI Applications
```

and:

```text
100 External Tools
```

Every AI application may need to integrate with many of those tools.

So we start getting:

```text
AI App A → GitHub
AI App A → Slack
AI App A → Database

AI App B → GitHub
AI App B → Slack
AI App B → Database

AI App C → GitHub
AI App C → Slack
AI App C → Database
```

The same integration work gets repeated.

### Key idea

> **Tools make AI more capable, but a large number of tools creates an integration and maintenance problem.**

---

# 12. New Scenario

Now imagine the AI ecosystem growing.

We have:

```text
AI Clients
 ├── ChatGPT
 ├── Claude
 ├── Cursor
 ├── IDE Agents
 └── Custom AI Agents
```

And we have:

```text
External Systems
 ├── GitHub
 ├── Slack
 ├── PostgreSQL
 ├── Google Drive
 ├── Jira
 └── AWS
```

Every AI client wants access to these systems.

If every client builds its own integration:

```text
Client A ── GitHub
Client B ── GitHub
Client C ── GitHub
Client D ── GitHub
```

GitHub integration has to be implemented repeatedly.

We need a **common standard**.

---

# 13. Problem with Tools

The problem isn't that tools are bad.

The problem is **how tools are integrated**.

Without a standard:

```text
AI Client
 ↓
Custom Integration
 ↓
External System
```

Different clients may define and implement tools differently.

This creates:

* duplicated work
* inconsistent interfaces
* maintenance problems
* vendor-specific integrations
* difficulty reusing tools

So we need a standardized way for AI applications to interact with external capabilities.

### Key idea

> **The problem is not tool usage; it is the lack of a common protocol for connecting AI applications to tools and context.**

---

# 14. Overview of the Problem

Let's summarize the entire problem.

### LLMs need context

```text
LLM
 ↓
Needs external information
```

### LLMs need capabilities

```text
LLM
 ↓
Needs tools
```

### There are many external systems

```text
GitHub
Slack
Database
Filesystem
Jira
APIs
```

### There are many AI applications

```text
ChatGPT
Claude
Cursor
Custom Agents
```

### Everyone builds their own integrations

```text
AI App A → Custom GitHub integration
AI App B → Custom GitHub integration
AI App C → Custom GitHub integration
```

This creates **fragmentation**.

So the question becomes:

> **Can we create a standard way for AI applications to connect with external tools and context?**

---

# 15. The Solution

The solution is:

# Model Context Protocol — MCP

MCP provides a **standardized protocol** for connecting AI applications with external capabilities and context.

Instead of:

```text
AI App
 ↓
Custom GitHub integration
```

we can have:

```text
AI App
 ↓
MCP
 ↓
GitHub MCP Server
 ↓
GitHub
```

Similarly:

```text
AI App
 ↓
MCP
 ↓
PostgreSQL MCP Server
 ↓
PostgreSQL
```

The important idea is **standardization**.

### Key idea

> **MCP defines a common protocol through which AI applications can interact with external tools, resources, and other capabilities.**

---

# 16. MCP

Now we can define MCP precisely.

> **Model Context Protocol (MCP) is an open protocol that standardizes how AI applications connect to external data sources, tools, and capabilities.**

The simplified architecture is:

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
      ▼
External System
```

For example:

```text
AI Application
      │
      ▼
  MCP Client
      │
      ▼
GitHub MCP Server
      │
      ▼
GitHub API
      │
      ▼
GitHub
```

MCP creates a **standard communication layer** between the AI application and the external capability.

---

# 17. MCP vs Tool Calling

This distinction is extremely important.

## Tool Calling

Tool Calling is primarily about:

> **How does an LLM request that a tool be executed?**

Example:

```text
LLM
 ↓
"I want to call search_github"
 ↓
arguments
 ↓
Application executes tool
```

---

## MCP

MCP is about:

> **How does an AI application communicate with external tool/data providers through a standardized protocol?**

So:

```text
Tool Calling
=
Model → Tool request
```

while:

```text
MCP
=
AI Application ↔ External Capability
through a standardized protocol
```

They can work together.

A useful mental model:

```text
              AI Application
                    │
                   LLM
                    │
              Tool Calling
                    │
               MCP Client
                    │
                   MCP
                    │
              MCP Server
                    │
                 Tool
                    │
            External System
```

### Key takeaway

> **Function Calling is a mechanism for invoking tools; MCP is a protocol for standardizing how AI applications interact with external capabilities.**

---

# 18. MCP vs API

MCP and APIs are also different.

An **API** is an interface provided by a software system.

For example:

```text
Your Application
      ↓
GitHub API
      ↓
GitHub
```

MCP can sit between an AI application and that API:

```text
AI Application
      ↓
MCP Client
      ↓
MCP
      ↓
GitHub MCP Server
      ↓
GitHub API
      ↓
GitHub
```

The MCP server can handle the details of interacting with the underlying API.

### Think of it this way

```text
API
=
How a software system exposes its functionality.

MCP
=
How AI applications can interact with tools/data
through a standardized AI-oriented protocol.
```

MCP does **not** replace APIs.

It can **use APIs internally**.

---

# 19. Server Does the Heavy Lifting

This is one of the most useful concepts.

Suppose the AI wants:

> "Get my open GitHub issues."

The AI doesn't need to know:

```text
GitHub API endpoint
HTTP method
Authentication headers
Pagination
Response format
Rate limits
```

Instead, it can interact with an MCP tool.

```text
AI
 ↓
get_open_issues()
 ↓
MCP Server
 ↓
Handles GitHub API details
 ↓
GitHub API
 ↓
GitHub
```

The MCP Server handles the implementation details.

So:

```text
AI
=
"What do I want to do?"

MCP Server
=
"How do I actually do it?"
```

### Key idea

> **The MCP server hides the complexity of the underlying system and exposes a standardized interface to the AI application.**

---

# 20. Benefits

MCP provides several important benefits.

## 1. Standardization

A common protocol reduces the need for custom integrations.

```text
Instead of:

AI A → Custom GitHub
AI B → Custom GitHub
AI C → Custom GitHub

We can have:

AI Clients
    ↓
   MCP
    ↓
GitHub MCP Server
```

---

## 2. Reusability

An MCP server can potentially be used by multiple compatible AI applications.

```text
ChatGPT ──┐
Claude ───┤
Cursor ───┤
Agent ────┘
     ↓
GitHub MCP Server
```

---

## 3. Separation of concerns

The AI application doesn't need to contain all external-system logic.

```text
AI Application
      │
      │ MCP
      ▼
MCP Server
      │
      ▼
External System
```

Each component has a clearer responsibility.

---

## 4. Discoverability

An MCP server can expose information about the capabilities it provides.

For example:

```text
Tools:
 ├── search_repository
 ├── get_issue
 ├── create_issue
 └── list_pull_requests
```

The client can discover these capabilities and make them available to the model.

---

## 5. Ecosystem

Standardization makes it easier for developers to build reusable MCP servers.

Instead of building integrations specifically for one AI application, developers can build against the MCP standard.

### Key idea

> **MCP reduces integration complexity by standardizing communication between AI applications and external capabilities.**

---

# 21. MCP Ecosystem

Finally, we get the MCP ecosystem.

Think of three layers:

```text
┌──────────────────────────────┐
│        AI Applications       │
│ ChatGPT / Claude / IDEs etc. │
└──────────────┬───────────────┘
               │
               │ MCP
               ▼
┌──────────────────────────────┐
│          MCP Servers         │
│ GitHub / DB / Slack / Files  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       External Systems       │
│ APIs / Databases / Services  │
└──────────────────────────────┘
```

An MCP server can expose capabilities such as:

### Tools

Actions the AI can request.

```text
create_issue()
search_database()
send_message()
```

### Resources

Information that can be provided to the AI application.

```text
documents
files
database information
application data
```

### Prompts

Reusable prompt templates or interaction patterns.

```text
code_review_prompt
summarization_prompt
```

This forms an ecosystem where:

```text
AI Applications
       ↓
    MCP Clients
       ↓
   MCP Protocol
       ↓
   MCP Servers
       ↓
Tools / Resources
       ↓
External Systems
```

---

# The Whole WHY in One Flow

This is the version I would actually memorize:

```text
LLMs
 ↓
Become widely adopted
 ↓
People want AI to interact with the real world
 ↓
AI needs Context
 ↓
AI needs Tools
 ↓
Function Calling enables tool usage
 ↓
Number of tools increases
 ↓
AI applications need many integrations
 ↓
Integrations become fragmented
 ↓
Same integrations are repeatedly implemented
 ↓
We need a common standard
 ↓
MCP
 ↓
Standardized communication between
AI applications and external capabilities
```

## The core idea

> **MCP exists because powerful AI systems need access to external context and capabilities, but building separate integrations for every AI application and every external system does not scale. MCP provides a standardized protocol for connecting them.**

And the three terms you absolutely should keep separate are:

```text
LLM
│
├── Tool Calling
│      └── Model requests a tool
│
├── API
│      └── Software system exposes functionality
│
└── MCP
       └── Standardized protocol for AI ↔ capabilities
```

This is the foundation. Once this **WHY** is solid, the next topic—**MCP Architecture: Host → Client → Server → Tools/Resources/Prompts**—will make much more sense.
