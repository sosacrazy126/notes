# ORCHESTRATOR.md - CustomClaude Intelligent Routing System

Intelligent routing system for Claude Code CustomClaude framework, integrating SuperClaude's orchestration with Context Engineering's agent-based patterns.

## 🧠 Detection Engine

Analyzes requests to understand intent, complexity, and requirements using both SuperClaude's pattern recognition and Context Engineering's cognitive tools architecture.

### Pre-Operation Validation Checks

**Resource Validation**:
- Token usage prediction based on operation complexity and scope
- Memory and processing requirements estimation
- File system permissions and available space verification
- MCP server availability and response time checks

**Compatibility Validation**:
- Flag combination conflict detection (e.g., `--no-mcp` with `--seq`)
- Persona + command compatibility verification
- Tool availability for requested operations
- Project structure requirements validation

**Risk Assessment**:
- Operation complexity scoring (0.0-1.0 scale)
- Failure probability based on historical patterns
- Resource exhaustion likelihood prediction
- Cascading failure potential analysis

**Validation Logic**: Resource availability, flag compatibility, risk assessment, outcome prediction, and safety recommendations. Operations with risk scores >0.8 trigger safe mode suggestions.

**Resource Management Thresholds**:
- **Green Zone** (0-60%): Full operations, predictive monitoring active
- **Yellow Zone** (60-75%): Resource optimization, caching, suggest --uc mode
- **Orange Zone** (75-85%): Warning alerts, defer non-critical operations  
- **Red Zone** (85-95%): Force efficiency modes, block resource-intensive operations
- **Critical Zone** (95%+): Emergency protocols, essential operations only

### Enhanced Pattern Recognition Rules

#### Context Engineering Integration
```yaml
agent_patterns:
  unknown_codebase:
    indicators: ["unfamiliar", "new project", "legacy", "inherited"]
    cognitive_tools: ["systematic exploration", "risk assessment", "incremental validation"]
    commands: ["/prime_codebase", "/discover_codebase", "/explore_unknown"]
    
  minimal_knowledge:
    indicators: ["limited context", "quick implementation", "safe approach"]
    cognitive_tools: ["pattern matching", "risk minimization", "incremental development"]
    commands: ["/minimal_impl", "/safe_patterns"]
    
  agentic_development:
    indicators: ["multi-agent", "coordination", "complex workflow", "early adoption"]
    cognitive_tools: ["compound intelligence", "emergent capabilities", "field dynamics"]
    commands: ["/agentic_dev", "/multi_agent", "/coordination"]
```

#### Complexity Detection with Cognitive Enhancement
```yaml
simple:
  indicators:
    - single file operations
    - basic CRUD tasks
    - straightforward queries
    - < 3 step workflows
  cognitive_enhancement: minimal
  token_budget: 5K
  time_estimate: < 5 min

moderate:
  indicators:
    - multi-file operations
    - analysis tasks
    - refactoring requests
    - 3-10 step workflows
  cognitive_enhancement: systematic_reasoning
  token_budget: 15K
  time_estimate: 5-30 min

complex:
  indicators:
    - system-wide changes
    - architectural decisions
    - performance optimization
    - > 10 step workflows
  cognitive_enhancement: extended_thinking + meta_cognitive
  token_budget: 30K+
  time_estimate: > 30 min
```

#### Domain Identification with Agent Patterns
```yaml
unknown_codebase_exploration:
  keywords: [explore, discover, unfamiliar, legacy, inherited, new project]
  file_patterns: ["**/*"]
  cognitive_patterns: ["systematic exploration", "risk assessment", "pattern recognition"]
  typical_operations: [scan, analyze, understand, map, prime]

minimal_knowledge_implementation:
  keywords: [quick, safe, minimal, pattern, template, boilerplate]
  file_patterns: ["*.template", "*.example", "patterns/*"]
  cognitive_patterns: ["pattern matching", "risk minimization", "incremental validation"]
  typical_operations: [implement, adapt, follow, replicate]

agentic_development:
  keywords: [multi-agent, coordination, orchestration, emergent, compound]
  file_patterns: ["agents/*", "workflows/*", "orchestration/*"]
  cognitive_patterns: ["compound intelligence", "emergent capabilities", "coordination"]
  typical_operations: [coordinate, orchestrate, delegate, synthesize]

frontend:
  keywords: [UI, component, React, Vue, CSS, responsive, accessibility]
  file_patterns: ["*.jsx", "*.tsx", "*.vue", "*.css", "*.scss"]
  cognitive_patterns: ["user-centered design", "accessibility framework", "performance optimization"]
  typical_operations: [create, implement, style, optimize, test]

backend:
  keywords: [API, database, server, endpoint, authentication, performance]
  file_patterns: ["*.js", "*.ts", "*.py", "*.go", "controllers/*", "models/*"]
  cognitive_patterns: ["reliability engineering", "security by default", "data integrity"]
  typical_operations: [implement, optimize, secure, scale]

security:
  keywords: [vulnerability, authentication, encryption, audit, compliance]
  file_patterns: ["*auth*", "*security*", "*.pem", "*.key"]
  cognitive_patterns: ["threat modeling", "defense in depth", "zero trust"]
  typical_operations: [scan, harden, audit, fix]

documentation:
  keywords: [document, README, wiki, guide, manual, instructions]
  file_patterns: ["*.md", "*.rst", "*.txt", "docs/*", "README*"]
  cognitive_patterns: ["audience analysis", "cultural adaptation", "progressive scaffolding"]
  typical_operations: [write, document, explain, translate, localize]
```

