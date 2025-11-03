#!/usr/bin/env python3
"""
Master Import Script - Phase 4
Imports top 10 characters with all adjustments

This script:
1. Adds missing corporations (Nexus Enraenra, Aethos Military Group)
2. Imports top 10 characters from JSON
3. Applies special case adjustments
4. Adds Mitsuko Frost manually
5. Verifies everything

Usage:
    python master_import.py [database_name]
    
Default: universe.db
"""

import subprocess
import sys


def run_step(description, script_name, *args):
    """Run a Python script and report results"""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    
    try:
        # Use the same Python interpreter that's running this script
        cmd = [sys.executable, script_name] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    json_file = "identifiers_delta04_full_canon.json"
    
    print("\n" + "="*60)
    print("PHASE 4: MASTER CHARACTER IMPORT")
    print("="*60)
    print(f"Database: {db_path}")
    print(f"JSON File: {json_file}")
    print("="*60)
    
    # Step 1: Add corporations
    if not run_step(
        "Add Missing Corporations",
        "add_corporations.py",
        db_path
    ):
        print("\n✗ Failed to add corporations")
        return 1
    
    # Step 2: Import characters (this will prompt for confirmation)
    print(f"\n{'='*60}")
    print("STEP: Import Top 10 Characters")
    print(f"{'='*60}\n")
    
    # Run json_importer interactively
    result = subprocess.run(
        [sys.executable, "json_importer.py", json_file, db_path]
    )
    
    if result.returncode != 0:
        print("\n✗ Character import cancelled or failed")
        return 1
    
    # Step 3: Apply adjustments
    if not run_step(
        "Apply Post-Import Adjustments",
        "post_import_adjustments.py",
        db_path
    ):
        print("\n✗ Failed to apply adjustments")
        return 1
    
    # Step 4: Verify results
    print(f"\n{'='*60}")
    print("VERIFYING IMPORT RESULTS")
    print(f"{'='*60}\n")
    
    # Count characters
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM characters")
    char_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM corporations")
    corp_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM character_corporate_affiliations")
    aff_count = cursor.fetchone()[0]
    
    print(f"✓ Characters: {char_count}")
    print(f"✓ Corporations: {corp_count}")
    print(f"✓ Affiliations: {aff_count}")
    
    # List imported characters
    print(f"\n{'='*60}")
    print("IMPORTED CHARACTERS")
    print(f"{'='*60}\n")
    
    cursor.execute("""
        SELECT character_name, codename, faction, primary_role, status
        FROM characters
        ORDER BY character_name
    """)
    
    for row in cursor.fetchall():
        name, codename, faction, role, status = row
        code_str = f" ({codename})" if codename else ""
        print(f"  • {name}{code_str}")
        print(f"    Faction: {faction} | Role: {role} | Status: {status}")
        print()
    
    conn.close()
    
    print(f"{'='*60}")
    print("✓ PHASE 4 MASTER IMPORT COMPLETE")
    print(f"{'='*60}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
