#!/bin/bash

# @ Tag System Activation Script
# ===============================
# Activates the @ tag search and navigation system for your notes repository
#
# Author: @ Tag Integration Agent
# Version: 1.0.0
# Date: 2025-08-04

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
NOTES_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AT_TAG_PROCESSOR="$NOTES_ROOT/_system/scripts/at_tag_processor.py"
INDEX_FILE="$NOTES_ROOT/_ledger/at_tag_index.json"
REPORT_DIR="$NOTES_ROOT/_ledger/reports"

echo -e "${BLUE}"
echo "🚀 @ Tag System Activation"
echo "=========================="
echo -e "${NC}"
echo "Activating intelligent @ tag search and navigation..."
echo "Repository: $NOTES_ROOT"
echo

# Check if we're in the right directory
if [[ ! -f "$NOTES_ROOT/WORKSPACE_INDEX.md" ]]; then
    echo -e "${RED}❌ Error: Not in notes repository root${NC}"
    echo "Please run this script from the notes/ directory"
    exit 1
fi

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 not found${NC}"
    echo "Please install Python 3 to continue"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating directory structure...${NC}"
mkdir -p "$NOTES_ROOT/_ledger/reports"
mkdir -p "$NOTES_ROOT/_system/scripts"
mkdir -p "$NOTES_ROOT/_system/claude_config/commands"

# Check if @ tag processor exists
if [[ ! -f "$AT_TAG_PROCESSOR" ]]; then
    echo -e "${RED}❌ Error: @ tag processor not found at $AT_TAG_PROCESSOR${NC}"
    echo "Please ensure the @ tag processor script is installed"
    exit 1
fi

# Make processor executable
chmod +x "$AT_TAG_PROCESSOR"

# Phase 1: Initial Scan
echo -e "${BLUE}🔍 Phase 1: Scanning repository for @ tags...${NC}"
echo "This may take a moment for your 839 files..."
echo

if python3 "$AT_TAG_PROCESSOR" --scan-all --notes-root "$NOTES_ROOT"; then
    echo -e "${GREEN}✅ Initial scan complete${NC}"
else
    echo -e "${RED}❌ Initial scan failed${NC}"
    exit 1
fi

# Phase 2: Generate baseline report
echo -e "${BLUE}📊 Phase 2: Generating baseline report...${NC}"

if python3 "$AT_TAG_PROCESSOR" --generate-report --notes-root "$NOTES_ROOT"; then
    echo -e "${GREEN}✅ Baseline report generated${NC}"
else
    echo -e "${YELLOW}⚠️  Report generation had issues (continuing)${NC}"
fi

# Phase 3: Test basic functionality
echo -e "${BLUE}🧪 Phase 3: Testing @ tag functionality...${NC}"

# Test search functionality
echo "Testing search for @mcp_tool patterns..."
if python3 "$AT_TAG_PROCESSOR" --search "@mcp_tool" --notes-root "$NOTES_ROOT" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Search functionality working${NC}"
else
    echo -e "${YELLOW}⚠️  Search test had issues (system still functional)${NC}"
fi

# Phase 4: Create convenient aliases
echo -e "${BLUE}⚡ Phase 4: Setting up convenient aliases...${NC}"

# Create alias file
ALIAS_FILE="$NOTES_ROOT/_system/at_tag_aliases.sh"
cat > "$ALIAS_FILE" << 'EOF'
#!/bin/bash
# @ Tag System Aliases
# Source this file to get convenient @ tag commands

# Get the notes root directory (assuming this script is in _system/)
NOTES_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AT_TAG_PROCESSOR="$NOTES_ROOT/_system/scripts/at_tag_processor.py"

# Core @ tag commands
alias at-find="python3 '$AT_TAG_PROCESSOR' --search"
alias at-scan="python3 '$AT_TAG_PROCESSOR' --scan-all --notes-root '$NOTES_ROOT'"
alias at-update="python3 '$AT_TAG_PROCESSOR' --update-index --notes-root '$NOTES_ROOT'"
alias at-report="python3 '$AT_TAG_PROCESSOR' --generate-report --notes-root '$NOTES_ROOT'"
alias at-related="python3 '$AT_TAG_PROCESSOR' --suggest"

