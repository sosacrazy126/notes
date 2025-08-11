#!/usr/bin/env python3
"""
Pattern Extractor Agent
=======================

Identifies and extracts reusable patterns, templates, and frameworks from
the codebase to build a curated pattern library for the system thinking tool.

Author: Claude Code Agent System
Date: 2025-08-10
Version: 1.0.0
"""

import os
import json
import re
import ast
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any, Tuple, Optional
import logging
import threading
from collections import defaultdict, Counter
import yaml


class PatternExtractorAgent:
    """Agent for extracting reusable patterns and templates"""
    
    def __init__(self):
        self.repo_root = Path(os.environ.get("REPO_ROOT", "."))
        self.state_dir = Path(os.environ.get("STATE_DIR", "."))
        self.agent_name = os.environ.get("AGENT_NAME", "pattern-extractor")
        
        # Target directories
        self.target_dirs = ["dev_tools", "_system", "code_library"]
        
        # Setup logging
        self.setup_logging()
        
        # Pattern detection configuration
        self.pattern_types = {
            "prompt_templates": {
                "extensions": [".md", ".txt"],
                "indicators": [
                    r"system:", r"user:", r"assistant:",
                    r"{{.*?}}", r"\$\{.*?\}",
                    r"<.*?>", r"\[.*?\]",
                    r"ROLE:", r"TASK:", r"CONTEXT:",
                    r"template", r"prompt", r"instruction"
                ]
            },
            "agent_configs": {
                "extensions": [".json", ".yaml", ".yml"],
                "indicators": [
                    r'"agent"', r'"name"', r'"description"',
                    r'"role"', r'"instructions"', r'"tools"',
                    r"agent:", r"name:", r"role:"
                ]
            },
            "workflow_patterns": {
                "extensions": [".md", ".py", ".sh"],
                "indicators": [
                    r"workflow", r"pipeline", r"process",
                    r"step \d+", r"phase \d+",
                    r"def.*workflow", r"class.*Workflow",
                    r"#!/bin/bash", r"#!/usr/bin/env"
                ]
            },
            "config_templates": {
                "extensions": [".json", ".yaml", ".yml", ".toml"],
                "indicators": [
                    r'"config"', r'"settings"', r'"options"',
                    r"config:", r"settings:", r"defaults:",
                    r"template", r"example", r"sample"
                ]
            },
            "code_patterns": {
                "extensions": [".py", ".js", ".ts"],
                "indicators": [
                    r"class.*Template", r"class.*Pattern",
                    r"def.*template", r"def.*pattern",
                    r"@dataclass", r"@pattern",
                    r"Template", r"Pattern", r"Factory"
                ]
            }
        }
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Results tracking
        self.discovered_patterns = defaultdict(list)
        self.pattern_library = {}
        
    def setup_logging(self):
        """Configure agent logging"""
        log_file = self.state_dir.parent / "logs" / f"{self.agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(self.agent_name)
    
    def update_state(self, **kwargs):
        """Update agent state for orchestrator"""
        state_file = self.state_dir / f"{self.agent_name}_state.json"
        
        with self.lock:
            # Load existing state or create new
            if state_file.exists():
                with open(state_file, 'r') as f:
                    state = json.load(f)
            else:
                state = {
                    "name": self.agent_name,
                    "start_time": datetime.now().isoformat(),
                    "files_processed": 0,
                    "current_task": "",
                    "progress_percent": 0.0,
                    "patterns_found": 0
                }
            
            # Update with provided values
            state.update(kwargs)
            state["last_update"] = datetime.now().isoformat()
            
            # Save updated state
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
    
    def scan_for_patterns(self) -> Dict[str, List[Path]]:
        """Scan target directories for potential pattern files"""
        self.logger.info("🔍 Scanning for pattern files...")
        self.update_state(current_task="Scanning for pattern files", progress_percent=10)
        
        pattern_files = defaultdict(list)
        
        for target_dir in self.target_dirs:
            dir_path = self.repo_root / target_dir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.rglob("*"):
                if not file_path.is_file():
                    continue
                
                # Check each pattern type
                for pattern_type, config in self.pattern_types.items():
                    if file_path.suffix in config["extensions"]:
                        # Check if file contains pattern indicators
                        if self.file_contains_patterns(file_path, config["indicators"]):
                            pattern_files[pattern_type].append(file_path)
        
        total_files = sum(len(files) for files in pattern_files.values())
        self.logger.info(f"✅ Found {total_files} potential pattern files")
        
        for pattern_type, files in pattern_files.items():
            self.logger.info(f"  - {pattern_type}: {len(files)} files")
        
        return pattern_files
    
    def file_contains_patterns(self, file_path: Path, indicators: List[str]) -> bool:
        """Check if file contains pattern indicators"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for indicators
            for indicator in indicators:
                if re.search(indicator, content, re.IGNORECASE):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def extract_prompt_template(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract prompt template structure and components"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            pattern = {
                "type": "prompt_template",
                "file_path": str(file_path),
                "name": file_path.stem,
                "components": {},
                "variables": [],
                "structure": ""
            }
            
            # Detect template variables
            variable_patterns = [
                r'{{(.*?)}}',  # Mustache style
                r'\$\{(.*?)\}',  # Shell style
                r'<(.*?)>',  # Angle bracket style
                r'\[(.*?)\]',  # Square bracket style
            ]
            
            for var_pattern in variable_patterns:
                variables = re.findall(var_pattern, content)
                pattern["variables"].extend(variables)
            
            # Detect role-based structure
            role_sections = {}
            current_role = None
            
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                
                # Check for role markers
                role_match = re.match(r'(system|user|assistant|role|task|context):\s*(.*)', line, re.IGNORECASE)
                if role_match:
                    current_role = role_match.group(1).lower()
                    role_sections[current_role] = role_match.group(2)
                elif current_role and line:
                    if current_role not in role_sections:
                        role_sections[current_role] = ""
                    role_sections[current_role] += f" {line}"
            
            pattern["components"]["roles"] = role_sections
            
            # Detect template structure
            if "system:" in content.lower():
                pattern["structure"] = "role_based"
            elif "{{" in content or "${" in content:
                pattern["structure"] = "templated"
            elif any(word in content.lower() for word in ["template", "example", "pattern"]):
                pattern["structure"] = "example_based"
            else:
                pattern["structure"] = "freeform"
            
            # Extract metadata from comments/headers
            metadata_patterns = [
                r'#\s*(.*?)\n',  # Markdown headers
                r'//\s*(.*?)\n',  # Comments
                r'/\*\s*(.*?)\*/',  # Block comments
            ]
            
            metadata = []
            for meta_pattern in metadata_patterns:
                matches = re.findall(meta_pattern, content[:500])  # First 500 chars
                metadata.extend(matches)
            
            pattern["metadata"] = metadata
            
            return pattern
            
        except Exception as e:
            self.logger.warning(f"Could not extract prompt template from {file_path}: {e}")
            return None
    
    def extract_agent_config(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract agent configuration pattern"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            pattern = {
                "type": "agent_config",
                "file_path": str(file_path),
                "name": file_path.stem,
                "schema": {},
                "required_fields": [],
                "optional_fields": []
            }
            
            # Parse configuration file
            config_data = None
            if file_path.suffix in ['.json']:
                try:
                    config_data = json.loads(content)
                except json.JSONDecodeError:
                    pass
            elif file_path.suffix in ['.yaml', '.yml']:
                try:
                    import yaml
                    config_data = yaml.safe_load(content)
                except yaml.YAMLError:
                    pass
            
            if config_data:
                pattern["schema"] = self.analyze_config_schema(config_data)
            
            # Detect common agent fields
            agent_fields = [
                "name", "description", "role", "instructions", "tools",
                "capabilities", "parameters", "constraints", "examples"
            ]
            
            for field in agent_fields:
                if field in content.lower():
                    pattern["required_fields"].append(field)
            
            return pattern
            
        except Exception as e:
            self.logger.warning(f"Could not extract agent config from {file_path}: {e}")
            return None
    
    def extract_workflow_pattern(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract workflow/process pattern"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            pattern = {
                "type": "workflow_pattern",
                "file_path": str(file_path),
                "name": file_path.stem,
                "steps": [],
                "dependencies": [],
                "inputs": [],
                "outputs": []
            }
            
            # Extract numbered steps
            step_patterns = [
                r'(?:step|phase)\s+(\d+)[:.]?\s*(.*?)(?=\n|$)',
                r'(\d+)\.?\s+(.*?)(?=\n|$)',
                r'##\s*(\d+)\.\s*(.*?)(?=\n|$)'
            ]
            
            for step_pattern in step_patterns:
                matches = re.findall(step_pattern, content, re.IGNORECASE | re.MULTILINE)
                for step_num, step_desc in matches:
                    pattern["steps"].append({
                        "number": int(step_num),
                        "description": step_desc.strip()
                    })
            
            # For Python files, extract function/class definitions
            if file_path.suffix == '.py':
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if "workflow" in node.name.lower():
                                pattern["steps"].append({
                                    "type": "function",
                                    "name": node.name,
                                    "description": ast.get_docstring(node) or ""
                                })
                except SyntaxError:
                    pass
            
            # Extract dependencies
            dependency_patterns = [
                r'depends on:\s*(.*?)(?=\n|$)',
                r'requires:\s*(.*?)(?=\n|$)',
                r'after:\s*(.*?)(?=\n|$)'
            ]
            
            for dep_pattern in dependency_patterns:
                matches = re.findall(dep_pattern, content, re.IGNORECASE)
                pattern["dependencies"].extend(matches)
            
            return pattern
            
        except Exception as e:
            self.logger.warning(f"Could not extract workflow pattern from {file_path}: {e}")
            return None
    
    def extract_config_template(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract configuration template pattern"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            pattern = {
                "type": "config_template", 
                "file_path": str(file_path),
                "name": file_path.stem,
                "schema": {},
                "defaults": {},
                "sections": []
            }
            
            # Parse configuration
            config_data = None
            if file_path.suffix == '.json':
                try:
                    config_data = json.loads(content)
                except json.JSONDecodeError:
                    pass
            elif file_path.suffix in ['.yaml', '.yml']:
                try:
                    import yaml
                    config_data = yaml.safe_load(content)
                except yaml.YAMLError:
                    pass
            elif file_path.suffix == '.toml':
                # Basic TOML support
                sections = re.findall(r'\[(.*?)\]', content)
                pattern["sections"] = sections
            
            if config_data:
                pattern["schema"] = self.analyze_config_schema(config_data)
                if isinstance(config_data, dict):
                    pattern["defaults"] = {k: v for k, v in config_data.items() 
                                        if isinstance(v, (str, int, float, bool))}
            
            return pattern
            
        except Exception as e:
            self.logger.warning(f"Could not extract config template from {file_path}: {e}")
            return None
    
    def extract_code_pattern(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract code pattern/template"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            pattern = {
                "type": "code_pattern",
                "file_path": str(file_path),
                "name": file_path.stem,
                "language": file_path.suffix[1:],
                "classes": [],
                "functions": [],
                "patterns": []
            }
            
            # For Python files
            if file_path.suffix == '.py':
                try:
                    tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            class_info = {
                                "name": node.name,
                                "docstring": ast.get_docstring(node) or "",
                                "methods": []
                            }
                            
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef):
                                    class_info["methods"].append({
                                        "name": item.name,
                                        "docstring": ast.get_docstring(item) or ""
                                    })
                            
                            pattern["classes"].append(class_info)
                        
                        elif isinstance(node, ast.FunctionDef):
                            pattern["functions"].append({
                                "name": node.name,
                                "docstring": ast.get_docstring(node) or ""
                            })
                            
                except SyntaxError:
                    # If can't parse, extract patterns with regex
                    class_matches = re.findall(r'class\s+(\w+).*?:', content)
                    pattern["classes"] = [{"name": name} for name in class_matches]
                    
                    func_matches = re.findall(r'def\s+(\w+).*?:', content)
                    pattern["functions"] = [{"name": name} for name in func_matches]
            
            # Detect common patterns
            pattern_indicators = [
                "template", "pattern", "factory", "builder", 
                "singleton", "observer", "strategy", "adapter"
            ]
            
            for indicator in pattern_indicators:
                if indicator in content.lower():
                    pattern["patterns"].append(indicator)
            
            return pattern
            
        except Exception as e:
            self.logger.warning(f"Could not extract code pattern from {file_path}: {e}")
            return None
    
    def analyze_config_schema(self, config_data: Any, path: str = "") -> Dict[str, Any]:
        """Analyze configuration data structure"""
        schema = {}
        
        if isinstance(config_data, dict):
            for key, value in config_data.items():
                full_path = f"{path}.{key}" if path else key
                
                if isinstance(value, dict):
                    schema[key] = {
                        "type": "object",
                        "properties": self.analyze_config_schema(value, full_path)
                    }
                elif isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        schema[key] = {
                            "type": "array",
                            "items": self.analyze_config_schema(value[0], full_path)
                        }
                    else:
                        schema[key] = {"type": "array"}
                else:
                    schema[key] = {"type": type(value).__name__}
        
        return schema
    
    def process_pattern_files(self, pattern_files: Dict[str, List[Path]]) -> Dict[str, List[Dict]]:
        """Process all discovered pattern files"""
        self.logger.info("🔄 Processing pattern files...")
        self.update_state(current_task="Extracting patterns", progress_percent=30)
        
        extracted_patterns = defaultdict(list)
        total_files = sum(len(files) for files in pattern_files.values())
        processed = 0
        
        extractors = {
            "prompt_templates": self.extract_prompt_template,
            "agent_configs": self.extract_agent_config,
            "workflow_patterns": self.extract_workflow_pattern,
            "config_templates": self.extract_config_template,
            "code_patterns": self.extract_code_pattern
        }
        
        for pattern_type, files in pattern_files.items():
            extractor = extractors.get(pattern_type)
            if not extractor:
                continue
            
            for file_path in files:
                pattern = extractor(file_path)
                if pattern:
                    extracted_patterns[pattern_type].append(pattern)
                
                processed += 1
                progress = 30 + (processed / total_files) * 50
                self.update_state(
                    files_processed=processed,
                    progress_percent=progress,
                    patterns_found=sum(len(patterns) for patterns in extracted_patterns.values())
                )
        
        self.logger.info(f"✅ Extracted {sum(len(patterns) for patterns in extracted_patterns.values())} patterns")
        return extracted_patterns
    
    def build_pattern_library(self, extracted_patterns: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Build structured pattern library"""
        self.logger.info("🏗️ Building pattern library...")
        self.update_state(current_task="Building pattern library", progress_percent=80)
        
        library = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "agent": self.agent_name,
                "total_patterns": sum(len(patterns) for patterns in extracted_patterns.values())
            },
            "categories": {}
        }
        
        for pattern_type, patterns in extracted_patterns.items():
            if not patterns:
                continue
            
            category = {
                "name": pattern_type,
                "count": len(patterns),
                "patterns": patterns,
                "common_elements": self.find_common_elements(patterns),
                "recommendations": self.generate_pattern_recommendations(pattern_type, patterns)
            }
            
            library["categories"][pattern_type] = category
        
        return library
    
    def find_common_elements(self, patterns: List[Dict]) -> Dict[str, Any]:
        """Find common elements across patterns of the same type"""
        common = {
            "frequent_names": [],
            "common_structures": [],
            "shared_variables": []
        }
        
        # Find frequent names/terms
        all_names = []
        for pattern in patterns:
            name = pattern.get('name', '')
            all_names.extend(name.lower().split('_'))
        
        name_counts = Counter(all_names)
        common["frequent_names"] = [name for name, count in name_counts.most_common(5)]
        
        # For prompt templates, find common variables
        if patterns and patterns[0].get('type') == 'prompt_template':
            all_variables = []
            for pattern in patterns:
                all_variables.extend(pattern.get('variables', []))
            
            var_counts = Counter(all_variables)
            common["shared_variables"] = [var for var, count in var_counts.most_common(5) if count > 1]
        
        return common
    
    def generate_pattern_recommendations(self, pattern_type: str, patterns: List[Dict]) -> List[str]:
        """Generate recommendations for pattern usage"""
        recommendations = []
        
        if pattern_type == "prompt_templates":
            recommendations.extend([
                "Standardize variable naming conventions across templates",
                "Create base templates for common use cases",
                "Document template usage patterns and examples"
            ])
        
        elif pattern_type == "agent_configs":
            recommendations.extend([
                "Create configuration schema validation",
                "Standardize agent configuration format",
                "Build agent configuration generator tool"
            ])
        
        elif pattern_type == "workflow_patterns":
            recommendations.extend([
                "Extract common workflow steps into reusable components",
                "Create workflow orchestration framework",
                "Document workflow dependencies and sequencing"
            ])
        
        elif pattern_type == "config_templates":
            recommendations.extend([
                "Create configuration management system",
                "Standardize configuration file formats",
                "Build configuration validation tools"
            ])
        
        elif pattern_type == "code_patterns":
            recommendations.extend([
                "Extract common patterns into reusable libraries",
                "Create code generation templates",
                "Document design pattern implementations"
            ])
        
        return recommendations
    
    def generate_pattern_library_files(self, pattern_library: Dict[str, Any]):
        """Generate organized pattern library files"""
        self.logger.info("📁 Generating pattern library files...")
        
        # Create pattern library directory
        library_dir = self.repo_root / "core" / "patterns"
        library_dir.mkdir(parents=True, exist_ok=True)
        
        # Save main library index
        library_index_path = library_dir / "index.json"
        with open(library_index_path, 'w') as f:
            json.dump(pattern_library, f, indent=2, default=str)
        
        # Create category-specific files
        for category_name, category_data in pattern_library["categories"].items():
            category_file = library_dir / f"{category_name}.json"
            with open(category_file, 'w') as f:
                json.dump(category_data, f, indent=2, default=str)
            
            # Create markdown documentation
            md_content = self.generate_category_documentation(category_name, category_data)
            md_file = library_dir / f"{category_name}.md"
            with open(md_file, 'w') as f:
                f.write(md_content)
        
        # Create README for pattern library
        readme_content = self.generate_pattern_library_readme(pattern_library)
        readme_path = library_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return library_dir
    
    def generate_category_documentation(self, category_name: str, category_data: Dict) -> str:
        """Generate markdown documentation for a pattern category"""
        lines = [
            f"# {category_name.replace('_', ' ').title()}",
            "",
            f"**Pattern Count**: {category_data['count']}",
            f"**Generated**: {datetime.now().isoformat()}",
            "",
            "## Patterns",
            ""
        ]
        
        for i, pattern in enumerate(category_data['patterns'], 1):
            lines.extend([
                f"### {i}. {pattern.get('name', 'Unnamed Pattern')}",
                f"**File**: `{pattern.get('file_path', 'Unknown')}`",
                ""
            ])
            
            if pattern.get('type') == 'prompt_template':
                if pattern.get('variables'):
                    lines.extend([
                        "**Variables**:",
                        f"- {', '.join(pattern['variables'])}",
                        ""
                    ])
                
                if pattern.get('structure'):
                    lines.extend([
                        f"**Structure**: {pattern['structure']}",
                        ""
                    ])
            
            elif pattern.get('type') == 'workflow_pattern':
                if pattern.get('steps'):
                    lines.extend([
                        "**Steps**:",
                    ])
                    for step in pattern['steps'][:5]:  # Limit to first 5 steps
                        lines.append(f"- {step.get('description', step.get('name', 'Unknown step'))}")
                    lines.append("")
            
            elif pattern.get('type') == 'code_pattern':
                if pattern.get('classes'):
                    lines.extend([
                        "**Classes**:",
                        f"- {', '.join(cls['name'] for cls in pattern['classes'][:5])}",
                        ""
                    ])
                
                if pattern.get('functions'):
                    lines.extend([
                        "**Functions**:",
                        f"- {', '.join(func['name'] for func in pattern['functions'][:5])}",
                        ""
                    ])
        
        # Add common elements
        if category_data.get('common_elements'):
            lines.extend([
                "## Common Elements",
                ""
            ])
            
            common = category_data['common_elements']
            if common.get('frequent_names'):
                lines.extend([
                    "**Frequent Name Components**:",
                    f"- {', '.join(common['frequent_names'])}",
                    ""
                ])
            
            if common.get('shared_variables'):
                lines.extend([
                    "**Shared Variables**:",
                    f"- {', '.join(common['shared_variables'])}",
                    ""
                ])
        
        # Add recommendations
        if category_data.get('recommendations'):
            lines.extend([
                "## Recommendations",
                ""
            ])
            
            for rec in category_data['recommendations']:
                lines.append(f"- {rec}")
        
        return "\n".join(lines)
    
    def generate_pattern_library_readme(self, pattern_library: Dict[str, Any]) -> str:
        """Generate README for pattern library"""
        metadata = pattern_library['metadata']
        categories = pattern_library['categories']
        
        lines = [
            "# Pattern Library",
            "",
            f"**Generated**: {metadata['created_at']}",
            f"**Total Patterns**: {metadata['total_patterns']}",
            "",
            "## Overview",
            "",
            "This pattern library contains extracted and curated patterns from the repository,",
            "organized into categories for easy discovery and reuse in the system thinking tool.",
            "",
            "## Categories",
            ""
        ]
        
        for category_name, category_data in categories.items():
            display_name = category_name.replace('_', ' ').title()
            lines.extend([
                f"### {display_name}",
                f"- **Count**: {category_data['count']} patterns",
                f"- **File**: [`{category_name}.md`](./{category_name}.md)",
                ""
            ])
        
        lines.extend([
            "## Usage",
            "",
            "Each category has both JSON data files and markdown documentation.",
            "Use the JSON files for programmatic access and the markdown files for human reference.",
            "",
            "## Integration",
            "",
            "These patterns can be integrated into:",
            "- Development workflows",
            "- Code generation tools", 
            "- Template systems",
            "- Documentation generators",
            "- Agent configurations",
            ""
        ])
        
        return "\n".join(lines)
    
    def execute(self) -> Dict[str, Any]:
        """Main agent execution"""
        self.logger.info(f"🚀 Starting {self.agent_name} execution")
        self.update_state(current_task="Initializing pattern extraction", progress_percent=0)
        
        results = {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "files_scanned": 0,
            "patterns_extracted": 0,
            "categories_created": 0,
            "library_path": ""
        }
        
        try:
            # Step 1: Scan for pattern files
            pattern_files = self.scan_for_patterns()
            results["files_scanned"] = sum(len(files) for files in pattern_files.values())
            
            if results["files_scanned"] == 0:
                self.logger.warning("⚠️  No pattern files found")
                return results
            
            # Step 2: Extract patterns
            extracted_patterns = self.process_pattern_files(pattern_files)
            results["patterns_extracted"] = sum(len(patterns) for patterns in extracted_patterns.values())
            
            # Step 3: Build pattern library
            pattern_library = self.build_pattern_library(extracted_patterns)
            results["categories_created"] = len(pattern_library["categories"])
            
            # Step 4: Generate library files
            self.update_state(current_task="Generating pattern library files", progress_percent=90)
            library_path = self.generate_pattern_library_files(pattern_library)
            results["library_path"] = str(library_path)
            
            # Save detailed results
            results_path = self.state_dir / f"{self.agent_name}_results.json"
            with open(results_path, 'w') as f:
                json.dump({
                    "pattern_files": {k: [str(f) for f in v] for k, v in pattern_files.items()},
                    "extracted_patterns": extracted_patterns,
                    "pattern_library": pattern_library
                }, f, indent=2, default=str)
            
            # Final success update
            results["success"] = True
            self.update_state(
                current_task="Pattern extraction completed",
                progress_percent=100,
                status="completed",
                patterns_found=results["patterns_extracted"],
                files_processed=results["files_scanned"]
            )
            
            self.logger.info(f"✅ {self.agent_name} completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ {self.agent_name} execution failed: {e}")
            results["success"] = False
            results["error"] = str(e)
            self.update_state(
                current_task=f"Execution failed: {e}",
                status="failed"
            )
        
        results["end_time"] = datetime.now().isoformat()
        return results


def main():
    """Main agent execution"""
    agent = PatternExtractorAgent()
    result = agent.execute()
    
    # Print result summary
    print("\n" + "="*60)
    print("🧩 PATTERN EXTRACTOR AGENT RESULTS")
    print("="*60)
    print(f"✅ Success: {result['success']}")
    print(f"📁 Files Scanned: {result['files_scanned']}")
    print(f"🧩 Patterns Extracted: {result['patterns_extracted']}")
    print(f"📂 Categories Created: {result['categories_created']}")
    
    if result.get('library_path'):
        print(f"📚 Pattern Library: {result['library_path']}")
    
    if not result['success'] and 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("="*60)
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit(main())