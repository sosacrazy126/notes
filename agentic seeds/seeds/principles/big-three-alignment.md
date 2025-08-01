# Big Three Alignment

> [!IMPORTANT]
> Every successful interaction with an AI coding assistant depends on the precise alignment of three critical elements: **Context**, **Model**, and **Prompt**.

## Key Insight
These three pillars form the foundational trinity of effective AI interaction. A weakness in one cannot be compensated for by strength in the others. Great AI coding happens at the "bullseye" where all three are perfectly balanced for the task at hand.

### The Three Pillars
1.  **Context:** The information the AI can see.
    *   **Goal:** Provide the *minimal sufficient* context. Too little causes hallucinations; too much causes confusion and high costs.
    *   **Includes:** Relevant files, documentation, library versions, and previous conversation turns.
2.  **Model:** The AI engine performing the task.
    *   **Goal:** Select the right model for the job. A simple task doesn't need a powerful, expensive reasoning model.
    *   **Includes:** `gpt-4o`, `claude-3.5-sonnet`, `gpt-4o-mini`, etc.
3.  **Prompt:** The instructions given to the AI.
    *   **Goal:** Craft clear, information-dense instructions that are unambiguous.
    *   **Includes:** Using action keywords, providing examples, and clearly stating the desired outcome.

### Example of Misalignment vs. Alignment

| Element     | Misaligned (Failure)                                | Aligned (Success)                                       |
| :---------- | :-------------------------------------------------- | :------------------------------------------------------ |
| **Context** | (Entire `src` directory is loaded)                  | `main.py`, `user_service.py`                            |
| **Model**   | `gpt-4o-mini` (Too weak for complex refactor)       | `claude-3.5-sonnet` (Appropriate for the task)          |
| **Prompt**  | "Fix the user stuff." (Vague)                       | "Refactor `user_service.py` to use the `Result` type." |

### Connections
- **Enables:** [[director-pattern]], [[spec-based-coding]]
- **Foundation for:** [[agentic-workflows]], [[all-ai-interaction]]

### Metadata
- **Domain:** AI Engineering Fundamentals
- **Source:** `principledaicodingv4.txt`, `multifileeditingv5.txt`
- **Tags:** #principles #fundamentals #ai-coding #context #model #prompt #balance #trinity #alignment
