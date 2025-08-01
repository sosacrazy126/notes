# Human-in-the-Loop Iteration

> [!TIP]
> A collaborative pattern where a user provides iterative, natural language feedback to an AI agent, allowing for the progressive refinement of a generated output.

## Key Insight
For creative or subjective tasks where the desired output is hard to define in a single prompt (e.g., UI design, data visualization), a tight, conversational feedback loop is far more effective than attempting a perfect one-shot generation.

### Application Flow
1.  **Initial Generation:** The user provides a high-level request (e.g., "Create a flowchart of our release process"). The AI generates the first version.
2.  **Iterative Refinement Loop:**
    *   The user provides specific, incremental feedback (e.g., "Add a step for QA review," "Make the deployment node green").
    *   The AI applies the feedback and regenerates the asset.
    *   The loop continues until the user is satisfied with the result.

### Example: Mermaid Diagram Generation

```plaintext
User: "Create a pie chart of my daily tasks."
AI: (Generates a basic pie chart)

User: "Add a new slice called 'Mastering AI Coding' with a value of 5%."
AI: (Regenerates the chart with the new slice)

User: "Change the title to 'Daily Time Allocation'."
AI: (Regenerates the chart with the new title)
```

### Connections
- **Related to:** [[iterative-refinement]]
- **Enables:** [[collaborative-creativity]], [[generative-art]]
- **Contrasts with:** [[one-shot-generation]], [[spec-based-coding]]

### Metadata
- **Domain:** Human-AI Interaction
- **Source:** `ag-KxYS8Vuw.md`
- **Tags:** #patterns #human-in-the-loop #iteration #feedback #diagramming #creative-tasks #conversational-ui
