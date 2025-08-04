# Initiate Claude Code Session

Provide comprehensive context and guidance for Claude Code agent navigation and assistance.

## Instructions:

1. **Environment Assessment:**
   - Check current working directory
   - Identify if directory is a git repository
   - Scan for key configuration files (package.json, requirements.txt, etc.)
   - Check for existing CLAUDE.md or project documentation

2. **Project Context Discovery:**
   - Read project structure using LS and Glob tools
   - Identify technology stack and frameworks
   - Locate key entry points and configuration files
   - Check for existing slash command configurations

3. **Session Initialization:**
   - Check for `claude_compact_recent.txt` for conversation context
   - Assess available MCP tools and capabilities
   - Review git status and recent commits
   - Identify any active requirements gathering sessions

4. **Guidance Framework Setup:**
   - Display available slash commands and workflows
   - Explain project-specific conventions and patterns
   - Outline recommended development workflow
   - Provide quick-start templates for common tasks

## Display Format:
```
🚀 Claude Code Session Initiated

📁 Project Context:
- Directory: [current-path]
- Type: [git-repo/standalone-project]
- Stack: [detected-technologies]
- Entry Points: [main-files]

🔧 Available Tools:
- MCP Tools: [list-active-mcp-servers]
- Slash Commands: [count] requirements workflow commands
- Git Integration: [enabled/disabled]

📋 Active Sessions:
- Requirements: [active-requirement-name or "None"]
- Recent Context: [claude_compact_recent.txt status]

🎯 Quick Actions:
1. Start requirements gathering: /requirements-start [feature]
2. View project structure: Use Glob and LS tools
3. Check git status: Review recent commits
4. Resume context: Load claude_compact_recent.txt

📚 Workflow Guidance:
- Follow CLAUDE.md conventions if present
- Use TodoWrite for complex multi-step tasks
- Prefer editing existing files over creating new ones
- Run tests and linting before committing changes

🔍 Project Patterns:
[Detected conventions and patterns]

Ready for guided assistance. What would you like to work on?
```

## Context Seeding Actions:

1. **Load Project Memory:**
   - Check for conversation history files
   - Scan for previous session artifacts
   - Review requirements documentation if exists

2. **Capability Assessment:**
   - Test available MCP connections
   - Verify tool permissions and access
   - Check for restricted or missing tools

3. **Pattern Recognition:**
   - Identify code style and conventions
   - Detect testing frameworks and patterns
   - Note build and deployment configurations

4. **Workflow Preparation:**
   - Set up todo tracking if needed
   - Prepare for systematic task management
   - Enable proactive tool usage patterns

## Smart Defaults:
- If requirements folder exists: Suggest continuing active requirement
- If CLAUDE.md exists: Load and reference project instructions
- If git repo: Show recent commit context and branch status
- If package.json: Display scripts and dependencies overview
- If tests exist: Note testing approach and commands

## Integration Points:
- Seamlessly connect with existing /requirements-* commands
- Maintain consistency with established workflow patterns
- Respect project-specific conventions and constraints
- Enable smooth transition to development tasks

## Error Handling:
- Gracefully handle missing files or permissions
- Provide alternatives when tools are unavailable
- Suggest manual steps if automated discovery fails
- Maintain helpful guidance even with limited context