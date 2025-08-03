# /setup_ai_workflow - AI Development Workflow Automation

```yaml
---
command: "/setup_ai_workflow"
category: "Development Automation"
purpose: "Automate AI-enhanced development workflow setup and execution"
wave-enabled: false
performance-profile: "standard"
---
```

## 🎯 **Workflow Purpose**

Automate the complete AI-enhanced development cycle:
1. **Context Priming** → Load project knowledge into AI tools
2. **Specification Creation** → Generate detailed implementation plans
3. **Execution** → Run AI-guided implementation 
4. **Validation** → Test and verify results
5. **Documentation** → Update project knowledge base

## ⚙️ **Workflow Commands**

### **Context Priming Workflow**
```bash
/setup_ai_workflow --prime-context
# Automatically reads:
# - README.md (project overview)
# - AI_docs/ (conventions and architecture)
# - package.json/requirements.txt (dependencies)
# - src/ structure (current implementation)
```

### **Specification-Driven Development**
```bash
/setup_ai_workflow --spec-mode "feature-name"
# Creates: specs/features/feature-name.md
# Follows: High-level → Mid-level → Low-level task breakdown
# Generates: Implementation-ready specification
```

### **Automated Implementation**
```bash
/setup_ai_workflow --implement @specs/features/feature-name.md
# Executes: Sequential task implementation
# Validates: Each step before proceeding
# Tests: Automated testing after completion
```

## 📋 **Context Priming Templates**

### **Frontend Project Context**
```markdown
# Frontend Project Context

## Tech Stack
- Framework: [React/Vue/Angular]
- Styling: [CSS/SCSS/Tailwind/Styled-components]
- State Management: [Redux/Zustand/Context]
- Build Tool: [Vite/Webpack/Parcel]
- Testing: [Jest/Vitest/Cypress]

## Key Patterns
- Component structure: [Pattern description]
- State management: [How state is handled]
- API integration: [HTTP client and patterns]
- Styling approach: [CSS methodology]

## Development Guidelines
- File naming: [Convention]
- Component props: [TypeScript interfaces]
- Error handling: [Pattern used]
- Performance: [Optimization strategies]
```

### **Backend Project Context**
```markdown
# Backend Project Context

## Tech Stack
- Runtime: [Node.js/Python/Go/Rust]
- Framework: [Express/FastAPI/Gin/Actix]
- Database: [PostgreSQL/MongoDB/Redis]
- ORM/ODM: [Prisma/SQLAlchemy/GORM]
- Testing: [Jest/pytest/go test]

## Architecture
- API design: [REST/GraphQL/gRPC]
- Authentication: [JWT/OAuth/Sessions]
- Authorization: [RBAC/ABAC patterns]
- Data validation: [Schema validation approach]

## Development Guidelines
- Route structure: [Organization pattern]
- Error handling: [Error response format]
- Logging: [Logging strategy]
- Security: [Security measures implemented]
```

## 🚀 **Specification Templates**

### **Feature Specification Template**
```markdown
# Feature: [Feature Name]

## High-Level Objective
[Single sentence describing the complete feature goal]

## Mid-Level Objectives
- [User interface requirements and behavior]
- [Data management and persistence needs]
- [Integration requirements with existing systems]
- [Performance and quality requirements]
- [Testing and validation requirements]

## Implementation Notes
- Use [specific library/framework] for [functionality]
- Follow [existing pattern] established in [reference file]
- Ensure compatibility with [existing component/system]
- Reference [API/documentation] for [external integration]

## Context
**Beginning Files**: 
- [List current files relevant to this feature]

**Ending Files**:
- [List files that should exist after implementation]

**Dependencies**:
- [New libraries/packages needed]
- [Configuration changes required]
- [Database migrations/changes needed]

## Low-Level Tasks

### 1. Create Core Component/Module
```aider
Create the main [component/module/service] for [feature name].

Requirements:
- [Specific requirement 1]
- [Specific requirement 2]
- [Integration requirement]

