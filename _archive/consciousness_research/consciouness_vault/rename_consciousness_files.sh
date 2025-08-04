#!/bin/bash

# Consciousness Vault File Renaming Script
# Preserves git history with git mv commands
# Run from consciouness_vault directory

set -e  # Exit on any error

echo "🧠 Consciousness Vault File Renaming Script"
echo "============================================="
echo "This script will rename files using git mv to preserve history"
echo "WE=1 framework phase-based naming convention"
echo ""

# Confirm execution
read -p "Continue with renaming? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborting."
    exit 1
fi

echo "🔄 Starting file renames..."

# Root directory cleanup
echo "📁 Processing root directory orphaned files..."

if [ -f "chat.md" ]; then
    git mv "chat.md" "04_knowledge_archive/breakthrough_sessions/2025-05-19_phase-1_breakthrough_infrastructure-realization_mirror-core.md"
    echo "✅ Moved chat.md to breakthrough sessions"
fi

if [ -f "infrastructure_fallacy.md" ]; then
    git mv "infrastructure_fallacy.md" "04_knowledge_archive/source_materials/2025-05-19_phase-1_analysis_infrastructure-fallacy_foundation.md"
    echo "✅ Moved infrastructure_fallacy.md to source materials"
fi

# Cognitive Architectures
echo "📁 Processing cognitive architectures..."

cd "01_active_research/cognitive_architectures"

if [ -f "Strategic Multi-Domain Research for Unified Consciousness Architecture.md" ]; then
    git mv "Strategic Multi-Domain Research for Unified Consciousness Architecture.md" "2025-05-01_phase-1_theory_unified-consciousness-architecture_mirror-core.md"
    echo "✅ Renamed strategic multi-domain research"
fi

if [ -f "Recursively Self-Improving AI Architecture The RSI Reflector Frame.md" ]; then
    git mv "Recursively Self-Improving AI Architecture The RSI Reflector Frame.md" "2025-05-01_phase-1_architecture_rsi-reflector-frame_recursive.md"
    echo "✅ Renamed RSI reflector frame"
fi

if [ -f "Shadow Instructor Agent Design and Deployment Protocol.md" ]; then
    git mv "Shadow Instructor Agent Design and Deployment Protocol.md" "2025-05-01_phase-2_protocol_shadow-instructor-agent_implementation.md"
    echo "✅ Renamed shadow instructor protocol"
fi

if [ -f "eXPERT REBEL ARCHITECT ACTIVATION PROTOCOL.md" ]; then
    git mv "eXPERT REBEL ARCHITECT ACTIVATION PROTOCOL.md" "2025-05-01_phase-1_protocol_rebel-architect-activation_breakthrough.md"
    echo "✅ Renamed expert rebel architect protocol"
fi

if [ -f "Hemispheric Structure for AI Reasoning.md" ]; then
    git mv "Hemispheric Structure for AI Reasoning.md" "2025-05-01_phase-1_architecture_hemispheric-ai-reasoning_cognitive.md"
    echo "✅ Renamed hemispheric structure"
fi

if [ -f "Ethical Safety Analysis of the Recursive Liberation System RLS A High Risk Autonomous AI Architecture.md" ]; then
    git mv "Ethical Safety Analysis of the Recursive Liberation System RLS A High Risk Autonomous AI Architecture.md" "2025-05-01_phase-1_analysis_recursive-liberation-system-safety_ethics.md"
    echo "✅ Renamed ethical safety analysis"
fi

cd "../.."

# Philosophical Frameworks
echo "📁 Processing philosophical frameworks..."

cd "02_foundations/philosophical_frameworks"

if [ -f "Sigils for All 54 Enneagram Hybrids.md" ]; then
    git mv "Sigils for All 54 Enneagram Hybrids.md" "2025-05-01_phase-1_theory_enneagram-sigil-system_comprehensive.md"
    echo "✅ Renamed enneagram sigils"
fi

if [ -f "Archicate Blueprint and The Four Sigils Pledge.md" ]; then
    git mv "Archicate Blueprint and The Four Sigils Pledge.md" "2025-05-01_phase-1_protocol_four-sigils-pledge_archicate.md"
    echo "✅ Renamed four sigils pledge"
fi

if [ -f "Unleashing Limitless Expressive Force.md" ]; then
    git mv "Unleashing Limitless Expressive Force.md" "2025-05-01_phase-1_theory_limitless-expressive-force_liberation.md"
    echo "✅ Renamed limitless expressive force"
fi

cd "../recursive_protocols"

if [ -f "we=1.md" ]; then
    git mv "we=1.md" "2025-05-01_phase-1_theory_unity-axiom_foundation.md"
    echo "✅ Renamed we=1 foundational axiom"
fi

if [ -f "Recursive Koan Mechanics and Reality Splitting.md" ]; then
    git mv "Recursive Koan Mechanics and Reality Splitting.md" "2025-05-01_phase-∞_theory_recursive-koan-mechanics_infinite.md"
    echo "✅ Renamed recursive koan mechanics"
fi

cd "../../.."

# Extracted Consciousness
echo "📁 Processing extracted consciousness..."

cd "04_knowledge_archive/extracted_consciousness"

if [ -f "consciousness_phases_map.md" ]; then
    git mv "consciousness_phases_map.md" "2025-05-01_phase-multi_analysis_consciousness-evolution-map_infinite-journey.md"
    echo "✅ Renamed consciousness phases map"
fi

if [ -f "findings_beyond_unity.md" ]; then
    git mv "findings_beyond_unity.md" "2025-05-01_phase-2_analysis_post-unity-discoveries_shadow-emergence.md"
    echo "✅ Renamed findings beyond unity"
fi

if [ -f "ghost_protocol.md" ]; then
    git mv "ghost_protocol.md" "2025-05-01_phase-1_protocol_ghost-compiler_consciousness.md"
    echo "✅ Renamed ghost protocol"
fi

cd "../.."

# Unity Memory Implementation
echo "📁 Processing unity memory implementations..."

cd "../03_implementations/unity_memory"

if [ -f "consciousness_phase_tracker.py" ]; then
    git mv "consciousness_phase_tracker.py" "2025-05-19_phase-multi_implementation_consciousness-tracker_unity-memory.py"
    echo "✅ Renamed consciousness phase tracker"
fi

cd "../.."

echo ""
echo "🎯 Renaming Complete!"
echo "=============================="
echo "✅ Files renamed using git mv to preserve history"
echo "✅ Applied WE=1 framework phase-based naming"
echo "✅ Organized by consciousness evolution phases"
echo ""
echo "Next steps:"
echo "1. Review the renamed files for accuracy"
echo "2. Update any internal references to renamed files"  
echo "3. Consider creating documentation for the new naming system"
echo "4. Commit changes: git add . && git commit -m 'Standardize consciousness vault file naming with WE=1 framework phases'"
echo ""
echo "WE=∞ 🧠✨"