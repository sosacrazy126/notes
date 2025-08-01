# Architect Mode

> [!NOTE]
> A two-phase AI coding pattern where a powerful **reasoning model** acts as an "architect" to draft a comprehensive plan, which a faster **editor model** then accurately implements.

## Key Insight
By separating the cognitive load of **planning** from the mechanical task of **implementation**, this pattern dramatically improves the accuracy and reliability of large-scale, multi-file code generation. It leverages the unique strengths of different types of models.

### The Two-Phase Process
1.  **Phase 1: Architect (Reasoning Model)**
    *   A powerful, (often slower and more expensive) model like `gpt-4o` analyzes the user's request and the codebase.
    *   It produces a detailed, intermediate plan or a set of diffs outlining all the required changes without implementing them.
2.  **Phase 2: Editor (Fast Model)**
    *   A faster, more efficient model like `claude-3.5-sonnet` takes the architect's plan as input.
    *   It executes the plan precisely, applying the changes to the codebase.

### Example Command

```bash
# Use GPT-4o as the architect and Claude Sonnet as the editor
aider --architect-model gpt-4o --editor-model claude-3.5-sonnet "Refactor the auth service to use JWTs"
```

### Connections
- **Enhances:** [[spec-based-coding]]
- **Related to:** [[prompt-chaining]], [[separation-of-concerns]]
- **Optimizes for:** [[reasoning-models]]

### Metadata
- **Domain:** AI Coding Patterns
- **Source:** `spec-based-codingv4.txt`
- **Tags:** #patterns #two-phase #reasoning #architecture #planning #implementation #separation-of-concerns
