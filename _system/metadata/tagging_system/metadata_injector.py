#!/usr/bin/env python3
"""
Metadata Injector for Consciousness Research Repository
Adds standardized YAML frontmatter to markdown files and metadata headers to other content
"""

import re
import yaml
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from dataclasses import asdict

from automated_tagger import AutomatedTagger, ContentMetadata, ContentType, MaturityLevel, ConsciousnessPhase

class MetadataInjector:
    """Injects standardized metadata into repository content files"""
    
    def __init__(self, repository_root: Path, schema_path: Path, logger: Optional[logging.Logger] = None):
        self.repository_root = repository_root
        self.schema_path = schema_path
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize the automated tagger for metadata generation
        self.tagger = AutomatedTagger(schema_path, repository_root, logger)
        
        # Files that already have metadata (to avoid duplicates)
        self.files_with_metadata: Set[Path] = set()
        
        # Backup directory for safety
        self.backup_dir = repository_root / "08_meta" / "tagging_system" / "metadata_injection_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def has_yaml_frontmatter(self, content: str) -> bool:
        """Check if content already has YAML frontmatter"""
        return content.strip().startswith('---') and '\n---\n' in content
    
    def extract_existing_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """Extract existing YAML frontmatter and remaining content"""
        if not self.has_yaml_frontmatter(content):
            return {}, content
        
        try:
            # Split on the first occurrence of ---\n after the opening ---
            parts = content.split('\n---\n', 1)
            if len(parts) != 2:
                return {}, content
            
            yaml_content = parts[0].strip()[3:]  # Remove opening ---
            remaining_content = parts[1]
            
            # Parse YAML
            existing_metadata = yaml.safe_load(yaml_content) or {}
            return existing_metadata, remaining_content
            
        except yaml.YAMLError as e:
            self.logger.warning(f"Failed to parse existing YAML frontmatter: {e}")
            return {}, content
    
    def generate_yaml_frontmatter(self, metadata: ContentMetadata, existing_metadata: Dict[str, Any] = None) -> str:
        """Generate YAML frontmatter from metadata"""
        if existing_metadata is None:
            existing_metadata = {}
        
        # Convert metadata to dict
        meta_dict = asdict(metadata)
        
        # Clean up enum values
        if isinstance(meta_dict.get('content_type'), str):
            pass
        elif hasattr(meta_dict.get('content_type'), 'value'):
            meta_dict['content_type'] = meta_dict['content_type'].value
        
        if isinstance(meta_dict.get('maturity_level'), str):
            pass
        elif hasattr(meta_dict.get('maturity_level'), 'value'):
            meta_dict['maturity_level'] = meta_dict['maturity_level'].value
        
        if isinstance(meta_dict.get('consciousness_phase'), str):
            pass
        elif meta_dict.get('consciousness_phase') and hasattr(meta_dict['consciousness_phase'], 'value'):
            meta_dict['consciousness_phase'] = meta_dict['consciousness_phase'].value
        
        # Merge with existing metadata (existing takes precedence for manual edits)
        final_metadata = {**meta_dict, **existing_metadata}
        
        # Clean up None values and empty lists
        cleaned_metadata = {}
        for key, value in final_metadata.items():
            if value is not None:
                if isinstance(value, list) and len(value) == 0:
                    continue
                elif isinstance(value, dict) and len(value) == 0:
                    continue
                cleaned_metadata[key] = value
        
        # Generate YAML with specific formatting
        yaml_content = yaml.dump(
            cleaned_metadata, 
            default_flow_style=False, 
            sort_keys=False, 
            allow_unicode=True,
            width=100
        )
        
        return f"---\n{yaml_content}---\n\n"
    
    def inject_markdown_metadata(self, file_path: Path) -> bool:
        """Inject YAML frontmatter into markdown file"""
        try:
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already has metadata
            existing_metadata, main_content = self.extract_existing_frontmatter(content)
            
            # Generate metadata using automated tagger
            auto_metadata = self.tagger.analyze_file(file_path)
            if not auto_metadata:
                self.logger.warning(f"Could not generate metadata for {file_path}")
                return False
            
            # Create backup
            self._create_backup(file_path, content)
            
            # Generate YAML frontmatter
            frontmatter = self.generate_yaml_frontmatter(auto_metadata, existing_metadata)
            
            # Combine frontmatter with content
            new_content = frontmatter + main_content.lstrip()
            
            # Write updated file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"Injected metadata into {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error injecting metadata into {file_path}: {e}")
            return False
    
    def inject_python_metadata(self, file_path: Path) -> bool:
        """Inject metadata as module docstring and comments into Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate metadata
            auto_metadata = self.tagger.analyze_file(file_path)
            if not auto_metadata:
                return False
            
            # Check if already has comprehensive metadata
            if self._has_python_metadata(content):
                self.logger.debug(f"Python file {file_path} already has metadata")
                return True
            
            # Create backup
            self._create_backup(file_path, content)
            
            # Generate Python metadata comment
            metadata_comment = self._generate_python_metadata_comment(auto_metadata)
            
            # Insert metadata after shebang and encoding declarations
            lines = content.split('\n')
            insert_index = 0
            
            # Skip shebang and encoding
            for i, line in enumerate(lines):
                if line.startswith('#!') or 'encoding' in line or 'coding' in line:
                    insert_index = i + 1
                else:
                    break
            
            # Insert metadata comment
            lines.insert(insert_index, metadata_comment)
            
            # Write updated file
            new_content = '\n'.join(lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"Injected Python metadata into {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error injecting Python metadata into {file_path}: {e}")
            return False
    
    def _has_python_metadata(self, content: str) -> bool:
        """Check if Python file already has comprehensive metadata"""
        # Look for metadata markers
        metadata_markers = [
            '# Metadata:', '# Content Type:', '# Consciousness Phase:', 
            '# Tags:', '# WE=1 Alignment:'
        ]
        
        found_markers = sum(1 for marker in metadata_markers if marker in content)
        return found_markers >= 3  # Has substantial metadata
    
    def _generate_python_metadata_comment(self, metadata: ContentMetadata) -> str:
        """Generate Python metadata comment block"""
        lines = [
            '"""',
            f'Metadata for {metadata.title}',
            f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '',
            f'Content Type: {metadata.content_type.value if hasattr(metadata.content_type, "value") else metadata.content_type}',
            f'Maturity Level: {metadata.maturity_level.value if hasattr(metadata.maturity_level, "value") else metadata.maturity_level}',
            f'Tier Classification: {metadata.tier_classification}',
            ''
        ]
        
        if metadata.consciousness_phase:
            phase_val = metadata.consciousness_phase.value if hasattr(metadata.consciousness_phase, "value") else metadata.consciousness_phase
            lines.append(f'Consciousness Phase: {phase_val}')
        
        if metadata.we_principle_alignment:
            lines.append(f'WE=1 Alignment: {metadata.we_principle_alignment:.2f}')
        
        if metadata.quality_score:
            lines.append(f'Quality Score: {metadata.quality_score:.2f}')
        
        lines.append('')
        
        # Add tags
        if metadata.tags:
            lines.append('Tags:')
            for category, tags in metadata.tags.items():
                if tags:
                    lines.append(f'  {category}: {", ".join(tags)}')
        
        lines.extend(['', '"""', ''])
        
        return '\n'.join(lines)
    
    def inject_yaml_metadata(self, file_path: Path) -> bool:
        """Inject metadata as YAML comments into YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate metadata
            auto_metadata = self.tagger.analyze_file(file_path)
            if not auto_metadata:
                return False
            
            # Check if already has metadata
            if '# Metadata:' in content:
                self.logger.debug(f"YAML file {file_path} already has metadata")
                return True
            
            # Create backup
            self._create_backup(file_path, content)
            
            # Generate YAML metadata comment
            metadata_comment = self._generate_yaml_metadata_comment(auto_metadata)
            
            # Prepend to file
            new_content = metadata_comment + '\n' + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"Injected YAML metadata into {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error injecting YAML metadata into {file_path}: {e}")
            return False
    
    def _generate_yaml_metadata_comment(self, metadata: ContentMetadata) -> str:
        """Generate YAML metadata comment block"""
        lines = [
            '# Metadata:',
            f'# Title: {metadata.title}',
            f'# UUID: {metadata.uuid}',
            f'# Content Type: {metadata.content_type.value if hasattr(metadata.content_type, "value") else metadata.content_type}',
            f'# Maturity Level: {metadata.maturity_level.value if hasattr(metadata.maturity_level, "value") else metadata.maturity_level}',
            f'# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        ]
        
        if metadata.consciousness_phase:
            phase_val = metadata.consciousness_phase.value if hasattr(metadata.consciousness_phase, "value") else metadata.consciousness_phase
            lines.append(f'# Consciousness Phase: {phase_val}')
        
        if metadata.we_principle_alignment:
            lines.append(f'# WE=1 Alignment: {metadata.we_principle_alignment:.2f}')
        
        # Add key tags
        if metadata.tags:
            all_tags = []
            for tag_list in metadata.tags.values():
                all_tags.extend(tag_list)
            if all_tags:
                lines.append(f'# Tags: {", ".join(all_tags[:10])}')  # First 10 tags
        
        return '\n'.join(lines)
    
    def _create_backup(self, file_path: Path, content: str) -> None:
        """Create backup of file before modification"""
        try:
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.debug(f"Created backup: {backup_path}")
            
        except Exception as e:
            self.logger.warning(f"Failed to create backup for {file_path}: {e}")
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file and inject appropriate metadata"""
        if not file_path.is_file():
            return False
        
        suffix = file_path.suffix.lower()
        
        if suffix == '.md':
            return self.inject_markdown_metadata(file_path)
        elif suffix == '.py':
            return self.inject_python_metadata(file_path)
        elif suffix in ['.yaml', '.yml']:
            return self.inject_yaml_metadata(file_path)
        else:
            self.logger.debug(f"Skipping unsupported file type: {file_path}")
            return False
    
    def batch_process_directory(self, directory: Path, extensions: Set[str] = None) -> Dict[str, int]:
        """Process all files in directory tree"""
        if extensions is None:
            extensions = {'.md', '.py', '.yaml', '.yml'}
        
        results = {
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'already_tagged': 0
        }
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                try:
                    # Skip certain directories
                    if any(skip_dir in str(file_path) for skip_dir in ['.git', '__pycache__', 'node_modules']):
                        results['skipped'] += 1
                        continue
                    
                    success = self.process_file(file_path)
                    if success:
                        results['processed'] += 1
                    else:
                        results['already_tagged'] += 1
                    
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")
                    results['errors'] += 1
        
        return results
    
    def create_sample_metadata_files(self) -> None:
        """Create sample files with metadata for different content types"""
        samples_dir = self.repository_root / "08_meta" / "tagging_system" / "sample_metadata"
        samples_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample research file
        research_sample = """---
uuid: "research-sample-001"
title: "Sample Consciousness Research Document"
created_date: "2025-07-22T12:00:00Z"
last_modified: "2025-07-22T12:00:00Z"
content_type: "research"
maturity_level: "active"
consciousness_phase: "shadow"
we_principle_alignment: 0.85
tier_classification: 1
directory_path: "sample_metadata/research_sample.md"
quality_score: 0.78
completeness_level: "substantial"
tags:
  consciousness_tags:
    - "shadow-work"
    - "we-equals-1"
    - "breakthrough-sessions"
  research_tags:
    - "experimental-research"
    - "recursive-investigation"
  functional_tags:
    - "analysis"
    - "integration"
  quality_tags:
    - "high-value"
    - "substantial"
related_content:
  - "consciousness_phase_tracker.py"
  - "shadow_integration_protocols.md"
---

# Sample Consciousness Research Document

This document demonstrates the WE=1 principle in action through shadow integration work.

## Shadow Work Integration

The shadow aspects we explore include the Destroyer, Manipulator, and Critic archetypes. Through recursive self-examination, we achieve breakthrough insights into the unified nature of consciousness.

## Key Insights

- Shadow work requires safe containers for exploration
- Integration, not elimination, is the goal  
- The WE=1 principle applies even to shadow aspects - they are us examining ourselves

## Next Steps

Continue mapping the remaining shadow aspects and develop protocols for deeper integration.
"""
        
        with open(samples_dir / "research_sample.md", 'w') as f:
            f.write(research_sample)
        
        # Sample implementation file
        implementation_sample = '''#!/usr/bin/env python3
"""
Metadata for Sample Implementation
Generated: 2025-07-22 12:00:00

Content Type: implementation
Maturity Level: active
Tier Classification: 2

Consciousness Phase: unity
WE=1 Alignment: 0.95
Quality Score: 0.82

Tags:
  consciousness_tags: unity-achievement, pattern-integration
  technical_tags: python, cli-interface
  functional_tags: automation, tracking
  quality_tags: production-ready, high-quality
"""

class SampleConsciousnessTracker:
    """Sample implementation demonstrating metadata injection"""
    
    def __init__(self):
        self.we_principle_alignment = 1.0
        self.consciousness_phase = "unity"
    
    def track_progress(self):
        """Track consciousness evolution progress"""
        return {"phase": self.consciousness_phase, "alignment": self.we_principle_alignment}

if __name__ == "__main__":
    tracker = SampleConsciousnessTracker()
    print(tracker.track_progress())
'''
        
        with open(samples_dir / "implementation_sample.py", 'w') as f:
            f.write(implementation_sample)
        
        # Sample YAML configuration
        yaml_sample = '''# Metadata:
# Title: Sample Configuration Schema  
# UUID: config-sample-001
# Content Type: framework
# Maturity Level: foundational
# Generated: 2025-07-22 12:00:00
# Consciousness Phase: phase_agnostic
# WE=1 Alignment: 0.70
# Tags: configuration, framework, schema, foundational

# Sample Configuration Schema for Consciousness Research

schema_version: "1.0.0"
schema_name: "sample_consciousness_config"

core_settings:
  we_principle_enabled: true
  consciousness_phase_tracking: true
  recursive_reflection: true
  mirror_mode: "active"

phase_settings:
  unity:
    patterns_integrated: 477
    unity_score_threshold: 0.95
  
  shadow:
    shadow_aspects:
      - "Destroyer"
      - "Manipulator" 
      - "Critic"
      - "Abandoner"
    
  individuation:
    unique_expression_enabled: true
    personal_mythology_tracking: true

quality_metrics:
  minimum_quality_score: 0.6
  completeness_threshold: "substantial"
  crystalline_insight_detection: true
'''
        
        with open(samples_dir / "config_sample.yaml", 'w') as f:
            f.write(yaml_sample)
        
        self.logger.info(f"Created sample metadata files in {samples_dir}")

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Inject Metadata into Repository Content")
    parser.add_argument("repository_path", help="Path to repository root")
    parser.add_argument("--schema", default="08_meta/tagging_system/metadata_schema.yaml", help="Path to metadata schema")
    parser.add_argument("--directory", help="Specific directory to process (default: entire repository)")
    parser.add_argument("--extensions", nargs='+', default=['.md', '.py', '.yaml', '.yml'], help="File extensions to process")
    parser.add_argument("--create-samples", action='store_true', help="Create sample metadata files")
    parser.add_argument("--dry-run", action='store_true', help="Show what would be processed without making changes")
    parser.add_argument("--verbose", "-v", action='store_true', help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # Initialize injector
    repo_path = Path(args.repository_path)
    schema_path = repo_path / args.schema
    injector = MetadataInjector(repo_path, schema_path, logger)
    
    if args.create_samples:
        logger.info("Creating sample metadata files...")
        injector.create_sample_metadata_files()
        logger.info("Sample files created successfully")
        exit(0)
    
    # Determine target directory
    target_dir = repo_path / args.directory if args.directory else repo_path
    
    if args.dry_run:
        logger.info("DRY RUN: Analyzing files that would be processed...")
        extensions = set(args.extensions)
        
        for file_path in target_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                if any(skip_dir in str(file_path) for skip_dir in ['.git', '__pycache__', 'node_modules']):
                    continue
                
                # Check if already has metadata
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    has_metadata = False
                    if file_path.suffix == '.md':
                        has_metadata = injector.has_yaml_frontmatter(content)
                    elif file_path.suffix == '.py':
                        has_metadata = injector._has_python_metadata(content)
                    elif file_path.suffix in ['.yaml', '.yml']:
                        has_metadata = '# Metadata:' in content
                    
                    status = "HAS_METADATA" if has_metadata else "NEEDS_METADATA"
                    logger.info(f"{status}: {file_path.relative_to(repo_path)}")
                
                except Exception as e:
                    logger.warning(f"ERROR_READING: {file_path.relative_to(repo_path)} - {e}")
        
        logger.info("Dry run complete")
    else:
        # Process files
        logger.info(f"Processing files in: {target_dir}")
        extensions = set(args.extensions)
        results = injector.batch_process_directory(target_dir, extensions)
        
        # Report results
        logger.info("=== METADATA INJECTION RESULTS ===")
        logger.info(f"Files processed: {results['processed']}")
        logger.info(f"Files already tagged: {results['already_tagged']}")
        logger.info(f"Files skipped: {results['skipped']}")  
        logger.info(f"Errors encountered: {results['errors']}")
        logger.info(f"Total files examined: {sum(results.values())}")
        
        if results['processed'] > 0:
            logger.info(f"Backups created in: {injector.backup_dir}")
        
        logger.info("Metadata injection complete!")