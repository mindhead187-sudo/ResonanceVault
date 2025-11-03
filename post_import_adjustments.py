#!/usr/bin/env python3
"""
Post-Import Adjustments
Handles special cases that need manual updates after import
"""

import sqlite3
import sys


def apply_adjustments(db_path="universe.db"):
    """Apply special case adjustments"""
    
    print("\n" + "="*60)
    print("APPLYING POST-IMPORT ADJUSTMENTS")
    print("="*60)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    adjustments = []
    
    # 1. Haruto Frost - Set as deceased, Shadow Core founder
    cursor.execute("SELECT character_id FROM characters WHERE character_name = 'Haruto Frost'")
    haruto = cursor.fetchone()
    if haruto:
        cursor.execute("""
            UPDATE characters 
            SET status = 'Deceased',
                faction = 'Shadow Core',
                primary_role = 'Founder',
                backstory = 'Founder of Shadow Core. Deceased under mysterious circumstances.'
            WHERE character_id = ?
        """, (haruto['character_id'],))
        adjustments.append("✓ Updated Haruto Frost: Deceased, Shadow Core Founder")
    
    # 2. Ren Kael - Set faction to CMM/Iron Sultura
    cursor.execute("SELECT character_id FROM characters WHERE character_name = 'Ren Kael'")
    ren = cursor.fetchone()
    if ren:
        cursor.execute("""
            UPDATE characters 
            SET faction = 'Iron Sultura'
            WHERE character_id = ?
        """, (ren['character_id'],))
        
        # Add CMM affiliation if not exists
        cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Corporate Memory Management'")
        cmm = cursor.fetchone()
        if cmm:
            cursor.execute("""
                SELECT affiliation_id FROM character_corporate_affiliations 
                WHERE character_id = ? AND corp_id = ?
            """, (ren['character_id'], cmm['corp_id']))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO character_corporate_affiliations 
                    (character_id, corp_id, affiliation_type, is_current)
                    VALUES (?, ?, 'Operative', 1)
                """, (ren['character_id'], cmm['corp_id']))
        adjustments.append("✓ Updated Ren Kael: Iron Sultura faction, CMM affiliation")
    
    # 3. Reika Hyōka Frost - Add protagonist marker
    cursor.execute("SELECT character_id FROM characters WHERE character_name LIKE 'Reika%Frost'")
    reika = cursor.fetchone()
    if reika:
        cursor.execute("""
            UPDATE characters 
            SET narrative_importance = 'Protagonist',
                character_archetype = 'The Leader'
            WHERE character_id = ?
        """, (reika['character_id'],))
        adjustments.append("✓ Updated Reika Frost: Marked as Protagonist")
    
    conn.commit()
    
    print()
    for adj in adjustments:
        print(f"  {adj}")
    
    if not adjustments:
        print("  No adjustments needed")
    
    print("\n✓ Adjustments complete")
    print("="*60)
    
    conn.close()


def add_mitsuko_frost(db_path="universe.db"):
    """Add Mitsuko Frost manually (not in JSON)"""
    
    print("\n" + "="*60)
    print("ADDING MITSUKO FROST")
    print("="*60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Check if exists
    cursor.execute("SELECT character_id FROM characters WHERE character_name = 'Mitsuko Frost'")
    if cursor.fetchone():
        print("  ⚠ Mitsuko Frost already exists")
        conn.close()
        return
    
    # Add Mitsuko
    cursor.execute("""
        INSERT INTO characters (
            character_name,
            faction,
            primary_role,
            status,
            relationship_status,
            family_notes,
            narrative_importance
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        'Mitsuko Frost',
        'Shadow Core',
        'Unknown',
        'Missing',
        'Married',
        'Wife of Haruto Frost (deceased), mother of Reika Frost',
        'Supporting'
    ))
    
    print("  ✓ Added Mitsuko Frost (Missing status)")
    
    # Add affiliation to Shadow Core/Nexus Enraenra
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Nexus Enraenra'")
    nexus = cursor.fetchone()
    if nexus:
        cursor.execute("""
            INSERT INTO character_corporate_affiliations 
            (character_id, corp_id, affiliation_type, is_current, affiliation_notes)
            VALUES (?, ?, ?, ?, ?)
        """, (cursor.lastrowid, nexus[0], 'Former Associate', 0, 'Missing since founding era'))
        print("  ✓ Linked to Nexus Enraenra")
    
    conn.commit()
    conn.close()
    
    print("\n✓ Mitsuko Frost added")
    print("="*60)


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    
    apply_adjustments(db_path)
    add_mitsuko_frost(db_path)
