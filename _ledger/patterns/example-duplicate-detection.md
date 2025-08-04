---
pattern_name: duplicate-content-detection
pattern_type: algorithm
source_files: [_ledger/scripts/find_duplicates.py]
confidence: 1.0
---

# Duplicate Content Detection Pattern

## Purpose
Identify duplicate files across a repository using content hashing to prevent redundant storage and maintain a clean knowledge base.

## Specification

### Inputs
- `root_path`: string, directory to scan
- `file_extensions`: array[string], file types to include (default: ['.md', '.txt'])
- `exclude_paths`: array[string], directories to skip (default: ['.git', 'node_modules'])

### Process
1. **Traverse Directory Tree**
   - Walk through all subdirectories from root_path
   - Skip excluded paths
   - Filter files by extension

2. **Generate Content Hash**
   - For each file, calculate SHA-256 hash
   - Handle read errors gracefully
   - Store hash → [file_paths] mapping

3. **Identify Duplicates**
   - Find hashes with multiple file paths
   - Group files by their location type

4. **Categorize Locations**
   - 'archived': Files in _archive/ directory
   - 'active': Files in working directories
   - 'system': Files in _system/ or .config/
   - 'new_additions': Recently added files

5. **Generate Report**
   - Group duplicates by hash
   - Show location categories
   - Recommend actions (delete from active if in archive)

### Outputs
- `duplicate_sets`: array of duplicate groups
  ```yaml
  - hash: string (SHA-256)
    files: array[string] (file paths)
    locations: map[string, array[string]] (categorized paths)
    recommendation: string (suggested action)
  ```
- `summary_stats`: duplication metrics
  ```yaml
  total_files: number
  duplicate_sets: number
  space_wasted: bytes
  deduplication_potential: percentage
  ```

### Constraints
- Memory efficient: Process files in chunks
- Performance: < 1 second per 1000 files
- Error handling: Continue on file read errors
- File size limit: Skip files > 100MB

### Examples

```yaml
example_basic:
  input:
    root_path: "/project"
    file_extensions: [".md"]
    exclude_paths: [".git"]
  output:
    duplicate_sets:
      - hash: "a1b2c3d4..."
        files: 
          - "/project/docs/readme.md"
          - "/project/_archive/old_readme.md"
        locations:
          active: ["/project/docs/readme.md"]
          archived: ["/project/_archive/old_readme.md"]
        recommendation: "Delete from active (exists in archive)"
    summary_stats:
      total_files: 150
      duplicate_sets: 12
      space_wasted: 524288
      deduplication_potential: 8.5

example_complex:
  input:
    root_path: "/workspace"
    file_extensions: [".md", ".txt", ".py"]
    exclude_paths: [".git", "__pycache__", "venv"]
  output:
    duplicate_sets:
      - hash: "e5f6g7h8..."
        files:
          - "/workspace/src/utils.py"
          - "/workspace/backup/utils.py"
          - "/workspace/old/utils_v1.py"
        locations:
          active: ["/workspace/src/utils.py"]
          backup: ["/workspace/backup/utils.py", "/workspace/old/utils_v1.py"]
        recommendation: "Keep active version, archive others"
```

### Implementation Notes

1. **Hash Calculation**
   - Use streaming hash for large files
   - Cache results for unchanged files (mtime-based)

2. **Parallel Processing**
   - Can parallelize hash calculation
   - Synchronize hash map updates

3. **Report Generation**
   - Markdown format for human reading
   - JSON format for programmatic use
   - Include visualization options

### Extension Points

1. **Content Similarity** (not just exact duplicates)
   - Fuzzy matching with similarity threshold
   - Identify near-duplicates

2. **Smart Recommendations**
   - Consider file age
   - Analyze import/reference patterns
   - Suggest consolidation strategies

3. **Integration Hooks**
   - Git pre-commit check
   - CI/CD pipeline integration
   - IDE plugin for real-time detection

---

*This pattern demonstrates the specification-first approach: clear inputs, process, outputs, and examples that any LLM can implement in any language.*