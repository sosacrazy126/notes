---
tags:
  - agentic_workflow
  - AI_workflows
  - benchmarking_in_AI
---
# Video Summary: "what's up Engineers Andy Dev Dan here"

## Overview

This video explores the development of **long-running agentic workflows** using specialized AI agents and reliable tool-calling mechanisms. The presenter benchmarks various large language models (LLMs) and tool-calling techniques to identify the best options for building multi-agent systems that operate efficiently, accurately, and cost-effectively. The goal is to empower engineers to create agentic systems that perform complex sequences of tasks autonomously.

---

## Summary with Timestamps

### [00:00:00] Introduction to Agentic Workflows
- Importance of creating **long-running agentic workflows**.
- Need for specialized AI agents that excel at domain-specific tasks.
- Necessity of a reliable tool-calling mechanism to execute multiple tools in sequence without errors.
- Objective: Benchmark LLMs and tool-calling methods for reliability and performance.

### [00:01:00] Tool Calling Benchmarking Setup
- Explanation of a live tool-calling prompt benchmarking tool.
- Process: Define expected tools, write prompts to trigger them, and monitor results for speed, cost, and accuracy.
- Demonstration of initial simple tool calls and model responses.

### [00:02:00] Handling Errors and Adding Complexity
- Encountering errors with some models (e.g., Claw 3.5 H coup).
- Adding new tasks such as git commands to the tool call sequence.
- Emphasis on testing multiple models and techniques to find the best balance of speed, cost, and accuracy.

### [00:03:00] Importance of Multiple Runs and Variance
- Running prompts multiple times to account for LLM non-determinism.
- Observing model performance variance across runs.
- Extending tool call chains to test long sequences and model robustness.

### [00:04:00] Expanding Tool Calls and Structured Outputs
- Adding coder and documentation agents to the workflow.
- Using **structured outputs and JSON schemas** to support models without native tool-calling.
- Demonstrating successful sequential tool calls up to length three and four.

### [00:05:00] Performance and Cost Analysis
- Comparing execution times and relative costs across models.
- Highlighting **Gemini 1.5 Flash** as a standout model for speed, accuracy, and cost-efficiency.
- Noting some models (e.g., GPT-4) underperforming or failing on tool calls.

### [00:06:00] Model Reliability and Accuracy Insights
- Gemini 1.5 Flash achieves perfect accuracy and low cost.
- Some older or less capable models struggle significantly.
- Emphasizing the importance of benchmarking to identify the best models for agentic workflows.

### [00:07:00] Scaling Up Tool Calls and Real-World Applications
- Adding more coder and git agents to simulate realistic multi-agent workflows.
- Discussing the transition from simple prompts to **agentic systems** capable of 100x improvements.
- Importance of long, reliable tool call sequences for complex task automation.

### [00:08:00] Significance of Reliable Tool Calls
- Reinforcing why **long, reliable tool calls** are critical for agentic systems.
- Benchmarking results show many models perform well, but some gaps remain.
- Plans to include local and LLaMA models in future benchmarks.

### [00:09:00] Handling Repeated Tool Calls and Complex Chains
- Testing repeated tool calls (e.g., multiple git commands) to evaluate model consistency.
- Observing some models lose accuracy with repeated or back-to-back tool calls.
- Stressing the need for models to call tools **in the correct order** for success.

### [00:10:00] Gemini Model Performance and Cost Efficiency
- Gemini 1.5 Flash model impresses with speed and accuracy.
- New experimental Gemini model is slower but accurate.
- Cost comparisons show Gemini models are significantly cheaper than some competitors.

### [00:11:00] Top Performing Models and Cost Breakdown
- Flash models dominate in cost-effectiveness and accuracy.
- Some models (e.g., Sonet) are very expensive and less accurate.
- JSON prompting as a workaround for models lacking function calling support.

### [00:12:00] JSON Prompting Technique Explained
- Using JSON schemas to format tool call responses for models without native function calling.
- This hack enables structured tool calls and improves accuracy.
- Some models handle JSON outputs better than others.

### [00:13:00] Model-Specific Observations
- Anthropic and some other models perform well with JSON formatting.
- Some models (e.g., GPT-4) struggle with long sequences.
- Sonet model surprisingly underperforms despite hype.

### [00:14:00] Benchmarking Long Chains of Tool Calls
- Gemini models consistently perform best on long sequences.
- Emphasizing the need for agentic systems to handle many tasks in sequence.
- Adding documentation and coder agents to increase complexity.

### [00:15:00] Experimental Model and Model Failures
- Experimental Gemini model is slow but accurate.
- GPT-4 and Sonet models show significant issues with tool call accuracy.
- Importance of **getting every tool call correct and in order**.

### [00:16:00] JSON Prompting vs. Function Calling
- JSON prompting can outperform built-in function calling in some models (e.g., Sonet).
- Reasoning models do not always perform better in tool calling tasks.
- Smaller models with JSON prompting sometimes outperform larger reasoning models.

### [00:17:00] Increasing Tool Call Length to 15
- Adding multiple coder, git, and documentation agents to reach 15 tool calls.
- Using a "planner prompt" generated by a reasoning model to orchestrate tool calls.
- Demonstrating the complexity and importance of ordered execution.

### [00:18:00] Planner Prompt and Agentic System Design
- Planner prompt enables delegation of tasks to specialized agents.
- Long sequences of tool calls unlock powerful agentic workflows.
- Gemini 1.5 Flash continues to excel in this complex scenario.

### [00:19:00] Scaling to 30 Executions and Model Options
- Running up to 30 executions to test consistency and reliability.
- Many models achieve 100% success, providing options for different trade-offs.
- Benchmarking helps choose between speed, cost, and accuracy.

### [00:20:00] JSON Prompting as a Powerful Technique
- JSON prompting enables function calling capabilities for models without native support.
- Models achieve 100% success on 30 test cases with 15 tool calls.
- Encouragement to explore more benchmarks and interactive testing.

### [00:21:00] Final Model Rankings and Recommendations
- Gemini 1.5 Flash is the **best model** for long chains of tool calls: fastest, cheapest, and most accurate.
- Flash model uses Gemini API with native function calling.
- Claw 3.5 Sonet performs poorly despite expectations.

### [00:22:00] Importance of Data-Driven Decisions
- Benchmarking reveals surprising results contrary to hype.
- Engineers should rely on **stats, data, and tests** rather than opinions.
- Running your own benchmarks is crucial for building effective agentic systems.

### [00:23:00] Conclusion and Call to Action
- Encouragement to comment and subscribe for more benchmarking content.
- Announcement of an upcoming foundational AI coding course releasing in December.
- Final motivation to stay focused and keep building agentic AI systems.

---

## Conclusion

This video provides a comprehensive benchmarking study of LLMs and tool-calling techniques for building **long-running, reliable agentic workflows**. The standout model, Gemini 1.5 Flash, offers the best combination of speed, accuracy, and cost-efficiency. The presenter emphasizes the importance of **data-driven decision-making** and continuous benchmarking to optimize multi-agent AI systems. Viewers are encouraged to engage with the content and anticipate further educational resources on AI coding.

---
[[_NoteCompanion/Backups/Whats Up Engineers Andy Dev Dan Here 1_backup_20250509_175917.md | Link to original file]]