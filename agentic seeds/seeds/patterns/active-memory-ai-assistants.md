# Active Memory for AI Assistants

> [!NOTE]
> A design pattern where a personal AI assistant maintains a working, short-term memory (like RAM) to hold relevant context for ongoing tasks, enabling more stateful and focused interactions.

## Key Insight
Statefulness is a primary challenge for AI assistants. An explicit, session-based "active memory," distinct from long-term knowledge, allows an assistant to maintain immediate context, much like a human's working memory.

### Application
1.  **Establish a Memory Store:** Create a simple, structured format for the active memory, such as a temporary JSON file.
2.  **Implement Memory Tools:** Build functions for the assistant to explicitly **`load`**, **`clear`**, and **`view`** content in its active memory.
3.  **Inject Memory into Prompts:** When performing tasks, automatically inject the contents of the active memory into the system prompt, often within a dedicated XML tag (e.g., `<active_memory>`).
4.  **Evolve to Automation:** Progress towards having the assistant automatically manage its own active memory based on the flow of the conversation.

### Example: Active Memory File

```json
// active_memory.json
{
  "current_focus": "structured_outputs_introduction_guide.md",
  "loaded_files": [
    "structured_outputs_examples.py"
  ],
  "key_concepts": [
    "structured outputs",
    "reasoning models",
    "pydantic validation"
  ]
}
```

### Connections
- **Enhances:** [[ai-assistants]]
- **Enables:** [[stateful-interaction]]
- **Related to:** [[context-management]]

### Metadata
- **Domain:** AI Assistant Design
- **Source:** `090oR--s__8.md`
- **Tags:** #patterns #ai-assistants #memory #statefulness #context #short-term-memory #RAM