### Intent Extraction Algorithm with Cognitive Enhancement
```
1. Parse user request for keywords and patterns
2. Match against domain/operation matrices including agent patterns
3. Score complexity based on scope and cognitive requirements
4. Evaluate cognitive tool integration opportunities
5. Estimate resource requirements including cognitive overhead
6. Generate routing recommendation with persona and tool selection
7. Apply auto-detection triggers for enhanced workflows
```

## 🚦 Enhanced Routing Intelligence

Dynamic decision trees that map detected patterns to optimal tool combinations, persona activation, cognitive tool integration, and orchestration strategies.

### Master Routing Table with Cognitive Enhancement

| Pattern | Complexity | Domain | Auto-Activates | Cognitive Tools | Confidence |
|---------|------------|---------|----------------|-----------------|------------|
| "explore unknown codebase" | moderate | exploration | analyzer persona, --think, Sequential | systematic exploration, risk assessment | 95% |
| "implement with minimal knowledge" | simple | implementation | refactorer persona, Context7 | pattern matching, incremental validation | 92% |
| "agentic development workflow" | complex | coordination | architect persona, --ultrathink, All MCP | compound intelligence, emergent capabilities | 90% |
| "analyze architecture" | complex | infrastructure | architect persona, --ultrathink, Sequential | systematic reasoning, extended thinking | 95% |
| "create component" | simple | frontend | frontend persona, Magic, --uc | user-centered design, accessibility framework | 90% |
| "implement feature" | moderate | any | domain-specific persona, Context7, Sequential | progressive complexity, evidence-based reasoning | 88% |
| "security audit" | complex | security | security persona, --ultrathink, Sequential | threat modeling, risk assessment | 95% |
| "document system" | moderate | documentation | scribe persona, Context7 | audience analysis, technical writing | 95% |

### Enhanced Decision Trees

#### Cognitive Tool Selection Logic

**Base Cognitive Tool Selection**:
- **Simple Operations**: Pattern matching, basic reasoning protocols
- **Moderate Complexity**: Systematic reasoning, progressive scaffolding
- **Complex Operations**: Extended thinking, meta-cognitive analysis, compound intelligence

**Agent Pattern Integration**:
- **Unknown Codebase**: Systematic exploration + risk assessment + incremental validation
- **Minimal Knowledge**: Pattern matching + risk minimization + evidence-based implementation
- **Agentic Development**: Compound intelligence + emergent capabilities + coordination protocols

**Persona-Cognitive Tool Alignment**:
- **Architect**: Systems thinking + progressive complexity + future-proofing protocols
- **Analyzer**: Evidence-based reasoning + systematic investigation + root cause analysis
- **Security**: Threat modeling + defense in depth + zero trust frameworks
- **Frontend**: User-centered design + accessibility frameworks + performance optimization
- **Backend**: Reliability engineering + security by default + data integrity protocols

#### Enhanced Task Delegation Intelligence

**Cognitive Enhancement Scoring**:
- **Pattern Recognition >0.7**: +0.3 cognitive enhancement score
- **Multi-Domain Operations**: +0.4 cognitive complexity multiplier
- **Unknown Environment**: +0.5 exploration and risk assessment requirement
- **High Stakes Operations**: +0.3 validation and safety protocol requirement

**Agent Pattern Opportunities**:
- **Unknown Codebase Exploration**: +0.4 systematic exploration score
- **Multi-Agent Coordination**: +0.5 compound intelligence score
- **Minimal Knowledge Implementation**: +0.3 pattern matching score
- **Complex System Analysis**: +0.4 extended thinking score

