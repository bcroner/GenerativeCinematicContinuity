#!/bin/bash
# =============================================================================
# Master Automation Setup Script for GCC Platform Repositories
# Usage: ./setup.sh
# =============================================================================

# Exit immediately if an execution pipeline command encounters an error
set -e

echo "================================================================="
echo "   GCC Platform Automation Onboarding Infrastructure Toolchain   "
echo "================================================================="

# 1. Check for basic host development requirements
echo -e "\n[Verification Pass]: Auditing runtime dependencies..."
for cmd in python3 g++ cmake; do
    if ! command -v $cmd &> /dev/null; then
        echo "  [Critical Error]: Required dependencies '$cmd' missing from host path system environment."
        exit 1
    fi
done
echo "  -> System packages verified successfully."

# 2. Build explicit directory matrices
echo -e "\n[Structural Matrix]: Generating required deployment directory paths..."
mkdir -p profiles environments docs unity_project/Assets/Scripts
echo "  -> Directory footprint initialized."

# 3. Compile Shared C++ Multi-Threaded Validation Libraries
SOURCE_FILE="DimacsParser.cpp"
if [ -f "$SOURCE_FILE" ]; then
    echo -e "\n[Compilation Pipeline]: Building native constraint acceleration binaries..."
    OS_TYPE="$(uname -s 2>/dev/null || echo "Windows")"
    
    if ] || [[ "$OS_TYPE" == *"MINGW"* ]]; then
        g++ -O3 -shared -std=c++11 "$SOURCE_FILE" -o libverification.dll
        echo "  -> Compiled Windows production target: libverification.dll"
    else
        g++ -O3 -shared -fPIC -std=c++11 "$SOURCE_FILE" -o libverification.dylib
        echo "  -> Compiled macOS production target: libverification.dylib"
    fi
else
    echo -e "\n[Compilation Skipped]: Core verification asset '$SOURCE_FILE' missing. Skipping library optimization steps."
fi

# 4. Final verification checklist compilation
echo -e "\n================================================================="
echo "    Setup Optimization Pass Successful. Platform Ready to Arm.   "
echo "================================================================="
echo "  1. Double-click 'visual_storyboard.html' to design character nodes."
echo "  2. Drag generated JSON arrays directly into the './profiles' path."
echo "  3. Launch your backend execution daemon via: python3 gcc_narrative_engine.py"
echo "================================================================="