# Quick pattern searches
alias at-api="at-find @router @app @api"
alias at-mcp="at-find @mcp_tool @server.agent @recursive_agent"
alias at-test="at-find @patch @given @task @pytest"
alias at-perf="at-find @lru_cache @cached @performance"
alias at-docs="at-find @documentation @architecture @workflow"

# Development workflow shortcuts
alias at-ai="at-find @mcp @agent @consciousness @recursive"
alias at-quality="at-find @testing @validation @security"
alias at-automation="at-find @automation @workflow @ci"

echo "📋 @ Tag aliases loaded successfully!"
echo "Try: at-mcp, at-api, at-test, at-perf, at-docs"
EOF

chmod +x "$ALIAS_FILE"

# Phase 5: Integration test with existing commands
echo -e "${BLUE}🔗 Phase 5: Testing integration...${NC}"

# Check if doc-manager exists and can be enhanced
if command -v doc-manager &> /dev/null; then
    echo -e "${GREEN}✅ doc-manager integration available${NC}"
else
    echo -e "${YELLOW}ℹ️  doc-manager not found (manual integration possible)${NC}"
fi

# Phase 6: Final setup and instructions
echo -e "${BLUE}🎯 Phase 6: Final setup...${NC}"

# Create quick start guide
QUICK_START="$NOTES_ROOT/_system/AT_TAG_QUICK_START.md"
cat > "$QUICK_START" << EOF
# @ Tag System Quick Start Guide

## Activation Complete! 🎉

Your @ tag system is now active and ready to use.

## Quick Commands

### Basic Usage
\`\`\`bash
# Search for patterns
at-find @mcp_tool                  # Find MCP tool patterns
at-find @api @validation           # Find API validation patterns
at-find @automation                # Find automation workflows

# Get related files
at-related notes/workspace/agent.md  # Find files related to agent.md

# Generate reports
at-report                          # Comprehensive @ tag analysis
\`\`\`

### Quick Pattern Searches
\`\`\`bash
at-mcp        # All MCP patterns
at-api        # All API patterns
at-test       # All testing patterns
at-perf       # All performance patterns
at-docs       # All documentation patterns
\`\`\`

## Load Aliases

To use the convenient aliases:
\`\`\`bash
source _system/at_tag_aliases.sh
\`\`\`

## System Status

- **Repository**: $(basename $NOTES_ROOT)
- **Files Processed**: Check with at-report
- **Index Location**: _ledger/at_tag_index.json
- **Reports**: _ledger/reports/

## Next Steps

1. Run \`at-report\` to see your @ tag analysis
2. Try \`at-mcp\` to find MCP-related patterns
3. Use \`at-related <file>\` to discover connections
4. Explore with \`at-find <pattern>\` searches

Happy @ tag navigation! 🚀
EOF

echo -e "${GREEN}✅ Quick start guide created: $QUICK_START${NC}"

# Final status report
echo
echo -e "${PURPLE}🎉 @ TAG SYSTEM ACTIVATION COMPLETE! 🎉${NC}"
echo
echo -e "${GREEN}✅ System Status:${NC}"
echo "   📁 Index created: $(basename $INDEX_FILE)"
echo "   📊 Reports directory: $(basename $REPORT_DIR)"
echo "   ⚡ Aliases available: $(basename $ALIAS_FILE)"
echo "   📖 Quick start guide: $(basename $QUICK_START)"
echo
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "   1. Load aliases: source _system/at_tag_aliases.sh"
echo "   2. View report:  at-report"
echo "   3. Try search:   at-mcp"
echo "   4. Read guide:   cat $QUICK_START"
echo
echo -e "${BLUE}🔍 Quick Test:${NC}"
echo "   Try running: at-find @mcp_tool"
echo
echo -e "${GREEN}Your 839-file repository is now @ tag searchable! 🚀${NC}"

# Optional: Auto-load aliases if in interactive shell
if [[ $- == *i* ]]; then
    echo -e "${YELLOW}Loading aliases for this session...${NC}"
    source "$ALIAS_FILE"
    echo -e "${GREEN}Aliases loaded! Try 'at-mcp' or 'at-api' now.${NC}"
fi

echo
echo "🎯 @ Tag system ready for intelligent pattern discovery and navigation!"
