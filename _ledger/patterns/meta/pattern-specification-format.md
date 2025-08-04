---
pattern_name: pattern-specification-format
pattern_type: meta
source_files: [self-referential]
confidence: 1.0
---

# Pattern Specification Format

## Purpose
Define the standard format for documenting reusable patterns in a way that enables AI-driven code generation while maintaining human readability.

## Specification

### Inputs
- `pattern_knowledge`: unstructured information about a pattern
- `pattern_type`: enum[workflow|architecture|algorithm|meta]
- `source_context`: where the pattern was discovered

### Process

1. **Extract Core Purpose**
   - Identify the problem being solved
   - Define success criteria
   - Clarify scope boundaries

2. **Define Interface**
   - List all inputs with types and constraints
   - Specify outputs with structure
   - Document side effects

3. **Describe Process**
   - Break into numbered steps
   - Include decision points
   - Specify error handling

4. **Add Constraints**
   - Performance requirements
   - Resource limitations
   - Security considerations

5. **Provide Examples**
   - Minimum 2 examples
   - Cover edge cases
   - Use YAML format

6. **Include Metadata**
   - Pattern name (kebab-case)
   - Pattern type
   - Source attribution
   - Confidence score

### Outputs
```yaml
pattern_document:
  front_matter:
    pattern_name: string
    pattern_type: string
    source_files: array[string]
    confidence: float (0.0-1.0)
  sections:
    - purpose: string
    - specification:
        inputs: array[parameter]
        process: array[step]
        outputs: array[result]
        constraints: array[requirement]
        examples: array[example]
    - implementation_notes: string (optional)
    - extension_points: array[string] (optional)
```

### Constraints
- Must be language-agnostic
- Focus on WHAT not HOW
- Examples must be concrete
- All sections except optional ones required
- Maximum 5000 words

### Examples

```yaml
minimal_pattern:
  input:
    pattern_knowledge: "Function that validates email addresses"
    pattern_type: "algorithm"
    source_context: "user-service.py"
  output:
    pattern_name: "email-validation"
    pattern_type: "algorithm"
    purpose: "Validate email addresses according to RFC 5322"
    specification:
      inputs:
        - email: string, email address to validate
      process:
        1. Check for @ symbol
        2. Validate local part (before @)
        3. Validate domain part (after @)
        4. Check total length < 254
      outputs:
        - valid: boolean
        - error: string (if invalid)

complex_pattern:
  input:
    pattern_knowledge: "Multi-stage deployment pipeline with rollback"
    pattern_type: "workflow"
    source_context: "ci-cd-documentation.md"
  output:
    pattern_name: "blue-green-deployment"
    pattern_type: "workflow"
    purpose: "Deploy with zero downtime and instant rollback"
    specification:
      inputs:
        - artifact: deployment package
        - environment: target environment
        - health_checks: array of endpoints
      process:
        1. Validate artifact integrity
        2. Provision new environment (green)
        3. Deploy to green
        4. Run smoke tests
        5. Switch traffic to green
        6. Monitor for errors
        7. Keep blue as backup
        8. After stability period, terminate blue
      outputs:
        - deployment_id: unique identifier
        - status: success|rolled_back|failed
        - metrics: performance data
```

### Implementation Notes

1. **Validation Rules**
   - Pattern name must be unique
   - Examples must be valid according to spec
   - Process steps must be actionable

2. **Quality Indicators**
   - High confidence: Extracted from working code
   - Medium confidence: Derived from documentation
   - Low confidence: Theoretical or untested

3. **Evolution Support**
   - Patterns can reference other patterns
   - Version tracking through git
   - Deprecation notices supported

### Extension Points

1. **Pattern Composition**
   - Combine simple patterns into complex ones
   - Define pattern prerequisites
   - Create pattern hierarchies

2. **Auto-Generation**
   - Generate tests from examples
   - Create documentation
   - Build IDE snippets

3. **Pattern Discovery**
   - ML-based pattern detection
   - Similarity clustering
   - Usage analytics

---

*This meta-pattern defines how all patterns should be documented. It is self-referential and follows its own format.*