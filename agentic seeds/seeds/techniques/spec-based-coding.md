# Spec-Based Coding

> [!IMPORTANT]
> Transform comprehensive plans (specifications) into powerful, multi-step prompts that can generate massive amounts of code in a single execution.

## Key Insight
**Great planning is great prompting.** For complex tasks, the most effective way to use a powerful reasoning model is to invest heavily in an upfront, detailed plan. The plan itself becomes the prompt.

### The Spec-Prompt Structure
1.  **High-Level Objective:** A single sentence defining the ultimate goal.
2.  **Mid-Level Objectives:** A bulleted list breaking the goal into 5-10 logical parts.
3.  **Implementation Notes:** Specific rules, constraints, or technical requirements the AI must follow.
4.  **Context Mapping:** Explicitly define the starting and ending state of files (what's available vs. what should be created).
5.  **Low-Level Tasks:** An ordered list of individual, information-dense prompts, often using AI-specific syntax like Aider's code blocks. This is where the detailed execution steps are defined.

### Example
```markdown
# High-Level Objective
Create a CLI application for transcript analytics.

# Low-Level Tasks
1.  `main.py`: Create the main CLI entry point using Typer.
2.  `analysis.py`: Implement a function to count word frequency.
3.  `reporting.py`: Add a function to generate a summary using the OpenAI API.
```

### Connections
- **Builds on:** [[big-three-alignment]]
- **Enables:** [[massive-code-generation]]
- **Works with:** [[architect-mode]]

### Metadata
- **Domain:** AI Coding Techniques
- **Source:** `spec-based-codingv4.txt`
- **Tags:** #techniques #planning #specs #prompting #specifications #code-generation #reasoning-models
