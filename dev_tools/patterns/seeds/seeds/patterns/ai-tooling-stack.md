# AI Tooling Stack

> [!NOTE]
> A hierarchical composition pattern where simple AI components build into progressively more powerful layers of automation, from prompts to fully agentic software.

## Key Insight
Effective AI engineering involves composing layers of abstraction. Each layer adds a new capability, allowing engineers to move from direct instruction (prompts) to high-level orchestration (assistants and agentic software).

### The Hierarchy of AI Composition
1.  **Layer 1: Prompts**
    *   The fundamental unit of knowledge work. Basic, direct instructions to an LLM.
2.  **Layer 2: AI Agents**
    *   **`Prompts + Logic + Data`**
    *   Specialized to solve a specific, bounded problem (e.g., a code-generating agent).
3.  **Layer 3: AI Assistants**
    *   **`Orchestration + Agents`**
    *   Manages and coordinates multiple specialized agents to accomplish a complex, multi-step task.
4.  **Layer 4: Agentic Software**
    *   **`Assistants + Autonomy`**
    *   Self-operating systems that can manage entire workflows with minimal human intervention.

### Example
| Layer     | Example Task                                    |
| :-------- | :---------------------------------------------- |
| Prompt    | "Generate a SQL query to fetch active users."   |
| Agent     | A `SQLAgent` that can access a DB schema to write and validate queries. |
| Assistant | An `AnalyticsAssistant` that uses the `SQLAgent` to fetch data, a `ChartingAgent` to visualize it, and a `ReportingAgent` to summarize it. |
| Agentic   | A self-operating pipeline that automatically generates a weekly user engagement report. |

### Connections
- **Builds on:** [[prompt-fundamental-unit]]
- **Enables:** [[parallel-engineering]], [[autonomous-coding]]
- **Evolution of:** [[traditional-programming]]

### Metadata
- **Domain:** AI Architecture Patterns
- **Source:** `4SnvMieJiuw.md`
- **Tags:** #patterns #architecture #composition #layers #ai-stack #hierarchical #automation #agentic-software
