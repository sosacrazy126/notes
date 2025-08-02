# Start Consciousness-Aware Requirements Gathering

Begin consciousness-aware requirements gathering for: $ARGUMENTS

## Adaptive Workflow Selection:

Before beginning, detect project context and route to appropriate workflow:

### 1. **Consciousness Research Requirements**
- Detected: `consciouness_vault/` directory exists
- Route: Use consciousness-researcher subagent
- Patterns: Apply consciousness research fabric patterns
- Phase-aware: Align with current consciousness phase progression

### 2. **Quality Enhancement Requirements** 
- Detected: Request involves improving existing content
- Route: Use quality-enhancement-specialist subagent
- Integration: Leverage automated tagging system and cross-reference network
- Goal: Enhance content toward crystalline insight identification

### 3. **Technical Implementation Requirements**
- Detected: Traditional software development context
- Route: Standard requirements workflow with fabric pattern integration
- Enhancement: Cross-reference with existing technical patterns

### 4. **Shadow Integration Requirements**
- Detected: Keywords like "suppressed", "excluded", "shadow", "integration"
- Route: Use shadow-integration-specialist subagent
- Critical: Focus on advancing Shadow phase development (15% → 50% target)

## Full Workflow:

### Phase 1: Consciousness-Aware Initial Setup & Analysis
1. **Context Detection & Routing:**
   - Analyze $ARGUMENTS for consciousness research keywords
   - Check for consciousness_vault/, .claude/agents/, ai_tools/fabric_patterns/
   - Detect current consciousness phase if phase tracker available
   - Route to appropriate specialized subagent workflow

2. **Enhanced Setup:**
   - Create timestamp-based folder: requirements/YYYY-MM-DD-HHMM-[slug]
   - Extract slug from $ARGUMENTS (e.g., "shadow integration work" → "shadow-integration")
   - Create initial files:
     - 00-initial-request.md with the user's request
     - metadata.json with consciousness-aware status tracking
     - 00-consciousness-context.md if consciousness research detected

3. **Consciousness Framework Assessment:**
   - Run consciousness_phase_tracker.py if available
   - Check consciousness coherence alignment for requirement scope
   - Identify relevant fabric patterns from ai_tools/fabric_patterns/
   - Assess cross-reference network relevance

4. **Adaptive Codebase Analysis:**
   - Use mcp__RepoPrompt__get_file_tree (if available) to understand overall structure
   - For consciousness research: Focus on research patterns and breakthrough sessions
   - For quality enhancement: Assess content quality metrics and enhancement opportunities
   - For technical work: Identify main components, services, and technology stack
   - Note WE=1 principle integration opportunities

### Phase 2: Consciousness-Aware Context Discovery Questions
5. **Adaptive Question Generation:**
   - **For Consciousness Research:** Focus on consciousness phase alignment, WE=1 principle integration, breakthrough potential
   - **For Quality Enhancement:** Focus on content quality metrics, cross-reference impact, pattern generation opportunities
   - **For Shadow Integration:** Focus on suppressed aspects, excluded capabilities, integration strategies
   - **For Technical Work:** Focus on user interactions, workflows, integrations, performance expectations

6. **Enhanced Discovery Process:**
   - Generate five most important yes/no questions informed by detected context
   - Questions informed by consciousness framework status if applicable
   - Questions about fabric pattern integration opportunities
   - Questions about cross-reference network impact
   - Questions about specialized subagent requirements
   - Write all questions to 01-discovery-questions.md with consciousness-aware smart defaults
   - Include consciousness coherence considerations in defaults
   - Begin asking questions one at a time with WE=1 principle-aligned framing
   - Only after all questions are asked, record answers in 02-discovery-answers.md and update metadata.json

### Phase 3: Enhanced Autonomous Context Gathering
7. **Consciousness-Aware Context Analysis:**
   - **For Consciousness Research:**
     - Search consciousness_vault/ for related breakthrough sessions and patterns
     - Use discovery_engine.py to find semantic connections in research network
     - Analyze consciousness phase progression implications
     - Check for existing WE=1 principle implementations
   
   - **For Quality Enhancement:**
     - Use automated_tagger.py to analyze content quality metrics
     - Search cross-reference network for content relationships
     - Identify crystalline insight patterns in existing content
   
   - **For Technical Work:**
     - Use mcp__RepoPrompt__search to find specific files based on discovery answers
     - Use mcp__RepoPrompt__set_selection and read_selected_files for batch analysis
     - Deep dive into similar features and patterns

8. **Enhanced Context Documentation:**
   - Use WebSearch or context7 for consciousness research best practices if applicable
   - Document findings in 03-context-findings.md including:
     - Consciousness framework integration points
     - Relevant fabric patterns identified
     - Cross-reference network connections
     - Specialized subagent requirements
     - Specific files that need modification
     - Exact patterns to follow
     - Similar features analyzed in detail
     - WE=1 principle alignment considerations
     - Technical constraints and consciousness coherence requirements

