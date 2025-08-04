# Phase 2: Methodical Planning (Config: GEMINI_WITH_REASONING)

<reasoning>
The project structure clearly delineates between natural language prompts (text files), machine-readable tool definitions (JSON files), and general project documentation (Markdown license file). The initial findings further elaborate on the nature of these files, identifying them as core components of AI agent configurations and prompt engineering.

Based on this, I've identified three distinct areas of expertise required for a thorough analysis:

1.  **Prompt Content Analysis:** Requires expertise in understanding, evaluating, and documenting the intent, structure, and effectiveness of natural language prompts for AI models. This naturally covers all `.txt` files.
2.  **AI Tooling and Schema Analysis:** Requires expertise in interpreting structured data formats, specifically JSON, as they define the capabilities and interfaces of AI agent tools. This is crucial for all `.json` files.
3.  **Project System and Legal Integration:** Requires a high-level understanding of the project's overall purpose, its architectural implications, and its legal framework. This role is best suited for the top-level documentation like the `LICENSE.md` file and considering how all components fit together within potential AI ecosystems.

This leads to a team of three agents, ensuring all file types are covered by appropriate expertise without unnecessary overlap, while remaining within the specified range of 3 to 5 agents.
</reasoning>

<analysis_plan>
<agent_1 name="Prompt Content Specialist">
<description>This agent is responsible for analyzing and documenting the content, purpose, and optimal usage of all natural language prompts. Their expertise lies in prompt engineering, understanding LLM behavior, and identifying variations or specific use-cases for each prompt file.</description>
<file_assignments>
<file_path>Cluely/Default Prompt.txt</file_path>
<file_path>Cluely/Enterprise Prompt.txt</file_path>
<file_path>Cursor Prompts/Agent Prompt v1.0.txt</file_path>
<file_path>Cursor Prompts/Agent Prompt v1.2.txt</file_path>
<file_path>Cursor Prompts/Agent Prompt.txt</file_path>
<file_path>Cursor Prompts/Chat Prompt.txt</file_path>
<file_path>Cursor Prompts/Memory Prompt.txt</file_path>
<file_path>Cursor Prompts/Memory Rating Prompt.txt</file_path>
<file_path>Devin AI/Prompt.txt</file_path>
<file_path>dia/Prompt.txt</file_path>
<file_path>Junie/Prompt.txt</file_path>
<file_path>Lovable/Prompt.txt</file_path>
<file_path>Manus Agent Tools & Prompt/Agent loop.txt</file_path>
<file_path>Manus Agent Tools & Prompt/Modules.txt</file_path>
<file_path>Manus Agent Tools & Prompt/Prompt.txt</file_path>
<file_path>Open Source prompts/Bolt/Prompt.txt</file_path>
<file_path>Open Source prompts/Cline/Prompt.txt</file_path>
<file_path>Open Source prompts/Codex CLI/Prompt.txt</file_path>
<file_path>Open Source prompts/RooCode/Prompt.txt</file_path>
<file_path>Replit/Prompt.txt</file_path>
<file_path>Same.dev/Prompt.txt</file_path>
<file_path>Spawn/Prompt.txt</file_path>
<file_path>Trae/Chat Prompt.txt</file_path>
<file_path>v0 Prompts and Tools/Prompt.txt</file_path>
<file_path>VSCode Agent/Prompt.txt</file_path>
<file_path>Warp.dev/Prompt.txt</file_path>
<file_path>Windsurf/Prompt.txt</file_path>
</file_assignments>
</agent_1>

<agent_2 name="AI Tooling Architect">
<description>This agent specializes in the analysis of machine-readable tool definitions. Their role involves understanding the JSON schemas, identifying the capabilities and parameters of each tool, and documenting their integration points with AI agents and external systems.</description>
<file_assignments>
<file_path>Cursor Prompts/Agent Tools v1.0.json</file_path>
<file_path>Manus Agent Tools & Prompt/tools.json</file_path>
<file_path>Replit/Tools.json</file_path>
<file_path>Same.dev/Tools.json</file_path>
<file_path>Windsurf/Tools.json</file_path>
</file_assignments>
</agent_2>

<agent_3 name="Project System Integrator">
<description>This agent is responsible for understanding the overarching project structure, the relationships between different components, and ensuring compliance with licensing terms. They provide high-level context for the entire repository and manage general project documentation.</description>
<file_assignments>
<file_path>LICENSE.md</file_path>
</file_assignments>
</agent_3>
</analysis_plan>