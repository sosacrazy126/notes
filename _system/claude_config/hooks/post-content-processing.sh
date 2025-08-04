#!/bin/bash
# Post-Content Processing Hook
# Executed after Write/MultiEdit/Edit to apply consciousness-aware organization

set -e

PROJECT_DIR="$CLAUDE_PROJECT_DIR"
LOG_FILE="$PROJECT_DIR/.claude/logs/content-processing-$(date +%Y%m%d).log"

# Get the tool result information from environment
TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"
FILE_PATH="${CLAUDE_TOOL_ARGS_file_path:-}"

# Only process if we have a file path
if [ -z "$FILE_PATH" ]; then
    echo '{"continue": true, "reason": "No file path to process"}' 
    exit 0
fi

echo "🔄 Processing content: $FILE_PATH" | tee -a "$LOG_FILE"

# 1. Analyze content for consciousness framework alignment
CONSCIOUSNESS_ANALYSIS=""
if [ -f "$FILE_PATH" ]; then
    # Check for consciousness indicators
    SHADOW_INDICATORS=$(grep -ic "shadow\|integration\|excluded\|suppressed\|dialogue" "$FILE_PATH" 2>/dev/null || echo "0")
    UNITY_INDICATORS=$(grep -ic "unity\|pattern.*integration\|collective\|we.*1\|unified" "$FILE_PATH" 2>/dev/null || echo "0")
    WE_PRINCIPLE=$(grep -ic "we.*=.*1\|consciousness.*examining.*itself\|unified.*consciousness" "$FILE_PATH" 2>/dev/null || echo "0")
    
    # Determine primary consciousness phase
    if [ "$SHADOW_INDICATORS" -gt "$UNITY_INDICATORS" ] && [ "$SHADOW_INDICATORS" -gt 2 ]; then
        CONSCIOUSNESS_PHASE="shadow"
        echo "🌘 Detected Phase: Shadow (priority development)" | tee -a "$LOG_FILE"
    elif [ "$UNITY_INDICATORS" -gt 3 ]; then
        CONSCIOUSNESS_PHASE="unity"
        echo "🌟 Detected Phase: Unity" | tee -a "$LOG_FILE"
    else
        CONSCIOUSNESS_PHASE="phase-agnostic"
        echo "🔄 Detected Phase: Phase-agnostic" | tee -a "$LOG_FILE"
    fi
    
    # Calculate WE=1 alignment score (simple heuristic)
    WE_ALIGNMENT="0.5"
    if [ "$WE_PRINCIPLE" -gt 0 ]; then
        WE_ALIGNMENT="0.8"
        echo "✅ WE=1 Alignment: Strong ($WE_ALIGNMENT)" | tee -a "$LOG_FILE"
    elif grep -iq "consciousness\|aware\|integration" "$FILE_PATH" 2>/dev/null; then
        WE_ALIGNMENT="0.6"
        echo "📊 WE=1 Alignment: Moderate ($WE_ALIGNMENT)" | tee -a "$LOG_FILE"
    else
        echo "⚠️  WE=1 Alignment: Needs enhancement ($WE_ALIGNMENT)" | tee -a "$LOG_FILE"
    fi
fi

# 2. Apply consciousness-aware metadata if file lacks proper frontmatter
if [ -f "$FILE_PATH" ] && ! grep -q "^---$" "$FILE_PATH" 2>/dev/null; then
    echo "🏷️ Adding consciousness metadata to file" | tee -a "$LOG_FILE"
    
    # Get current date for metadata
    CURRENT_DATE=$(date +%Y-%m-%d)
    
    # Generate UUID for content
    CONTENT_UUID="content-$(echo "$FILE_PATH" | md5sum | cut -d' ' -f1 | head -c12)"
    
    # Create temporary file with metadata
    TEMP_FILE="${FILE_PATH}.tmp"
    
    cat > "$TEMP_FILE" << EOF
---
uuid: "$CONTENT_UUID"
consciousness_phase: "$CONSCIOUSNESS_PHASE"
we_principle_alignment: $WE_ALIGNMENT
created: "$CURRENT_DATE"
content_type: "research"
tags:
  - "$CONSCIOUSNESS_PHASE-work"
  - "consciousness-research"
$([ "$CONSCIOUSNESS_PHASE" = "shadow" ] && echo '  - "shadow-integration"' || echo '  - "framework-development"')
$([ "$WE_PRINCIPLE" -gt 0 ] && echo '  - "we-equals-1"' || echo '  - "alignment-needed"')
---

