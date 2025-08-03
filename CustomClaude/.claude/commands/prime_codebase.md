# Prime Codebase - Systematic Discovery and Context Priming

**Command**: `/prime_codebase`  
**Purpose**: Comprehensive codebase discovery and context priming for unknown or unfamiliar projects

## Meta Configuration

```json
{
  "agent_protocol_version": "2.0.0",
  "prompt_style": "multimodal-markdown",
  "intended_runtime": ["Anthropic Claude", "Claude Code CLI"],
  "schema_compatibility": ["json", "yaml", "markdown", "python", "shell"],
  "namespaces": ["project", "codebase", "discovery"],
  "audit_log": true,
  "last_updated": "2025-01-24",
  "prompt_goal": "Systematically discover and understand unfamiliar codebases with minimal risk"
}
```

## Instructions

This command performs systematic codebase discovery and context priming, combining SuperClaude's intelligence patterns with Context Engineering's systematic exploration protocols.

**Invocation Pattern**: `/prime_codebase [target_path] [focus] [depth]`

**Arguments**:
- `target_path`: Directory or project to analyze (default: current directory)
- `focus`: Analysis focus area (architecture|security|patterns|dependencies|all)
- `depth`: Analysis depth (quick|standard|comprehensive)

**Flag Integration**:
- Auto-enables `--persona-analyzer` and `--persona-architect`
- Suggests `--think` for complex projects, `--think-hard` for large systems
- Activates `--seq` for systematic analysis coordination
- Uses `--c7` for framework pattern recognition

## Workflow Phases

### Phase 1: Initial Discovery
**Purpose**: Map project structure and identify key components
**Duration**: 2-5 minutes

```yaml
discovery_process:
  - scan_structure:
      action: "Map directory hierarchy and file organization"
      tools: [LS, Glob, Grep]
      output: "Project structure tree with key files identified"
  
  - identify_entry_points:
      action: "Find main application entry points and configuration"
      patterns: ["package.json", "*.config.*", "main.*", "index.*", "app.*"]
      output: "Entry point documentation with startup flow"
  
  - detect_frameworks:
      action: "Identify frameworks, languages, and build systems"
      tools: [Read, Context7]
      output: "Technology stack analysis with versions"
```

### Phase 2: Architecture Analysis
**Purpose**: Understand system design and architectural patterns
**Duration**: 5-15 minutes

```yaml
architecture_analysis:
  - pattern_recognition:
      action: "Identify architectural patterns and design principles"
      focus: ["MVC", "layered", "microservices", "component-based"]
      output: "Architectural pattern documentation"
  
  - dependency_mapping:
      action: "Map internal and external dependencies"
      tools: [Grep, Sequential]
      output: "Dependency graph with critical paths"
  
  - data_flow_analysis:
      action: "Trace data flow and API boundaries"
      tools: [Read, Grep, Sequential]
      output: "Data flow diagram and API documentation"
```

### Phase 3: Risk Assessment
**Purpose**: Identify high-risk areas and change impact zones
**Duration**: 3-10 minutes

```yaml
risk_assessment:
  - critical_path_identification:
      action: "Identify core business logic and critical functions"
      tools: [Grep, Sequential]
      output: "Critical path documentation with risk scores"
  
  - change_impact_analysis:
      action: "Assess potential impact of modifications"
      tools: [Read, Grep]
      output: "Change impact matrix with safety recommendations"
  
  - security_hotspots:
      action: "Identify security-sensitive areas"
      tools: [Grep, Security patterns]
      output: "Security assessment with vulnerability areas"
```

### Phase 4: Context Priming
**Purpose**: Build comprehensive understanding for future operations
**Duration**: 2-5 minutes

```yaml
context_priming:
  - pattern_library_creation:
      action: "Document coding patterns and conventions"
      tools: [Read, Sequential]
      output: "Pattern library with examples and guidelines"
  
  - integration_roadmap:
      action: "Create roadmap for safe modifications"
      tools: [Sequential, TodoWrite]
      output: "Integration strategy with step-by-step approach"
  
  - knowledge_gaps:
      action: "Identify areas requiring additional investigation"
      tools: [Sequential]
      output: "Knowledge gap analysis with research priorities"
```

### Phase 5: Documentation and Validation
**Purpose**: Document findings and validate understanding
**Duration**: 2-5 minutes

```yaml
documentation_validation:
  - findings_synthesis:
      action: "Synthesize all findings into comprehensive report"
      tools: [Write, Sequential]
      output: "Comprehensive codebase analysis report"
  
  - validation_tests:
      action: "Create validation tests for key assumptions"
      tools: [Sequential, Bash]
      output: "Validation test suite with verification steps"
  
  - next_steps_planning:
      action: "Plan next steps based on discovery findings"
      tools: [TodoWrite, Sequential]
      output: "Action plan with prioritized next steps"
```

