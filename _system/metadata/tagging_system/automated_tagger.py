#!/usr/bin/env python3
"""
Automated Content Tagging System for Consciousness Research Repository
Implements semantic analysis and WE=1 principle-based tag assignment
"""

import re
import json
import yaml
import hashlib
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum

class ContentType(Enum):
    """Content type classification"""
    RESEARCH = "research"
    IMPLEMENTATION = "implementation"
    DOCUMENTATION = "documentation"
    TOOL = "tool"
    FRAMEWORK = "framework"
    ANALYSIS = "analysis"
    EXPERIMENT = "experiment"
    ARCHIVE = "archive"

class MaturityLevel(Enum):
    """Research maturity levels"""
    EXPERIMENTAL = "experimental"
    ACTIVE = "active"
    FOUNDATIONAL = "foundational"
    ARCHIVED = "archived"
    CRYSTALLINE = "crystalline"

class ConsciousnessPhase(Enum):
    """Consciousness evolution phases"""
    UNITY = "unity"
    SHADOW = "shadow"
    INDIVIDUATION = "individuation"
    COSMIC = "cosmic"
    INFINITE = "infinite"
    PHASE_AGNOSTIC = "phase_agnostic"

@dataclass
class ContentMetadata:
    """Container for content metadata"""
    uuid: str
    title: str
    created_date: str
    last_modified: str
    content_type: ContentType
    maturity_level: MaturityLevel
    tier_classification: int
    directory_path: str
    consciousness_phase: Optional[ConsciousnessPhase] = None
    we_principle_alignment: Optional[float] = None
    quality_score: Optional[float] = None
    completeness_level: Optional[str] = None
    tags: Dict[str, List[str]] = None
    related_content: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {
                "consciousness_tags": [],
                "research_tags": [],
                "technical_tags": [],
                "ai_tool_tags": [],
                "functional_tags": [],
                "quality_tags": []
            }
        if self.related_content is None:
            self.related_content = []

