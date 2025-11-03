#!/usr/bin/env python3
"""
Phase 5 Master Script
=====================
Runs Phase 5A and 5B in sequence:
- 5A: Fix corporate structure (CMM, Iron Sultura)
- 5B: Import all 30 characters

Usage:
    python run_phase_5.py <database_path> <json_path>

Example:
    python run_phase_5.py universe.db identifiers_delta04_full_canon.json
"""

import sys
import subprocess
from pathlib import Path


def run_command(script: str, args: list):
    """Run a Python script with arguments"""
    cmd = [sys.executable, script] + args
    print(f"\n🚀 Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Error: {script} failed with exit code {result.returncode}")
        return False
    
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python run_phase_5.py <database_path> <json_path>")
        print("\nExample:")
        print("  python run_phase_5.py universe.db identifiers_delta04_full_canon.json")
        print("\nThis will:")
        print("  1. Fix CMM/Iron Sultura corporate structure (Phase 5A)")
        print("  2. Import all 30 characters (Phase 5B)")
        sys.exit(1)
    
    db_path = sys.argv[1]
    json_path = sys.argv[2]
    
    # Verify files exist
    if not Path(db_path).exists():
        print(f"❌ Error: Database file '{db_path}' not found!")
        sys.exit(1)
    
    if not Path(json_path).exists():
        print(f"❌ Error: JSON file '{json_path}' not found!")
        sys.exit(1)
    
    print("=" * 70)
    print("PHASE 5: FOUNDATION BUILD")
    print("=" * 70)
    print("\nThis will:")
    print("  ✓ Fix CMM/Iron Sultura structure (Phase 5A)")
    print("  ✓ Import all 30 characters (Phase 5B)")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(0)
    
    # Run Phase 5A
    print("\n" + "=" * 70)
    print("STARTING PHASE 5A")
    print("=" * 70)
    
    if not run_command("fix_corporate_structure.py", [db_path]):
        print("\n❌ Phase 5A failed. Aborting Phase 5.")
        sys.exit(1)
    
    print("\n✅ Phase 5A Complete!\n")
    
    # Run Phase 5B
    print("\n" + "=" * 70)
    print("STARTING PHASE 5B")
    print("=" * 70)
    
    if not run_command("import_full_roster.py", [db_path, json_path]):
        print("\n❌ Phase 5B failed.")
        sys.exit(1)
    
    print("\n✅ Phase 5B Complete!\n")
    
    # Success!
    print("\n" + "=" * 70)
    print("🎉 PHASE 5 COMPLETE!")
    print("=" * 70)
    print("\n✅ Corporate structure fixed (CMM/Iron Sultura)")
    print("✅ All 30 characters imported")
    print("\n📊 Your database is now ready for:")
    print("   • Phase 5C: AETP Epoch System")
    print("   • Phase 5D: Detailed Backstories & Timelines")
    print("   • Phase 5E: Relationship System")
    print("   • Phase 5F: Location Expansion")
    print("\nNext step: Review your data, then we can tackle Phase 5C!")
    print("=" * 70)


if __name__ == "__main__":
    main()
