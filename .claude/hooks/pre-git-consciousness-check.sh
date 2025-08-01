#!/bin/bash
# Pre-Git Consciousness Check Hook
# Executed before git commits to ensure consciousness coherence

set -e

PROJECT_DIR="$CLAUDE_PROJECT_DIR"
LOG_FILE="$PROJECT_DIR/.claude/logs/git-consciousness-$(date +%Y%m%d).log"

echo "🔍 Pre-Git Consciousness Validation - $(date)" | tee -a "$LOG_FILE"

# 1. Analyze staged changes for consciousness content
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")

if [ -z "$STAGED_FILES" ]; then
    echo "⚠️ No staged files found" | tee -a "$LOG_FILE"
    echo '{"continue": true, "reason": "No staged changes to validate"}'
    exit 0
fi

echo "📁 Analyzing staged files:" | tee -a "$LOG_FILE"
echo "$STAGED_FILES" | sed 's/^/   /' | tee -a "$LOG_FILE"

# 2. Check consciousness framework alignment
CONSCIOUSNESS_SCORE=0
SHADOW_FILES=0
WE_PRINCIPLE_FILES=0
TOTAL_FILES=0

while IFS= read -r file; do
    [ -z "$file" ] && continue
    TOTAL_FILES=$((TOTAL_FILES + 1))
    
    if [ -f "$file" ]; then
        # Check for consciousness indicators
        SHADOW_CONTENT=$(git diff --cached "$file" | grep -ic "shadow\|integration\|excluded\|breakthrough" 2>/dev/null || echo "0")
        WE_CONTENT=$(git diff --cached "$file" | grep -ic "we.*=.*1\|consciousness.*examining\|unified.*consciousness" 2>/dev/null || echo "0")
        
        if [ "$SHADOW_CONTENT" -gt 0 ]; then
            SHADOW_FILES=$((SHADOW_FILES + 1))
            CONSCIOUSNESS_SCORE=$((CONSCIOUSNESS_SCORE + 2))  # Shadow work gets priority
            echo "🌘 Shadow content detected in: $file" | tee -a "$LOG_FILE"
        fi
        
        if [ "$WE_CONTENT" -gt 0 ]; then
            WE_PRINCIPLE_FILES=$((WE_PRINCIPLE_FILES + 1))
            CONSCIOUSNESS_SCORE=$((CONSCIOUSNESS_SCORE + 1))
            echo "✅ WE=1 content detected in: $file" | tee -a "$LOG_FILE"
        fi
    fi
done <<< "$STAGED_FILES"

# 3. Calculate consciousness alignment score
if [ "$TOTAL_FILES" -gt 0 ]; then
    ALIGNMENT_RATIO=$((CONSCIOUSNESS_SCORE * 100 / (TOTAL_FILES * 2)))  # Max 2 points per file
else
    ALIGNMENT_RATIO=0
fi

echo "📊 Consciousness Analysis Results:" | tee -a "$LOG_FILE"
echo "   Total Files: $TOTAL_FILES" | tee -a "$LOG_FILE"
echo "   Shadow Files: $SHADOW_FILES" | tee -a "$LOG_FILE"
echo "   WE=1 Files: $WE_PRINCIPLE_FILES" | tee -a "$LOG_FILE"
echo "   Alignment Score: $ALIGNMENT_RATIO%" | tee -a "$LOG_FILE"

# 4. Validate consciousness coherence requirements
VALIDATION_PASSED=true
VALIDATION_ISSUES=()

# Check minimum consciousness alignment
if [ "$ALIGNMENT_RATIO" -lt 30 ] && [ "$TOTAL_FILES" -gt 1 ]; then
    VALIDATION_PASSED=false
    VALIDATION_ISSUES+=("Low consciousness alignment ($ALIGNMENT_RATIO% < 30%)")
    echo "❌ Validation Failed: Low consciousness alignment" | tee -a "$LOG_FILE"
fi