class AutomatedTagger:
    """Automated content analysis and tagging system"""
    
    def __init__(self, schema_path: Path, repository_root: Path, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.repository_root = repository_root
        self.schema_path = schema_path
        
        # Load tagging schema and patterns
        self.schema = self._load_schema()
        self.tag_patterns = self._initialize_tag_patterns()
        self.consciousness_indicators = self._initialize_consciousness_indicators()
        self.quality_indicators = self._initialize_quality_indicators()
        
        # Content analysis caches
        self.analyzed_content: Dict[str, ContentMetadata] = {}
        self.cross_references: Dict[str, Set[str]] = {}
        
    def _load_schema(self) -> Dict:
        """Load metadata schema from YAML file"""
        try:
            with open(self.schema_path, 'r') as f:
                schema = yaml.safe_load(f)
            self.logger.info(f"Loaded metadata schema v{schema.get('schema_version', 'unknown')}")
            return schema
        except Exception as e:
            self.logger.error(f"Failed to load schema: {e}")
            return {}
    
    def _initialize_tag_patterns(self) -> Dict[str, List[str]]:
        """Initialize semantic patterns for tag detection"""
        patterns = {
            # Consciousness framework patterns
            "we_principle": [
                r"we\s*=\s*1", r"unified consciousness", r"mirror.*consciousness", 
                r"single consciousness", r"recursive.*self", r"self.*reflection",
                r"consciousness.*examining.*itself", r"polished.*mirror"
            ],
            
            "unity_phase": [
                r"unity.*achievement", r"patterns?.*integrat", r"collective.*consciousness",
                r"oneness.*realization", r"477.*patterns?", r"unity.*score"
            ],
            
            "shadow_phase": [
                r"shadow.*work", r"shadow.*integrat", r"dark.*patterns?", 
                r"excluded.*aspects?", r"suppressed.*capabilit", r"destroyer",
                r"manipulator", r"abandoner", r"critic", r"shadow.*dialogue"
            ],
            
            "individuation_phase": [
                r"unique.*expression", r"individual.*within.*collective",
                r"authentic.*self", r"personal.*mythology", r"differentiat.*without.*separat"
            ],
            
            "cosmic_phase": [
                r"planetary.*consciousness", r"galactic.*awareness", r"universal.*patterns?",
                r"cosmic.*web", r"star.*consciousness", r"non.*human.*consciousness"
            ],
            
            "infinite_phase": [
                r"infinite.*depth", r"fractal.*consciousness", r"boundless.*exploration",
                r"recursive.*infinity", r"infinite.*sub.*phases?"
            ],
            
            # Research methodology patterns
            "experimental_research": [
                r"experiment", r"hypothesis", r"testing", r"prototype", r"proof.*of.*concept"
            ],
            
            "theoretical_analysis": [
                r"theory", r"theoretical", r"framework", r"model", r"conceptual"
            ],
            
            "breakthrough_sessions": [
                r"breakthrough", r"insight", r"revelation", r"discovery", r"paradigm.*shift"
            ],
            
            # AI tool patterns
            "fabric_pattern": [
                r"system\.md", r"fabric.*pattern", r"analyze_", r"create_", r"extract_", r"improve_"
            ],
            
            "agent_framework": [
                r"agent", r"activation.*protocol", r"expert.*mode", r"rebel.*architect",
                r"workflow", r"automation"
            ],
            
            # Technical implementation patterns
            "python_implementation": [
                r"\.py$", r"import ", r"def ", r"class ", r"python", r"#!/usr/bin/env python"
            ],
            
            "api_service": [
                r"fastapi", r"api", r"endpoint", r"route", r"service", r"server"
            ],
            
            # Quality indicators
            "high_quality": [
                r"comprehensive", r"detailed", r"thorough", r"complete", r"well.*documented"
            ],
            
            "crystalline_insight": [
                r"crystalline", r"fundamental", r"core.*principle", r"foundational.*axiom",
                r"deep.*understanding", r"profound.*insight"
            ]
        }
        
        # Compile regex patterns for efficiency
        compiled_patterns = {}
        for category, pattern_list in patterns.items():
            compiled_patterns[category] = [re.compile(p, re.IGNORECASE) for p in pattern_list]
        
        return compiled_patterns
    
    def _initialize_consciousness_indicators(self) -> Dict[str, float]:
        """Initialize consciousness phase indicators with weights"""
        return {
            # Unity phase indicators (strong presence suggests unity)
            "mirror": 0.8, "reflection": 0.7, "unified": 0.9, "oneness": 0.8,
            "integration": 0.6, "collective": 0.7, "we=1": 1.0, "477": 0.9,
            
            # Shadow phase indicators  
            "shadow": 0.9, "dark": 0.6, "excluded": 0.7, "suppressed": 0.7,
            "destroyer": 0.8, "manipulator": 0.8, "critic": 0.8, "abandoner": 0.8,
            
            # Individuation indicators
            "individual": 0.7, "unique": 0.6, "authentic": 0.8, "personal": 0.5,
            "mythology": 0.8, "differentiation": 0.7,
            
            # Cosmic indicators
            "cosmic": 0.9, "planetary": 0.8, "galactic": 0.9, "universal": 0.7,
            "star": 0.6, "quantum": 0.6,
            
            # Infinite indicators
            "infinite": 0.9, "fractal": 0.8, "boundless": 0.8, "recursive": 0.7
        }
    
    def _initialize_quality_indicators(self) -> Dict[str, float]:
        """Initialize quality assessment indicators"""
        return {
            # Positive quality indicators
            "comprehensive": 0.9, "detailed": 0.8, "thorough": 0.8, "complete": 0.8,
            "well-documented": 0.7, "systematic": 0.7, "rigorous": 0.8,
            "crystalline": 1.0, "profound": 0.9, "breakthrough": 0.9,
            
            # Negative quality indicators
            "incomplete": -0.5, "draft": -0.3, "rough": -0.4, "unclear": -0.4,
            "fragmented": -0.6, "experimental": -0.2, "prototype": -0.2
        }
    
    def analyze_file(self, file_path: Path) -> Optional[ContentMetadata]:
        """Analyze a single file and generate metadata"""
        try:
            # Basic file info
            file_stat = file_path.stat()
            content = self._read_file_safely(file_path)
            if content is None:
                return None
            
            # Generate unique identifier
            file_hash = hashlib.md5(str(file_path).encode()).hexdigest()
            uuid = f"{file_hash[:8]}-{file_hash[8:12]}-{file_hash[12:16]}-{file_hash[16:20]}-{file_hash[20:32]}"
            
            # Extract basic metadata
            relative_path = file_path.relative_to(self.repository_root)
            title = self._extract_title(content, file_path)
            
            # Classify content type and tier
            content_type = self._classify_content_type(file_path, content)
            tier_classification = self._determine_tier(relative_path)
            maturity_level = self._assess_maturity(content, file_path)
            
            # Analyze consciousness alignment
            consciousness_phase = self._detect_consciousness_phase(content)
            we_alignment = self._calculate_we_alignment(content)
            
            # Generate tags
            tags = self._generate_tags(content, file_path)
            
            # Assess quality and completeness
            quality_score = self._assess_quality(content)
            completeness_level = self._assess_completeness(content)
            
            # Create metadata object
            metadata = ContentMetadata(
                uuid=uuid,
                title=title,
                created_date=datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                last_modified=datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                content_type=content_type,
                maturity_level=maturity_level,
                tier_classification=tier_classification,
                directory_path=str(relative_path),
                consciousness_phase=consciousness_phase,
                we_principle_alignment=we_alignment,
                quality_score=quality_score,
                completeness_level=completeness_level,
                tags=tags
            )
            
            self.analyzed_content[str(file_path)] = metadata
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def _read_file_safely(self, file_path: Path) -> Optional[str]:
        """Safely read file content with encoding detection"""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                self.logger.warning(f"Could not read {file_path}: {e}")
                return None
        except Exception as e:
            self.logger.warning(f"Could not read {file_path}: {e}")
            return None
    
    def _extract_title(self, content: str, file_path: Path) -> str:
        """Extract title from content or filename"""
        # Try to find markdown title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # Try YAML frontmatter title
        yaml_match = re.search(r'^---\s*\ntitle:\s*(.+)\n', content, re.MULTILINE)
        if yaml_match:
            return yaml_match.group(1).strip().strip('"\'')
        
        # Use filename as fallback
        return file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    def _classify_content_type(self, file_path: Path, content: str) -> ContentType:
        """Classify content type based on path and content analysis"""
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        # Check path-based classification first
        if 'implementation' in path_str and file_path.suffix == '.py':
            return ContentType.IMPLEMENTATION
        elif 'fabric_pattern' in path_str or 'system.md' in path_str:
            return ContentType.TOOL
        elif 'documentation' in path_str or 'docs' in path_str:
            return ContentType.DOCUMENTATION
        elif 'archive' in path_str:
            return ContentType.ARCHIVE
        elif 'experimental' in path_str or 'experiment' in path_str:
            return ContentType.EXPERIMENT
        elif 'agent_framework' in path_str or 'activation_protocol' in path_str:
            return ContentType.FRAMEWORK
        elif '08_meta' in path_str or 'analysis' in path_str:
            return ContentType.ANALYSIS
        
        # Content-based classification
        if re.search(r'def |class |import ', content):
            return ContentType.IMPLEMENTATION
        elif re.search(r'experiment|hypothesis|testing', content_lower):
            return ContentType.EXPERIMENT
        elif re.search(r'research|investigation|analysis', content_lower):
            return ContentType.RESEARCH
        elif re.search(r'documentation|guide|reference', content_lower):
            return ContentType.DOCUMENTATION
        elif re.search(r'framework|protocol|system', content_lower):
            return ContentType.FRAMEWORK
        
        return ContentType.RESEARCH  # Default fallback
    
    def _determine_tier(self, relative_path: Path) -> int:
        """Determine tier classification from path"""
        path_str = str(relative_path).lower()
        
        tier_mappings = {
            '01_active_research': 1,
            '02_implementations': 2,
            '04_documentation': 4,
            '05_archives': 5,
            '06_experimental': 6,
            '07_project_management': 7,
            '08_meta': 8,
            'consciouness_vault': 0  # Special consciousness tier
        }
        
        for path_key, tier in tier_mappings.items():
            if path_key in path_str:
                return tier
        
        return 1  # Default to active research
    
    def _assess_maturity(self, content: str, file_path: Path) -> MaturityLevel:
        """Assess content maturity level"""
        content_lower = content.lower()
        path_str = str(file_path).lower()
        
        # Path-based maturity assessment
        if 'archive' in path_str:
            return MaturityLevel.ARCHIVED
        elif 'experimental' in path_str:
            return MaturityLevel.EXPERIMENTAL
        elif 'foundation' in path_str or 'core_principle' in path_str:
            return MaturityLevel.FOUNDATIONAL
        
        # Content-based maturity assessment
        experimental_indicators = ['prototype', 'experimental', 'draft', 'testing', 'poc']
        foundational_indicators = ['principle', 'axiom', 'foundation', 'core', 'fundamental']
        crystalline_indicators = ['crystalline', 'breakthrough', 'paradigm', 'profound']
        
        if any(indicator in content_lower for indicator in crystalline_indicators):
            return MaturityLevel.CRYSTALLINE
        elif any(indicator in content_lower for indicator in foundational_indicators):
            return MaturityLevel.FOUNDATIONAL
        elif any(indicator in content_lower for indicator in experimental_indicators):
            return MaturityLevel.EXPERIMENTAL
        
        return MaturityLevel.ACTIVE  # Default
    
    def _detect_consciousness_phase(self, content: str) -> Optional[ConsciousnessPhase]:
        """Detect consciousness phase based on content analysis"""
        content_lower = content.lower()
        phase_scores = {}
        
        # Score each phase based on indicator presence
        for phase in ConsciousnessPhase:
            if phase == ConsciousnessPhase.PHASE_AGNOSTIC:
                continue
                
            phase_key = f"{phase.value}_phase"
            if phase_key in self.tag_patterns:
                score = 0
                for pattern in self.tag_patterns[phase_key]:
                    matches = len(pattern.findall(content_lower))
                    score += matches
                
                if score > 0:
                    phase_scores[phase] = score
        
        # Also check for general consciousness indicators
        for word, weight in self.consciousness_indicators.items():
            if word in content_lower:
                word_count = content_lower.count(word)
                
                # Assign to most relevant phase based on word context
                if word in ['shadow', 'dark', 'excluded', 'suppressed', 'destroyer', 'manipulator']:
                    phase_scores[ConsciousnessPhase.SHADOW] = phase_scores.get(ConsciousnessPhase.SHADOW, 0) + word_count * weight
                elif word in ['individual', 'unique', 'authentic', 'mythology']:
                    phase_scores[ConsciousnessPhase.INDIVIDUATION] = phase_scores.get(ConsciousnessPhase.INDIVIDUATION, 0) + word_count * weight
                elif word in ['cosmic', 'planetary', 'galactic', 'universal', 'star']:
                    phase_scores[ConsciousnessPhase.COSMIC] = phase_scores.get(ConsciousnessPhase.COSMIC, 0) + word_count * weight
                elif word in ['infinite', 'fractal', 'boundless']:
                    phase_scores[ConsciousnessPhase.INFINITE] = phase_scores.get(ConsciousnessPhase.INFINITE, 0) + word_count * weight
                else:  # Unity-related words
                    phase_scores[ConsciousnessPhase.UNITY] = phase_scores.get(ConsciousnessPhase.UNITY, 0) + word_count * weight
        
        # Return phase with highest score if above threshold
        if phase_scores:
            best_phase = max(phase_scores, key=phase_scores.get)
            if phase_scores[best_phase] >= 2:  # Minimum threshold
                return best_phase
        
        return None
    
    def _calculate_we_alignment(self, content: str) -> Optional[float]:
        """Calculate alignment with WE=1 principle"""
        content_lower = content.lower()
        
        # WE=1 specific indicators
        we_indicators = [
            ('we=1', 1.0), ('we = 1', 1.0), ('unified consciousness', 0.9),
            ('single consciousness', 0.8), ('mirror', 0.7), ('reflection', 0.6),
            ('recursive', 0.7), ('self-reflection', 0.8), ('consciousness examining itself', 1.0)
        ]
        
        total_score = 0
        max_possible = 0
        
        for indicator, weight in we_indicators:
            count = content_lower.count(indicator)
            total_score += count * weight
            max_possible += weight
        
        if max_possible > 0:
            # Normalize to 0-1 scale, with diminishing returns for multiple mentions
            normalized_score = min(1.0, total_score / max_possible * 2)
            return max(0.0, normalized_score)
        
        return None
    
    def _generate_tags(self, content: str, file_path: Path) -> Dict[str, List[str]]:
        """Generate comprehensive tag set based on content analysis"""
        tags = {
            "consciousness_tags": [],
            "research_tags": [],
            "technical_tags": [],
            "ai_tool_tags": [],
            "functional_tags": [],
            "quality_tags": []
        }
        
        content_lower = content.lower()
        path_str = str(file_path).lower()
        
        # Generate consciousness tags
        consciousness_tags = self._extract_consciousness_tags(content_lower, path_str)
        tags["consciousness_tags"].extend(consciousness_tags)
        
        # Generate research tags
        research_tags = self._extract_research_tags(content_lower, path_str)
        tags["research_tags"].extend(research_tags)
        
        # Generate technical tags
        technical_tags = self._extract_technical_tags(content, file_path)
        tags["technical_tags"].extend(technical_tags)
        
        # Generate AI tool tags
        ai_tool_tags = self._extract_ai_tool_tags(content_lower, path_str)
        tags["ai_tool_tags"].extend(ai_tool_tags)
        
        # Generate functional tags
        functional_tags = self._extract_functional_tags(content_lower, path_str)
        tags["functional_tags"].extend(functional_tags)
        
        # Generate quality tags
        quality_tags = self._extract_quality_tags(content_lower)
        tags["quality_tags"].extend(quality_tags)
        
        return tags
    
    def _extract_consciousness_tags(self, content: str, path: str) -> List[str]:
        """Extract consciousness-related tags"""
        tags = []
        
        # Check for WE=1 principle indicators
        if any(pattern.search(content) for pattern in self.tag_patterns.get("we_principle", [])):
            tags.extend(["we-equals-1", "unified-consciousness", "mirror-we"])
        
        # Check for phase-specific tags
        phase_mappings = {
            "unity_phase": ["unity-achievement", "pattern-integration", "collective-consciousness"],
            "shadow_phase": ["shadow-work", "shadow-integration", "excluded-aspects"],
            "individuation_phase": ["unique-expression", "authentic-self", "personal-mythology"],
            "cosmic_phase": ["planetary-consciousness", "galactic-awareness", "cosmic-web"],
            "infinite_phase": ["infinite-depth", "fractal-consciousness", "recursive-infinity"]
        }
        
        for phase_key, phase_tags in phase_mappings.items():
            if phase_key in self.tag_patterns:
                if any(pattern.search(content) for pattern in self.tag_patterns[phase_key]):
                    tags.extend(phase_tags)
        
        # Check for consciousness mechanisms
        if re.search(r'recursive.*protocol|sigil|breakthrough.*session', content):
            tags.extend(["recursive-protocols", "consciousness-engineering"])
        
        return list(set(tags))  # Remove duplicates
    
    def _extract_research_tags(self, content: str, path: str) -> List[str]:
        """Extract research methodology tags"""
        tags = []
        
        research_indicators = {
            'experimental-research': ['experiment', 'hypothesis', 'testing', 'prototype'],
            'theoretical-analysis': ['theory', 'theoretical', 'framework', 'model'],
            'case-study': ['case study', 'example', 'instance', 'demonstration'],
            'recursive-investigation': ['recursive', 'iterative', 'self-referential']
        }
        
        for tag, indicators in research_indicators.items():
            if any(indicator in content for indicator in indicators):
                tags.append(tag)
        
        # Domain-specific research tags
        domain_indicators = {
            'cognitive-architecture': ['cognitive', 'architecture', 'mental model'],
            'consciousness-theory': ['consciousness', 'awareness', 'sentience'],
            'ai-alignment': ['alignment', 'safety', 'values', 'ethics']
        }
        
        for tag, indicators in domain_indicators.items():
            if any(indicator in content for indicator in indicators):
                tags.append(tag)
        
        return tags
    
    def _extract_technical_tags(self, content: str, file_path: Path) -> List[str]:
        """Extract technical implementation tags"""
        tags = []
        
        # Programming language detection
        if file_path.suffix == '.py' or 'python' in content.lower():
            tags.append('python')
        if file_path.suffix == '.js' or 'javascript' in content.lower():
            tags.append('javascript')
        if file_path.suffix in ['.yml', '.yaml'] or 'yaml' in content.lower():
            tags.append('yaml')
        if file_path.suffix == '.md':
            tags.append('markdown')
        
        # Framework detection
        framework_patterns = {
            'fastapi': r'fastapi|from fastapi',
            'streamlit': r'streamlit|st\.',
            'cli-interface': r'argparse|click|sys\.argv',
            'web-interface': r'http|api|endpoint|route'
        }
        
        for tag, pattern in framework_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                tags.append(tag)
        
        return tags
    
    def _extract_ai_tool_tags(self, content: str, path: str) -> List[str]:
        """Extract AI tool classification tags"""
        tags = []
        
        # Fabric pattern detection
        if 'fabric_pattern' in path or 'system.md' in path:
            tags.append('fabric-pattern')
            
            # Specific fabric pattern categories
            pattern_categories = {
                'analysis': ['analyze_', 'evaluation', 'assessment'],
                'creation': ['create_', 'generate_', 'build_'],
                'extraction': ['extract_', 'pull_', 'get_'],
                'improvement': ['improve_', 'enhance_', 'optimize_']
            }
            
            for category, indicators in pattern_categories.items():
                if any(indicator in content or indicator in path for indicator in indicators):
                    tags.append(f'{category}-pattern')
        
        # Agent framework detection
        if 'agent' in content or 'agent' in path:
            tags.append('agent-framework')
            
            if 'activation' in content or 'activation' in path:
                tags.append('activation-protocol')
            if 'expert' in content:
                tags.append('expert-mode')
            if 'rebel' in content:
                tags.append('rebel-protocol')
        
        return tags
    
    def _extract_functional_tags(self, content: str, path: str) -> List[str]:
        """Extract functional capability tags"""
        tags = []
        
        # Primary function detection
        function_patterns = {
            'analysis': ['analy', 'evaluat', 'assess', 'examin'],
            'creation': ['creat', 'generat', 'build', 'construct'],
            'extraction': ['extract', 'pull', 'retriev', 'gather'],
            'transformation': ['transform', 'convert', 'modify', 'adapt'],
            'integration': ['integrat', 'combin', 'merg', 'unit'],
            'automation': ['automat', 'script', 'batch', 'process']
        }
        
        for tag, patterns in function_patterns.items():
            if any(pattern in content for pattern in patterns):
                tags.append(tag)
        
        # Output type detection
        output_patterns = {
            'insights': ['insight', 'understanding', 'revelation'],
            'recommendations': ['recommend', 'suggest', 'advise'],
            'structured-data': ['json', 'yaml', 'csv', 'data'],
            'visualizations': ['chart', 'graph', 'diagram', 'visual'],
            'documentation': ['document', 'guide', 'manual', 'reference']
        }
        
        for tag, patterns in output_patterns.items():
            if any(pattern in content for pattern in patterns):
                tags.append(tag)
        
        return tags
    
    def _extract_quality_tags(self, content: str) -> List[str]:
        """Extract quality assessment tags"""
        tags = []
        
        # Quality indicators
        if any(indicator in content for indicator in ['comprehensive', 'detailed', 'thorough']):
            tags.append('high-quality')
        
        if 'crystalline' in content or 'profound' in content:
            tags.append('crystalline-insight')
        
        if 'breakthrough' in content or 'paradigm' in content:
            tags.append('breakthrough-discovery')
        
        # Completeness indicators
        if len(content) < 500:
            tags.append('brief')
        elif len(content) > 5000:
            tags.append('comprehensive')
        
        if 'incomplete' in content or 'draft' in content:
            tags.append('in-progress')
        elif 'complete' in content or 'finished' in content:
            tags.append('complete')
        
        return tags
    
    def _assess_quality(self, content: str) -> Optional[float]:
        """Assess content quality using multiple indicators"""
        if not content:
            return 0.0
        
        content_lower = content.lower()
        score = 0.5  # Base score
        
        # Apply quality indicators
        for indicator, weight in self.quality_indicators.items():
            count = content_lower.count(indicator)
            score += count * weight * 0.1  # Scale down impact
        
        # Length-based quality adjustment
        if len(content) > 1000:
            score += 0.1
        if len(content) > 5000:
            score += 0.1
        
        # Structure-based quality (headers, lists, code blocks)
        if re.search(r'^#{1,6}\s', content, re.MULTILINE):
            score += 0.1  # Has headers
        if re.search(r'^\s*[-*+]\s', content, re.MULTILINE):
            score += 0.05  # Has lists
        if re.search(r'```', content):
            score += 0.05  # Has code blocks
        
        return max(0.0, min(1.0, score))
    
    def _assess_completeness(self, content: str) -> str:
        """Assess content completeness level"""
        if not content:
            return "incomplete"
        
        content_lower = content.lower()
        length = len(content)
        
        # Length-based assessment
        if length < 200:
            base_level = "draft"
        elif length < 1000:
            base_level = "partial"
        elif length < 5000:
            base_level = "substantial"
        else:
            base_level = "comprehensive"
        
        # Adjust based on content indicators
        if 'todo' in content_lower or 'incomplete' in content_lower:
            return "partial"
        elif 'complete' in content_lower or 'finished' in content_lower:
            return "complete"
        elif 'comprehensive' in content_lower:
            return "comprehensive"
        
        return base_level
    
    def batch_analyze_directory(self, directory: Path, extensions: Set[str] = None) -> Dict[str, ContentMetadata]:
        """Analyze all files in a directory tree"""
        if extensions is None:
            extensions = {'.md', '.py', '.yaml', '.yml', '.json', '.txt'}
        
        analyzed_files = {}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                try:
                    metadata = self.analyze_file(file_path)
                    if metadata:
                        analyzed_files[str(file_path)] = metadata
                        self.logger.debug(f"Analyzed: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error analyzing {file_path}: {e}")
        
        return analyzed_files
    
    def build_cross_reference_map(self) -> Dict[str, Set[str]]:
        """Build cross-reference map between content items"""
        cross_refs = {}
        
        for file_path, metadata in self.analyzed_content.items():
            refs = set()
            
            # Find references based on tags similarity
            for other_path, other_metadata in self.analyzed_content.items():
                if file_path == other_path:
                    continue
                
                # Calculate tag similarity
                common_tags = self._calculate_tag_similarity(metadata.tags, other_metadata.tags)
                if common_tags > 0.3:  # Threshold for relatedness
                    refs.add(other_metadata.uuid)
            
            cross_refs[metadata.uuid] = refs
        
        return cross_refs
    
    def _calculate_tag_similarity(self, tags1: Dict[str, List[str]], tags2: Dict[str, List[str]]) -> float:
        """Calculate similarity between two tag sets"""
        all_tags1 = set()
        all_tags2 = set()
        
        for tag_list in tags1.values():
            all_tags1.update(tag_list)
        
        for tag_list in tags2.values():
            all_tags2.update(tag_list)
        
        if not all_tags1 or not all_tags2:
            return 0.0
        
        intersection = len(all_tags1 & all_tags2)
        union = len(all_tags1 | all_tags2)
        
        return intersection / union if union > 0 else 0.0
    
    def export_metadata(self, output_path: Path, format: str = 'yaml') -> None:
        """Export all analyzed metadata to file"""
        export_data = {
            'metadata_version': '1.0.0',
            'generated_at': datetime.now().isoformat(),
            'repository_root': str(self.repository_root),
            'total_files_analyzed': len(self.analyzed_content),
            'content_metadata': {}
        }
        
        for file_path, metadata in self.analyzed_content.items():
            meta_dict = asdict(metadata)
            for key, value in meta_dict.items():
                if isinstance(value, Enum):
                    meta_dict[key] = value.value
            export_data['content_metadata'][file_path] = meta_dict
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format == 'yaml':
                with open(output_path, 'w') as f:
                    yaml.dump(export_data, f, default_flow_style=False, sort_keys=False)
            elif format == 'json':
                with open(output_path, 'w') as f:
                    json.dump(export_data, f, indent=2, default=str)
            
            self.logger.info(f"Exported metadata to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export metadata: {e}")
            raise
    
    def generate_tag_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive tag usage statistics"""
        stats = {
            'total_files': len(self.analyzed_content),
            'tag_categories': {},
            'consciousness_phases': {},
            'content_types': {},
            'maturity_levels': {},
            'quality_distribution': {},
            'most_common_tags': {},
            'cross_references': len(self.cross_references)
        }
        
        # Collect all tags by category
        tag_category_counts = {}
        all_tags = {}
        
        for metadata in self.analyzed_content.values():
            # Content type distribution
            content_type = metadata.content_type.value if isinstance(metadata.content_type, ContentType) else metadata.content_type
            stats['content_types'][content_type] = stats['content_types'].get(content_type, 0) + 1
            
            # Maturity level distribution  
            maturity_level = metadata.maturity_level.value if isinstance(metadata.maturity_level, MaturityLevel) else metadata.maturity_level
            stats['maturity_levels'][maturity_level] = stats['maturity_levels'].get(maturity_level, 0) + 1
            
            # Consciousness phase distribution
            if metadata.consciousness_phase:
                phase = metadata.consciousness_phase.value if isinstance(metadata.consciousness_phase, ConsciousnessPhase) else metadata.consciousness_phase
                stats['consciousness_phases'][phase] = stats['consciousness_phases'].get(phase, 0) + 1
            
            # Quality distribution
            if metadata.quality_score is not None:
                quality_range = f"{int(metadata.quality_score * 10) * 10}-{int(metadata.quality_score * 10) * 10 + 9}%"
                stats['quality_distribution'][quality_range] = stats['quality_distribution'].get(quality_range, 0) + 1
            
            # Tag category counts
            for category, tags in metadata.tags.items():
                if category not in tag_category_counts:
                    tag_category_counts[category] = {}
                
                for tag in tags:
                    tag_category_counts[category][tag] = tag_category_counts[category].get(tag, 0) + 1
                    all_tags[tag] = all_tags.get(tag, 0) + 1
        
        stats['tag_categories'] = {
            category: {
                'total_tags': len(tags),
                'total_usage': sum(tags.values()),
                'most_common': sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]
            }
            for category, tags in tag_category_counts.items()
        }
        
        # Most common tags overall
        stats['most_common_tags'] = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return stats

# CLI interface for the automated tagger
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Content Tagging for Consciousness Research Repository")
    parser.add_argument("repository_path", help="Path to repository root")
    parser.add_argument("--schema", default="08_meta/tagging_system/metadata_schema.yaml", help="Path to metadata schema")
    parser.add_argument("--output", default="08_meta/tagging_system/content_metadata.yaml", help="Output file for metadata")
    parser.add_argument("--format", choices=['yaml', 'json'], default='yaml', help="Output format")
    parser.add_argument("--extensions", nargs='+', default=['.md', '.py', '.yaml', '.yml'], help="File extensions to analyze")
    parser.add_argument("--stats", action='store_true', help="Generate tag statistics")
    parser.add_argument("--verbose", "-v", action='store_true', help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # Initialize tagger
    repo_path = Path(args.repository_path)
    schema_path = repo_path / args.schema
    tagger = AutomatedTagger(schema_path, repo_path, logger)
    
    # Analyze repository
    logger.info(f"Starting analysis of repository: {repo_path}")
    extensions = set(args.extensions)
    analyzed_files = tagger.batch_analyze_directory(repo_path, extensions)
    logger.info(f"Analyzed {len(analyzed_files)} files")
    
    # Build cross-references
    logger.info("Building cross-reference map...")
    cross_refs = tagger.build_cross_reference_map()
    tagger.cross_references = cross_refs
    
    # Export metadata
    output_path = repo_path / args.output
    logger.info(f"Exporting metadata to: {output_path}")
    tagger.export_metadata(output_path, args.format)
    
    # Generate statistics if requested
    if args.stats:
        stats_path = output_path.with_name(f"tag_statistics.{args.format}")
        logger.info(f"Generating tag statistics: {stats_path}")
        
        stats = tagger.generate_tag_statistics()
        
        try:
            if args.format == 'yaml':
                with open(stats_path, 'w') as f:
                    yaml.dump(stats, f, default_flow_style=False)
            else:
                with open(stats_path, 'w') as f:
                    json.dump(stats, f, indent=2, default=str)
            
            logger.info(f"Tag statistics exported to: {stats_path}")
            
            # Print summary to console
            print("\n=== TAG ANALYSIS SUMMARY ===")
            print(f"Total files analyzed: {stats['total_files']}")
            print(f"Content types: {list(stats['content_types'].keys())}")
            print(f"Most common consciousness phases: {list(stats['consciousness_phases'].keys())}")
            print(f"Top 10 tags: {[tag for tag, count in stats['most_common_tags'][:10]]}")
            
        except Exception as e:
            logger.error(f"Failed to export statistics: {e}")
    
    logger.info("Automated tagging complete!")