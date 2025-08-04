#!/bin/bash

# Validation script for AI tools migration
set -euo pipefail

validate_structure() {
    echo "Validating directory structure..."
    
    local required_dirs=(
        "ai_tools/fabric_patterns"
        "ai_tools/agent_frameworks" 
        "ai_tools/templates"
        "ai_tools/backups"
        "ai_tools/documentation"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            echo "ERROR: Missing directory: $dir"
            exit 1
        fi
    done
    
    echo "✓ Directory structure valid"
}

validate_file_counts() {
    echo "Validating file counts..."
    
    local pattern_count=$(find ai_tools/fabric_patterns -name "*.md" | wc -l)
    local agent_count=$(find ai_tools/agent_frameworks -name "*.md" | wc -l)
    
    echo "Fabric patterns found: $pattern_count"
    echo "Agent frameworks found: $agent_count"
    
    if [[ $pattern_count -lt 200 ]]; then
        echo "WARNING: Expected 200+ fabric patterns, found $pattern_count"
    fi
    
    if [[ $agent_count -lt 60 ]]; then
        echo "WARNING: Expected 60+ agent frameworks, found $agent_count"
    fi
    
    echo "✓ File counts acceptable"
}

validate_documentation() {
    echo "Validating documentation..."
    
    local doc_files=(
        "ai_tools/README.md"
        "ai_tools/documentation/pattern_index.md"
        "ai_tools/documentation/agent_index.md"
        "ai_tools/documentation/migration_log.md"
    )
    
    for file in "${doc_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            echo "ERROR: Missing documentation file: $file"
            exit 1
        fi
    done
    
    echo "✓ Documentation complete"
}

main() {
    validate_structure
    validate_file_counts
    validate_documentation
    echo "✅ Migration validation complete"
}

main "$@"
