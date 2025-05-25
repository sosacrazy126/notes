---
tags:
  - Greptile
  - CLI_design
  - codebase_comprehension
---
```markdown
# OVERVIEW

What It Does: Manages indexed repositories for status checks, natural language queries, and searches with branch-specific and advanced analysis modes.  

Why People Use It: Simplifies codebase interaction by enabling efficient searches, smart queries, and precise control over repository indexing and branch targeting.  

# HOW TO USE IT  

Most Common Syntax:  
- **Index Repository**: `greptile-cli index owner/repo [BRANCH]`  
- **Check Status**: `greptile-cli status owner/repo [-b BRANCH]`  
- **Query Repository**: `greptile-cli query "question" --repository-spec owner/repo [--genius]`  
- **Search Repository**: `greptile-cli search "term" --repository-spec owner/repo [-b BRANCH]`  

# COMMON USE CASES  

- For Indexing a GitHub Repository’s Default Branch: `greptile-cli index owner/repo`  
- For Checking a GitLab Branch Status: `greptile-cli status gitlab:group/proj:dev`  
- For Advanced Query with Genius Mode: `greptile-cli query "Fix the bug" --repository-spec owner/repo --genius`  
- For Searching a Specific Branch: `greptile-cli search "API key" --repository-spec owner/repo -b feature`  

# MOST IMPORTANT AND USED OPTIONS AND FEATURES  

- `--genius`: Enables deeper analysis for smarter query results (slower, for `query`/`search`).  
- `-b, --branch`: Specifies the branch (e.g., `develop`), used with shorthand repository specs.  
- `--repository-spec`: Explicitly defines a repository (GitHub, GitLab) and branch via shorthand or full format (e.g., `gitlab:group/proj:main`).  
- `--format [json/text/rich]`: Tailors output format (default: `rich` for human-readable results).  
- `--reload`: Forces reindexing even if already indexed (for `index` cmd).  
- `--force`: Bypasses cached status checks (for `status` cmd).  
```