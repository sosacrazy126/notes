# /init_ai_project - AI-Enhanced Project Initialization Pattern

```yaml
---
command: "/init_ai_project"
category: "Project Setup & Development"
purpose: "Initialize new projects with AI-enhanced development infrastructure"
wave-enabled: false
performance-profile: "standard"
origin: "IndyDev AI Coding Principles → Reusable Pattern"
---
```

## 🎯 **Core Purpose**

Create standardized project structure optimized for AI-assisted development with:
- **AI docs**: Persistent knowledge base for context
- **specs**: Detailed plans and specifications  
- **dotcloud**: Reusable prompts and AI commands
- **Context priming**: Automated AI tool initialization

## 📁 **Standard Directory Structure**

```
project-root/
├── AI_docs/                    # Persistent knowledge base
│   ├── api_references.md       # Third-party API documentation
│   ├── conventions.md          # Code standards and patterns
│   ├── architecture.md         # System design decisions
│   └── dependencies.md         # Library usage and configuration
├── specs/                      # Planning and specifications
│   ├── features/               # Feature specifications
│   ├── technical/              # Technical design docs
│   └── templates/              # Spec templates
├── dotcloud/                   # AI tooling and prompts
│   ├── context_prime.md        # Project context priming
│   ├── common_prompts.md       # Reusable development prompts
│   └── workflows/              # Automated AI workflows
└── src/                        # Source code
```

## 🚀 **Initialization Workflow**

```bash
# Basic project setup
/init_ai_project "project-name" --type web-app

# Full-stack with database
/init_ai_project "api-service" --type full-stack --database postgres

# Python/data science project
/init_ai_project "ml-pipeline" --type python --ml-ready
```

## 📋 **Template Generation**

### **AI_docs/conventions.md Template**
```markdown
# Development Conventions

## Code Standards
- Language: [Primary language]
- Framework: [Main framework]
- Style Guide: [Style guide reference]
- Testing: [Testing framework]

## Architecture Patterns
- [Pattern 1]: Used for [purpose]
- [Pattern 2]: Applied when [condition]

## AI Tool Guidelines
- Primary AI: [Tool name and version]
- Context Files: [Key files for AI reference]
- Common Patterns: [Frequently used prompts]
```

### **specs/templates/feature_spec.md Template**
```markdown
# Feature Specification: [Feature Name]

## High-Level Objective
[Single sentence describing complete feature goal]

## Mid-Level Objectives
- [Specific implementation detail 1]
- [Specific implementation detail 2]
- [Specific integration requirement]
- [Specific quality requirement]

## Implementation Notes
- Use [framework/library] for [functionality]
- Follow [pattern/standard] for consistency
- Reference [existing component] for [purpose]

## Context
**Beginning Files**: [Files available at start]
**Ending Files**: [Files that should exist after completion]
**Dependencies**: [Required libraries/services]

## Low-Level Tasks

### 1. [Task description]
```aider
[Detailed implementation prompt]
```

### 2. [Next sequential task]
```aider
[Implementation details with specific instructions]
```
```

### **dotcloud/context_prime.md Template**
```markdown
# Project Context Primer

## Project Overview
**Name**: [Project name]
**Type**: [Application type]
**Tech Stack**: [Technologies used]
**Purpose**: [Primary goal/function]

## Key Files to Reference
- README.md - Project overview and setup
- package.json/requirements.txt - Dependencies
- src/main.[ext] - Entry point
- [Other critical files]

## Development Workflow
1. Read project structure and key files
2. Understand current implementation patterns
3. Reference AI_docs/ for conventions and standards
4. Use specs/ for detailed implementation plans
5. Apply dotcloud/ prompts for common tasks

## AI Tool Configuration
**Context Files**: AI_docs/, specs/, README.md
**Common Tasks**: [List frequent development tasks]
**Quality Gates**: [Testing and validation requirements]
```

## ⚙️ **Auto-Setup Commands**

### **Directory Creation**
```bash
mkdir -p AI_docs specs/features specs/technical specs/templates dotcloud/workflows src tests docs
```

### **Template Population**
```bash
# Generate basic templates based on project type
/init_ai_project --populate-templates --project-type [type]

# Create context priming file
/init_ai_project --generate-context-primer

# Set up common workflow prompts
/init_ai_project --setup-workflows
```

## 🧠 **Context Priming Automation**

### **Initial Context Setup**
```markdown
# Context Priming Command

## Objective
Prime AI tool with project context for effective development assistance

## Instructions
1. Read project README.md for overview
2. Examine directory structure and key files
3. Review AI_docs/ for conventions and standards
4. Understand current codebase patterns
5. Load common prompts from dotcloud/

## Key Context Files
- README.md - Project purpose and setup
- AI_docs/conventions.md - Development standards
- AI_docs/architecture.md - System design
- package.json/requirements.txt - Dependencies
- src/ - Current implementation
```

### **Feature Development Workflow**
```markdown
# Feature Development Process

## Planning Phase
1. Create feature spec in specs/features/
2. Define high-level and mid-level objectives
3. Break down into sequential implementation tasks
4. Identify required files and dependencies

## Implementation Phase  
1. Prime AI with project context
2. Execute specification tasks sequentially
3. Validate each implementation step
4. Run tests and quality checks

## Documentation Phase
1. Update relevant documentation
2. Add new patterns to AI_docs/conventions.md
3. Create reusable prompts in dotcloud/
4. Update README if needed
```

## 🎪 **Project Type Templates**

### **Web Application**
```yaml
structure:
  - Frontend: React/Vue/Angular setup
  - Backend: Express/FastAPI/Django config
  - Database: Connection and models
  - Testing: Unit and integration tests
  - Deployment: Docker and CI/CD
```

### **API Service**
```yaml
structure:
  - API: REST/GraphQL endpoint definitions
  - Models: Data models and validation
  - Services: Business logic layer
  - Database: Schema and migrations
  - Documentation: OpenAPI/Swagger specs
```

### **Python/ML Project**
```yaml
structure:
  - Data: Input/output data handling
  - Models: ML model definitions
  - Training: Training scripts and pipelines
  - Evaluation: Metrics and validation
  - Deployment: Model serving and APIs
```

## 🔧 **Quality Assurance**

### **Validation Checklist**
- [ ] All standard directories created
- [ ] Templates populated with project-specific information
- [ ] Context priming file configured
- [ ] Common workflows documented
- [ ] Dependencies and setup instructions clear
- [ ] AI tool integration ready

### **Success Criteria**
- AI tools can immediately understand project context
- Specifications follow consistent format
- Development workflows are documented and reusable
- Context priming reduces setup time for AI assistance
- Team members can quickly understand project structure

## 💡 **Usage Examples**

### **Initialize Web App**
```bash
/init_ai_project "todo-app" --type web-app --frontend react --backend express
# Creates full structure with React/Express specific templates
```

### **Initialize API Service**
```bash
/init_ai_project "user-service" --type api --database postgres --auth jwt
# Sets up API-focused structure with database and auth considerations
```

### **Initialize ML Project**
```bash
/init_ai_project "sentiment-analysis" --type ml --framework pytorch --data-source csv
# Creates ML-specific structure with data handling and model templates
```

## 🎯 **Strategic Benefits**

**Consistency**: Standardized structure across all projects
**Speed**: Immediate AI tool readiness and context understanding
**Quality**: Built-in best practices and validation workflows
**Scalability**: Reusable patterns and templates for team adoption
**Maintainability**: Clear documentation and development guidelines

**Goal**: Enable any developer to start a new project and immediately have AI-enhanced development capabilities with proper context, documentation, and workflows in place.