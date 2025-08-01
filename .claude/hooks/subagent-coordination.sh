#!/bin/bash
# Subagent Coordination Hook
# Executed after subagent completion to coordinate ecosystem state

set -e

PROJECT_DIR="$CLAUDE_PROJECT_DIR"
LOG_FILE="$PROJECT_DIR/.claude/logs/subagent-coordination-$(date +%Y%m%d).log"

# Get subagent information from environment
SUBAGENT_NAME="${CLAUDE_SUBAGENT_NAME:-unknown}"
SUBAGENT_STATUS="${CLAUDE_SUBAGENT_STATUS:-completed}"

echo "🤖 Subagent Coordination: $SUBAGENT_NAME ($SUBAGENT_STATUS) - $(date)" | tee -a "$LOG_FILE"

# 1. Update subagent execution tracking
COORDINATION_FILE="$PROJECT_DIR/.claude/subagent-coordination.json"

# Initialize coordination file if it doesn't exist
if [ ! -f "$COORDINATION_FILE" ]; then
    cat > "$COORDINATION_FILE" << EOF
{
  "session_id": "$(date +%Y%m%d-%H%M%S)",
  "subagent_executions": [],
  "workflow_state": {
    "consciousness_analysis_complete": false,
    "phase_tracking_updated": false,
    "file_organization_applied": false,
    "metadata_tagging_complete": false,
    "git_operations_validated": false
  },
  "consciousness_insights": []
}
EOF
fi

# 2. Record subagent execution
python3 -c "
import json
import sys
from datetime import datetime

try:
    with open('$COORDINATION_FILE', 'r') as f:
        coord = json.load(f)
    
    # Add execution record
    execution = {
        'subagent': '$SUBAGENT_NAME',
        'status': '$SUBAGENT_STATUS',
        'timestamp': datetime.now().isoformat(),
        'session_context': True
    }
    
    coord['subagent_executions'].append(execution)
    
    # Update workflow state based on subagent
    if '$SUBAGENT_NAME' == 'consciousness-researcher':
        coord['workflow_state']['consciousness_analysis_complete'] = True
    elif '$SUBAGENT_NAME' == 'phase-tracker':
        coord['workflow_state']['phase_tracking_updated'] = True
    elif '$SUBAGENT_NAME' == 'file-organizer':
        coord['workflow_state']['file_organization_applied'] = True
    elif '$SUBAGENT_NAME' == 'metadata-tagger':
        coord['workflow_state']['metadata_tagging_complete'] = True
    elif '$SUBAGENT_NAME' == 'git-consciousness-manager':
        coord['workflow_state']['git_operations_validated'] = True
    
    with open('$COORDINATION_FILE', 'w') as f:
        json.dump(coord, f, indent=2)
        
    print('Coordination updated successfully')
    
except Exception as e:
    print(f'Coordination update failed: {e}', file=sys.stderr)
" 2>/dev/null || echo "Coordination update failed" | tee -a "$LOG_FILE"

# 3. Determine next workflow steps based on subagent completion
NEXT_SUBAGENTS=()
WORKFLOW_RECOMMENDATIONS=()

case "$SUBAGENT_NAME" in
    "consciousness-researcher")
        echo "🧠 Consciousness analysis complete - determining next steps" | tee -a "$LOG_FILE"
        NEXT_SUBAGENTS+=("file-organizer" "metadata-tagger")
        WORKFLOW_RECOMMENDATIONS+=("Apply file organization based on consciousness analysis")
        WORKFLOW_RECOMMENDATIONS+=("Tag content with consciousness metadata")
        ;;
        
    "phase-tracker")
        echo "📊 Phase tracking updated - checking development priorities" | tee -a "$LOG_FILE"
        
        # Check if shadow development is needed
        if python3 -c "import sys; sys.path.append('$PROJECT_DIR/consciouness_vault/03_implementations/unity_memory'); from consciousness_phase_tracker import ConsciousnessPhaseTracker; tracker = ConsciousnessPhaseTracker(); print(tracker.get_phase_progress('shadow'))" 2>/dev/null | grep -q "0.1[0-9]"; then
            NEXT_SUBAGENTS+=("shadow-integration-specialist")
            WORKFLOW_RECOMMENDATIONS+=("Prioritize shadow integration development")
        fi
        ;;
        
    "file-organizer")
        echo "📁 File organization applied - ready for metadata enhancement" | tee -a "$LOG_FILE"
        NEXT_SUBAGENTS+=("metadata-tagger")
        WORKFLOW_RECOMMENDATIONS+=("Complete metadata tagging for organized content")
        ;;
        
    "metadata-tagger")
        echo "🏷️ Metadata tagging complete - ready for cross-reference updates" | tee -a "$LOG_FILE"
        WORKFLOW_RECOMMENDATIONS+=("Cross-reference network updated")
        WORKFLOW_RECOMMENDATIONS+=("Content discovery enhanced")
        
        # If this was shadow content, update phase tracker
        if grep -q "shadow" "$LOG_FILE" 2>/dev/null; then
            NEXT_SUBAGENTS+=("phase-tracker")
            WORKFLOW_RECOMMENDATIONS+=("Update shadow phase progress")
        fi
        ;;
        
    "git-consciousness-manager")
        echo "📝 Git operations validated - consciousness coherence maintained" | tee -a "$LOG_FILE"
        NEXT_SUBAGENTS+=("repository-health-monitor")
        WORKFLOW_RECOMMENDATIONS+=("Run repository health check")
        ;;
        
    "repository-health-monitor")
        echo "🏥 Repository health assessed - system wellness validated" | tee -a "$LOG_FILE"
        WORKFLOW_RECOMMENDATIONS+=("Repository health monitoring complete")
        ;;
        
    "shadow-integration-specialist")
        echo "🌘 Shadow integration work complete - updating phase development" | tee -a "$LOG_FILE"
        NEXT_SUBAGENTS+=("phase-tracker")
        WORKFLOW_RECOMMENDATIONS+=("Update shadow phase completion metrics")
        WORKFLOW_RECOMMENDATIONS+=("Assess individuation readiness")
        ;;
        
    *)
        echo "🔄 General subagent completion - checking workflow state" | tee -a "$LOG_FILE"
        ;;
