---
tags:
  - AI
  - coding
  - multifile_editing
---
# Summary of "what's up Engineers Andy Dev Dan here"

This video explores the use of AI coding tools, focusing on the open-source tool **AER** as an alternative to the commercial application **Cursor**. It demonstrates how to build and iterate on diagrams using a Mermaid AI agent, highlights the benefits of AI-assisted coding, and showcases practical coding workflows with AER. The video emphasizes the importance of diversifying AI tools and leveraging generative AI for efficient engineering communication.

---

## Introduction and Context

### [00:00:00] Introduction to AI Coding Tools
- Andy Dev Dan introduces the topic of AI coding tools, highlighting the recent popularity of **Cursor** due to its multifile editing composer feature.
- He cautions against relying solely on Cursor as it is a closed-source commercial product.
- Presents **AER**, an open-source, LLM-based AI coding tool that offers more control and is free with multiple LLM providers.
- Sets the stage for demonstrating an alternative AI agent for diagramming using Mermaid.

---

## Building and Iterating Diagrams with Mermaid AI Agent

### [00:01:00] Overview of Mermaid AI Agent
- Explanation of Mermaid as a text-based diagramming and charting tool.
- Demonstrates running commands to generate node-edge diagrams from simple text prompts.
- Shows how the Mermaid AI agent reads input files, generates diagrams, and supports iterative improvements.

### [00:02:00] Iterative Diagram Generation
- Walkthrough of the prompt structure using Python's Typer function.
- Example prompt: flowchart explaining the importance of communication via diagramming in engineering.
- Demonstrates iterative commands to add nodes, group benefits, and adjust diagram layout (e.g., left-to-right orientation).

### [00:03:00] Finalizing Diagram Connections
- Adds edges between nodes to complete the flowchart.
- Highlights the power of generative AI combined with Mermaid for rapid asset generation.
- Discusses saving generated diagrams and the need to preserve all iteration versions.

---

## AI Coding Workflow with AER

### [00:04:00] Setting Up AER for Diagram Saving
- Introduces terminal-based usage of AER for AI coding.
- Shows adding source files to AER's context window for better code understanding.
- Uses AER's `/ask` command to identify where and how diagrams are saved in the codebase.

### [00:06:00] Reusing Existing Functionality
- Explores existing utility functions for building file paths to output directories.
- Demonstrates how AER suggests code changes to save diagrams in the output directory with iteration numbers.

### [00:07:00] Implementing AI-Suggested Changes
- Walks through applying AER's code modifications, including imports and updated save logic.
- Emphasizes the value of human-in-the-loop iterative AI coding using `/ask` and `/make` commands.

### [00:08:00] Drafting and Refining Iteration Saving
- Requests AER to draft changes for saving every iteration of Mermaid diagrams.
- Reviews the reasoning behind AI coding suggestions before implementation.
- Updates main loop to save incremented iteration files.

---

## Demonstration: Creating and Iterating on Pie Charts

### [00:09:00] Running Iterative Pie Chart Example
- Opens a new terminal and runs the Mermaid AI agent to generate a pie chart.
- Adds new pie slices via AI prompts, e.g., "mastering AI coding with Andy Dev Dan."
- Verifies saved files reflect iterative changes with new slices.

### [00:11:00] Encouragement to Engage with AI Coding
- Encourages viewers to like and subscribe for more AI coding content.
- Highlights the importance of staying current with generative AI tools like AER and Cursor.

---

## Advanced Features: Bulk Diagram Generation

### [00:12:00] Introducing Bulk Command for Multiple Iterations
- Plans a new command to generate multiple versions of a flowchart using a `-c` flag.
- Adds necessary files to AER's context and requests code changes to support bulk generation.

### [00:14:00] AI-Assisted Multifile Changes
- AER automatically updates multiple files to implement the bulk command.
- Creates new parameter types and input files as needed.
- Reviews generated code and reruns prompts to test bulk generation.

### [00:15:00] Results of Bulk Diagram Generation
- Successfully generates multiple versions of setup instruction flowcharts.
- Shows variations in verbosity and detail across generated diagrams.
- Demonstrates the power of generating multiple design options quickly.

---

## Reflections on AI Coding Tools and Future Trends

### [00:17:00] Performance and Cost Metrics
- Highlights AER's efficiency with token usage and cost tracking.
- Notes the trend toward larger context windows (up to 100 million tokens) in LLMs.
- Mentions emerging companies pushing context window limits.

### [00:18:00] AER's Leadership in AI Coding
- Praises Paul and AER for leading benchmarks in AI coding performance.
- Suggests Cursor could benefit from publishing similar benchmarks.
- Recommends AER as a customizable, free alternative to Cursor.

### [00:20:00] Importance of Diagramming and Communication
- Emphasizes the value of generating and iterating diagrams quickly for engineering communication.
- Encourages mid to senior engineers to use diagrams to convey work value effectively.
- Advocates for using generative AI tools to accelerate diagram creation and iteration.

---

## Conclusion and Call to Action

### [00:21:00] Final Thoughts on AI Tool Diversification
- Reiterates the importance of diversifying AI coding tools rather than relying on a single commercial product.
- Encourages staying close to prompts and tooling for maximum control.
- Invites viewers to join the journey of exploring AI coding tools, stay updated on trends, and engage with the community.

---

# Key Takeaways

- **AER** is a powerful, open-source AI coding assistant that offers more control and is cost-effective compared to commercial tools like Cursor.
- Using a **Mermaid AI agent** enables rapid, iterative diagram generation directly from text prompts.
- The **human-in-the-loop** approach with AER’s `/ask` and `/make` commands enhances AI coding accuracy and customization.
- Generating **multiple diagram versions** helps explore design options and improves communication.
- Staying **diversified and informed** about AI coding tools is crucial in the fast-evolving generative AI landscape.

---

This video provides a comprehensive guide to leveraging AI for coding and diagramming, demonstrating practical workflows and encouraging engineers to adopt open-source tools for greater flexibility and innovation.

---
[[_NoteCompanion/Backups/Whats Up Engineers Andy Dev Dan Here 1 2_backup_20250509_175955.md | Link to original file]]