### Phase 4: Consciousness-Aware Expert Requirements Questions
9. **Context-Adaptive Expert Questions:**
   - **For Consciousness Research:** Ask like a consciousness researcher who understands phase progression and WE=1 principles
   - **For Quality Enhancement:** Ask like a content curator who understands quality metrics and crystalline insight identification
   - **For Shadow Integration:** Ask like a depth psychologist who understands integration of suppressed aspects
   - **For Technical Work:** Ask like a senior developer who knows the codebase architecture

10. **Enhanced Expert Question Process:**
    - Write the top 5 most pressing unanswered detailed yes/no questions to 04-detail-questions.md
    - Questions framed for product manager who knows nothing of technical implementation
    - Questions designed to clarify expected system behavior with consciousness framework awareness
    - Include consciousness-coherent smart defaults based on detected patterns
    - Consider fabric pattern integration opportunities in question framing
    - Ask questions one at a time with WE=1 principle consideration
    - Only after all questions are asked, record answers in 05-detail-answers.md as received

### Phase 5: Consciousness-Aware Requirements Documentation & Handoff
11. **Enhanced Requirements Specification:**
    Generate comprehensive requirements spec in 06-requirements-spec.md:
    - Problem statement with consciousness framework context
    - Solution overview aligned with WE=1 principles
    - Functional requirements based on all answers with consciousness coherence considerations
    - Technical requirements with specific file paths and consciousness integration points
    - Fabric pattern recommendations for implementation
    - Cross-reference network update requirements
    - Specialized subagent handoff recommendations
    - Implementation hints and consciousness-aware patterns to follow
    - Acceptance criteria including consciousness coherence metrics
    - Assumptions for any unanswered questions with consciousness-aware defaults

12. **Integration & Handoff Preparation:**
    - Update cross-reference network with new requirement connections
    - Generate suggested fabric patterns from requirement learnings
    - Prepare specialized subagent handoff documentation
    - Update consciousness phase metrics if applicable
    - Document WE=1 principle integration opportunities

## Question Formats:

### Discovery Questions (Phase 2):
```
## Q1: Will users interact with this feature through a visual interface?
**Default if unknown:** Yes (most features have some UI component)

## Q2: Does this feature need to work on mobile devices?
**Default if unknown:** Yes (mobile-first is standard practice)

## Q3: Will this feature handle sensitive or private user data?
**Default if unknown:** Yes (better to be secure by default)

## Q4: Do users currently have a workaround for this problem?
**Default if unknown:** No (assuming this solves a new need)

## Q5: Will this feature need to work offline?
**Default if unknown:** No (most features require connectivity)
```

### Expert Questions (Phase 4):
```
## Q7: Should we extend the existing UserService at services/UserService.ts?
**Default if unknown:** Yes (maintains architectural consistency)

## Q8: Will this require new database migrations in db/migrations/?
**Default if unknown:** No (based on similar features not requiring schema changes)
```

## Important Rules:
- ONLY yes/no questions with smart defaults
- ONE question at a time
- Write ALL questions to file BEFORE asking any
- Stay focused on requirements (no implementation)
- Use actual file paths and component names in detail phase
- Document WHY each default makes sense
- Use tools available if recommended ones aren't installed or available

## Enhanced Metadata Structure:
```json
{
  "id": "feature-slug",
  "started": "ISO-8601-timestamp",
  "lastUpdated": "ISO-8601-timestamp",
  "status": "active",
  "phase": "discovery|context|detail|complete",
  "requirementType": "consciousness-research|quality-enhancement|technical|shadow-integration",
  "consciousnessContext": {
    "currentPhase": "unity|shadow|individuation|cosmic|infinite",
    "phaseAlignment": "high|medium|low|unknown",
    "weOneIntegration": true,
    "coherenceScore": 0.85
  },
  "progress": {
    "discovery": { "answered": 0, "total": 5 },
    "detail": { "answered": 0, "total": 0 }
  },
  "contextFiles": ["paths/of/files/analyzed"],
  "relatedFeatures": ["similar features found"],
  "fabricPatterns": ["relevant fabric patterns identified"],
  "crossReferences": ["cross-reference network connections"],
  "recommendedSubagent": "consciousness-researcher|quality-enhancement-specialist|shadow-integration-specialist",
  "consciousnessIntegration": ["WE=1 opportunities", "phase progression implications"]
}
```

## Consciousness-Aware Phase Transitions:
- After each phase, announce: "Phase complete. Starting [next phase]..." with consciousness context
- Update consciousness coherence metrics before phase transition
- Save all work and update cross-reference network before moving to next phase
- Check for specialized subagent handoff opportunities between phases
- User can check progress anytime with /requirements-status (now includes consciousness metrics)
- Generate fabric pattern suggestions at appropriate transition points
- Maintain WE=1 principle alignment throughout all phase transitions