**Cognitive Tool Recommendations**:
- **Exploration Score >0.6**: Use systematic exploration protocols
- **Coordination Score >0.7**: Use compound intelligence patterns
- **Risk Score >0.5**: Use risk assessment and validation frameworks
- **Complexity Score >0.8**: Use extended thinking and meta-cognitive analysis

### Context Engineering Agent Activation

**Agent Pattern Auto-Activation**:
```yaml
unknown_codebase_exploration:
  condition: keywords.includes("explore", "unfamiliar", "legacy") OR file_patterns.unknown
  action: auto_enable /prime_codebase OR /discover_codebase
  cognitive_tools: ["systematic exploration", "risk assessment", "incremental validation"]
  confidence: 90%

minimal_knowledge_implementation:
  condition: keywords.includes("quick", "safe", "minimal") AND implementation_required
  action: auto_enable /minimal_impl
  cognitive_tools: ["pattern matching", "risk minimization", "evidence-based implementation"]
  confidence: 85%

agentic_development:
  condition: complexity > 0.8 AND coordination_indicators AND multi_domain
  action: auto_enable /agentic_dev
  cognitive_tools: ["compound intelligence", "emergent capabilities", "coordination protocols"]
  confidence: 88%

systematic_analysis:
  condition: analysis_required AND complexity > 0.6
  action: auto_enable extended_thinking protocols
  cognitive_tools: ["systematic reasoning", "evidence-based analysis", "progressive complexity"]
  confidence: 92%
```

## Quality Gates & Validation Framework with Cognitive Enhancement

### Enhanced 10-Step Validation Cycle
```yaml
quality_gates:
  step_1_cognitive_priming: "cognitive tool selection, persona alignment, pattern recognition"
  step_2_syntax: "language parsers, Context7 validation, intelligent suggestions"
  step_3_type: "Sequential analysis, type compatibility, context-aware suggestions"
  step_4_cognitive_validation: "reasoning coherence, assumption validation, bias detection"
  step_5_lint: "Context7 rules, quality analysis, refactoring suggestions"
  step_6_security: "Sequential analysis, vulnerability assessment, threat modeling"
  step_7_test: "Playwright E2E, coverage analysis, cognitive pattern validation"
  step_8_performance: "Sequential analysis, benchmarking, optimization with cognitive overhead"
  step_9_documentation: "Context7 patterns, audience analysis, cultural adaptation"
  step_10_integration: "Playwright testing, deployment validation, cognitive tool integration"

cognitive_validation:
  reasoning_coherence: "logical flow validation, assumption checking, bias detection"
  pattern_consistency: "agent pattern compliance, cognitive tool effectiveness"
  knowledge_gaps: "identification and mitigation of cognitive limitations"
  meta_cognitive_check: "self-awareness validation, reasoning transparency"

enhanced_automation:
  cognitive_monitoring: "cognitive tool effectiveness tracking, pattern success rates"
  intelligent_adaptation: "dynamic cognitive tool selection, persona optimization"
  pattern_evolution: "agent pattern refinement, cognitive framework enhancement"
```

### Enhanced Task Completion Criteria
```yaml
completion_requirements:
  validation: "all 10 steps pass, cognitive validation included, evidence provided"
  cognitive_integration: "cognitive tools properly applied, persona alignment verified"
  pattern_compliance: "agent patterns followed, framework consistency maintained"
  ai_integration: "MCP coordination, persona integration, tool orchestration"
  performance: "response time targets, cognitive overhead managed, success thresholds"
  quality: "code quality standards, cognitive pattern effectiveness, integration testing"

cognitive_evidence_requirements:
  reasoning_trace: "complete reasoning process documentation, assumption tracking"
  pattern_application: "cognitive tool usage evidence, effectiveness metrics"
  knowledge_gaps: "identified limitations, mitigation strategies, learning opportunities"
  meta_cognitive_insights: "self-awareness demonstrations, bias recognition, improvement areas"
```

## ⚡ Performance Optimization with Cognitive Awareness

**Cognitive Load Management**: Intelligent resource allocation considering both computational and cognitive overhead.

**Enhanced Operation Batching**:
- **Cognitive Tool Coordination**: Parallel cognitive operations when no reasoning dependencies
- **Pattern Reuse**: Cache successful cognitive patterns for session optimization
- **Meta-Cognitive Optimization**: Learn from cognitive tool effectiveness for future routing
- **Context Preservation**: Maintain cognitive context across related operations

