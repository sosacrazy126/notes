---
topics: "agentic AI, LLM collaboration, iterative AI workflows, multi-agent systems, AI decision-making"

tags: ["#youtube", "#agentic_workflow", "#LLM_agent_collaboration", "#iterative_AI_workflows"]

summary: "This video demonstrates how multiple large language model agents collaborate in an iterative loop to create and refine a marketing plan, showcasing advanced decision-making and agentic AI workflows beyond single LLM calls."

---

[![YouTube Video](https://www.youtube.com/watch?v=XXXXXXX)](https://www.youtube.com/watch?v=XXXXXXX)

**Detailed Summary:**

- The video introduces the concept of agentic AI, where multiple LLM agents work together in a loop to perform complex tasks by writing, critiquing, and deciding iteratively, moving beyond traditional single LLM text generation.

- It presents a marketing plan creation use case involving four specialized agents: an Orchestrator Agent managing the loop, a Writing Agent drafting the plan, a Critiquing Agent providing feedback, and an "Is It Done" Agent determining if the plan is complete.

- The workflow cycle starts with the Writing Agent producing a draft, followed by evaluation from the "Is It Done" Agent. If incomplete, the Critiquing Agent offers feedback, prompting the Writing Agent to revise the plan. This loop repeats until completion is confirmed.

- A code walkthrough shows a Jupyter notebook setup with two LLMs (OpenAI and X AI) and three agents configured with specific prompts to guide drafting, critiquing, and final decision-making. The "Is It Done" Agent signals completion using specific tags.

- The video demonstrates running each agent individually to illustrate their roles: initial drafting by the Writing Agent, evaluation by the "Is It Done" Agent (initially returning "no"), and detailed feedback from the Critiquing Agent.

- The orchestrator runs the full loop for up to 10 iterations, with the plan improving through successive revisions until the "Is It Done" Agent returns "yes," indicating completion after about three revisions.

- Analysis shows each revision enhances the marketing plan’s detail, formatting, and competitive analysis, illustrating how agentic AI produces superior outputs compared to single LLM calls.

- The conclusion highlights the benefits of agentic AI workflows with decision-making agents for sophisticated tasks and encourages further exploration of agent-based AI approaches.

- The video ends with a call to action inviting viewer comments, feedback, and suggestions for future content on advanced agentic AI examples.

---
[[_NoteCompanion/Backups/Agentic AI and LLM Collaboration in Workflow Loops_backup_20250512_073301.md | Link to original file]]