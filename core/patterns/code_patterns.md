# Code Patterns

**Pattern Count**: 28
**Generated**: 2025-08-10T23:22:25.400718

## Patterns

### 1. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/dev_tools/ast-grep-mcp/main.py`

**Classes**:
- DumpFormat

**Functions**:
- dump_syntax_tree, test_match_code_rule, find_code, find_code_by_rule, run_ast_grep_dump

### 2. demo_flow
**File**: `/home/evilbastardxd/Desktop/tools/notes/dev_tools/ast-grep-mcp/demo_flow.py`

**Functions**:
- create_demo_project, run_mcp_tool, demonstrate_flow, show_tool_capabilities

### 3. duplicate_hunter_agent
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/duplicate_hunter_agent.py`

**Classes**:
- DuplicateHunterAgent

**Functions**:
- main, __init__, setup_logging, update_state, calculate_content_hash

### 4. orchestrator
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/orchestrator.py`

**Classes**:
- AgentConfig, AgentState, OrchestrationState, ParallelAgentOrchestrator

**Functions**:
- __init__, update_agent_state, get_agent_state, all_dependencies_met, get_phase_summary

### 5. system_architect_agent
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/system_architect_agent.py`

**Classes**:
- SystemArchitectAgent, ContentSearcher, WorkspaceHealthChecker

**Functions**:
- __init__, setup_logging, update_state, load_agent_results, create_new_directory_structure

### 6. workspace_optimizer_agent
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/workspace_optimizer_agent.py`

**Classes**:
- WorkspaceOptimizerAgent

**Functions**:
- main, __init__, setup_logging, update_state, calculate_directory_size

### 7. pattern_extractor_agent
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/pattern_extractor_agent.py`

**Classes**:
- PatternExtractorAgent

**Functions**:
- main, __init__, setup_logging, update_state, scan_for_patterns

### 8. content_evaluator_agent
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/content_evaluator_agent.py`

**Classes**:
- ContentEvaluatorAgent

**Functions**:
- main, __init__, setup_logging, update_state, collect_files_to_evaluate

### 9. backup_creator_agent
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/parallel-agents/backup_creator_agent.py`

**Classes**:
- BackupCreatorAgent

**Functions**:
- main, __init__, setup_logging, update_state, create_git_backup

### 10. tmux_utils
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/Tmux-Orchestrator/tmux_utils.py`

**Classes**:
- TmuxWindow, TmuxSession, TmuxOrchestrator

**Functions**:
- __init__, get_tmux_sessions, capture_window_content, get_window_info, send_keys_to_window

### 11. at_tag_processor
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/scripts/at_tag_processor.py`

**Classes**:
- AtTag, TaggedFile, TagIndex, AtTagProcessor

**Functions**:
- main, __init__, detect_at_tags, process_file, scan_repository

### 12. validate_links
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/scripts/validate_links.py`

**Classes**:
- LinkValidator

**Functions**:
- main, __init__, extract_links_from_file, is_valid_url, validate_file

### 13. doc_health_dashboard
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/monitoring/doc_health_dashboard.py`

**Classes**:
- DocumentationHealthDashboard

**Functions**:
- main, __init__, analyze_file_statistics, check_link_health, analyze_api_coverage

### 14. automated_tagger
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/metadata/tagging_system/automated_tagger.py`

**Classes**:
- ContentType, MaturityLevel, ConsciousnessPhase, ContentMetadata, AutomatedTagger

**Functions**:
- __post_init__, __init__, _load_schema, _initialize_tag_patterns, _initialize_consciousness_indicators

### 15. discovery_engine
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/metadata/tagging_system/discovery_engine.py`

**Classes**:
- ContentType, MaturityLevel, ConsciousnessPhase, ContentMetadata, SearchQuery

**Functions**:
- __post_init__, __post_init__, __init__, _load_metadata, _build_indices

### 16. metadata_injector
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/metadata/tagging_system/metadata_injector.py`

**Classes**:
- MetadataInjector

**Functions**:
- __init__, has_yaml_frontmatter, extract_existing_frontmatter, generate_yaml_frontmatter, inject_markdown_metadata

### 17. integration-test-suite
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/claude_config/testing/integration-test-suite.py`

**Classes**:
- TestResult, IntegrationTestCoordinator

**Functions**:
- main, __init__, setup_logging, run_comprehensive_integration_tests, analyze_ecosystem_state

### 18. agent_deployment_test
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/claude_config/testing/agent_deployment_test.py`

**Classes**:
- AgentDeploymentTester

**Functions**:
- main, __init__, test_claude_code_available, list_available_agents, generate_deployment_commands

### 19. agent_recognition_validator
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/claude_config/testing/agent_recognition_validator.py`

**Classes**:
- AgentRecognitionValidator

**Functions**:
- main, __init__, parse_agent_frontmatter, validate_agent_specification, scan_agents_directory

### 20. coordination-dashboard
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/claude_config/monitoring/coordination-dashboard.py`

**Classes**:
- class, CoordinationMonitor

**Functions**:
- __init__, signal_handler, start_monitoring, collect_coordination_metrics, calculate_we_principle_coherence

### 21. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/.obsidian/plugins/vibesidian/main.js`

### 22. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/.obsidian/plugins/mesh-ai/main.js`

### 23. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/.obsidian/plugins/fileorganizer2000/main.js`

### 24. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/.obsidian/plugins/khoj/main.js`

### 25. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/.obsidian/plugins/pieces-for-developers/main.js`

### 26. main
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/.obsidian/plugins/terminal/main.js`

### 27. persistence
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/scheduler-mcp/mcp_scheduler/persistence.py`

**Classes**:
- Database

**Functions**:
- __init__, _create_tables, save_task, get_task, get_all_tasks

### 28. task
**File**: `/home/evilbastardxd/Desktop/tools/notes/_system/scheduler-mcp/mcp_scheduler/task.py`

**Classes**:
- TaskStatus, TaskType, Task, TaskExecution

**Functions**:
- sanitize_ascii, validate_ascii_fields, validate_command, validate_api_url, validate_prompt

## Common Elements

**Frequent Name Components**:
- agent, main, demo, flow, duplicate

## Recommendations

- Extract common patterns into reusable libraries
- Create code generation templates
- Document design pattern implementations