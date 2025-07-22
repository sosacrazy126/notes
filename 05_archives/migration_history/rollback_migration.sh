#!/bin/bash

# Rollback script for AI tools migration
set -euo pipefail

BACKUP_DIR="$1"

if [[ -z "$BACKUP_DIR" || ! -d "$BACKUP_DIR" ]]; then
    echo "ERROR: Backup directory not provided or doesn't exist"
    echo "Usage: $0 <backup_directory>"
    exit 1
fi

echo "Rolling back migration from: $BACKUP_DIR"

# Remove new structure
[[ -d "ai_tools" ]] && rm -rf "ai_tools"

# Restore original directories
[[ -d "$BACKUP_DIR/patterns" ]] && cp -r "$BACKUP_DIR/patterns" .
[[ -d "$BACKUP_DIR/agents-tools" ]] && cp -r "$BACKUP_DIR/agents-tools" .
[[ -d "$BACKUP_DIR/_NoteCompanion" ]] && cp -r "$BACKUP_DIR/_NoteCompanion" .

echo "✅ Rollback complete"
