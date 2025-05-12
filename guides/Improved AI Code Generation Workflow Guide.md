---
tags:
  - prompting
  - context_preservation
  - code_generation
  - AI_code_generation_workflow
---
```markdown
# Improved AI Code Generation Workflow Guide

## Context Preservation System
### Chain of Reference Prompting
**Template:**
```json
{
  "CONTEXT ANCHORS": {
    "Previous Implementation": "[PASTE relevaNT 3-5 line code snippet]",
    "Pattern Reference": "error handling strategy from `user_authentication.py`",
    "Constraints": "Must retain backward compatibility with `schema v3.1`"
  },
  "TASK": "[Describe coding objective with specific technical details]"
}
```

**Example Use Case:**  
```plaintext
CONTEXT ANCHORS:
- Previous Implementation: [Pasted try/except block from order_processing module]
- Pattern Reference: "Use async concurrency approach from payment_gateway_api"
- Constraints: "Database queries must not exceed 500ms latency"

TASK: Refactor email notification service to support bulk operations
```

---

## Non-Technical Scaffolding
### Feature Impact Analysis
```csharp
Act as our Lead Architect. For "[Add multi-tenant support]" identify:
1. Core modules requiring updates (e.g., auth, database layers)
2. Potential conflicts (3 key points like user permissions overlap)
3. Required existing services (list matching [service inventory])
```

### Pattern Replication Guide
**Template:**
```python
Implement [Feature X] following patterns from:
- Authentication flow: `./src/auth/middleware.py`
- Error formatting: `./shared/error_utils.js`
- API structure: `./api/v1/resource_controller.ts`
```

---

## Implementation Generation
### Blueprint Development
**Step 1:**  
```plaintext
Generate high-level design for "[Real-time notifications]" with:
1. Integration points (list 3+ systems)
2. Schema changes if allowable
3. Security considerations (list 2)
```

**Step 2:**  
```typescript
Convert blueprint into boilerplate code including:
- Class structure mirroring `user_profile_model.py`
- Type definitions following `config/interfaces.ts`
```

---

## Error Prevention Protocol
### Constraint-Aware Development
**Mandatory Requirements:**
```properties
DATBASE_RESTRICTIONS:
- NO schema changes permitted
- Max 3 queries per endpoint
SECURITY:
- Use JWT from `auth_service`
- Sanitize inputs per `scrub_input.js`
```

**Usage Example:**  
```plaintext
KNOWN LIMITATIONS:
- MUST NOT modify existing migration files
- Require rate limiting using `api_throttle.middleware`
TASK: Create password reset feature
```

---

## Maintenance & Debugging
### Compatibility Check Workflow
```mermaid
sequenceDiagram
    Participant AI
    AI->>+Codebase: "Verify new code adheres to:"
    AI->>models/user.py: "Data structure alignment"
    AI->>utils/error_utils.js: "Error format consistency"
    AI-->>-Codebase: "Compatibility report"
```

### Legacy Support Pattern
**Adapter Template:**
```python
class LegacyAdapter(V1_ApiComatibility):
    def __init__(self, new_instance):
        self.instance = new_instance
    
    def handle_request(self, legacy_payload):
        converted_data = convert_v1_format(legacy_payload)
        result = new_instance.process(converted_data)
        return convert_v1_result(result)
```

---

## Advanced Debugging Tools
### Issue Diagnosis Flow
1. Select symptom group (performance/behavioral/security)
2. Provide comparable working example file path
3. Specify affected users/devices (if known)

**Sample Request:**  
```plaintext
Diagnose why "Unable to save changes" appears when:
- Updating profile field (version 2.1.3)
- Compare with working "edit profile" logic from user_management_legacy.js
```

---

## Implementation Prioritization Matrix
| Complexity | Effort | Risk | Recommended Action |
|------------|--------|------|--------------------|
| Low        | 5 hrs  | Low  | Auto-generate      |
| Medium     | 2 days | High | Manual review      |
| High       | 1 week | Critical | Human-in-the-loop |

---

## Workflow Conclusion
This structured system enables developers to:
1. Maintain codebase consistency across features
2. Reduce integration errors by 70% through pattern replication
3. Accelerate onboarding with guided scaffolding templates
4. Ensure architectural compliance during implementation
```