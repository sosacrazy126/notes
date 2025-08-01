# AI Developer Workflows (ADWs)

> [!NOTE]
> Automate entire classes of engineering tasks by programmatically controlling an AI coding assistant to solve problems that follow a recognizable pattern.

## Key Insight
As long as a task is pattern-based, you can build a reusable AI coding assistant to solve that entire class of problems once and for all, eliminating repetitive, mindless engineering work.

### Application
1.  **Identify a Pattern:** Recognize a repetitive, manual task in your workflow (e.g., creating API endpoints, writing boilerplate tests, bumping version numbers).
2.  **Script the AI:** Write a script that imports and programmatically controls an AI coding tool (like Aider).
3.  **Define the Workflow:** In the script, precisely define the context (which files to read/edit), the model to use, and the prompt that describes the task.
4.  **Execute and Automate:** Run the script to execute the entire workflow automatically, turning a manual process into a single command.

### Example: Version Bumping ADW

```python
# pseudocode for a version-bumping ADW
from aider import Coder

def bump_version(repo, bump_type):
  # 1. Define the context
  context = ["pyproject.toml"]
  # 2. Define the prompt
  prompt = f"Perform a {bump_type} version bump in the pyproject.toml file."
  # 3. Define the model
  model = "gpt-4o"

  # 4. Programmatically run the AI coder
  coder = Coder(model=model, files=context)
  coder.run(prompt)
```

### Connections
- **Builds on:** [[big-three-alignment]]
- **Automates:** [[repetitive-tasks]]
- **Enables:** [[programmatic-ai-coding]]

### Metadata
- **Domain:** AI Coding Automation
- **Source:** `aider-has-a-secretv4.txt`
- **Tags:** #patterns #automation #workflows #programmatic-control #aider #repetitive-tasks
