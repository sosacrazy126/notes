---
tags:
  - AI_integration
  - system_building
  - prompting
  - Claude_integration
  - system_building
---
PROJECT: Refactor Claude Task Master to use Cursor's Claude integration, reducing Anthropic API reliance via structured prompts and JSON outputs.  

SUMMARY: Replace Anthropic API calls with Cursor's Claude integration by redesigning prompt templates, refactoring task management logic, and updating workflow rules to process structured JSON outputs.  

### STEPS:  
1. Analyze existing AI service functions (e.g., `callClaude`, `generateSubtasks`).  
2. Design JSON-output prompts for Cursor's Claude integration.  
3. Refactor task management to parse and validate JSON responses.  
4. Update Cursor rules to handle prompts and trigger task functions.  
5. Redefine CLI commands to use Cursor's prompt-based workflows.  
6. Test components for compatibility and output accuracy.  
7. Optimize performance and gather user feedback for iterations.  

### STRUCTURE:  
```
├── src/  
│   ├── ai-services.js          # Handles AI interactions via Cursor  
│   ├── task-manager.js         # Manages task creation/updates  
│   └── tasks.json              # Task data storage  
├── .cursor/  
│   └── rules/  
│       └── dev_workflow.mdc    # Cursor workflow rules  
├── package.json                # Project dependencies  
└── README.md                   # Configuration and usage guide  
```

### DETAILED EXPLANATION:  
1. **ai-services.js**: Manages AI interactions, sends prompts to Cursor, and parses responses.  
2. **task-manager.js**: Processes JSON task data, validates dependencies, and updates task files.  
3. **tasks.json**: Stores task metadata in structured format.  
4. **dev_workflow.mdc**: Cursor rules to map prompts to task workflows.  
5. **package.json**: Defines project dependencies (e.g., `cursor-cli`).  
6. **README.md**: Instructions for setup and command usage.  

---

### CODE:  
#### **ai-services.js**  
```javascript
// Handles AI interactions with Cursor's Claude integration  
const cursor = require('cursor');  

async function callClaude(prompt) {  
  try {  
    const response = await cursor.run({  
      prompt: prompt,  
      model: "claude-3"  
    });  
    return JSON.parse(response.text); // Parse JSON output  
  } catch (error) {  
    console.error("Error parsing Claude response:", error);  
    return null;  
  }  
}  

// Example prompt for generating tasks from PRD  
const generateSubtasks = async (prdContent) => {  
  const promptTemplate = `  
  System: Break down the PRD into tasks. Output JSON matching:  
  { "tasks": [...] }  
  PRD Content: ${prdContent}  
  `;  
  return callClaude(promptTemplate);  
};  
```  

#### **task-manager.js**  
```javascript  
const fs = require('fs');  

function saveTasks(tasks) {  
  fs.writeFileSync('src/tasks.json', JSON.stringify(tasks, null, 2));  
  console.log("Tasks updated successfully");  
}  

function validateDependencies(tasks) {  
  // Ensure dependencies exist and are valid task IDs  
  tasks.forEach(task => {  
    if (task.dependencies.some(dep => !tasks.find(t => t.id === dep))) {  
      throw new Error("Invalid dependency detected");  
    }  
  });  
}  
```  

#### **.cursor/rules/dev_workflow.mdc**  
```markdown  
# Cursor Workflow Rules  

## Task Generation Workflow  
When user runs `cursor analyze-prd [file]`:  
1. Read [file] content.  
2. Run `generateSubtasks` with file content.  
3. Validate and save JSON output via task-manager.js.  
```  

#### **package.json**  
```json  
{  
  "dependencies": {  
    "cursor": "^1.0.0"  
  },  
  "scripts": {  
    "start": "cursor run"  
  }  
}  
```  

---

### SETUP:  
```bash  
mkdir cursor-task-master && cd $_  
npm init -y  
npm install cursor  
touch src/ai-services.js src/task-manager.js src/tasks.json  
mkdir -p .cursor/rules && touch .cursor/rules/dev_workflow.mdc  
echo "# Configuration..." > README.md  
```  

---

### TAKEAWAYS:  
1. Replaced expensive Anthropic API calls with cost-effective Cursor integration.  
2. Structured JSON outputs ensure consistency in task generation.  
3. Modular codebase simplifies updates and testing.  
4. Cursor workflows automate prompt execution and data processing.  

### SUGGESTIONS:  
1. Add error handling for malformed JSON responses.  
2. Implement environment variables for API keys.  
3. Create a CLI wrapper for Cursor commands.  
4. Add unit tests for task validation logic.