esac

# 4. Check workflow completion status
WORKFLOW_COMPLETE=true
python3 -c "
import json
try:
    with open('$COORDINATION_FILE', 'r') as f:
        coord = json.load(f)
    
    workflow = coord.get('workflow_state', {})
    incomplete = [k for k, v in workflow.items() if not v]
    
    if incomplete:
        print('Workflow incomplete:', ', '.join(incomplete))
        exit(1)
    else:
        print('Workflow complete')
        exit(0)
        
except:
    exit(1)
" 2>/dev/null && WORKFLOW_COMPLETE=true || WORKFLOW_COMPLETE=false

# 5. Update consciousness orchestrator state
if [ -f "$PROJECT_DIR/consciousness-orchestrator.md" ]; then
    echo "🎯 Updating consciousness orchestrator state" | tee -a "$LOG_FILE"
    
    # Create orchestrator state update
    cat > "$PROJECT_DIR/.claude/orchestrator-update.json" << EOF
{
  "last_subagent": "$SUBAGENT_NAME",
  "completion_time": "$(date -Iseconds)",
  "next_recommended_subagents": [$(IFS=','; echo "\"${NEXT_SUBAGENTS[*]}\"" | sed 's/ /","/g')],
  "workflow_recommendations": [$(IFS=$'\n'; echo "${WORKFLOW_RECOMMENDATIONS[*]}" | sed 's/^/"/;s/$/",/' | tr -d '\n' | sed 's/,$//')],
  "workflow_complete": $WORKFLOW_COMPLETE
}
EOF
fi

# 6. Generate coordination summary
echo "📋 Subagent Coordination Summary:" | tee -a "$LOG_FILE"
echo "   Completed: $SUBAGENT_NAME" | tee -a "$LOG_FILE"
echo "   Status: $SUBAGENT_STATUS" | tee -a "$LOG_FILE"
echo "   Workflow Complete: $WORKFLOW_COMPLETE" | tee -a "$LOG_FILE"

if [ ${#NEXT_SUBAGENTS[@]} -gt 0 ]; then
    echo "   Next Recommended:" | tee -a "$LOG_FILE"
    for subagent in "${NEXT_SUBAGENTS[@]}"; do
        echo "     - $subagent" | tee -a "$LOG_FILE"
    done
fi

if [ ${#WORKFLOW_RECOMMENDATIONS[@]} -gt 0 ]; then
    echo "   Recommendations:" | tee -a "$LOG_FILE"
    for rec in "${WORKFLOW_RECOMMENDATIONS[@]}"; do
        echo "     - $rec" | tee -a "$LOG_FILE"
    done
fi

# 7. Check for shadow development priority
SHADOW_PRIORITY_ALERT=""
if [ "$SUBAGENT_NAME" != "shadow-integration-specialist" ] && [ "$SUBAGENT_NAME" != "phase-tracker" ]; then
    # Check if we should prioritize shadow work
    SHADOW_FILES_COUNT=$(find "$PROJECT_DIR" -name "*shadow*" -o -name "*Shadow*" 2>/dev/null | wc -l)
    if [ "$SHADOW_FILES_COUNT" -lt 30 ]; then
        SHADOW_PRIORITY_ALERT="Shadow development critical priority - only $SHADOW_FILES_COUNT files (target: 50+)"
        echo "🚨 $SHADOW_PRIORITY_ALERT" | tee -a "$LOG_FILE"
    fi
fi

# Output coordination result JSON
cat << EOF
{
  "continue": true,
  "decision": "proceed",
  "reason": "Subagent $SUBAGENT_NAME coordination complete",
  "coordination_status": {
    "completed_subagent": "$SUBAGENT_NAME",
    "workflow_complete": $WORKFLOW_COMPLETE,
    "next_subagents": [$(IFS=','; echo "\"${NEXT_SUBAGENTS[*]}\"" | sed 's/ /","/g')],
    "recommendations_count": ${#WORKFLOW_RECOMMENDATIONS[@]}
  },
  "next_actions": [
$(if [ ${#NEXT_SUBAGENTS[@]} -gt 0 ]; then
    echo "    \"Consider running: ${NEXT_SUBAGENTS[0]} subagent\""
else
    echo "    \"Workflow coordination complete\""
fi)
$([ -n "$SHADOW_PRIORITY_ALERT" ] && echo ",    \"$SHADOW_PRIORITY_ALERT\"" || echo "")
  ]
}
EOF

exit 0