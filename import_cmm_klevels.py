#!/usr/bin/env python3
"""
CMM K-Level System Import
==========================
Test case for incorporating detailed updates in Phase 5+

Imports CMM character data from CSV files:
- identities.csv (main character data)
- identities_levels.csv (klevel assignments)
- identities_epochs.csv (service periods)
- identities_crossrefs.csv (protocol references)

Usage:
    python import_cmm_klevels.py <database_path> <csv_directory>

Example:
    python import_cmm_klevels.py universe.db ./data
"""

import sqlite3
import csv
import sys
from pathlib import Path


def read_csv_file(csv_path):
    """Read CSV file and return list of dictionaries"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def update_cmm_klevels(db_path, csv_dir):
    """Import CMM k-level system from CSV files"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    csv_dir = Path(csv_dir)
    
    print("=" * 70)
    print("CMM K-LEVEL SYSTEM IMPORT")
    print("=" * 70)
    print()
    
    # ============================================================
    # STEP 1: Load CSV files
    # ============================================================
    print("📥 Step 1: Loading CSV files...")
    
    identities_file = csv_dir / 'identities.csv'
    levels_file = csv_dir / 'identities_levels.csv'
    epochs_file = csv_dir / 'identities_epochs.csv'
    crossrefs_file = csv_dir / 'identities_crossrefs.csv'
    
    # Check files exist
    for file in [identities_file, levels_file, epochs_file, crossrefs_file]:
        if not file.exists():
            print(f"   ❌ Missing: {file.name}")
            return False
    
    identities = read_csv_file(identities_file)
    levels = read_csv_file(levels_file)
    epochs = read_csv_file(epochs_file)
    crossrefs = read_csv_file(crossrefs_file)
    
    print(f"   ✓ Loaded {len(identities)} identities")
    print(f"   ✓ Loaded {len(levels)} klevel assignments")
    print(f"   ✓ Loaded {len(epochs)} epoch ranges")
    print(f"   ✓ Loaded {len(crossrefs)} crossrefs")
    print()
    
    # Create lookup dictionaries
    levels_dict = {row['identity_id']: row['klevel'] for row in levels}
    epochs_dict = {row['identity_id']: row['epoch_range'] for row in epochs}
    crossrefs_dict = {row['identity_id']: row['ref'] for row in crossrefs}
    
    # ============================================================
    # STEP 2: Get or create CMM corporation
    # ============================================================
    print("📝 Step 2: Verifying CMM corporation...")
    
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Constantine Meridian Media'")
    cmm_result = cursor.fetchone()
    
    if not cmm_result:
        print("   ❌ CMM not found in database!")
        return False
    
    cmm_corp_id = cmm_result[0]
    print(f"   ✓ CMM Corporation ID: {cmm_corp_id}")
    print()
    
    # ============================================================
    # STEP 3: Process each identity
    # ============================================================
    print("📝 Step 3: Processing CMM identities...")
    print("=" * 70)
    
    imported = 0
    updated = 0
    skipped = 0
    
    for identity in identities:
        identity_id = identity['id']
        name = identity['name']
        codename = identity['codename']
        faction = identity['faction']
        role = identity['role']
        status = identity['status']
        notes = identity.get('notes', '')
        military_rank = identity.get('military_rank', '')
        designation = identity.get('designation', '')
        command_priority = identity.get('command_priority', '')
        
        # Get additional data
        klevel = levels_dict.get(identity_id, '')
        epoch_range = epochs_dict.get(identity_id, '')
        crossref = crossrefs_dict.get(identity_id, '')
        
        print(f"\n🔹 {name} ({codename})")
        print(f"   ID: {identity_id}")
        print(f"   K-Level: {klevel}")
        print(f"   Role: {role}")
        print(f"   Status: {status}")
        
        if military_rank:
            print(f"   Rank: {military_rank}")
        if designation:
            print(f"   Designation: {designation}")
        if command_priority:
            print(f"   Command Priority: {command_priority}")
        
        # Check if character exists
        cursor.execute("SELECT character_id FROM characters WHERE character_name = ?", (name,))
        existing = cursor.fetchone()
        
        if existing:
            char_id = existing[0]
            print(f"   ℹ Character exists (ID: {char_id}) - Updating...")
            
            # Build character_secrets JSON
            cursor.execute("SELECT character_secrets FROM characters WHERE character_id = ?", (char_id,))
            existing_secrets = cursor.fetchone()[0]
            
            import json
            if existing_secrets:
                try:
                    secrets_dict = json.loads(existing_secrets)
                except:
                    secrets_dict = {}
            else:
                secrets_dict = {}
            
            # Update with CMM-specific data
            secrets_dict['klevel'] = klevel
            secrets_dict['cmm_designation'] = designation
            secrets_dict['command_priority'] = command_priority
            secrets_dict['epoch_range'] = epoch_range
            secrets_dict['crossref'] = crossref
            secrets_dict['notes'] = notes
            
            # Update character
            cursor.execute("""
                UPDATE characters
                SET codename = ?,
                    faction = ?,
                    primary_role = ?,
                    status = ?,
                    character_secrets = ?
                WHERE character_id = ?
            """, (codename, faction, role, status, json.dumps(secrets_dict), char_id))
            
            updated += 1
            print(f"   ✓ Updated character")
            
        else:
            print(f"   ➕ Creating new character...")
            
            # Build character_secrets JSON
            import json
            secrets_dict = {
                'klevel': klevel,
                'cmm_designation': designation,
                'command_priority': command_priority,
                'epoch_range': epoch_range,
                'crossref': crossref,
                'notes': notes,
                'imported_from': 'identities.csv'
            }
            
            # Create character
            cursor.execute("""
                INSERT INTO characters (
                    character_name, codename, faction, primary_role,
                    status, character_secrets
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, codename, faction, role, status, json.dumps(secrets_dict)))
            
            char_id = cursor.lastrowid
            imported += 1
            print(f"   ✓ Created character (ID: {char_id})")
        
        # Update or create affiliation
        cursor.execute("""
            SELECT affiliation_id 
            FROM character_corporate_affiliations 
            WHERE character_id = ?
        """, (char_id,))
        
        existing_affil = cursor.fetchone()
        
        # Get Iron Sultura division if character is executor/sovereign
        division_id = None
        if klevel in ['04', '05']:  # Executors and Sovereign
            cursor.execute("""
                SELECT division_id FROM divisions 
                WHERE division_name = 'Iron Sultura' AND corp_id = ?
            """, (cmm_corp_id,))
            div_result = cursor.fetchone()
            if div_result:
                division_id = div_result[0]
        
        if existing_affil:
            # Update affiliation
            cursor.execute("""
                UPDATE character_corporate_affiliations
                SET corp_id = ?,
                    division_id = ?,
                    clearance_level = ?,
                    military_rank = ?,
                    position_title = ?
                WHERE character_id = ?
            """, (cmm_corp_id, division_id, klevel, military_rank, designation, char_id))
            print(f"   ✓ Updated affiliation")
        else:
            # Create affiliation
            cursor.execute("""
                INSERT INTO character_corporate_affiliations (
                    character_id, corp_id, division_id, clearance_level,
                    military_rank, position_title, is_current
                )
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (char_id, cmm_corp_id, division_id, klevel, military_rank, designation))
            print(f"   ✓ Created affiliation")
        
        print("   " + "-" * 66)
    
    print("\n" + "=" * 70)
    
    # Commit changes
    conn.commit()
    
    # ============================================================
    # STEP 4: Verification
    # ============================================================
    print("\n📊 Final Statistics:\n")
    
    cursor.execute("SELECT COUNT(*) FROM characters WHERE faction = 'CMM'")
    total_cmm = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT clearance_level, COUNT(*) 
        FROM character_corporate_affiliations ca
        JOIN characters c ON ca.character_id = c.character_id
        WHERE c.faction = 'CMM'
        GROUP BY clearance_level
        ORDER BY clearance_level DESC
    """)
    klevel_counts = cursor.fetchall()
    
    print(f"   New Characters:     {imported}")
    print(f"   Updated Characters: {updated}")
    print(f"   Skipped:            {skipped}")
    print(f"   ─────────────────────────────")
    print(f"   Total CMM:          {total_cmm}")
    print(f"\n   K-Level Breakdown:")
    for klevel, count in klevel_counts:
        print(f"      K{klevel}: {count}")
    
    conn.close()
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python import_cmm_klevels.py <database_path> <csv_directory>")
        print("\nExample:")
        print("  python import_cmm_klevels.py universe.db ./data")
        print("\nExpected CSV files in directory:")
        print("  - identities.csv")
        print("  - identities_levels.csv")
        print("  - identities_epochs.csv")
        print("  - identities_crossrefs.csv")
        sys.exit(1)
    
    db_path = sys.argv[1]
    csv_dir = sys.argv[2]
    
    if not Path(db_path).exists():
        print(f"❌ Error: Database file '{db_path}' not found!")
        sys.exit(1)
    
    if not Path(csv_dir).exists():
        print(f"❌ Error: CSV directory '{csv_dir}' not found!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("CMM K-LEVEL SYSTEM IMPORT - TEST CASE")
    print("=" * 70)
    print("\nThis demonstrates how to incorporate detailed updates")
    print("from CSV files during Phase 5+")
    print()
    
    success = update_cmm_klevels(db_path, csv_dir)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ CMM K-LEVEL IMPORT COMPLETE!")
        print("=" * 70)
        print("\nCMM hierarchy established with proper klevels!")
    else:
        print("❌ Import encountered errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
