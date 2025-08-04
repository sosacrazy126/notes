# Director Pattern

> [!NOTE]
> An agentic workflow that **closes the loop** by combining AI code generation with automated execution and evaluation, allowing for iterative problem-solving.

## Key Insight
By adding an **execution command** and an **evaluator** to the standard `Context-Model-Prompt` trio, an AI assistant can autonomously generate code, run it, check the output, and then use the feedback to iteratively refine the code until the task is complete.

### The Director Loop
1.  **Generate:** The AI generates code based on an initial prompt.
2.  **Execute:** A predefined shell command (the `execution_command`) runs the newly generated code (e.g., `uv run pytest`).
3.  **Evaluate:** An evaluator (often another LLM call, i.e., "LLM-as-a-judge") assesses the output of the execution command.
4.  **Feedback & Repeat:**
    *   If the evaluation is successful, the loop terminates.
    *   If it fails, the error output is used as feedback to generate a new, improved prompt, and the loop continues.

### Example: `director.yaml` Configuration

```yaml
# The core prompt to start the process
prompt: "Refactor the user service to be more performant."

# The model doing the coding
model: "claude-3.5-sonnet"

# The command to run after code is generated
execution_command: "uv run pytest --disable-warnings"

# The model that judges the result
evaluator_model: "gpt-4o"

# The maximum number of attempts
max_iterations: 5
```

### Connections
- **Related to:** [[agentic-workflows]]
- **Enables:** [[autonomous-coding]]
- **Builds on:** [[big-three-alignment]]

### Metadata
- **Domain:** AI Coding Patterns
- **Source:** `letthecodewriteitselfv4.txt`
- **Tags:** #patterns #automation #agentic #loops #autonomous-coding #feedback-loops #execution #evaluation