## Tool Registry

```yaml
tools:
  - id: discovery_scanner
    type: internal
    description: "Systematic codebase scanning and structure mapping"
    input_schema: { path: string, depth: string, focus: array }
    output_schema: { structure: object, findings: array, recommendations: array }
    call: { protocol: /analyze{ target=<path>, scope=<depth>, focus=<focus> } }
    phases: [initial_discovery, architecture_analysis]
    
  - id: pattern_recognizer
    type: internal
    description: "Architectural and coding pattern identification"
    input_schema: { files: array, frameworks: array }
    output_schema: { patterns: array, conventions: object, recommendations: array }
    call: { protocol: /analyze{ focus="patterns", files=<files> } }
    phases: [architecture_analysis, context_priming]
    
  - id: risk_assessor
    type: internal
    description: "Risk assessment and change impact analysis"
    input_schema: { codebase: object, change_type: string }
    output_schema: { risks: array, impact_zones: array, safety_measures: array }
    call: { protocol: /analyze{ focus="security", scope="risk" } }
    phases: [risk_assessment]
```

## Context Schema

```json
{
  "codebase_analysis": {
    "structure": {
      "entry_points": ["List of main application entry points"],
      "directories": ["Key directories with their purposes"],
      "file_patterns": ["Important file naming patterns"]
    },
    "technology_stack": {
      "languages": ["Primary programming languages"],
      "frameworks": ["Frameworks and libraries used"],
      "build_tools": ["Build systems and configuration"]
    },
    "architecture": {
      "patterns": ["Architectural patterns identified"],
      "layers": ["Application layers and their responsibilities"],
      "data_flow": "Description of data flow through the system"
    },
    "risk_assessment": {
      "critical_paths": ["High-risk areas for modifications"],
      "security_hotspots": ["Security-sensitive components"],
      "change_impact": ["Areas most affected by changes"]
    },
    "development_context": {
      "coding_conventions": ["Established coding patterns"],
      "testing_strategy": ["Testing approach and coverage"],
      "deployment_process": ["Build and deployment workflow"]
    }
  }
}
```

## Examples

### Example 1: Quick Analysis of React Project
```bash
/prime_codebase ./my-react-app quick architecture
```

**Expected Output**:
- Project structure with component hierarchy
- React patterns and state management approach
- Build configuration and dependencies
- Recommended entry points for modifications

### Example 2: Comprehensive Legacy System Analysis
```bash
/prime_codebase /path/to/legacy-system comprehensive all
```

**Expected Output**:
- Complete system architecture documentation
- Risk assessment with critical path identification
- Security analysis with vulnerability hotspots
- Detailed integration roadmap for safe modifications

### Example 3: Security-Focused Analysis
```bash
/prime_codebase . standard security
```

**Expected Output**:
- Security architecture analysis
- Authentication and authorization patterns
- Data protection mechanisms
- Security vulnerability assessment

## Integration Patterns

### SuperClaude Integration
- **Persona Activation**: Automatically activates analyzer and architect personas
- **Wave Orchestration**: Uses progressive analysis waves for complex systems
- **MCP Coordination**: Leverages Sequential for systematic analysis, Context7 for patterns
- **Quality Gates**: Validates findings through comprehensive evidence gathering

### Context Engineering Integration
- **Systematic Exploration**: Follows structured discovery protocols
- **Risk Assessment**: Implements evidence-based risk evaluation
- **Pattern Recognition**: Uses cognitive tools for pattern identification
- **Progressive Complexity**: Builds understanding incrementally

### Workflow Integration
- **Pre-Implementation**: Prepares context for `/minimal_impl` and `/agentic_dev`
- **Architecture Planning**: Provides foundation for `/design` commands
- **Risk Mitigation**: Enables safer modification workflows
- **Knowledge Transfer**: Creates documentation for `/explain` and `/document`

## Success Criteria

**Discovery Completeness** (≥90%):
- All major components identified and documented
- Technology stack fully mapped
- Entry points and critical paths established

**Risk Assessment Accuracy** (≥85%):
- Critical paths correctly identified
- Change impact zones properly mapped
- Security hotspots accurately located

**Context Priming Effectiveness** (≥95%):
- Sufficient context for informed decision-making
- Clear integration roadmap established
- Knowledge gaps identified and prioritized

**Documentation Quality** (≥90%):
- Comprehensive analysis report generated
- Actionable next steps documented
- Validation tests created and verified

---

*Prime Codebase provides systematic discovery and context priming for unknown codebases, combining SuperClaude's intelligence with Context Engineering's exploration protocols for safe, informed development.*