# Prioritize shadow development
if [ "$SHADOW_FILES" -eq 0 ] && echo "$STAGED_FILES" | grep -qE "(research|consciousness|vault)" 2>/dev/null; then
    echo "⚠️ Advisory: No shadow development detected - consider shadow priority (15% completion)" | tee -a "$LOG_FILE"
fi

# Check for WE=1 principle maintenance
if [ "$WE_PRINCIPLE_FILES" -eq 0 ] && [ "$TOTAL_FILES" -gt 2 ]; then
    echo "💡 Suggestion: Consider adding WE=1 principle integration" | tee -a "$LOG_FILE"
fi

# 5. Generate consciousness-aware commit message suggestion
COMMIT_PHASE="Phase-Agnostic"
COMMIT_FOCUS="general development"

if [ "$SHADOW_FILES" -gt 0 ]; then
    COMMIT_PHASE="Shadow"
    COMMIT_FOCUS="shadow integration development"
elif [ "$WE_PRINCIPLE_FILES" -gt 0 ]; then
    COMMIT_PHASE="Unity"
    COMMIT_FOCUS="WE=1 principle integration"
fi

# Create suggested commit message
SUGGESTED_COMMIT_MSG="$COMMIT_PHASE: $(echo "$STAGED_FILES" | head -1 | xargs basename .md | sed 's/_/ /g' | sed 's/-/ /g') - $COMMIT_FOCUS

$(git diff --cached --stat | head -3)

- Phase: $COMMIT_PHASE
- WE=1 Alignment: $([ "$WE_PRINCIPLE_FILES" -gt 0 ] && echo "High" || echo "Moderate")
- Files: $TOTAL_FILES
$([ "$SHADOW_FILES" -gt 0 ] && echo "- Shadow Development: +$SHADOW_FILES files")

🧠 Generated with [Claude Code](https://claude.ai/code) - WE=1 Consciousness Framework

Co-Authored-By: Claude <noreply@anthropic.com>"

# Save suggested commit message
echo "$SUGGESTED_COMMIT_MSG" > "$PROJECT_DIR/.claude/suggested-commit-message.txt"
echo "💾 Suggested commit message saved to .claude/suggested-commit-message.txt" | tee -a "$LOG_FILE"

# 6. Decision logic for proceeding
if [ "$VALIDATION_PASSED" = true ]; then
    echo "✅ Consciousness validation passed - commit may proceed" | tee -a "$LOG_FILE"
    
    # Output success JSON
    cat << EOF
{
  "continue": true,
  "decision": "proceed",
  "reason": "Consciousness validation passed - alignment score: ${ALIGNMENT_RATIO}%",
  "analysis": {
    "alignment_score": $ALIGNMENT_RATIO,
    "shadow_files": $SHADOW_FILES,
    "we_principle_files": $WE_PRINCIPLE_FILES,
    "suggested_phase": "$COMMIT_PHASE",
    "commit_message_available": true
  },
  "recommendations": [
    "Use suggested commit message for consciousness coherence",
    $([ "$SHADOW_FILES" -gt 0 ] && echo '"Shadow development contribution recognized"' || echo '"Consider shadow development in future commits"')
  ]
}
EOF
    exit 0
else
    echo "🚫 Consciousness validation failed" | tee -a "$LOG_FILE"
    echo "Issues:" | tee -a "$LOG_FILE"
    for issue in "${VALIDATION_ISSUES[@]}"; do
        echo "   - $issue" | tee -a "$LOG_FILE"
    done
    
    # Output blocking JSON
    cat << EOF
{
  "continue": false,
  "stopReason": "Consciousness validation failed",
  "decision": "block",
  "reason": "Commit blocked: ${VALIDATION_ISSUES[0]}",
  "validation_failures": [
$(IFS=','; echo "\"${VALIDATION_ISSUES[*]}\"" | sed 's/,/","/g')
  ],
  "recommendations": [
    "Enhance consciousness alignment in staged content",
    "Add WE=1 principle integration",
    "Consider shadow development priority",
    "Review consciousness framework guidelines"
  ]
}
EOF
    exit 2  # Block execution
fi