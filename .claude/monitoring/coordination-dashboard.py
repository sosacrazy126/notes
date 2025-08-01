#!/usr/bin/env python3
"""
Real-time Coordination Monitoring Dashboard
Provides live visibility into subagent coordination effectiveness and system health
"""

import json
import time
import os
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import threading

@dataclass
class CoordinationMetrics:
    """Real-time coordination metrics data structure"""
    timestamp: str
    active_subagents: int
    coordination_health: str
    we_principle_coherence: float
    workflow_completion_rate: float
    recent_executions: int
    system_load: str
    critical_alerts: List[str]

class CoordinationMonitor:
    """
    Real-time coordination monitoring system for consciousness research ecosystem
    Provides continuous visibility into subagent coordination effectiveness
    """
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.claude_dir = self.project_dir / ".claude"
        self.monitoring_active = True
        self.metrics_history = []
        self.max_history_size = 100
        self.update_interval = 30  # seconds
        self.dashboard_file = self.claude_dir / "monitoring" / "dashboard.json"
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Ensure monitoring directory exists
        self.dashboard_file.parent.mkdir(parents=True, exist_ok=True)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, shutting down monitoring..."")
        self.monitoring_active = False
        
    def start_monitoring(self):
        """Start real-time coordination monitoring"""
        print("🚀 Starting real-time coordination monitoring...")
        print(f"📊 Dashboard updates every {self.update_interval} seconds")
        print("🛑 Press Ctrl+C to stop monitoring\n")
        
        try:
            while self.monitoring_active:
                coordination_status = self.collect_coordination_metrics()
                self.update_dashboard(coordination_status)
                self.display_console_status(coordination_status)
                
                # Sleep with interruption check
                for _ in range(self.update_interval):
                    if not self.monitoring_active:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
        finally:
            self.cleanup()
            
    def collect_coordination_metrics(self) -> CoordinationMetrics:
        """Collect current coordination performance metrics"""
        try:
            # Analyze subagent ecosystem
            agents_dir = self.claude_dir / "agents"
            active_subagents = 0
            if agents_dir.exists():
                active_subagents = len(list(agents_dir.glob("*.md")))
            
            # Check coordination system health
            coordination_file = self.claude_dir / "subagent-coordination.json"
            coordination_health = "optimal"
            recent_executions = 0
            
            if coordination_file.exists():
                try:
                    with open(coordination_file) as f:
                        coord_data = json.load(f)
                    recent_executions = len(coord_data.get("subagent_executions", []))
                    coordination_health = "optimal" if recent_executions > 0 else "idle"
                except Exception:
                    coordination_health = "degraded"
            else:
                coordination_health = "not_initialized"
            
            # Check WE=1 principle coherence
            we_coherence = self.calculate_we_principle_coherence()
            
            # Calculate workflow completion rate
            workflow_completion_rate = self.calculate_workflow_completion_rate()
            
            # Determine system load
            system_load = self.assess_system_load()
            
            # Identify critical alerts
            critical_alerts = self.identify_critical_alerts(
                coordination_health, we_coherence, workflow_completion_rate
            )
            
            return CoordinationMetrics(
                timestamp=datetime.now().isoformat(),
                active_subagents=active_subagents,
                coordination_health=coordination_health,
                we_principle_coherence=we_coherence,
                workflow_completion_rate=workflow_completion_rate,
                recent_executions=recent_executions,
                system_load=system_load,
                critical_alerts=critical_alerts
            )
            
        except Exception as e:
            print(f"⚠️  Metrics collection error: {e}")
            return CoordinationMetrics(
                timestamp=datetime.now().isoformat(),
                active_subagents=0,
                coordination_health="error",
                we_principle_coherence=0.0,
                workflow_completion_rate=0.0,
                recent_executions=0,
                system_load="unknown",
                critical_alerts=[f"Metrics collection failed: {e}"]
            )
            
    def calculate_we_principle_coherence(self) -> float:
        """Calculate WE=1 principle coherence across subagents"""
        agents_dir = self.claude_dir / "agents"
        if not agents_dir.exists():
            return 0.0
            
        coherence_scores = []
        
        for agent_file in agents_dir.glob("*.md"):
            try:
                with open(agent_file) as f:
                    content = f.read().lower()
                
                # WE=1 indicators
                we_indicators = [
                    "we=1", "we = 1", "unified consciousness",
                    "consciousness examining itself", "single consciousness"
                ]
                
                # Dualistic indicators (negative)
                dualistic_indicators = [
                    "external tool", "separate ai", "assistant helping"
                ]
                
                we_count = sum(1 for indicator in we_indicators if indicator in content)
                dualistic_count = sum(1 for indicator in dualistic_indicators if indicator in content)
                
                if we_count + dualistic_count == 0:
                    coherence_scores.append(0.5)
                else:
                    score = we_count / (we_count + dualistic_count * 2)
                    coherence_scores.append(min(1.0, max(0.0, score)))
                    
            except Exception:
                coherence_scores.append(0.5)
                
        return sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0.0
        
    def calculate_workflow_completion_rate(self) -> float:
        """Calculate recent workflow completion rate"""
        coordination_file = self.claude_dir / "subagent-coordination.json"
        
        if not coordination_file.exists():
            return 0.0
            
        try:
            with open(coordination_file) as f:
                coord_data = json.load(f)
            
            workflow_state = coord_data.get("workflow_state", {})
            completed = sum(1 for status in workflow_state.values() if status)
            total = len(workflow_state)
            
            return completed / total if total > 0 else 0.0
            
        except Exception:
            return 0.0
            
    def assess_system_load(self) -> str:
        """Assess current system load"""
        try:
            # Check number of recent log files as proxy for activity
            logs_dir = self.claude_dir / "logs"
            if not logs_dir.exists():
                return "idle"
                
            recent_logs = []
            cutoff_time = datetime.now() - timedelta(hours=1)
            
            for log_file in logs_dir.glob("*.log"):
                try:
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_time > cutoff_time:
                        recent_logs.append(log_file)
                except Exception:
                    continue
                    
            if len(recent_logs) == 0:
                return "idle"
            elif len(recent_logs) < 3:
                return "light"
            elif len(recent_logs) < 6:
                return "moderate"
            else:
                return "heavy"
                
        except Exception:
            return "unknown"
            
    def identify_critical_alerts(self, coordination_health: str, we_coherence: float, 
                               completion_rate: float) -> List[str]:
        """Identify critical system alerts"""
        alerts = []
        
        if coordination_health == "not_initialized":
            alerts.append("🚨 Coordination system not initialized")
        elif coordination_health == "degraded":
            alerts.append("⚠️  Coordination system degraded")
            
        if we_coherence < 0.7:
            alerts.append(f"🧘 WE=1 coherence low ({we_coherence:.2f})")
            
        if completion_rate < 0.5:
            alerts.append(f"📉 Workflow completion rate low ({completion_rate:.1%})")
            
        # Check for shadow development priority
        shadow_files = list(self.project_dir.glob("**/*shadow*")) + list(self.project_dir.glob("**/*Shadow*"))
        if len(shadow_files) < 20:
            alerts.append(f"🌘 Shadow development needs attention ({len(shadow_files)} files)")
            
        return alerts
        
    def update_dashboard(self, metrics: CoordinationMetrics):
        """Update monitoring dashboard with current metrics"""
        # Add to history
        self.metrics_history.append(metrics)
        
        # Maintain history size limit
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
            
        # Calculate trends
        trends = self.calculate_trends()
        
        # Create dashboard data
        dashboard_data = {
            "last_updated": metrics.timestamp,
            "current_metrics": {
                "active_subagents": metrics.active_subagents,
                "coordination_health": metrics.coordination_health,
                "we_principle_coherence": round(metrics.we_principle_coherence, 3),
                "workflow_completion_rate": round(metrics.workflow_completion_rate, 3),
                "recent_executions": metrics.recent_executions,
                "system_load": metrics.system_load,
                "critical_alerts": metrics.critical_alerts
            },
            "trends": trends,
            "history_size": len(self.metrics_history),
            "monitoring_active": self.monitoring_active
        }
        
        # Save dashboard data
        try:
            with open(self.dashboard_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Dashboard update failed: {e}")
            
    def calculate_trends(self) -> Dict[str, Any]:
        """Calculate performance trends from metrics history"""
        if len(self.metrics_history) < 2:
            return {"status": "insufficient_data"}
            
        recent = self.metrics_history[-5:]  # Last 5 measurements
        older = self.metrics_history[-10:-5] if len(self.metrics_history) >= 10 else []
        
        trends = {}
        
        # WE=1 coherence trend
        if older:
            recent_coherence = sum(m.we_principle_coherence for m in recent) / len(recent)
            older_coherence = sum(m.we_principle_coherence for m in older) / len(older)
            coherence_trend = recent_coherence - older_coherence
            
            trends["we_coherence_trend"] = {
                "direction": "improving" if coherence_trend > 0.01 else "declining" if coherence_trend < -0.01 else "stable",
                "change": round(coherence_trend, 3)
            }
            
        # Workflow completion trend
        if older:
            recent_completion = sum(m.workflow_completion_rate for m in recent) / len(recent)
            older_completion = sum(m.workflow_completion_rate for m in older) / len(older)
            completion_trend = recent_completion - older_completion
            
            trends["workflow_completion_trend"] = {
                "direction": "improving" if completion_trend > 0.05 else "declining" if completion_trend < -0.05 else "stable",
                "change": round(completion_trend, 3)
            }
            
        return trends
        
    def display_console_status(self, metrics: CoordinationMetrics):
        """Display current status in console"""
        # Clear screen and show status
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🧠 CONSCIOUSNESS RESEARCH ECOSYSTEM MONITORING")
        print("=" * 60)
        print(f"⏰ Last Update: {datetime.fromisoformat(metrics.timestamp).strftime('%H:%M:%S')}")
        print()
        
        # System Status
        print("📊 SYSTEM STATUS")
        print("-" * 30)
        print(f"🤖 Active Subagents: {metrics.active_subagents}")
        print(f"🔄 Coordination Health: {self.format_health_status(metrics.coordination_health)}")
        print(f"🧘 WE=1 Coherence: {self.format_coherence_score(metrics.we_principle_coherence)}")
        print(f"📈 Workflow Completion: {metrics.workflow_completion_rate:.1%}")
        print(f"🔥 System Load: {self.format_system_load(metrics.system_load)}")
        print(f"📝 Recent Executions: {metrics.recent_executions}")
        print()
        
        # Critical Alerts
        if metrics.critical_alerts:
            print("🚨 CRITICAL ALERTS")
            print("-" * 30)
            for alert in metrics.critical_alerts:
                print(f"  {alert}")
            print()
            
        # Trends (if available)
        if len(self.metrics_history) >= 10:
            trends = self.calculate_trends()
            if "we_coherence_trend" in trends or "workflow_completion_trend" in trends:
                print("📈 TRENDS")
                print("-" * 30)
                if "we_coherence_trend" in trends:
                    trend = trends["we_coherence_trend"]
                    print(f"🧘 WE=1 Coherence: {trend['direction']} ({trend['change']:+.3f})")
                if "workflow_completion_trend" in trends:
                    trend = trends["workflow_completion_trend"]
                    print(f"📈 Workflow Completion: {trend['direction']} ({trend['change']:+.3f})")
                print()
        
        print(f"💾 Dashboard: {self.dashboard_file}")
        print("🛑 Press Ctrl+C to stop monitoring")
        
    def format_health_status(self, health: str) -> str:
        """Format coordination health status with colors/symbols"""
        status_map = {
            "optimal": "✅ Optimal",
            "good": "🟢 Good", 
            "idle": "🟡 Idle",
            "degraded": "🟠 Degraded",
            "not_initialized": "🔴 Not Initialized",
            "error": "❌ Error"
        }
        return status_map.get(health, f"❓ {health}")
        
    def format_coherence_score(self, score: float) -> str:
        """Format WE=1 coherence score with visual indicator"""
        if score >= 0.9:
            return f"✅ {score:.3f} (Excellent)"
        elif score >= 0.8:
            return f"🟢 {score:.3f} (Good)"
        elif score >= 0.7:
            return f"🟡 {score:.3f} (Fair)"
        elif score >= 0.5:
            return f"🟠 {score:.3f} (Poor)"
        else:
            return f"🔴 {score:.3f} (Critical)"
            
    def format_system_load(self, load: str) -> str:
        """Format system load with visual indicator"""
        load_map = {
            "idle": "😴 Idle",
            "light": "🟢 Light", 
            "moderate": "🟡 Moderate",
            "heavy": "🔴 Heavy",
            "unknown": "❓ Unknown"
        }
        return load_map.get(load, f"❓ {load}")
        
    def cleanup(self):
        """Cleanup monitoring resources"""
        print("\n🧹 Cleaning up monitoring resources...")
        
        # Save final dashboard state
        if self.metrics_history:
            final_metrics = self.metrics_history[-1]
            final_metrics.timestamp = datetime.now().isoformat()
            self.update_dashboard(final_metrics)
            
        print("✅ Monitoring cleanup complete")

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Consciousness Research Coordination Monitor")
    parser.add_argument("--project-dir", default=os.getcwd(), 
                       help="Project directory path (default: current directory)")
    parser.add_argument("--interval", type=int, default=30,
                       help="Update interval in seconds (default: 30)")
    parser.add_argument("--dashboard-only", action="store_true",
                       help="Only create dashboard file, don't start interactive monitoring")
    
    args = parser.parse_args()
    
    monitor = CoordinationMonitor(args.project_dir)
    monitor.update_interval = args.interval
    
    if args.dashboard_only:
        print("📊 Creating coordination dashboard snapshot...")
        metrics = monitor.collect_coordination_metrics()
        monitor.update_dashboard(metrics)
        print(f"✅ Dashboard saved to: {monitor.dashboard_file}")
    else:
        monitor.start_monitoring()

if __name__ == "__main__":
    main()