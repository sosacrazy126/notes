# Backup Retention Policy

## Overview
This document establishes retention policies for backup files and historical content in the consciousness research repository.

## Backup Categories

### 1. Consciousness Research Backups
**Location**: `/05_archives/backup_consolidation/`
- **Content**: 14 backup files from June 19, 2025 (NoteCompanion backups)
- **Size**: 492KB total
- **Retention**: Permanent (historical research value)
- **Files include**:
  - Shadow Instructor Agent backup (86KB)
  - Strategic Multi-Domain Research backups (2 versions, 144KB total)
  - Truth exploration backup (150KB)
  - Recursive Koan Mechanics backup (10KB)
  - Enneagram Sigils backup (7KB)
  - Various Untitled research pieces

### 2. Historical Cleanup Archive
**Location**: `/05_archives/backup_consolidation/historical_cleanup_backup_20250721.tar.gz`
- **Content**: Previous repository cleanup backup
- **Size**: 57MB compressed
- **Retention**: 1 year (July 2026) - can be purged after verification
- **Purpose**: Safety backup from previous organization efforts

### 3. Migration History
**Location**: `/05_archives/migration_history/`
- **Content**: AI tools migration scripts and logs
- **Size**: ~35KB
- **Retention**: Permanent (operational history)
- **Files**:
  - `migration_log_20250719_170839.log`
  - `migration_log_20250719_170850.log`
  - `rollback_migration.sh`
  - `validate_migration.sh`
  - `migrate_ai_tools.sh`

### 4. Safety Backups
**Location**: Repository root (temporary)
- **Content**: Pre-cleanup safety backup
- **Size**: 301KB
- **File**: `safety_backup_before_cleanup_20250721_204148.tar.gz`
- **Retention**: 30 days (can be purged after August 20, 2025)

## Retention Guidelines

### Immediate Cleanup Candidates
- Duplicate backup directories (removed)
- Empty migration backup directories (removed)
- Obsolete .smart-env backup files (removed)
- Temporary migration artifacts (cleaned)

### Permanent Retention
- Consciousness research backups (unique historical content)
- Migration operation logs (operational history)
- Original migration scripts (reproducibility)

### Scheduled Cleanup
- Safety backups: Review and purge after 30 days
- Large historical archives: Review annually for relevance

## Space Optimization Achieved
- **Before cleanup**: 492KB + 492KB + 32KB + 57MB = ~58MB
- **After consolidation**: 492KB + 57MB = ~57.5MB
- **Space saved**: ~500KB (duplicate elimination)
- **Organization improvement**: Centralized from 4 scattered locations to 2 organized archives

## Backup Verification Protocol
1. Verify safety backup integrity before purging
2. Confirm all unique content preserved in consolidation
3. Test migration rollback capability if needed
4. Document any backup deletions in this policy