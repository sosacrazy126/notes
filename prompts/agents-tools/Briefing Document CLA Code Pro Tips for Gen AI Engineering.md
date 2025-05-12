---
tags:
  - agentic_workflow
  - AI_agents
---
# Overview

This briefing document summarizes key themes and actionable insights from two sources focusing on leveraging **CLA Code**, **Model Context Protocol (mCP)**, and **AI coding assistants/agents** to achieve **"asymmetric engineering"** in the age of generative AI. The central theme revolves around shifting from **"vibe coding"** (low-hanging fruit, manual work) to **"system building"** – creating reusable systems that leverage AI agents to automate and accelerate the software development process. **CLA Code**, particularly with the advancements in **Sonet 3.7**, is presented as a breakthrough tool for this **"agentic coding"** paradigm, especially when combined with the contextual power of **mCP**.

---

## Main Themes and Important Ideas

### The Paradigm Shift: From Vibe Coding to System Building

- Engineers should focus on building **"systems that build systems."**
- Leverage tools like **CLA Code** and AI agents to automate repetitive tasks and create reusable value.
- *"Vibe coding is the lowest hanging fruit; system building enables you to reuse the value you create over and over and over..."*
- This shift enables **"asymmetric engineering,"** where a small effort yields significant output through intelligent automation.

### CLA Code as a Key Enabler for Agentic Coding

- **CLA Code**, especially with **Anthropic's Sonet 3.7**, is a crucial tool for building and utilizing AI coding agents.
- *"CLA Code with Sonet 3.7 (Breakthrough Tool)"*
- The new text editor in **Sonet 3.7** allows agents to edit files precisely, a fundamental requirement for autonomous coding tasks.

### The Importance of Context (Context is King)

- Providing AI coding tools with the necessary context is paramount for their effectiveness.
- *"If you've been working in the AI coding space and if you've been working with language models you always want to be feeding CLA Code and your AI coding tools the context it needs to get the job done."*
- Engineers need to **think from the perspective of their AI agents** to understand what information and tools they need to accomplish tasks.

### Tools for Building Systems that Build Systems

| Tool/Concept                  | Description                                                                                  |
|------------------------------|----------------------------------------------------------------------------------------------|
| **CLA Code**                 | Central platform for interacting with AI agents.                                            |
| **mCP (Model Context Protocol)** | Mechanism for providing context and tools to AI agents through servers and predefined prompts. |
| **AI Coding Assistants and Agents** | Intelligent entities that perform coding and other development tasks.                        |

### Top Six CLA Code Pro Tips

These provide practical guidance on using **CLA Code** effectively:

1. **Context Priming**: Initializing CLA with project context at startup.
   - Use README prompts (e.g., get ls files) to help CLA understand the codebase.
   - Leverage parallel reads for efficient context loading.
   - Speeds up work and makes CLA more effective.
   - *"...when you first startup CLA it's effectively an empty agent it doesn't see what you see it can't see your code base it doesn't know what you know it's basically a blank page it's a blank agent we need to let it know what you're working on."*

2. **Context is King**: Actively feed AI tools the necessary information.
   - Think from the AI agent's perspective.
   - Use **Collectors** (e.g., fetch, fir crawl mCP) to gather context.
   - Use **Executors** (e.g., file editor agent) to perform actions.
   - The new file editor agent (Sonet 3.7) is a significant Executor.
   - The "token efficient tool use beta flag" can optimize resource usage.
   - *"...I think of mCP servers and tools in two classes we have collectors and we have executors first you collect contacts with your collectors and then you execute crud operations..."*

3. **Check Release Notes**: Use the `/release` command to stay updated on new CLA Code features.
   - *"...if we type slash release you can see that there are release notes now that's tip three it might seem simple but the CLA Code Engineers are really shipping in the shadows here and you want to be keeping track of everything you're releasing..."*

4. **Utilize Thinking Mode**: Leverage Claude's reasoning capabilities with commands like `/think`, `/think harder`, `/ultra think`.
   - Combine thinking mode with other tips, such as the efficiency flag, for more intelligent agent behavior.
   - *"...you can say ask Claude to make a plan with thinking mode so obviously they're tapping into Claude's Hybrid Base reasoning model capabilities if you say think think harder or Ultra think you will tap into these..."*

5. **Leverage Built-in Prompts (mCP)**: Use slash commands (e.g., `/fetch`, `/sql`) for quick access to predefined prompts within mCP servers.
   - mCP servers can have predefined prompts with variable inputs, making common tasks easier to initiate.
   - *"...the key thing I want to show off here is not the fetch tool again it's the fact that you can use these slash commands to quickly activate one of the prompts..."*

6. **Quickly Add mCP Servers (JSON)**: Add mCP servers using JSON string format with the `cla mcp add` command.
   - A step-by-step wizard (`cla mcp setup`) is also available for adding mCP servers.
   - Provides flexibility and speed in integrating new tools.
   - *"...you'll see that we can add mCP servers as JSON string so this is a simple but very useful way to get up and running with mCP servers inside of CLA Code..."*

### The Future of Engineering: Agentic Coding

- Agentic coding is the **"next big phase"** of software development.
- Combining **CLA Code** with **Sonet 3.7** and **mCP** enables extended agent capabilities.
- Focus shifts towards designing and architecting effective AI agents.
- Gathering and utilizing appropriate collection and execution tools for agents is crucial.
- *"...the next big phase is agentic coding and at the forefront really you know the poster child for this is CLA Code specifically with 3.7 Sonet it's a breakthrough tool that's allowing new capabilities for agented coding when you combine it with mCP you can now equip your AI coding assistant your agent to coding tool with all of the capabilities it needs to run not just programming tasks but to run tools that allow you to collect and execute across various domains..."*

### Importance of Tooling and Experimentation

- Engineers should actively build their **suite of tools** of both collection and execution tools.
- Experiment with different mCP servers and understand their capabilities.
- The specific tools needed depend on the engineer's domain and technology stack.

---

## Key Takeaways

- Embrace the shift towards building systems that utilize AI agents for software development.
- Master **CLA Code** and its new features, particularly those related to **Sonet 3.7**.
- Recognize the critical role of **context** in enabling effective AI coding agents and implement strategies for context priming and management.
- Utilize **mCP** to extend the capabilities of **CLA Code** by integrating various tools and defining reusable prompts.
- Stay informed about new **CLA Code** releases and leverage features like thinking mode to enhance agent intelligence.
- Focus on agent design and architecture as agentic coding becomes more prevalent.
- Actively explore and integrate collection and execution tools relevant to your engineering workflows.

---

This briefing highlights the significant potential of **CLA Code** and related technologies to revolutionize software engineering through intelligent automation. By adopting the principles outlined in these sources, engineers can achieve greater efficiency and impact in the age of generative AI.

---

#asymmetric_engineering  
#system_building

---

> [[_NoteCompanion/Backups/Briefing Document CLA Code Pro Tips for Gen AI Engineering_backup_20250410_195124.md | Link to original file]]

---
[[_NoteCompanion/Backups/Briefing Document CLA Code Pro Tips for Gen AI Engineering_backup_20250509_164305.md | Link to original file]]