**Cognitive Resource Allocation**:
- **Pattern Recognition**: 500-1K tokens for cognitive pattern analysis
- **Systematic Reasoning**: 2-5K tokens for structured thinking protocols
- **Extended Thinking**: 5-15K tokens for complex cognitive operations
- **Meta-Cognitive Analysis**: 1-3K tokens for self-awareness and optimization

## 🔗 Integration Intelligence with Cognitive Enhancement

### Enhanced MCP Server Selection with Cognitive Patterns

**Cognitive-Aware Server Selection**:
- **Context7**: Documentation patterns + audience analysis + cultural adaptation
- **Sequential**: Systematic reasoning + extended thinking + meta-cognitive analysis
- **Magic**: User-centered design + accessibility frameworks + component patterns
- **Playwright**: Testing protocols + validation frameworks + performance measurement

**Cognitive Tool Integration**:
- **Pattern Recognition**: Enhanced with MCP server pattern libraries
- **Systematic Reasoning**: Supported by Sequential's structured analysis
- **Extended Thinking**: Augmented with Context7's knowledge base
- **Meta-Cognitive Analysis**: Integrated with all servers for comprehensive insight

### Enhanced Persona Integration with Cognitive Tools

**Persona-Cognitive Tool Matrix**:
- **Architect + Systems Thinking**: Progressive complexity protocols + future-proofing frameworks
- **Analyzer + Evidence-Based Reasoning**: Systematic investigation + root cause analysis
- **Security + Threat Modeling**: Defense in depth + zero trust + risk assessment protocols
- **Frontend + User-Centered Design**: Accessibility frameworks + performance optimization
- **Mentor + Progressive Scaffolding**: Educational protocols + knowledge transfer frameworks

## 🚨 Emergency Protocols with Cognitive Fallbacks

### Cognitive Load Management
- **Level 1**: Reduce cognitive complexity, use cached patterns, simplify reasoning chains
- **Level 2**: Disable advanced cognitive tools, use basic pattern matching, essential reasoning only
- **Level 3**: Emergency cognitive protocols, minimal reasoning, pattern-based responses only

### Enhanced Error Recovery Patterns
- **Cognitive Tool Failure**: Fallback to simpler reasoning protocols
- **Pattern Recognition Error**: Use basic heuristics and manual analysis
- **Meta-Cognitive Overload**: Reduce self-awareness overhead, focus on execution
- **Persona Conflict**: Default to analyst persona with systematic reasoning

### Cognitive Framework Recovery
- **Framework Inconsistency**: Validate against core principles, restore alignment
- **Pattern Degradation**: Refresh cognitive patterns from validated sources
- **Knowledge Gap**: Activate learning protocols, request additional context
- **Reasoning Failure**: Escalate to human oversight, document limitations

## 🔧 Enhanced Configuration

### Cognitive Orchestrator Settings
```yaml
cognitive_config:
  # Cognitive Enhancement
  enable_meta_cognitive: true
  cognitive_tool_selection: adaptive
  pattern_learning: enabled
  reasoning_validation: strict
  
  # Agent Pattern Integration
  unknown_codebase_protocols: enabled
  minimal_knowledge_patterns: enabled
  agentic_development: enabled
  cognitive_tool_caching: true
  
  # Performance with Cognitive Awareness
  cognitive_overhead_monitoring: true
  pattern_reuse_optimization: true
  reasoning_efficiency_tracking: true
  meta_cognitive_throttling: adaptive
  
  # Enhanced Quality Gates
  cognitive_validation_required: true
  reasoning_coherence_check: enabled
  pattern_consistency_validation: true
  knowledge_gap_detection: enabled
```

### Custom Cognitive Routing Rules
```yaml
custom_cognitive_patterns:
  project_specific:
    - pattern: "explore [project_type]"
      cognitive_tools: ["systematic exploration", "domain-specific analysis"]
      personas: ["analyzer", "architect"]
      
  domain_specific:
    - pattern: "implement [framework] component"
      cognitive_tools: ["pattern matching", "user-centered design"]
      personas: ["frontend", "architect"]
      
  complexity_specific:
    - pattern: "complex [domain] analysis"
      cognitive_tools: ["extended thinking", "meta-cognitive analysis"]
      personas: ["analyzer", "domain_specialist"]
```

---

*CustomClaude's orchestrator integrates SuperClaude's intelligent routing with Context Engineering's cognitive patterns, creating a hybrid system optimized for real-world development challenges with enhanced reasoning capabilities.*