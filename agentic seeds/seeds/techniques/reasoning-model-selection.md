# Reasoning Model Selection

> [!IMPORTANT]
> Know when to deploy expensive, powerful reasoning models (like the GPT-4o series) versus faster, cheaper base models by evaluating task complexity and precision requirements.

## Key Insight
Reasoning models excel at tasks requiring deep thinking, complex constraint satisfaction, and high accuracy on nuanced instructions. However, they are overkill and inefficient for simple, straightforward operations.

### Use Case Analysis

**Deploy Reasoning Models When:**
- Multiple, complex constraints must be satisfied simultaneously.
- The task requires deep, multi-step logical reasoning.
- High-fidelity adherence to specific instructions (like SEO keywords) is critical.
- Accuracy and quality are more important than speed and cost.
- You are executing a complex multi-file change via a spec prompt.

**Use Faster Base Models When:**
- The task involves simple transformations or generation.
- Speed and low latency are the primary concerns.
- Operations are budget-conscious.
- A straightforward, single-step prompt is sufficient.

### Example
| Task                                           | Recommendation          | Rationale                                    |
| ---------------------------------------------- | ----------------------- | -------------------------------------------- |
| Generate YouTube chapters with SEO constraints | **Reasoning Model**     | Requires satisfying multiple, nuanced rules. |
| Perform a simple variable rename across files  | **Fast Base Model**     | A simple, mechanical task with low ambiguity.|
| Architect a new microservice from a spec     | **Reasoning Model**     | Demands planning and understanding complex interactions.|
| Summarize a short block of text              | **Fast Base Model**     | Low-complexity task, speed is often preferred.|

### Connections
- **Related to:** [[model-selection]]
- **Part of:** [[big-three-alignment]]
- **Enhances:** [[spec-based-coding]]

### Metadata
- **Domain:** AI Model Selection
- **Source:** `GUVrOa4V8iE.md`
- **Tags:** #techniques #reasoning-models #model-selection #o1-series #optimization #cost-benefit #performance
