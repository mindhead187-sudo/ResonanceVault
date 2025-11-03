#!/usr/bin/env python3
"""
Phase 5A: Fix Corporate Structure
==================================
Corrects the lore issues:
1. Rename "Corporate Memory Management" → "Constantine Meridian Media (CMM)"
2. Make Iron Sultura a division UNDER CMM (not separate)
3. Update character affiliations accordingly
4. Fix Ren Kael's affiliation

Author: Phase 5A Foundation Fix
"""

import sqlite3
import sys
from pathlib import Path


def fix_corporate_structure(db_path: str):
    """Apply all corporate structure fixes"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Phase 5A: Fixing Corporate Structure\n")
    
    # ============================================================
    # STEP 1: Check if CMM exists, if not create it
    # ============================================================
    print("📝 Step 1: Checking for Constantine Meridian Media...")
    
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name LIKE '%Corporate Memory%'")
    old_cmm = cursor.fetchone()
    
    if old_cmm:
        # Rename existing
        print("   ℹ Found 'Corporate Memory Management' - renaming...")
        cursor.execute("""
            UPDATE corporations 
            SET corp_name = 'Constantine Meridian Media',
                mission_statement = 'A ruthless media conglomerate led by Kyra Eve Constantine, dedicated to dismantling Nexus Enraenra through information warfare, cyber operations, and military contracting. Founded in Chicago (2023) as a vehicle for generational vendetta.',
                industry = 'Media & Intelligence',
                sector = 'Information Warfare'
            WHERE corp_id = ?
        """, (old_cmm[0],))
        cmm_id = old_cmm[0]
        print(f"   ✓ Renamed to Constantine Meridian Media (CMM) - ID: {cmm_id}")
    else:
        # Check if CMM already exists
        cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Constantine Meridian Media'")
        existing_cmm = cursor.fetchone()
        
        if existing_cmm:
            cmm_id = existing_cmm[0]
            print(f"   ✓ Constantine Meridian Media already exists - ID: {cmm_id}")
        else:
            # Create new
            print("   ➕ Creating Constantine Meridian Media...")
            cursor.execute("""
                INSERT INTO corporations (
                    corp_name, legal_name, industry, sector,
                    mission_statement, secret_agenda, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                'Constantine Meridian Media',
                'Constantine Meridian Media LLC',
                'Media & Intelligence',
                'Information Warfare',
                'A ruthless media conglomerate led by Kyra Eve Constantine, dedicated to dismantling Nexus Enraenra through information warfare, cyber operations, and military contracting.',
                'Founded in Chicago (2023) as a vehicle for generational vendetta against Reika Frost and Nexus Enraenra.',
                'Active'
            ))
            cmm_id = cursor.lastrowid
            print(f"   ✓ Created Constantine Meridian Media - ID: {cmm_id}")
    
    print(f"   ℹ CMM ID: {cmm_id}\n")
    
    
    # ============================================================
    # STEP 2: Check if Iron Sultura exists as corporation
    # ============================================================
    print("📝 Step 2: Checking Iron Sultura status...")
    
    cursor.execute("SELECT corp_id, corp_name FROM corporations WHERE corp_name LIKE '%Iron Sultura%'")
    iron_sultura = cursor.fetchone()
    
    if iron_sultura:
        print(f"   ⚠ Iron Sultura found as separate corporation (ID: {iron_sultura[0]})")
        print("   ℹ Will need to migrate affiliations and delete...")
        
        # Migrate any affiliations from Iron Sultura corp to CMM
        cursor.execute("""
            UPDATE character_corporate_affiliations 
            SET corp_id = ?
            WHERE corp_id = ?
        """, (cmm_id, iron_sultura[0]))
        
        migrated = cursor.rowcount
        print(f"   ✓ Migrated {migrated} affiliation(s) to CMM")
        
        # Delete Iron Sultura as corporation
        cursor.execute("DELETE FROM corporations WHERE corp_id = ?", (iron_sultura[0],))
        print(f"   ✓ Deleted Iron Sultura as separate corporation")
    else:
        print("   ✓ Iron Sultura not found as corporation (good!)")
    
    print()
    
    
    # ============================================================
    # STEP 3: Create/Update divisions table if needed
    # ============================================================
    print("📝 Step 3: Ensuring divisions table exists...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS divisions (
            division_id INTEGER PRIMARY KEY AUTOINCREMENT,
            division_name TEXT NOT NULL,
            corp_id INTEGER NOT NULL,
            description TEXT,
            leader_character_id INTEGER,
            emblem TEXT,
            headquarters TEXT,
            FOREIGN KEY (corp_id) REFERENCES corporations(corp_id),
            FOREIGN KEY (leader_character_id) REFERENCES characters(character_id)
        )
    """)
    
    print("   ✓ Divisions table ready\n")
    
    
    # ============================================================
    # STEP 4: Create Iron Sultura as division under CMM
    # ============================================================
    print("📝 Step 4: Creating Iron Sultura as CMM division...")
    
    # Check if Iron Sultura division already exists
    cursor.execute("""
        SELECT division_id FROM divisions 
        WHERE division_name = 'Iron Sultura' AND corp_id = ?
    """, (cmm_id,))
    
    existing_division = cursor.fetchone()
    
    if existing_division:
        print(f"   ℹ Iron Sultura division already exists (ID: {existing_division[0]})")
        iron_sultura_div_id = existing_division[0]
    else:
        # Get Kyra's ID for leader_character_id
        cursor.execute("SELECT character_id FROM characters WHERE character_name LIKE '%Kyra%Constantine%'")
        kyra = cursor.fetchone()
        kyra_id = kyra[0] if kyra else None
        
        cursor.execute("""
            INSERT INTO divisions (division_name, corp_id, description, leader_character_id, emblem, headquarters)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Iron Sultura',
            cmm_id,
            'CMM\'s militarized executive board - a ruthless cadre marked by military emblems (Skull, Trident, Shield, Talon, Crescent, Blade) operating from Chicago. Executes Kyra\'s vendetta with brutal precision.',
            kyra_id,
            'Skull, Trident, Shield, Talon, Crescent, Blade',
            'Chicago, USA'
        ))
        
        iron_sultura_div_id = cursor.lastrowid
        print(f"   ✓ Created Iron Sultura division (ID: {iron_sultura_div_id})")
        if kyra_id:
            print(f"   ✓ Assigned Kyra Constantine as leader")
    
    # Also ensure Shadow Core division exists under Nexus Enraenra
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Nexus Enraenra'")
    nexus_result = cursor.fetchone()
    
    if nexus_result:
        nexus_id = nexus_result[0]
        
        cursor.execute("""
            SELECT division_id FROM divisions 
            WHERE division_name = 'Shadow Core' AND corp_id = ?
        """, (nexus_id,))
        
        existing_shadow = cursor.fetchone()
        
        if existing_shadow:
            print(f"   ℹ Shadow Core division already exists (ID: {existing_shadow[0]})")
        else:
            # Get Reika's ID for leader
            cursor.execute("SELECT character_id FROM characters WHERE character_name LIKE '%Reika%Frost%'")
            reika = cursor.fetchone()
            reika_id = reika[0] if reika else None
            
            cursor.execute("""
                INSERT INTO divisions (division_name, corp_id, description, leader_character_id, headquarters)
                VALUES (?, ?, ?, ?, ?)
            """, (
                'Shadow Core',
                nexus_id,
                'Nexus Enraenra\'s covert reaction force - elite operatives marked by unique sigils, operating in shadows to protect corporate interests and maintain global stability.',
                reika_id,
                'Tokyo, Japan'
            ))
            
            shadow_core_id = cursor.lastrowid
            print(f"   ✓ Created Shadow Core division (ID: {shadow_core_id})")
            if reika_id:
                print(f"   ✓ Assigned Reika Frost as leader")
    
    print()
    
    
    # ============================================================
    # STEP 5: Add division_id to character_corporate_affiliations if not exists
    # ============================================================
    print("📝 Step 5: Updating affiliations schema...")
    
    # Check if division_id column exists
    cursor.execute("PRAGMA table_info(character_corporate_affiliations)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'division_id' not in columns:
        cursor.execute("""
            ALTER TABLE character_corporate_affiliations 
            ADD COLUMN division_id INTEGER REFERENCES divisions(division_id)
        """)
        print("   ✓ Added division_id column to character_corporate_affiliations")
    else:
        print("   ℹ division_id column already exists")
    
    print()
    
    
    # ============================================================
    # STEP 6: Update Iron Sultura characters to CMM with division
    # ============================================================
    print("📝 Step 6: Updating Iron Sultura character affiliations...")
    
    # Get Iron Sultura division ID
    cursor.execute("""
        SELECT division_id FROM divisions 
        WHERE division_name = 'Iron Sultura' AND corp_id = ?
    """, (cmm_id,))
    
    iron_sultura_div = cursor.fetchone()
    
    if iron_sultura_div:
        iron_sultura_div_id = iron_sultura_div[0]
        
        # Find characters with faction = 'Iron Sultura'
        cursor.execute("""
            SELECT character_id, character_name FROM characters 
            WHERE faction = 'Iron Sultura'
        """)
        
        iron_sultura_chars = cursor.fetchall()
        
        for char_id, char_name in iron_sultura_chars:
            # Check if affiliation exists
            cursor.execute("""
                SELECT affiliation_id FROM character_corporate_affiliations 
                WHERE character_id = ?
            """, (char_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing affiliation
                cursor.execute("""
                    UPDATE character_corporate_affiliations 
                    SET corp_id = ?,
                        division_id = ?
                    WHERE character_id = ?
                """, (cmm_id, iron_sultura_div_id, char_id))
                print(f"   ✓ Updated {char_name} → CMM (Iron Sultura division)")
            else:
                # Create new affiliation
                cursor.execute("""
                    INSERT INTO character_corporate_affiliations (character_id, corp_id, division_id, is_current)
                    VALUES (?, ?, ?, 1)
                """, (char_id, cmm_id, iron_sultura_div_id))
                print(f"   ✓ Created affiliation for {char_name} → CMM (Iron Sultura division)")
    else:
        print("   ⚠ Could not find Iron Sultura division ID")
    
    print()
    
    
    # ============================================================
    # STEP 7: Verify the changes
    # ============================================================
    print("📊 Verification:\n")
    
    # Check CMM
    cursor.execute("""
        SELECT corp_id, corp_name, mission_statement 
        FROM corporations 
        WHERE corp_name = 'Constantine Meridian Media'
    """)
    cmm = cursor.fetchone()
    if cmm:
        print(f"✓ CMM Corporation: {cmm[1]} (ID: {cmm[0]})")
    
    # Check Iron Sultura division
    cursor.execute("""
        SELECT d.division_id, d.division_name, c.corp_name as corp_name
        FROM divisions d
        JOIN corporations c ON d.corp_id = c.corp_id
        WHERE d.division_name = 'Iron Sultura'
    """)
    division = cursor.fetchone()
    if division:
        print(f"✓ Iron Sultura Division: {division[1]} under {division[2]} (ID: {division[0]})")
    
    # Check Iron Sultura characters
    cursor.execute("""
        SELECT COUNT(*) 
        FROM characters 
        WHERE faction = 'Iron Sultura'
    """)
    char_count = cursor.fetchone()[0]
    print(f"✓ Iron Sultura Characters: {char_count}")
    
    # Check affiliations
    cursor.execute("""
        SELECT COUNT(*) 
        FROM character_corporate_affiliations ca
        JOIN divisions d ON ca.division_id = d.division_id
        WHERE d.division_name = 'Iron Sultura'
    """)
    affil_count = cursor.fetchone()[0]
    print(f"✓ Iron Sultura Affiliations: {affil_count}")
    
    print()
    
    # Commit changes
    conn.commit()
    print("✅ All changes committed successfully!\n")
    
    conn.close()
    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python fix_corporate_structure.py <database_path>")
        print("\nExample:")
        print("  python fix_corporate_structure.py universe.db")
        sys.exit(1)
    
    db_path = sys.argv[1]
    
    if not Path(db_path).exists():
        print(f"❌ Error: Database file '{db_path}' not found!")
        sys.exit(1)
    
    print("=" * 60)
    print("PHASE 5A: CORPORATE STRUCTURE FIX")
    print("=" * 60)
    print()
    
    success = fix_corporate_structure(db_path)
    
    if success:
        print("=" * 60)
        print("✅ PHASE 5A COMPLETE!")
        print("=" * 60)
        print("\nNext Step: Run Phase 5B to import all 30 characters")
    else:
        print("❌ Phase 5A encountered errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
