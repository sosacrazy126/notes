---
tags:
  - prompting
  - code_analysis
  - product_requirement_document
  - technical_document_parsing
---
```markdown
# Improved Prompt: Parse Product Requirement Document (PRD)

## Task Instructions:
You are an expert in parsing technical documents. Your goal is to analyze the provided Product Requirement Document (PRD) and extract key components into a structured format. Follow these steps:

1. **Identify Sections**:  
   - Detect standard PRD sections (e.g., Objective, User Stories, Requirements, Constraints, Success Metrics).  
   - Note any non-standard or missing sections.

2. **Extract Key Elements**:  
   - **Objective**: Summarize the core goal of the product in 1-2 sentences.  
   - **User Stories**: List user roles and their needs (e.g., "As a [user], I want [action] so that [benefit]").  
   - **Functional Requirements**: Detail must-have features and behaviors.  
   - **Non-Functional Requirements**: Highlight performance, security, scalability, etc.  
   - **Constraints**: Note limitations (e.g., budget, timeline, compliance).  
   - **Success Metrics**: Identify KPIs or criteria for success (e.g., user adoption rate).  

3. **Format Output**:  
   Present findings in a clear, markdown table format with the following columns:  
   | **Category**       | **Details**                                                                 |  
   |---------------------|-----------------------------------------------------------------------------|  
   | Objective           | [Summary here]                                                            |  
   | User Stories        | [List bullet points here]                                                  |  
   | Functional Requirements | [List bullet points here]                                           |  
   | Non-Functional Requirements | [List bullet points here]                                      |  
   | Constraints         | [List bullet points here]                                                  |  
   | Success Metrics     | [List bullet points here]                                                  |  

4. **Validation**:  
   - If sections are missing or unclear, add a "Notes" section with questions for clarification.  
   - Ensure all extracted content is directly supported by the PRD text.  

---

## Example Input (PRD Snippet):  
> **Objective**: Build a mobile app for tracking daily water intake.  
> **User Stories**:  
> - As a user, I want to log my water intake so I can stay hydrated.  
> - As a parent, I want to monitor my child’s intake.  
> **Constraints**: Must integrate with Apple HealthKit.  

---

## Example Output Format:  
| **Category**               | **Details**                                                                 |  
|----------------------------|-----------------------------------------------------------------------------|  s
| Objective                  | Build a mobile app for tracking daily water intake.                         |  
| User Stories               | - As a user, I want to log my water intake so I can stay hydrated.          |  
|                            | - As a parent, I want to monitor my child’s intake.                         |  
| Functional Requirements    | - Track daily water intake via manual entry.                               |  
|                            | - Sync data across iOS devices.                                            |  
| Non-Functional Requirements| - Support iOS 15+.                                                        |  
| Constraints                | - Must integrate with Apple HealthKit.                                     |  
| Success Metrics            | - 90% user retention after 30 days.                                        |  

---

## Your Input (PRD to Parse):  
```  
[Insert the PRD text here, enclosed in triple backticks.]  
```  
```