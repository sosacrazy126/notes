# Context Management

> [!IMPORTANT]
> Effective AI coding requires precise, deliberate control over the files and information the AI assistant can see and modify. The composition of the **context window** is the single most important factor in determining the success of a multi-file edit.

## Key Insight
Context is the critical first pillar of the [[big-three-alignment]]. Too little context causes the AI to hallucinate or make incorrect assumptions. Too much context (or irrelevant context) confuses the AI, degrades performance, and increases cost. The art is in finding the perfect, minimal-sufficient context.

### Application
-   **Start Minimally:** Begin with the single most relevant file in the context.
-   **Add Progressively:** Add additional files only as they are explicitly needed. Use the AI to help you discover what's missing.
-   **Be Explicit:** Use explicit file paths and symbol names in your prompts to guide the AI's attention.
-   **Distinguish Read-Only vs. Editable:** Clearly separate which files are for reference (read-only) and which are intended to be modified. This prevents unintended side effects.
-   **Monitor Context Size:** Always be aware of your token count. A lean context window is a fast and effective one.

### Example

**Good (Precise and Minimal Context):**
1.  **Add `main.py` to context.**
2.  **Prompt:** "Move the `parse_arguments` function from `main.py` into a new file called `arg_parser.py`."
3.  **Result:** The AI knows exactly which function to move and where to put it, without needing any other files in context.

**Bad (Vague and Overloaded Context):**
1.  **Add the entire `src/` directory to context.**
2.  **Prompt:** "Refactor the argument handling."
3.  **Result:** The AI is confused, slow, and may make incorrect changes to unrelated files.

### Connections
- **Part of:** [[big-three-alignment]]
- **Enables:** [[multi-file-editing]], [[token-efficient-architecture]]
- **Related to:** [[information-density]]

### Metadata
- **Domain:** AI Coding Fundamentals
- **Source:** `multifileeditingv5.txt`
- **Tags:** #principles #context #multi-file #context-window #token-efficiency #precision
