# Token-Efficient Architecture

> [!IMPORTANT]
> Design codebases to be optimally understood and operated on by AI coding agents, with a primary focus on minimizing the amount of context (tokens) required for any given modification.

## Key Insight
**Managing context is managing results.** In the generative AI age, a codebase's architecture directly impacts its token efficiency. A well-structured, token-efficient architecture leads to faster, cheaper, and more accurate results from AI coding tools.

### Core Tenets
-   **Modularity:** Keep components small, focused, and with a clear separation of concerns. This allows the AI to load only the relevant pieces into its context window.
-   **Descriptive Naming:** Use clear, unambiguous names for files, directories, classes, and functions. This provides a low-token way for the AI to understand the purpose of different code elements.
-   **High Test Coverage:** A comprehensive test suite provides a reliable, low-token way for an AI agent to verify its changes without needing to understand the entire application logic.
-   **Logical Structure:** Employ clear architectural patterns (e.g., Atomic Design, Layered Architecture) that are easy for both humans and AI to navigate.

### Example: File Structure

**High Token Efficiency (Good):**
```plaintext
# Atomic Design: Small, independent, and easy to load specific context.
source/
  atoms/      
    - insert.py
    - query.py
  molecules/  
    - user_model.py # Composes atoms, clear purpose
```

**Low Token Efficiency (Bad):**
```plaintext
# Monolithic: Vague, large files require loading the entire thing into context.
source/
  - database_stuff.py 
  - utils.py # Overloaded with unrelated functions
```

### Connections
- **Related to:** [[context-management]]
- **Enables:** [[efficient-ai-operation]], [[cost-optimization]]
- **Contrasts with:** [[monolithic-architecture]]

### Metadata
- **Domain:** AI Architecture
- **Source:** `dabeidyv5dg.md`
- **Tags:** #principles #architecture #token-efficiency #context-management #ai-agents #modularity #separation-of-concerns