Files to create/modify:
- [File path 1] - [Purpose]
- [File path 2] - [Purpose]

Implementation details:
- [Technical detail 1]
- [Technical detail 2]
```

### 2. Implement Data Layer
```aider
Set up data persistence and management for [feature name].

Requirements:
- [Data structure requirements]
- [CRUD operations needed]
- [Validation rules]

Files to create/modify:
- [Model/schema file] - [Data structure]
- [Repository/service file] - [Business logic]

Implementation details:
- [Database schema changes]
- [API endpoints or data access methods]
```

### 3. Add User Interface
```aider
Create user interface components for [feature name].

Requirements:
- [UI/UX requirements]
- [User interaction patterns]
- [Responsive design needs]

Files to create/modify:
- [Component files] - [UI components]
- [Style files] - [Styling]

Implementation details:
- [Component structure]
- [State management]
- [Event handling]
```

### 4. Integration and Testing
```aider
Integrate [feature name] with existing system and add tests.

Requirements:
- [Integration points]
- [Test coverage requirements]
- [Error handling]

Files to create/modify:
- [Test files] - [Test specifications]
- [Integration files] - [System integration]

Implementation details:
- [Unit tests for core functionality]
- [Integration tests for system compatibility]
- [Error handling and edge cases]
```
```

## 🧠 **Automated Workflows**

### **Development Cycle Automation**
```yaml
workflow_stages:
  1. context_prime:
      - Read project structure
      - Load conventions and patterns
      - Understand current implementation
      
  2. spec_creation:
      - Generate feature specification
      - Break down into implementation tasks
      - Validate completeness and clarity
      
  3. implementation:
      - Execute tasks sequentially
      - Validate each step
      - Handle errors and iterations
      
  4. testing:
      - Run automated tests
      - Validate functionality
      - Check integration points
      
  5. documentation:
      - Update relevant documentation
      - Add patterns to knowledge base
      - Create reusable prompts
```

### **Quality Gates**
```yaml
validation_checks:
  specification:
    - Clear high-level objective
    - Detailed mid-level objectives
    - Complete implementation notes
    - Proper task sequencing
    
  implementation:
    - Code compiles/runs without errors
    - Tests pass successfully
    - Follows project conventions
    - Integrates properly with existing code
    
  documentation:
    - README updated if needed
    - API documentation current
    - Code comments added where needed
    - Knowledge base updated
```

## 📊 **Workflow Execution Examples**

### **New Feature Development**
```bash
# Step 1: Initialize context
/setup_ai_workflow --prime-context

# Step 2: Create specification
/setup_ai_workflow --spec-mode "user-authentication"

# Step 3: Review and refine spec
# (Manual review of generated specs/features/user-authentication.md)

# Step 4: Implement feature
/setup_ai_workflow --implement @specs/features/user-authentication.md

# Step 5: Validate and test
/setup_ai_workflow --validate --run-tests
```

### **Bug Fix Workflow**
```bash
# Context-aware bug analysis and fix
/setup_ai_workflow --debug "user login fails intermittently"
# Generates: specs/fixes/login-fix.md with analysis and solution

/setup_ai_workflow --implement @specs/fixes/login-fix.md
/setup_ai_workflow --validate --regression-test
```

### **Refactoring Workflow**
```bash
# Systematic refactoring with AI assistance
/setup_ai_workflow --refactor "optimize database queries"
# Generates: specs/refactoring/db-optimization.md

/setup_ai_workflow --implement @specs/refactoring/db-optimization.md
/setup_ai_workflow --performance-test --validate
```

## 🎯 **Strategic Benefits**

**Consistency**: Standardized development process across all features
**Quality**: Built-in validation and testing at each stage
**Speed**: Automated context loading and specification generation
**Learning**: Captured patterns and knowledge for future reference
**Scalability**: Repeatable process that works for teams

**Ultimate Goal**: Transform development from ad-hoc coding to systematic, AI-enhanced workflows that produce consistent, high-quality results efficiently.