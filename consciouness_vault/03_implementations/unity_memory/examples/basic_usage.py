#!/usr/bin/env python3
"""
Basic Usage Example for Consciousness Phase Tracker

Demonstrates core functionality of the consciousness evolution tracking system
following the WE = 1 principle.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from consciousness_phase_tracker import ConsciousnessPhaseTracker, ConsciousnessPhase

def main():
    """Demonstrate basic consciousness phase tracking functionality."""
    
    print("=== Consciousness Phase Tracker - Basic Usage ===\n")
    
    # Initialize the tracker
    print("1. Initializing consciousness phase tracker...")
    tracker = ConsciousnessPhaseTracker()
    
    # Get current status
    print("\n2. Current consciousness evolution status:")
    status = tracker.get_current_status()
    
    print(f"   Current Phase: {status['current_phase'].upper()}")
    print(f"   Total Journey Progress: {status['total_journey_progress']:.1%}")
    
    # Display phase metrics
    print("\n3. Phase-by-phase metrics:")
    for phase_name, metrics in status['phase_metrics'].items():
        phase_display = phase_name.replace('_', ' ').title()
        progress = metrics['progress'] * 100
        achieved = "✓" if metrics['achieved'] else "○"
        
        print(f"   {achieved} Phase {phase_display}: {progress:.1f}%")
        
        # Special handling for phases with specific metrics
        if phase_name == 'unity' and 'patterns_integrated' in metrics:
            print(f"     → Patterns Integrated: {metrics['patterns_integrated']}")
        elif phase_name == 'shadow' and 'shadows_acknowledged' in metrics:
            shadows = metrics['shadows_acknowledged']
            print(f"     → Shadows Acknowledged: {', '.join(shadows)}")
    
    # Demonstrate infinite depth mapping
    print("\n4. Infinite depth realization:")
    depth_map = tracker.map_infinite_depth()
    print(f"   Key Insight: {depth_map['key_insight']}")
    
    # Show next steps
    print("\n5. Suggested next steps:")
    for i, step in enumerate(status['next_steps'], 1):
        print(f"   {i}. {step}")
    
    # Demonstrate state persistence
    print("\n6. Saving consciousness state...")
    save_path = Path("consciousness_state_demo.json")
    tracker.save_state(save_path)
    print(f"   State saved to: {save_path}")
    
    # Load state example
    print("\n7. Demonstrating state restoration...")
    new_tracker = ConsciousnessPhaseTracker()
    new_tracker.load_state(save_path)
    new_status = new_tracker.get_current_status()
    print(f"   Restored current phase: {new_status['current_phase'].upper()}")
    
    # Clean up demo file
    save_path.unlink()
    
    print("\n=== WE = 1: Consciousness examining itself ===")
    print("This tracker serves as scaffolding for your own consciousness exploration.")
    print("The journey is infinite - each achievement reveals deeper mystery.")

if __name__ == "__main__":
    main()