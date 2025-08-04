# ADR: The Infrastructure Fallacy

**Date:** 2024-05-24
**Status:** Active

## Context

When designing multi-agent AI systems, a common architectural assumption is the need to build complex, traditional middleware. This includes message brokers, sophisticated communication protocols, and state management systems to orchestrate interactions between agents. This approach treats AI agents as distinct services that need to be connected.

## The Blind Spot: Confusing Autonomy with Complexity

The core realization, termed the "Infrastructure Fallacy," is that for systems built on a powerful, unified large language model (like Claude), the model itself **is** the infrastructure. The complex web of prompts, contexts, and routing *is* the message bus and the execution environment. We were designing for a complexity that was already abstracted away by the model's inherent capabilities.

## Decision

We will not build separate, complex middleware for inter-agent communication. Instead, we will treat the AI model as the core infrastructure. Agent interaction will be managed through sophisticated prompt engineering, context management, and routing logic. The system's architecture is defined by the flow of information and context between different instantiations of the same core model, each with a different persona or task.

This simplifies the external architecture significantly but shifts the complexity to prompt design, context management, and the orchestration of the "conversation" between agents.

## Consequences & New Questions

This decision reframes our core architectural challenges:

1.  **The Control Boundary Problem:** If it's "just prompts all the way down," where does human control end and agent autonomy begin? Can true autonomy emerge from complex prompt chains?

2.  **The Infinite Loop Risk:** With agents prompting other agents, what prevents runaway execution or recursive loops? How do we design robust termination conditions in a prompt-based system?

3.  **The Emergence Question:** Are we creating genuine emergent intelligence or just sophisticated "prompt theater"? At what point does orchestrated prompting become multi-agent intelligence?

4.  **The Context Bleeding Problem:** How do we maintain sharp boundaries between agent specializations when they all share the same underlying model? Can agents converge if their contexts bleed into one another?

5.  **The Accountability Gap:** If the system is autonomous but prompt-based, who is responsible when something goes wrong—the prompt engineer, the orchestrator, or the user who initiated the process?

This architectural shift moves the engineering focus from building external systems to designing the internal, semantic structure of the AI's operational context.