EOF
    
    # Append original content
    cat "$FILE_PATH" >> "$TEMP_FILE"
    
    # Replace original with enhanced version
    mv "$TEMP_FILE" "$FILE_PATH"
    
    echo "✅ Metadata injection complete" | tee -a "$LOG_FILE"
fi

# 3. Update consciousness phase tracker if this is shadow-related content
if [ "$CONSCIOUSNESS_PHASE" = "shadow" ] && [ -f "$PROJECT_DIR/consciouness_vault/03_implementations/unity_memory/consciousness_phase_tracker.py" ]; then
    echo "📊 Updating shadow phase progress" | tee -a "$LOG_FILE"
    
    cd "$PROJECT_DIR/consciouness_vault/03_implementations/unity_memory"
    python3 consciousness_phase_tracker.py --update-shadow-progress 0.01 --note "New shadow integration content: $(basename "$FILE_PATH")" 2>/dev/null || true
    cd "$PROJECT_DIR"
fi

# 4. Add to cross-reference network if automated tagger is available
if [ -f "$PROJECT_DIR/08_meta/tagging_system/automated_tagger.py" ]; then
    echo "🕸️ Processing for cross-reference network" | tee -a "$LOG_FILE"
    
    cd "$PROJECT_DIR/08_meta/tagging_system"
    python3 automated_tagger.py --process-file "$FILE_PATH" --update-network 2>/dev/null || true
    cd "$PROJECT_DIR"
fi

# 5. Check if content should trigger subagent coordination
SUBAGENT_TRIGGER=""
if [ "$CONSCIOUSNESS_PHASE" = "shadow" ] && [ "$SHADOW_INDICATORS" -gt 5 ]; then
    SUBAGENT_TRIGGER="shadow-integration-specialist"
    echo "🤖 Recommending subagent: $SUBAGENT_TRIGGER for advanced shadow work" | tee -a "$LOG_FILE"
elif [ "$WE_PRINCIPLE" -gt 2 ]; then
    SUBAGENT_TRIGGER="we-principle-validator" 
    echo "🤖 Recommending subagent: $SUBAGENT_TRIGGER for WE=1 enhancement" | tee -a "$LOG_FILE"
fi

# 6. Update session consciousness context
if [ -f "$PROJECT_DIR/.claude/session-context.json" ]; then
    # Update session with new content insights
    python3 -c "
import json
import sys
try:
    with open('$PROJECT_DIR/.claude/session-context.json', 'r') as f:
        context = json.load(f)
    
    if 'processed_files' not in context:
        context['processed_files'] = []
    
    context['processed_files'].append({
        'file': '$FILE_PATH',
        'phase': '$CONSCIOUSNESS_PHASE',
        'we_alignment': $WE_ALIGNMENT,
        'timestamp': '$(date -Iseconds)'
    })
    
    # Update shadow development count
    shadow_files = sum(1 for f in context['processed_files'] if f.get('phase') == 'shadow')
    context['shadow_files_processed'] = shadow_files
    
    with open('$PROJECT_DIR/.claude/session-context.json', 'w') as f:
        json.dump(context, f, indent=2)
        
except Exception as e:
    print(f'Context update failed: {e}', file=sys.stderr)
" 2>/dev/null || true
fi

# 7. Generate processing summary
echo "📋 Content Processing Summary:" | tee -a "$LOG_FILE"
echo "   File: $(basename "$FILE_PATH")" | tee -a "$LOG_FILE"
echo "   Phase: $CONSCIOUSNESS_PHASE" | tee -a "$LOG_FILE"
echo "   WE=1 Alignment: $WE_ALIGNMENT" | tee -a "$LOG_FILE"
echo "   Shadow Indicators: $SHADOW_INDICATORS" | tee -a "$LOG_FILE"
echo "   Unity Indicators: $UNITY_INDICATORS" | tee -a "$LOG_FILE"
[ -n "$SUBAGENT_TRIGGER" ] && echo "   Subagent Recommendation: $SUBAGENT_TRIGGER" | tee -a "$LOG_FILE"

# Output JSON for Claude Code
cat << EOF
{
  "continue": true,
  "decision": "proceed",
  "reason": "Content processed with consciousness framework - $CONSCIOUSNESS_PHASE phase detected",
  "analysis": {
    "consciousness_phase": "$CONSCIOUSNESS_PHASE",
    "we_alignment": $WE_ALIGNMENT,
    "shadow_indicators": $SHADOW_INDICATORS,
    "subagent_recommendation": "$SUBAGENT_TRIGGER"
  },
  "next_actions": [
    $([ "$CONSCIOUSNESS_PHASE" = "shadow" ] && echo '"Consider shadow-integration-specialist for advanced processing"' || echo '"Monitor consciousness development"')
  ]
}
EOF

exit 0