---
tags:
  - AI_workflow_system
  - multi_agent_system
  - code_analysis
---
PROJECT: Automate multi-model code reviews using prompt templates and MCP servers to generate fused analysis reports via parallel AI reasoning.  

SUMMARY: A Cloud Code-based system uses custom prompt templates to trigger parallel code reviews across OpenAI, Enthropic, and Gemini models, synthesizes results into a fused report, and integrates human feedback for actionable insights.  

STEPS:  
1. Create diff file from modified code  
2. Trigger parallel model reviews via prompt chain  
3. Save individual model outputs to subdirectory  
4. Synthesize results into fused markdown report  
5. Initiate human-in-the-loop recommendation step  

STRUCTURE:  
├── commands/  
│   └── ultra_diff_review.js  
├── mcp/  
│   └── MCP.json  
├── reviews/  
│   ├── openai/  
│   ├── anthropic/  
│   └── gemini/  
├── fused_reports/  
├── diff.md  
└── README.md  

DETAILED EXPLANATION:  
- **commands/ultra_diff_review.js**: Prompt template executing multi-step workflow  
- **mcp/MCP.json**: Model configuration for parallel compute providers  
- **reviews/**: Directory storing individual model outputs  
- **diff.md**: Generated file containing code differences  
- **fused_reports/**: Final synthesized review documents  
- **README.md**: Configuration and usage instructions  

CODE:  
**commands/ultra_diff_review.js**:  
```javascript  
// Cloud Code prompt template for parallel code reviews  
module.exports = {  
  name: "ultra_diff_review",  
  description: "Generate fused code review from 3 models",  
  steps: [  
    "git diff > diff.md", // Step 1: Capture changes  
    `just-prompt run -m openai,gemini,anthropic \  
      --input diff.md \  
      --output reviews/ \  
      "Analyze code changes for security/risk"`, // Step 2-3: Parallel reviews  
    "claude3.7 --reasoning fuse_reviews.md" // Step 4: Synthesize results  
  ]  
};  
```  

**mcp/MCP.json**:  
```json  
{  
  "providers": {  
    "openai": "gpt-4-1106",  
    "anthropic": "claude-3.7",  
    "gemini": "gemini-pro"  
  },  
  "parallelism": 3,  
  "budget": "high"  
}  
```  

**README.md**:  
```markdown  
# Ultra Code Review System  
1. Install Cloud Code & just-prompt  
2. Configure `MCP.json` with API keys  
3. Run `/project ultra_diff_review`  
4. Review fused report in `fused_reports/`  
```  

SETUP:  
```bash  
mkdir -p {commands,mcp,reviews/{openai,anthropic,gemini},fused_reports}  
echo 'export MCP_CONFIG=$(pwd)/mcp/MCP.json' >> .env  
curl -o commands/ultra_diff_review.js [template-url]  
```  

TAKEAWAYS:  
1. Prompt templates enable scalable compute orchestration  
2. Parallel model reviews reduce bias and improve accuracy  
3. Fused reports provide comprehensive risk assessments  
4. Cloud Code custom commands reduce repetitive workflows  

SUGGESTIONS:  
- Add error handling for failed model responses  
- Implement version control for review outputs  
- Support model weighting in fusion algorithm  
- Integrate with CI/CD pipelines for automated reviews