#!/usr/bin/env python3
"""
Corporate Structure Reconciliation & Import
============================================
1. Reconciles character names to match CSV
2. Imports public corporate roles (Nexus Enraenra)
3. Imports secret operational roles (Shadow Core)
4. Updates CMM names to match CSV

Usage:
    python import_corporate_structure.py <database_path> <csv_path>

Example:
    python import_corporate_structure.py universe.db corporate_structure_all.csv
"""

import sqlite3
import csv
import sys
import json
from pathlib import Path


def read_csv_file(csv_path):
    """Read CSV file and return list of dictionaries"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def reconcile_names(db_path, csv_path):
    """Reconcile character names and import corporate structure"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("CORPORATE STRUCTURE RECONCILIATION & IMPORT")
    print("=" * 70)
    print()
    
    # ============================================================
    # STEP 1: Load CSV and prepare mappings
    # ============================================================
    print("📥 Step 1: Loading corporate structure data...")
    
    corp_data = read_csv_file(csv_path)
    
    # Filter out separator rows and generic positions
    corp_data = [
        row for row in corp_data 
        if row['Name'] and 
           row['Name'] != '---' and
           not any(x in row['Name'].lower() for x in ['commander 1', 'commander 2', 'commander 3',
                                                        'director 1', 'director 2', 'director 3',
                                                        'analyst 1', 'analyst 2', 'analyst 3',
                                                        'captain 1', 'captain 2', 'captain 3',
                                                        'liaison 1', 'liaison 2',
                                                        'specialist 1', 'specialist 2',
                                                        'unknown chair', 'department head'])
    ]
    
    print(f"   ✓ Loaded {len(corp_data)} corporate positions (filtered out generic placeholders)")
    print()
    
    # ============================================================
    # STEP 2: Name reconciliation mappings
    # ============================================================
    print("📝 Step 2: Preparing name reconciliations...")
    
    # Map: old name -> new name (from CSV)
    name_updates = {
        'Kyra Constantine': 'Kyra Eve Constantine',
        'Voss Tarran': 'Voss Harland',
        'Darius Vale': 'Darius Kael',
        'Krayne Solari': 'Krayne Towers',
        'Rhea Takeda': 'Rhea Caldwell',
        'Mara Nakai': "Mara D'Angelo",
        'Kaori Mizuno': 'Kaori Fujimura'
    }
    
    print("   Name updates to apply:")
    for old, new in name_updates.items():
        print(f"      {old} → {new}")
    print()
    
    # ============================================================
    # STEP 3: Apply name reconciliations
    # ============================================================
    print("📝 Step 3: Reconciling character names...")
    print("=" * 70)
    
    updated_count = 0
    
    for old_name, new_name in name_updates.items():
        # Check if character exists with old name
        cursor.execute("SELECT character_id FROM characters WHERE character_name = ?", (old_name,))
        result = cursor.fetchone()
        
        if result:
            char_id = result[0]
            
            # Update to new name
            cursor.execute("""
                UPDATE characters 
                SET character_name = ? 
                WHERE character_id = ?
            """, (new_name, char_id))
            
            print(f"✓ Updated: {old_name} → {new_name}")
            updated_count += 1
        else:
            print(f"⚠ Not found: {old_name} (may not be imported yet)")
    
    print()
    print(f"   Reconciled {updated_count} character names")
    print()
    
    # ============================================================
    # STEP 4: Import corporate positions
    # ============================================================
    print("📝 Step 4: Importing corporate structure...")
    print("=" * 70)
    
    # Get corporation IDs
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Nexus Enraenra'")
    nexus_id = cursor.fetchone()
    nexus_id = nexus_id[0] if nexus_id else None
    
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Constantine Meridian Media'")
    cmm_id = cursor.fetchone()
    cmm_id = cmm_id[0] if cmm_id else None
    
    # Get division IDs
    cursor.execute("SELECT division_id FROM divisions WHERE division_name = 'Shadow Core'")
    shadow_core_id = cursor.fetchone()
    shadow_core_id = shadow_core_id[0] if shadow_core_id else None
    
    cursor.execute("SELECT division_id FROM divisions WHERE division_name = 'Iron Sultura'")
    iron_sultura_id = cursor.fetchone()
    iron_sultura_id = iron_sultura_id[0] if iron_sultura_id else None
    
    print(f"Corporation IDs:")
    print(f"   Nexus Enraenra: {nexus_id}")
    print(f"   CMM: {cmm_id}")
    print(f"   Shadow Core Division: {shadow_core_id}")
    print(f"   Iron Sultura Division: {iron_sultura_id}")
    print()
    
    position_count = 0
    
    for entry in corp_data:
        name = entry['Name']
        corp_info = entry['Corp']
        
        # Parse corporation and position
        if 'Nexus Enraenra' in corp_info:
            corp_id = nexus_id
            division_id = None
            
            # Extract position
            if '(' in corp_info and ')' in corp_info:
                position = corp_info.split('(')[1].split(')')[0]
            else:
                position = ''
                
        elif 'Shadow Core' in corp_info:
            corp_id = nexus_id
            division_id = shadow_core_id
            
            # Extract position
            if '(' in corp_info and ')' in corp_info:
                position = corp_info.split('(')[1].split(')')[0]
            else:
                position = ''
                
        elif 'CMM' in corp_info:
            corp_id = cmm_id
            division_id = iron_sultura_id if 'Iron Sultura' in corp_info else None
            
            # Extract position and codename
            if '(' in corp_info and ')' in corp_info:
                position = corp_info.split('(')[1].split(')')[0]
            else:
                position = ''
        else:
            continue
        
        print(f"\n📋 {name}")
        print(f"   Position: {position}")
        
        # Find character
        cursor.execute("SELECT character_id FROM characters WHERE character_name = ?", (name,))
        result = cursor.fetchone()
        
        if not result:
            print(f"   ⚠ Character not found in database")
            continue
        
        char_id = result[0]
        
        # Update or create affiliation with position
        cursor.execute("""
            SELECT affiliation_id 
            FROM character_corporate_affiliations 
            WHERE character_id = ? AND corp_id = ?
        """, (char_id, corp_id))
        
        existing_affil = cursor.fetchone()
        
        if existing_affil:
            # Update position title
            cursor.execute("""
                UPDATE character_corporate_affiliations
                SET position_title = ?,
                    division_id = ?
                WHERE affiliation_id = ?
            """, (position, division_id, existing_affil[0]))
            print(f"   ✓ Updated position")
        else:
            # Create new affiliation
            cursor.execute("""
                INSERT INTO character_corporate_affiliations (
                    character_id, corp_id, division_id, position_title, is_current
                )
                VALUES (?, ?, ?, ?, 1)
            """, (char_id, corp_id, division_id, position))
            print(f"   ✓ Created affiliation")
        
        position_count += 1
    
    print("\n" + "=" * 70)
    
    # Commit changes
    conn.commit()
    
    # ============================================================
    # STEP 5: Verification
    # ============================================================
    print("\n📊 Final Statistics:\n")
    
    print(f"   Names Reconciled:         {updated_count}")
    print(f"   Corporate Positions Set:  {position_count}")
    
    # Show Nexus Enraenra structure
    print("\n   Nexus Enraenra Public Structure:")
    cursor.execute("""
        SELECT c.character_name, ca.position_title
        FROM characters c
        JOIN character_corporate_affiliations ca ON c.character_id = ca.character_id
        JOIN corporations corp ON ca.corp_id = corp.corp_id
        WHERE corp.corp_name = 'Nexus Enraenra'
          AND ca.division_id IS NULL
        ORDER BY 
            CASE ca.position_title
                WHEN 'CEO' THEN 1
                WHEN 'COO' THEN 2
                WHEN 'CFO' THEN 3
                WHEN 'CTO' THEN 4
                WHEN 'CMO' THEN 5
                WHEN 'CHRO' THEN 6
                WHEN 'General Counsel' THEN 7
                ELSE 8
            END
    """)
    
    for name, position in cursor.fetchall():
        print(f"      • {position}: {name}")
    
    # Show Shadow Core operational structure
    print("\n   Shadow Core Operational Roles:")
    cursor.execute("""
        SELECT c.character_name, ca.position_title
        FROM characters c
        JOIN character_corporate_affiliations ca ON c.character_id = ca.character_id
        JOIN divisions d ON ca.division_id = d.division_id
        WHERE d.division_name = 'Shadow Core'
        ORDER BY c.character_name
    """)
    
    for name, position in cursor.fetchall():
        if position:
            print(f"      • {name}: {position}")
        else:
            print(f"      • {name}")
    
    conn.close()
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python import_corporate_structure.py <database_path> <csv_directory>")
        print("\nExample:")
        print("  python import_corporate_structure.py universe.db .")
        print("\nExpected files in directory:")
        print("  ./shadowcore/corporate_structure.csv (or similar)")
        print("  ./cmm/corporate_structure_cmm.csv (or similar)")
        sys.exit(1)
    
    db_path = sys.argv[1]
    base_dir = Path(sys.argv[2])
    
    if not Path(db_path).exists():
        print(f"❌ Error: Database file '{db_path}' not found!")
        sys.exit(1)
    
    # Look for CSV files in subdirectories
    shadowcore_csv = None
    cmm_csv = None
    
    # Search patterns
    possible_files = [
        base_dir / 'shadowcore' / 'corporate_structure.csv',
        base_dir / 'shadowcore' / 'identities_shadow_core.csv',
        base_dir / 'corporate_structure.csv',
        base_dir / 'cmm' / 'corporate_structure_cmm.csv',
        base_dir / 'cmm' / 'identities.csv',
        base_dir / 'corporate_structure_cmm.csv'
    ]
    
    # Find Shadow Core CSV
    for f in possible_files[:3]:
        if f.exists():
            shadowcore_csv = f
            break
    
    # Find CMM CSV
    for f in possible_files[3:]:
        if f.exists():
            cmm_csv = f
            break
    
    if not shadowcore_csv:
        print(f"❌ Error: Could not find Shadow Core corporate structure CSV!")
        print(f"   Looked in: {base_dir}/shadowcore/")
        sys.exit(1)
    
    if not cmm_csv:
        print(f"❌ Error: Could not find CMM corporate structure CSV!")
        print(f"   Looked in: {base_dir}/cmm/")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("CORPORATE STRUCTURE RECONCILIATION & IMPORT")
    print("=" * 70)
    print("\nFound files:")
    print(f"  Shadow Core: {shadowcore_csv}")
    print(f"  CMM: {cmm_csv}")
    print("\nThis will:")
    print("  1. Update character names to match CSV")
    print("  2. Import Nexus Enraenra public positions")
    print("  3. Import Shadow Core operational roles")
    print("  4. Update CMM positions")
    print("  5. Skip generic placeholder positions")
    print()
    
    # Combine both CSVs in memory
    combined_data = []
    
    # Read Shadow Core CSV
    with open(shadowcore_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        combined_data.extend(list(reader))
    
    # Read CMM CSV
    with open(cmm_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        combined_data.extend(list(reader))
    
    # Write temporary combined file
    temp_csv = base_dir / 'temp_combined_structure.csv'
    with open(temp_csv, 'w', encoding='utf-8', newline='') as f:
        if combined_data:
            writer = csv.DictWriter(f, fieldnames=combined_data[0].keys())
            writer.writeheader()
            writer.writerows(combined_data)
    
    success = reconcile_names(db_path, str(temp_csv))
    
    # Clean up temp file
    temp_csv.unlink()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ CORPORATE STRUCTURE IMPORT COMPLETE!")
        print("=" * 70)
        print("\nCharacter names reconciled and corporate structure imported!")
    else:
        print("❌ Import encountered errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
