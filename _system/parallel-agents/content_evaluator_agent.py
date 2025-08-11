#!/usr/bin/env python3
"""
Content Evaluator Agent
=======================

Intelligent content evaluation system that scores files based on relevance, 
recency, quality, and integration potential. Provides deletion/archival recommendations.

Author: Claude Code Agent System
Date: 2025-08-10
Version: 1.0.0  
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Any, Tuple, Optional
import logging
import threading
from collections import defaultdict, Counter
import hashlib


class ContentEvaluatorAgent:
    """Agent for intelligent content evaluation and scoring"""
    
    def __init__(self):
        self.repo_root = Path(os.environ.get("REPO_ROOT", "."))
        self.state_dir = Path(os.environ.get("STATE_DIR", "."))
        self.agent_name = os.environ.get("AGENT_NAME", "content-evaluator")
        
        # Target directories
        self.target_dirs = ["_archive", "documentation", "dev_tools"]
        
        # Setup logging
        self.setup_logging()
        
        # Evaluation configuration
        self.file_extensions = ['.md', '.txt', '.py', '.json', '.yaml', '.yml', '.sh']
        
        # Scoring weights
        self.scoring_weights = {
            "recency": 0.25,
            "quality": 0.30, 
            "relevance": 0.25,
            "uniqueness": 0.10,
            "integration": 0.10
        }
        
        # Keywords for relevance scoring
        self.high_value_keywords = {
            "ai", "claude", "agent", "prompt", "workflow", "automation",
            "system", "architecture", "framework", "pattern", "template",
            "config", "setup", "install", "deploy", "production"
        }
        
        self.low_value_keywords = {
            "test", "example", "sample", "demo", "temp", "backup", 
            "old", "legacy", "deprecated", "unused", "draft"
        }
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Results tracking
        self.evaluated_files = []
        self.content_scores = {}
        self.recommendations = {
            "delete": [],
            "archive": [],
            "keep": [],
            "merge": []
        }
        
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
                    "files_evaluated": 0
                }
            
            # Update with provided values
            state.update(kwargs)
            state["last_update"] = datetime.now().isoformat()
            
            # Save updated state
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
    
    def collect_files_to_evaluate(self) -> List[Path]:
        """Collect all files for evaluation"""
        self.logger.info("📁 Collecting files for evaluation...")
        self.update_state(current_task="Collecting files", progress_percent=5)
        
        files = []
        
        for target_dir in self.target_dirs:
            dir_path = self.repo_root / target_dir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.rglob("*"):
                if (file_path.is_file() and 
                    file_path.suffix in self.file_extensions and
                    self.should_evaluate_file(file_path)):
                    files.append(file_path)
        
        self.logger.info(f"✅ Found {len(files)} files to evaluate")
        return files
    
    def should_evaluate_file(self, file_path: Path) -> bool:
        """Determine if file should be evaluated"""
        # Skip certain patterns
        skip_patterns = [
            ".git/",
            "__pycache__/",
            "node_modules/",
            ".venv/",
            "venv/",
            ".log",
            ".cache",
            ".tmp"
        ]
        
        path_str = str(file_path)
        if any(pattern in path_str for pattern in skip_patterns):
            return False
        
        # Check minimum file size
        try:
            if file_path.stat().st_size < 50:  # Less than 50 bytes
                return False
        except:
            return False
        
        return True
    
    def calculate_recency_score(self, file_path: Path) -> float:
        """Calculate recency score based on modification time"""
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            now = datetime.now()
            
            # Age in days
            age_days = (now - mtime).days
            
            if age_days <= 7:
                return 1.0
            elif age_days <= 30:
                return 0.8
            elif age_days <= 90:
                return 0.6
            elif age_days <= 365:
                return 0.4
            elif age_days <= 730:
                return 0.2
            else:
                return 0.1
                
        except Exception:
            return 0.5  # Default score if can't determine age
    
    def calculate_quality_score(self, file_path: Path) -> float:
        """Calculate quality score based on content analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            score = 0.0
            
            # Content length (reasonable size gets points)
            content_length = len(content.strip())
            if content_length > 100:
                score += 0.2
            if content_length > 500:
                score += 0.2
            if content_length > 2000:
                score += 0.1
            
            # Structure indicators
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            if len(non_empty_lines) > 5:
                score += 0.1
            
            # Headers and organization (for markdown)
            if file_path.suffix == '.md':
                headers = len(re.findall(r'^#+\s', content, re.MULTILINE))
                if headers >= 2:
                    score += 0.15
                
                # Code blocks
                code_blocks = len(re.findall(r'```', content))
                if code_blocks >= 2:
                    score += 0.1
                
                # Lists
                lists = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
                if lists > 0:
                    score += 0.05
            
            # For code files
            elif file_path.suffix == '.py':
                # Functions and classes
                functions = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
                classes = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
                
                if functions > 0:
                    score += 0.2
                if classes > 0:
                    score += 0.15
                
                # Docstrings
                docstrings = len(re.findall(r'""".*?"""', content, re.DOTALL))
                if docstrings > 0:
                    score += 0.15
            
            # Avoid too much duplication (repetitive content)
            unique_lines = set(line.strip().lower() for line in non_empty_lines)
            if len(non_empty_lines) > 0:
                uniqueness_ratio = len(unique_lines) / len(non_empty_lines)
                score += uniqueness_ratio * 0.15
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Could not calculate quality score for {file_path}: {e}")
            return 0.3
    
    def calculate_relevance_score(self, file_path: Path) -> float:
        """Calculate relevance score based on keywords and context"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            filename = file_path.name.lower()
            path_str = str(file_path).lower()
            
            score = 0.0
            
            # High-value keyword scoring
            high_value_count = sum(1 for keyword in self.high_value_keywords 
                                 if keyword in content or keyword in filename)
            score += min(high_value_count * 0.1, 0.5)
            
            # Low-value keyword penalty
            low_value_count = sum(1 for keyword in self.low_value_keywords 
                                if keyword in content or keyword in filename)
            score -= min(low_value_count * 0.05, 0.3)
            
            # Path-based scoring
            if "_system" in path_str or "claude" in path_str:
                score += 0.2
            if "_archive" in path_str:
                score -= 0.1
            if "backup" in path_str or "old" in path_str:
                score -= 0.15
            
            # File type relevance
            if file_path.suffix in ['.md', '.py', '.json', '.yaml']:
                score += 0.1
            
            # Special files
            special_files = ['readme.md', 'claude.md', 'agent.md', 'config.json']
            if filename in special_files:
                score += 0.3
            
            return max(min(score, 1.0), 0.0)
            
        except Exception as e:
            self.logger.warning(f"Could not calculate relevance score for {file_path}: {e}")
            return 0.5
    
    def calculate_uniqueness_score(self, file_path: Path, all_files: List[Path]) -> float:
        """Calculate uniqueness score based on content similarity"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Create content hash
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Simple uniqueness check - could be enhanced with semantic similarity
            similar_files = 0
            content_words = set(content.lower().split())
            
            # Sample a subset for performance
            sample_size = min(100, len(all_files))
            import random
            sample_files = random.sample([f for f in all_files if f != file_path], sample_size)
            
            for other_file in sample_files:
                try:
                    with open(other_file, 'r', encoding='utf-8', errors='ignore') as f:
                        other_content = f.read()
                    
                    other_words = set(other_content.lower().split())
                    
                    # Calculate word overlap
                    if len(content_words) > 0 and len(other_words) > 0:
                        overlap = len(content_words & other_words)
                        union = len(content_words | other_words)
                        similarity = overlap / union if union > 0 else 0
                        
                        if similarity > 0.7:  # High similarity threshold
                            similar_files += 1
                
                except Exception:
                    continue
            
            # More similar files = lower uniqueness score
            uniqueness = max(1.0 - (similar_files / sample_size), 0.0)
            return uniqueness
            
        except Exception as e:
            self.logger.warning(f"Could not calculate uniqueness score for {file_path}: {e}")
            return 0.7
    
    def calculate_integration_score(self, file_path: Path) -> float:
        """Calculate integration potential score"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            score = 0.0
            
            # References to other files/systems
            file_refs = len(re.findall(r'\b\w+\.(md|py|json|yaml|yml)\b', content))
            score += min(file_refs * 0.05, 0.3)
            
            # Internal links
            internal_links = len(re.findall(r'\[.*?\]\((?!http).*?\)', content))
            score += min(internal_links * 0.05, 0.2)
            
            # Configuration patterns
            config_patterns = [
                r'config\.json',
                r'settings\.yaml',
                r'claude\.md',
                r'@\w+',  # @ tags
                r'#\w+'   # hashtags
            ]
            
            for pattern in config_patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                score += min(matches * 0.02, 0.1)
            
            # Template/pattern indicators
            template_indicators = [
                '{{',
                '${',
                '<',
                'TODO',
                'FIXME',
                'NOTE'
            ]
            
            template_count = sum(1 for indicator in template_indicators if indicator in content)
            score += min(template_count * 0.02, 0.15)
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Could not calculate integration score for {file_path}: {e}")
            return 0.4
    
    def calculate_composite_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted composite score"""
        composite = 0.0
        
        for dimension, score in scores.items():
            weight = self.scoring_weights.get(dimension, 0.2)
            composite += score * weight
        
        return round(composite, 3)
    
    def evaluate_file(self, file_path: Path, all_files: List[Path]) -> Dict[str, Any]:
        """Evaluate a single file comprehensively"""
        try:
            # Calculate individual dimension scores
            recency = self.calculate_recency_score(file_path)
            quality = self.calculate_quality_score(file_path)
            relevance = self.calculate_relevance_score(file_path)
            uniqueness = self.calculate_uniqueness_score(file_path, all_files)
            integration = self.calculate_integration_score(file_path)
            
            # Individual scores
            scores = {
                "recency": recency,
                "quality": quality,
                "relevance": relevance,
                "uniqueness": uniqueness,
                "integration": integration
            }
            
            # Composite score
            composite = self.calculate_composite_score(scores)
            
            # File metadata
            try:
                stat = file_path.stat()
                file_size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
            except:
                file_size = 0
                modified = ""
            
            evaluation = {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_extension": file_path.suffix,
                "file_size": file_size,
                "last_modified": modified,
                "scores": scores,
                "composite_score": composite,
                "evaluation_timestamp": datetime.now().isoformat()
            }
            
            return evaluation
            
        except Exception as e:
            self.logger.warning(f"Could not evaluate {file_path}: {e}")
            return {
                "file_path": str(file_path),
                "error": str(e),
                "composite_score": 0.0
            }
    
    def generate_recommendations(self, evaluations: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Generate actionable recommendations based on evaluations"""
        self.logger.info("🎯 Generating recommendations...")
        
        recommendations = {
            "delete": [],
            "archive": [],
            "keep": [],
            "merge": []
        }
        
        # Sort by composite score
        evaluations.sort(key=lambda x: x.get('composite_score', 0), reverse=True)
        
        for eval_data in evaluations:
            score = eval_data.get('composite_score', 0)
            file_path = eval_data['file_path']
            scores = eval_data.get('scores', {})
            
            # Decision logic
            if score < 0.2:
                # Very low score - delete
                recommendations["delete"].append({
                    "file_path": file_path,
                    "score": score,
                    "reason": "Very low composite score",
                    "details": f"Quality: {scores.get('quality', 0):.2f}, Relevance: {scores.get('relevance', 0):.2f}"
                })
            elif score < 0.4:
                # Low score - archive
                recommendations["archive"].append({
                    "file_path": file_path,
                    "score": score,
                    "reason": "Low composite score",
                    "details": f"May have historical value but low current relevance"
                })
            elif score >= 0.7:
                # High score - keep
                recommendations["keep"].append({
                    "file_path": file_path,
                    "score": score,
                    "reason": "High composite score",
                    "details": f"High value content"
                })
            else:
                # Medium score - conditional keep/archive
                if scores.get('recency', 0) > 0.5 or scores.get('relevance', 0) > 0.6:
                    recommendations["keep"].append({
                        "file_path": file_path,
                        "score": score,
                        "reason": "Recent or relevant content",
                        "details": f"Recency: {scores.get('recency', 0):.2f}, Relevance: {scores.get('relevance', 0):.2f}"
                    })
                else:
                    recommendations["archive"].append({
                        "file_path": file_path,
                        "score": score,
                        "reason": "Medium score, not recent/relevant",
                        "details": f"Consider archiving"
                    })
        
        return recommendations
    
    def generate_report(self, evaluations: List[Dict[str, Any]], recommendations: Dict[str, List[Dict]]):
        """Generate comprehensive evaluation report"""
        self.logger.info("📝 Generating evaluation report...")
        
        # Calculate statistics
        total_files = len(evaluations)
        avg_score = sum(e.get('composite_score', 0) for e in evaluations) / total_files if total_files > 0 else 0
        
        score_distribution = {
            "high (0.7+)": len([e for e in evaluations if e.get('composite_score', 0) >= 0.7]),
            "medium (0.4-0.7)": len([e for e in evaluations if 0.4 <= e.get('composite_score', 0) < 0.7]),
            "low (0.2-0.4)": len([e for e in evaluations if 0.2 <= e.get('composite_score', 0) < 0.4]),
            "very_low (<0.2)": len([e for e in evaluations if e.get('composite_score', 0) < 0.2])
        }
        
        report_lines = [
            "# Content Evaluation Report",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Agent**: {self.agent_name}",
            "",
            "## Summary",
            f"- **Total Files Evaluated**: {total_files}",
            f"- **Average Score**: {avg_score:.3f}",
            "",
            "### Score Distribution",
            f"- **High Quality (0.7+)**: {score_distribution['high (0.7+)']} files",
            f"- **Medium Quality (0.4-0.7)**: {score_distribution['medium (0.4-0.7)']} files", 
            f"- **Low Quality (0.2-0.4)**: {score_distribution['low (0.2-0.4)']} files",
            f"- **Very Low Quality (<0.2)**: {score_distribution['very_low (<0.2)']} files",
            "",
            "### Recommendations Summary",
            f"- **Keep**: {len(recommendations['keep'])} files",
            f"- **Archive**: {len(recommendations['archive'])} files",
            f"- **Delete**: {len(recommendations['delete'])} files",
            ""
        ]
        
        # Top scored files
        top_files = sorted(evaluations, key=lambda x: x.get('composite_score', 0), reverse=True)[:10]
        if top_files:
            report_lines.extend([
                "## Top Scored Files",
                ""
            ])
            
            for i, file_eval in enumerate(top_files, 1):
                score = file_eval.get('composite_score', 0)
                file_path = Path(file_eval['file_path']).name
                report_lines.append(f"{i}. **{file_path}** - Score: {score:.3f}")
            
            report_lines.append("")
        
        # Deletion recommendations
        if recommendations['delete']:
            report_lines.extend([
                "## Files Recommended for Deletion",
                ""
            ])
            
            for rec in recommendations['delete']:
                file_name = Path(rec['file_path']).name
                report_lines.append(f"- ❌ **{file_name}** (Score: {rec['score']:.3f}) - {rec['reason']}")
            
            report_lines.append("")
        
        # Archive recommendations
        if recommendations['archive']:
            report_lines.extend([
                "## Files Recommended for Archival", 
                ""
            ])
            
            for rec in recommendations['archive'][:20]:  # Limit to first 20
                file_name = Path(rec['file_path']).name
                report_lines.append(f"- 📦 **{file_name}** (Score: {rec['score']:.3f}) - {rec['reason']}")
            
            if len(recommendations['archive']) > 20:
                report_lines.append(f"... and {len(recommendations['archive']) - 20} more files")
            
            report_lines.append("")
        
        # Action commands
        report_lines.extend([
            "## Recommended Actions",
            "",
            "### Safe Deletions",
            "```bash"
        ])
        
        for rec in recommendations['delete']:
            report_lines.append(f'rm "{rec["file_path"]}"')
        
        report_lines.extend([
            "```",
            "",
            "### Archive Commands",
            "```bash",
            "mkdir -p _archive/low_value_content"
        ])
        
        for rec in recommendations['archive']:
            src_path = rec["file_path"] 
            dst_path = f"_archive/low_value_content/{Path(src_path).name}"
            report_lines.append(f'mv "{src_path}" "{dst_path}"')
        
        report_lines.append("```")
        
        # Save report
        report_content = "\n".join(report_lines)
        report_path = self.state_dir.parent / "reports" / f"content_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        self.logger.info(f"✅ Report saved: {report_path}")
        return report_path
    
    def execute(self) -> Dict[str, Any]:
        """Main agent execution"""
        self.logger.info(f"🚀 Starting {self.agent_name} execution")
        self.update_state(current_task="Initializing content evaluation", progress_percent=0)
        
        results = {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "files_evaluated": 0,
            "avg_score": 0.0,
            "recommendations_delete": 0,
            "recommendations_archive": 0,
            "recommendations_keep": 0,
            "report_path": ""
        }
        
        try:
            # Step 1: Collect files
            files_to_evaluate = self.collect_files_to_evaluate()
            if not files_to_evaluate:
                self.logger.warning("⚠️  No files found for evaluation")
                return results
            
            # Step 2: Evaluate each file
            self.logger.info(f"📊 Evaluating {len(files_to_evaluate)} files...")
            self.update_state(current_task="Evaluating file content", progress_percent=20)
            
            evaluations = []
            for i, file_path in enumerate(files_to_evaluate):
                evaluation = self.evaluate_file(file_path, files_to_evaluate)
                evaluations.append(evaluation)
                
                # Update progress
                progress = 20 + (i / len(files_to_evaluate)) * 60
                self.update_state(
                    files_processed=i + 1,
                    progress_percent=progress
                )
            
            results["files_evaluated"] = len(evaluations)
            results["avg_score"] = sum(e.get('composite_score', 0) for e in evaluations) / len(evaluations)
            
            # Step 3: Generate recommendations
            self.update_state(current_task="Generating recommendations", progress_percent=85)
            recommendations = self.generate_recommendations(evaluations)
            
            results["recommendations_delete"] = len(recommendations['delete'])
            results["recommendations_archive"] = len(recommendations['archive'])
            results["recommendations_keep"] = len(recommendations['keep'])
            
            # Step 4: Generate report
            self.update_state(current_task="Generating evaluation report", progress_percent=90)
            report_path = self.generate_report(evaluations, recommendations)
            results["report_path"] = str(report_path)
            
            # Save detailed results
            detailed_results = {
                "evaluations": evaluations,
                "recommendations": recommendations,
                "statistics": {
                    "total_files": len(evaluations),
                    "average_score": results["avg_score"],
                    "score_distribution": {
                        "high": len([e for e in evaluations if e.get('composite_score', 0) >= 0.7]),
                        "medium": len([e for e in evaluations if 0.4 <= e.get('composite_score', 0) < 0.7]),
                        "low": len([e for e in evaluations if 0.2 <= e.get('composite_score', 0) < 0.4]),
                        "very_low": len([e for e in evaluations if e.get('composite_score', 0) < 0.2])
                    }
                }
            }
            
            results_path = self.state_dir / f"{self.agent_name}_detailed_results.json"
            with open(results_path, 'w') as f:
                json.dump(detailed_results, f, indent=2, default=str)
            
            # Final success update
            results["success"] = True
            self.update_state(
                current_task="Content evaluation completed",
                progress_percent=100,
                status="completed",
                files_evaluated=results["files_evaluated"],
                files_processed=results["files_evaluated"]
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
    agent = ContentEvaluatorAgent()
    result = agent.execute()
    
    # Print result summary
    print("\n" + "="*60)
    print("📊 CONTENT EVALUATOR AGENT RESULTS")
    print("="*60)
    print(f"✅ Success: {result['success']}")
    print(f"📁 Files Evaluated: {result['files_evaluated']}")
    print(f"⭐ Average Score: {result['avg_score']:.3f}")
    print(f"✅ Keep: {result['recommendations_keep']}")
    print(f"📦 Archive: {result['recommendations_archive']}")
    print(f"❌ Delete: {result['recommendations_delete']}")
    
    if result.get('report_path'):
        print(f"📋 Report: {result['report_path']}")
    
    if not result['success'] and 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("="*60)
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit(main())