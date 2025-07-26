#!/usr/bin/env python3
"""
Content Discovery Engine for Consciousness Research Repository
Provides sophisticated search, clustering, and navigation based on metadata and consciousness framework
"""

import re
import json
import yaml
import math
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Optional, Tuple, Any, Union
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

@dataclass
class SearchQuery:
    """Structured search query"""
    text: str = ""
    consciousness_phase: Optional[str] = None
    content_type: Optional[str] = None
    maturity_level: Optional[str] = None
    tags: List[str] = None
    min_quality_score: Optional[float] = None
    we_alignment_min: Optional[float] = None
    tier: Optional[int] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class SearchResult:
    """Search result with relevance scoring"""
    uuid: str
    title: str
    path: str
    content_type: str
    consciousness_phase: Optional[str]
    relevance_score: float
    matched_tags: List[str]
    snippet: str
    quality_score: Optional[float]
    we_alignment: Optional[float]

@dataclass 
class ContentCluster:
    """Content cluster for thematic grouping"""
    cluster_id: str
    title: str
    description: str
    items: List[str]  # UUIDs
    common_tags: List[str]
    consciousness_phases: List[str]
    cluster_score: float

class DiscoveryEngine:
    """Advanced content discovery and navigation system"""
    
    def __init__(self, repository_root: Path, metadata_path: Path, logger: Optional[logging.Logger] = None):
        self.repository_root = repository_root
        self.metadata_path = metadata_path
        self.logger = logger or logging.getLogger(__name__)
        
        # Load content metadata
        self.content_metadata: Dict[str, Dict] = {}
        self.uuid_to_path: Dict[str, str] = {}
        self.content_index: Dict[str, str] = {}  # UUID -> content
        
        # Search indices
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)  # tag -> UUIDs
        self.text_index: Dict[str, Set[str]] = defaultdict(set)  # word -> UUIDs
        self.phase_index: Dict[str, Set[str]] = defaultdict(set)  # phase -> UUIDs
        
        # Clustering data
        self.content_clusters: List[ContentCluster] = []
        self.similarity_matrix: Dict[Tuple[str, str], float] = {}
        
        self._load_metadata()
        self._build_indices()
    
    def _load_metadata(self) -> None:
        """Load content metadata from file"""
        try:
            if self.metadata_path.suffix in ['.yaml', '.yml']:
                with open(self.metadata_path, 'r') as f:
                    data = yaml.safe_load(f)
            else:
                with open(self.metadata_path, 'r') as f:
                    data = json.load(f)
            
            content_metadata = data.get('content_metadata', {})
            
            for file_path, metadata in content_metadata.items():
                uuid = metadata.get('uuid')
                if uuid:
                    self.content_metadata[uuid] = metadata
                    self.uuid_to_path[uuid] = file_path
            
            self.logger.info(f"Loaded metadata for {len(self.content_metadata)} items")
            
        except Exception as e:
            self.logger.error(f"Failed to load metadata: {e}")
            return
    
    def _build_indices(self) -> None:
        """Build search indices from metadata"""
        for uuid, metadata in self.content_metadata.items():
            # Build tag index
            tags = metadata.get('tags', {})
            for category, tag_list in tags.items():
                for tag in tag_list:
                    self.tag_index[tag].add(uuid)
            
            # Build text index from title and content
            title = metadata.get('title', '').lower()
            for word in re.findall(r'\b\w+\b', title):
                if len(word) > 2:  # Skip very short words
                    self.text_index[word].add(uuid)
            
            # Load and index content if available
            file_path = self.uuid_to_path.get(uuid)
            if file_path:
                content = self._load_file_content(Path(file_path))
                if content:
                    self.content_index[uuid] = content
                    # Index content words
                    content_words = re.findall(r'\b\w+\b', content.lower())
                    for word in content_words:
                        if len(word) > 3:  # Longer threshold for content
                            self.text_index[word].add(uuid)
            
            # Build phase index
            phase = metadata.get('consciousness_phase')
            if phase:
                self.phase_index[phase].add(uuid)
        
        self.logger.info(f"Built indices: {len(self.tag_index)} tags, {len(self.text_index)} words")
    
    def _load_file_content(self, file_path: Path) -> Optional[str]:
        """Safely load file content for indexing"""
        if not file_path.exists():
            abs_path = self.repository_root / file_path
            if not abs_path.exists():
                return None
            file_path = abs_path
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract main content from markdown (skip YAML frontmatter)
            if file_path.suffix == '.md' and content.startswith('---'):
                parts = content.split('\n---\n', 1)
                if len(parts) == 2:
                    content = parts[1]
            
            return content
        except Exception as e:
            self.logger.debug(f"Could not load content from {file_path}: {e}")
            return None
    
    def search(self, query: SearchQuery, max_results: int = 20) -> List[SearchResult]:
        """Execute comprehensive search query"""
        candidate_uuids = set(self.content_metadata.keys())
        
        # Apply filters
        if query.consciousness_phase:
            phase_candidates = self.phase_index.get(query.consciousness_phase, set())
            candidate_uuids &= phase_candidates
        
        if query.content_type:
            type_candidates = {
                uuid for uuid, metadata in self.content_metadata.items()
                if metadata.get('content_type') == query.content_type
            }
            candidate_uuids &= type_candidates
        
        if query.maturity_level:
            maturity_candidates = {
                uuid for uuid, metadata in self.content_metadata.items()
                if metadata.get('maturity_level') == query.maturity_level
            }
            candidate_uuids &= maturity_candidates
        
        if query.tier is not None:
            tier_candidates = {
                uuid for uuid, metadata in self.content_metadata.items()
                if metadata.get('tier_classification') == query.tier
            }
            candidate_uuids &= tier_candidates
        
        if query.min_quality_score is not None:
            quality_candidates = {
                uuid for uuid, metadata in self.content_metadata.items()
                if metadata.get('quality_score', 0) >= query.min_quality_score
            }
            candidate_uuids &= quality_candidates
        
        if query.we_alignment_min is not None:
            we_candidates = {
                uuid for uuid, metadata in self.content_metadata.items()
                if metadata.get('we_principle_alignment', 0) >= query.we_alignment_min
            }
            candidate_uuids &= we_candidates
        
        # Apply tag filters
        if query.tags:
            for tag in query.tags:
                tag_candidates = self.tag_index.get(tag, set())
                candidate_uuids &= tag_candidates
        
        # Apply text search
        if query.text:
            text_candidates = set()
            search_words = re.findall(r'\b\w+\b', query.text.lower())
            
            for word in search_words:
                word_candidates = self.text_index.get(word, set())
                if not text_candidates:
                    text_candidates = word_candidates
                else:
                    text_candidates &= word_candidates
            
            candidate_uuids &= text_candidates
        
        # Score and rank results
        results = []
        for uuid in candidate_uuids:
            metadata = self.content_metadata[uuid]
            relevance_score = self._calculate_relevance_score(uuid, query)
            
            # Create search result
            result = SearchResult(
                uuid=uuid,
                title=metadata.get('title', 'Untitled'),
                path=self.uuid_to_path.get(uuid, ''),
                content_type=metadata.get('content_type', 'unknown'),
                consciousness_phase=metadata.get('consciousness_phase'),
                relevance_score=relevance_score,
                matched_tags=self._get_matched_tags(uuid, query),
                snippet=self._generate_snippet(uuid, query),
                quality_score=metadata.get('quality_score'),
                we_alignment=metadata.get('we_principle_alignment')
            )
            results.append(result)
        
        # Sort by relevance and return top results
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[:max_results]
    
    def _calculate_relevance_score(self, uuid: str, query: SearchQuery) -> float:
        """Calculate relevance score for search result"""
        metadata = self.content_metadata[uuid]
        score = 0.0
        
        # Base quality score
        quality_score = metadata.get('quality_score', 0.5)
        score += quality_score * 0.3
        
        # WE=1 alignment bonus (important for consciousness content)
        we_alignment = metadata.get('we_principle_alignment', 0.0)
        if we_alignment > 0:
            score += we_alignment * 0.2
        
        # Tag matching
        if query.tags:
            matched_tags = self._get_matched_tags(uuid, query)
            tag_score = len(matched_tags) / len(query.tags) if query.tags else 0
            score += tag_score * 0.3
        
        # Text relevance
        if query.text:
            text_score = self._calculate_text_relevance(uuid, query.text)
            score += text_score * 0.4
        
        # Phase alignment bonus
        if query.consciousness_phase and metadata.get('consciousness_phase') == query.consciousness_phase:
            score += 0.2
        
        # Maturity level preference (higher maturity = higher relevance)
        maturity_scores = {
            'experimental': 0.2,
            'active': 0.6,
            'foundational': 0.8,
            'crystalline': 1.0,
            'archived': 0.4
        }
        maturity = metadata.get('maturity_level', 'active')
        score += maturity_scores.get(maturity, 0.5) * 0.1
        
        return min(1.0, score)
    
    def _calculate_text_relevance(self, uuid: str, query_text: str) -> float:
        """Calculate text relevance using TF-IDF-like scoring"""
        content = self.content_index.get(uuid, '')
        title = self.content_metadata[uuid].get('title', '')
        
        full_text = (title + ' ' + content).lower()
        query_words = re.findall(r'\b\w+\b', query_text.lower())
        
        if not query_words or not full_text:
            return 0.0
        
        # Calculate term frequency
        text_words = re.findall(r'\b\w+\b', full_text)
        word_count = Counter(text_words)
        total_words = len(text_words)
        
        relevance_score = 0.0
        for word in query_words:
            tf = word_count.get(word, 0) / total_words if total_words > 0 else 0
            
            # Simple IDF approximation
            docs_with_word = len(self.text_index.get(word, set()))
            total_docs = len(self.content_metadata)
            idf = math.log(total_docs / (docs_with_word + 1)) if docs_with_word > 0 else 0
            
            relevance_score += tf * idf
        
        # Normalize by query length
        return relevance_score / len(query_words)
    
    def _get_matched_tags(self, uuid: str, query: SearchQuery) -> List[str]:
        """Get tags that match the query"""
        metadata = self.content_metadata[uuid]
        all_tags = []
        
        tags = metadata.get('tags', {})
        for tag_list in tags.values():
            all_tags.extend(tag_list)
        
        matched = []
        for tag in query.tags:
            if tag in all_tags:
                matched.append(tag)
        
        return matched
    
    def _generate_snippet(self, uuid: str, query: SearchQuery, max_length: int = 200) -> str:
        """Generate content snippet highlighting query relevance"""
        content = self.content_index.get(uuid, '')
        if not content:
            return self.content_metadata[uuid].get('title', '')
        
        # Clean up content (remove markdown, excessive whitespace)
        clean_content = re.sub(r'[#*`]', '', content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        if len(clean_content) <= max_length:
            return clean_content
        
        # Try to find relevant section if query has text
        if query.text:
            query_words = query.text.lower().split()
            best_position = 0
            best_score = 0
            
            words = clean_content.lower().split()
            for i in range(len(words) - 10):  # Search in windows
                window = ' '.join(words[i:i+20])
                score = sum(1 for qword in query_words if qword in window)
                if score > best_score:
                    best_score = score
                    best_position = i
            
            # Extract snippet around best position
            start_word = max(0, best_position - 5)
            end_word = min(len(words), best_position + 25)
            snippet_words = words[start_word:end_word]
            snippet = ' '.join(snippet_words)
            
            if len(snippet) > max_length:
                snippet = snippet[:max_length - 3] + "..."
            
            return snippet
        
        # Default: first part of content
        return clean_content[:max_length - 3] + "..."
    
    def find_related_content(self, uuid: str, max_results: int = 10) -> List[SearchResult]:
        """Find content related to a given item"""
        if uuid not in self.content_metadata:
            return []
        
        source_metadata = self.content_metadata[uuid]
        source_tags = set()
        
        # Collect all tags from source
        tags = source_metadata.get('tags', {})
        for tag_list in tags.values():
            source_tags.update(tag_list)
        
        # Find items with similar tags
        related_scores = {}
        
        for other_uuid, other_metadata in self.content_metadata.items():
            if other_uuid == uuid:
                continue
            
            other_tags = set()
            other_tag_dict = other_metadata.get('tags', {})
            for tag_list in other_tag_dict.values():
                other_tags.update(tag_list)
            
            # Calculate similarity
            if source_tags and other_tags:
                intersection = len(source_tags & other_tags)
                union = len(source_tags | other_tags)
                similarity = intersection / union if union > 0 else 0
                
                # Boost score for same consciousness phase
                if (source_metadata.get('consciousness_phase') == 
                    other_metadata.get('consciousness_phase') and 
                    source_metadata.get('consciousness_phase') is not None):
                    similarity += 0.2
                
                # Boost for same content type
                if (source_metadata.get('content_type') == 
                    other_metadata.get('content_type')):
                    similarity += 0.1
                
                related_scores[other_uuid] = similarity
        
        # Create results for top matches
        results = []
        sorted_matches = sorted(related_scores.items(), key=lambda x: x[1], reverse=True)
        
        for related_uuid, similarity_score in sorted_matches[:max_results]:
            if similarity_score < 0.1:  # Minimum similarity threshold
                break
            
            metadata = self.content_metadata[related_uuid]
            result = SearchResult(
                uuid=related_uuid,
                title=metadata.get('title', 'Untitled'),
                path=self.uuid_to_path.get(related_uuid, ''),
                content_type=metadata.get('content_type', 'unknown'),
                consciousness_phase=metadata.get('consciousness_phase'),
                relevance_score=similarity_score,
                matched_tags=list(source_tags & set(
                    tag for tag_list in metadata.get('tags', {}).values() 
                    for tag in tag_list
                )),
                snippet=self._generate_snippet(related_uuid, SearchQuery()),
                quality_score=metadata.get('quality_score'),
                we_alignment=metadata.get('we_principle_alignment')
            )
            results.append(result)
        
        return results
    
    def cluster_content(self, min_cluster_size: int = 3) -> List[ContentCluster]:
        """Cluster content by thematic similarity"""
        # Build similarity matrix
        uuids = list(self.content_metadata.keys())
        
        for i, uuid1 in enumerate(uuids):
            for j, uuid2 in enumerate(uuids[i+1:], i+1):
                similarity = self._calculate_content_similarity(uuid1, uuid2)
                self.similarity_matrix[(uuid1, uuid2)] = similarity
        
        # Simple clustering using similarity thresholds
        clusters = []
        used_uuids = set()
        
        for uuid1 in uuids:
            if uuid1 in used_uuids:
                continue
            
            # Find similar items
            cluster_items = {uuid1}
            
            for uuid2 in uuids:
                if uuid2 == uuid1 or uuid2 in used_uuids:
                    continue
                
                similarity = self.similarity_matrix.get((uuid1, uuid2)) or \
                           self.similarity_matrix.get((uuid2, uuid1), 0)
                
                if similarity > 0.3:  # Similarity threshold
                    cluster_items.add(uuid2)
            
            if len(cluster_items) >= min_cluster_size:
                cluster = self._create_cluster(cluster_items)
                clusters.append(cluster)
                used_uuids.update(cluster_items)
        
        self.content_clusters = clusters
        return clusters
    
    def _calculate_content_similarity(self, uuid1: str, uuid2: str) -> float:
        """Calculate similarity between two content items"""
        metadata1 = self.content_metadata[uuid1]
        metadata2 = self.content_metadata[uuid2]
        
        similarity = 0.0
        
        # Tag similarity
        tags1 = set()
        tags2 = set()
        
        for tag_list in metadata1.get('tags', {}).values():
            tags1.update(tag_list)
        
        for tag_list in metadata2.get('tags', {}).values():
            tags2.update(tag_list)
        
        if tags1 and tags2:
            tag_similarity = len(tags1 & tags2) / len(tags1 | tags2)
            similarity += tag_similarity * 0.5
        
        # Phase similarity
        phase1 = metadata1.get('consciousness_phase')
        phase2 = metadata2.get('consciousness_phase')
        
        if phase1 and phase2 and phase1 == phase2:
            similarity += 0.3
        
        # Content type similarity
        if metadata1.get('content_type') == metadata2.get('content_type'):
            similarity += 0.2
        
        return min(1.0, similarity)
    
    def _create_cluster(self, cluster_items: Set[str]) -> ContentCluster:
        """Create a content cluster from a set of items"""
        # Find common tags
        all_tag_sets = []
        all_phases = set()
        
        for uuid in cluster_items:
            metadata = self.content_metadata[uuid]
            
            item_tags = set()
            for tag_list in metadata.get('tags', {}).values():
                item_tags.update(tag_list)
            all_tag_sets.append(item_tags)
            
            phase = metadata.get('consciousness_phase')
            if phase:
                all_phases.add(phase)
        
        # Find intersection of tags (common to most items)
        common_tags = set.intersection(*all_tag_sets) if all_tag_sets else set()
        
        # Generate cluster metadata
        cluster_id = f"cluster_{hash(frozenset(cluster_items)) % 10000:04d}"
        
        # Create title from most common tags and phases
        title_parts = []
        if common_tags:
            title_parts.extend(sorted(list(common_tags))[:3])
        if all_phases:
            title_parts.extend(sorted(list(all_phases)))
        
        title = " + ".join(title_parts).title() if title_parts else "Content Cluster"
        
        # Generate description
        content_types = Counter(
            self.content_metadata[uuid].get('content_type', 'unknown') 
            for uuid in cluster_items
        )
        
        description = f"Cluster of {len(cluster_items)} items including " + \
                     ", ".join(f"{count} {ctype}" for ctype, count in content_types.most_common(3))
        
        # Calculate cluster score (average quality)
        quality_scores = [
            self.content_metadata[uuid].get('quality_score', 0.5) 
            for uuid in cluster_items
        ]
        cluster_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        return ContentCluster(
            cluster_id=cluster_id,
            title=title,
            description=description,
            items=list(cluster_items),
            common_tags=list(common_tags),
            consciousness_phases=list(all_phases),
            cluster_score=cluster_score
        )
    
    def get_consciousness_phase_progression(self) -> Dict[str, Any]:
        """Analyze consciousness phase progression across content"""
        phase_stats = {
            'phase_distribution': Counter(),
            'phase_quality': {},
            'phase_progression': [],
            'cross_phase_references': defaultdict(list)
        }
        
        # Analyze phase distribution and quality
        for uuid, metadata in self.content_metadata.items():
            phase = metadata.get('consciousness_phase')
            if phase:
                phase_stats['phase_distribution'][phase] += 1
                
                quality = metadata.get('quality_score', 0.5)
                if phase not in phase_stats['phase_quality']:
                    phase_stats['phase_quality'][phase] = []
                phase_stats['phase_quality'][phase].append(quality)
        
        # Calculate average quality per phase
        for phase, qualities in phase_stats['phase_quality'].items():
            phase_stats['phase_quality'][phase] = {
                'average': sum(qualities) / len(qualities),
                'count': len(qualities),
                'max': max(qualities),
                'min': min(qualities)
            }
        
        # Analyze progression patterns
        phase_order = ['unity', 'shadow', 'individuation', 'cosmic', 'infinite']
        progression_data = []
        
        for i, phase in enumerate(phase_order):
            if phase in phase_stats['phase_distribution']:
                progression_data.append({
                    'phase': phase,
                    'order': i,
                    'count': phase_stats['phase_distribution'][phase],
                    'quality': phase_stats['phase_quality'].get(phase, {}).get('average', 0)
                })
        
        phase_stats['phase_progression'] = progression_data
        
        return phase_stats
    
    def generate_discovery_report(self) -> Dict[str, Any]:
        """Generate comprehensive discovery and analytics report"""
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_content_items': len(self.content_metadata),
                'indexed_tags': len(self.tag_index),
                'indexed_words': len(self.text_index)
            },
            'content_distribution': {},
            'consciousness_analysis': {},
            'quality_analysis': {},
            'tag_analysis': {},
            'discovery_recommendations': []
        }
        
        # Content distribution analysis
        content_types = Counter(
            metadata.get('content_type', 'unknown') 
            for metadata in self.content_metadata.values()
        )
        
        maturity_levels = Counter(
            metadata.get('maturity_level', 'unknown') 
            for metadata in self.content_metadata.values()
        )
        
        tier_distribution = Counter(
            metadata.get('tier_classification', 0) 
            for metadata in self.content_metadata.values()
        )
        
        report['content_distribution'] = {
            'by_type': dict(content_types),
            'by_maturity': dict(maturity_levels),
            'by_tier': dict(tier_distribution)
        }
        
        # Consciousness analysis
        report['consciousness_analysis'] = self.get_consciousness_phase_progression()
        
        # WE=1 alignment analysis
        we_alignments = [
            metadata.get('we_principle_alignment', 0) 
            for metadata in self.content_metadata.values()
            if metadata.get('we_principle_alignment') is not None
        ]
        
        if we_alignments:
            report['consciousness_analysis']['we_alignment'] = {
                'average': sum(we_alignments) / len(we_alignments),
                'count': len(we_alignments),
                'high_alignment_count': sum(1 for w in we_alignments if w > 0.8),
                'distribution': Counter(f"{int(w*10)*10}-{int(w*10)*10+9}%" for w in we_alignments)
            }
        
        # Quality analysis
        quality_scores = [
            metadata.get('quality_score', 0) 
            for metadata in self.content_metadata.values()
            if metadata.get('quality_score') is not None
        ]
        
        if quality_scores:
            report['quality_analysis'] = {
                'average_quality': sum(quality_scores) / len(quality_scores),
                'high_quality_count': sum(1 for q in quality_scores if q > 0.8),
                'quality_distribution': Counter(f"{int(q*10)*10}-{int(q*10)*10+9}%" for q in quality_scores)
            }
        
        # Tag analysis
        all_tags = []
        tag_categories = defaultdict(list)
        
        for metadata in self.content_metadata.values():
            tags = metadata.get('tags', {})
            for category, tag_list in tags.items():
                all_tags.extend(tag_list)
                tag_categories[category].extend(tag_list)
        
        report['tag_analysis'] = {
            'total_unique_tags': len(set(all_tags)),
            'most_common_tags': dict(Counter(all_tags).most_common(20)),
            'tags_by_category': {
                category: dict(Counter(tags).most_common(10))
                for category, tags in tag_categories.items()
            }
        }
        
        # Generate recommendations
        recommendations = []
        
        # Quality recommendations
        low_quality_count = sum(1 for q in quality_scores if q < 0.5) if quality_scores else 0
        if low_quality_count > 0:
            recommendations.append({
                'type': 'quality_improvement',
                'description': f'{low_quality_count} items have quality scores below 0.5 and could benefit from enhancement',
                'priority': 'medium'
            })
        
        # WE=1 alignment recommendations
        if we_alignments:
            low_alignment_count = sum(1 for w in we_alignments if w < 0.5)
            if low_alignment_count > 0:
                recommendations.append({
                    'type': 'consciousness_alignment',
                    'description': f'{low_alignment_count} items have low WE=1 alignment and may need consciousness framework integration',
                    'priority': 'high'
                })
        
        # Content gap analysis
        phase_counts = report['consciousness_analysis']['phase_distribution']
        if 'shadow' in phase_counts and phase_counts['shadow'] < phase_counts.get('unity', 0) * 0.3:
            recommendations.append({
                'type': 'content_development',
                'description': 'Shadow phase content is underrepresented compared to Unity phase. Consider developing more shadow integration materials.',
                'priority': 'high'
            })
        
        report['discovery_recommendations'] = recommendations
        
        return report

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Content Discovery Engine")
    parser.add_argument("repository_path", help="Path to repository root")
    parser.add_argument("--metadata", default="08_meta/tagging_system/content_metadata.yaml", help="Path to content metadata")
    parser.add_argument("--search", help="Search query text")
    parser.add_argument("--phase", help="Filter by consciousness phase")
    parser.add_argument("--type", help="Filter by content type")  
    parser.add_argument("--tags", nargs='+', help="Filter by tags")
    parser.add_argument("--min-quality", type=float, help="Minimum quality score")
    parser.add_argument("--related", help="Find content related to UUID")
    parser.add_argument("--cluster", action='store_true', help="Generate content clusters")
    parser.add_argument("--report", action='store_true', help="Generate discovery report")
    parser.add_argument("--max-results", type=int, default=20, help="Maximum search results")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--verbose", "-v", action='store_true', help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # Initialize discovery engine
    repo_path = Path(args.repository_path)
    metadata_path = repo_path / args.metadata
    engine = DiscoveryEngine(repo_path, metadata_path, logger)
    
    results = {}
    
    # Execute requested operations
    if args.search or args.phase or args.type or args.tags:
        logger.info("Executing search...")
        
        query = SearchQuery(
            text=args.search or "",
            consciousness_phase=args.phase,
            content_type=args.type,
            tags=args.tags or [],
            min_quality_score=args.min_quality
        )
        
        search_results = engine.search(query, args.max_results)
        results['search_results'] = [asdict(result) for result in search_results]
        
        print(f"\n=== SEARCH RESULTS ({len(search_results)}) ===")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result.title}")
            print(f"   Path: {result.path}")
            print(f"   Relevance: {result.relevance_score:.3f} | Quality: {result.quality_score or 'N/A'}")
            print(f"   Phase: {result.consciousness_phase or 'N/A'} | Type: {result.content_type}")
            if result.matched_tags:
                print(f"   Tags: {', '.join(result.matched_tags)}")
            print(f"   Snippet: {result.snippet}")
            print()
    
    if args.related:
        logger.info(f"Finding content related to {args.related}...")
        related_results = engine.find_related_content(args.related, args.max_results)
        results['related_results'] = [asdict(result) for result in related_results]
        
        print(f"\n=== RELATED CONTENT ({len(related_results)}) ===")
        for i, result in enumerate(related_results, 1):
            print(f"{i}. {result.title}")
            print(f"   Similarity: {result.relevance_score:.3f}")
            print(f"   Matched tags: {', '.join(result.matched_tags)}")
            print()
    
    if args.cluster:
        logger.info("Generating content clusters...")
        clusters = engine.cluster_content()
        results['clusters'] = [asdict(cluster) for cluster in clusters]
        
        print(f"\n=== CONTENT CLUSTERS ({len(clusters)}) ===")
        for i, cluster in enumerate(clusters, 1):
            print(f"{i}. {cluster.title}")
            print(f"   Items: {len(cluster.items)}")
            print(f"   Score: {cluster.cluster_score:.3f}")
            print(f"   Common tags: {', '.join(cluster.common_tags[:5])}")
            print(f"   Phases: {', '.join(cluster.consciousness_phases)}")
            print()
    
    if args.report:
        logger.info("Generating discovery report...")
        report = engine.generate_discovery_report()
        results['discovery_report'] = report
        
        print("\n=== DISCOVERY REPORT ===")
        print(f"Total content items: {report['metadata']['total_content_items']}")
        print(f"Indexed tags: {report['metadata']['indexed_tags']}")
        print(f"Most common tags: {list(report['tag_analysis']['most_common_tags'].keys())[:10]}")
        print(f"Consciousness phases: {list(report['consciousness_analysis']['phase_distribution'].keys())}")
        
        if report['discovery_recommendations']:
            print("\nRecommendations:")
            for rec in report['discovery_recommendations']:
                print(f"- {rec['description']} ({rec['priority']} priority)")
    
    # Output results if requested
    if args.output and results:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if output_path.suffix in ['.yaml', '.yml']:
            with open(output_path, 'w') as f:
                yaml.dump(results, f, default_flow_style=False)
        else:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {output_path}")
    
    logger.info("Discovery engine operations complete!")