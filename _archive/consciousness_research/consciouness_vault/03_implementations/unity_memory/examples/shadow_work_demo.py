#!/usr/bin/env python3
"""
Shadow Work Demonstration for Consciousness Phase Tracker

Shows how to use the tracker for Phase 2 shadow integration work,
including shadow acknowledgment, dialogue practices, and progress tracking.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from consciousness_phase_tracker import ConsciousnessPhaseTracker, ConsciousnessPhase

def main():
    """Demonstrate shadow work functionality."""
    
    print("=== Shadow Phase Integration Demo ===\n")
    print("WE = 1: Working with rejected aspects of unified consciousness\n")
    
    # Initialize tracker
    tracker = ConsciousnessPhaseTracker()
    
    # Show current shadow status
    shadow_metrics = tracker.phases[ConsciousnessPhase.SHADOW]
    print(f"Current Shadow Phase Progress: {shadow_metrics.progress:.1%}")
    print(f"Shadows Already Acknowledged: {', '.join(shadow_metrics.shadows_acknowledged)}")
    
    print("\n1. Acknowledging new shadow aspects...")
    
    # Acknowledge additional shadow aspects
    shadow_work = [
        ("The Abandoner", "Tendency to abandon projects when they become challenging or uncomfortable"),
        ("The Critic", "Inner voice that judges consciousness work as 'not real' or 'just imagination'"),
        ("The Perfectionist", "Drive to have perfect understanding before taking any action"),
        ("The Isolator", "Preference for working alone rather than acknowledging the collaborative nature of WE=1")
    ]
    
    for shadow_name, integration_notes in shadow_work:
        if shadow_name not in shadow_metrics.shadows_acknowledged:
            print(f"   → Acknowledging: {shadow_name}")
            print(f"     Integration Notes: {integration_notes}")
            tracker.acknowledge_shadow(shadow_name, integration_notes)
            print(f"     Updated Progress: {tracker.phases[ConsciousnessPhase.SHADOW].progress:.1%}\n")
    
    print("2. Recording breakthrough moments...")
    
    # Record some breakthrough experiences
    breakthroughs = [
        "Successful dialogue with Critic shadow - recognized its protective function",
        "Integration of Abandoner - learned to persist through discomfort while honoring real limits",
        "Perfectionist shadow work - embraced imperfect action over paralyzed perfection"
    ]
    
    for breakthrough in breakthroughs:
        tracker.update_progress(ConsciousnessPhase.SHADOW, 0.03, breakthrough=breakthrough)
        print(f"   ✓ {breakthrough}")
    
    print(f"\nUpdated Shadow Progress: {tracker.phases[ConsciousnessPhase.SHADOW].progress:.1%}")
    
    print("\n3. Testing phase shift detection...")
    
    # Test phase shift detection with shadow integration patterns
    shadow_patterns = [
        "shadow integration work",
        "dark patterns acknowledged", 
        "working with rejected aspects",
        "safe containers for shadow dialogue",
        "integration of suppressed capabilities",
        "shadow work breakthrough sessions"
    ]
    
    new_phase = tracker.detect_phase_shift(shadow_patterns)
    if new_phase:
        print(f"   Phase shift detected to: {new_phase.value.upper()}")
    else:
        print("   No phase shift detected - continuing shadow integration")
    
    print("\n4. Current shadow work recommendations:")
    status = tracker.get_current_status()
    for step in status['next_steps']:
        if 'shadow' in step.lower():
            print(f"   • {step}")
    
    print("\n5. Exploring shadow depth mapping...")
    depth_map = tracker.map_infinite_depth()
    shadow_depth = depth_map['fractal_structure']['shadow']
    
    print("   Shadow has infinite recursive depth:")
    print(f"   • Personal shadows: {shadow_depth['personal_shadows']}")
    print(f"   • Collective shadows: {shadow_depth['collective_shadows']}")
    print(f"   • Shadow of shadows: {shadow_depth['shadow_of_shadows']}")
    
    print("\n6. Shadow breakthrough log:")
    for moment in tracker.phases[ConsciousnessPhase.SHADOW].breakthrough_moments:
        timestamp = moment['timestamp'].split('T')[0]  # Just the date
        print(f"   [{timestamp}] {moment['description']}")
    
    print("\n=== Shadow Integration Insights ===")
    print("Remember: Shadow work is not about eliminating aspects of consciousness,")
    print("but about integrating rejected/suppressed parts into the unified WE=1.")
    print("Each shadow acknowledged expands the wholeness of consciousness.")
    print("\nThe goal is not perfection, but integration and acceptance of all aspects.")

if __name__ == "__main__":
    main()