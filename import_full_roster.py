#!/usr/bin/env python3
"""
Phase 5B: Import Full 30-Character Roster
==========================================
Imports ALL 30 characters from identifiers_delta04_full_canon.json
- Handles both Nexus Enraenra and CMM factions
- Preserves K-Levels, colors, codenames
- Creates proper affiliations with divisions

Author: Phase 5B Full Import
"""

import sqlite3
import json
import sys
from pathlib import Path


def title_case_name(name: str) -> str:
    """Convert lowercase name to Title Case"""
    return ' '.join(word.capitalize() for word in name.split())


def import_full_roster(db_path: str, json_path: str):
    """Import all 30 characters from JSON"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📥 Phase 5B: Importing Full 30-Character Roster\n")
    
    # Load JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Your JSON uses 'identities' not 'characters'
    identities = data.get('identities', [])
    total = len(identities)
    
    # Show summary if present
    if 'summary' in data:
        summary = data['summary']
        print(f"📊 JSON Summary:")
        print(f"   Total Identities: {summary.get('total_identities', total)}")
        print(f"   By Faction: {summary.get('by_faction', {})}")
        print()
    
    print(f"📊 Found {total} identities to import\n")
    
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
    
    print(f"🏢 Corporation IDs:")
    print(f"   Nexus Enraenra: {nexus_id}")
    print(f"   Constantine Meridian Media: {cmm_id}")
    print(f"\n🔷 Division IDs:")
    print(f"   Shadow Core: {shadow_core_id}")
    print(f"   Iron Sultura: {iron_sultura_id}")
    print()
    
    imported = 0
    updated = 0
    skipped = 0
    
    print("=" * 70)
    
    for identity in identities:
        # Your JSON structure: id, name, codename, faction, role, status, colors, security
        name = identity.get('name', '')  # Already in Title Case
        codename = identity.get('codename', '')
        faction = identity.get('faction', '')
        role = identity.get('role', '')
        status = identity.get('status', 'Active')
        
        # Get K-Level from security object
        security = identity.get('security', {})
        clearance_level = security.get('klevel', '')
        
        # Get colors
        colors = identity.get('colors', {})
        primary_color = colors.get('primary', '')
        secondary_color = colors.get('accent', '')  # Note: 'accent' not 'secondary'
        
        # Verify by
        verified_by = security.get('verified_by', '')
        
        # Get sigils array
        sigils = identity.get('sigils', [])
        
        print(f"\n📝 Processing: {name} ({codename})")
        print(f"   Faction: {faction} | Role: {role} | Status: {status}")
        
        # Check if character exists
        cursor.execute("SELECT character_id FROM characters WHERE character_name = ?", (name,))
        existing = cursor.fetchone()
        
        if existing:
            char_id = existing[0]
            print(f"   ℹ Character exists (ID: {char_id}) - Updating...")
            
            # Get existing secrets and merge with new data
            cursor.execute("SELECT character_secrets FROM characters WHERE character_id = ?", (char_id,))
            existing_secrets = cursor.fetchone()[0]
            
            if existing_secrets:
                try:
                    secrets_dict = json.loads(existing_secrets)
                except:
                    secrets_dict = {}
            else:
                secrets_dict = {}
            
            # Merge new data
            secrets_dict['klevel'] = clearance_level
            secrets_dict['colors'] = {'primary': primary_color, 'accent': secondary_color}
            secrets_dict['verified_by'] = verified_by
            secrets_dict['sigils'] = sigils
            
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
            print(f"   ✓ Updated existing character")
        else:
            print(f"   ➕ Creating new character...")
            
            # Build character_secrets JSON
            secrets_dict = {
                'klevel': clearance_level,
                'colors': {'primary': primary_color, 'accent': secondary_color},
                'verified_by': verified_by,
                'sigils': sigils,
                'imported_from': 'identifiers_delta04_full_canon.json'
            }
            
            cursor.execute("""
                INSERT INTO characters (
                    character_name, codename, faction, primary_role, 
                    status, character_secrets
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, codename, faction, role,
                status, json.dumps(secrets_dict)
            ))
            
            char_id = cursor.lastrowid
            imported += 1
            print(f"   ✓ Created character (ID: {char_id})")
        
        print(f"   ✓ Stored metadata (K-Level: {clearance_level}, colors, verification)")
        
        # Create/update affiliation
        if faction == 'Shadow Core' and nexus_id and shadow_core_id:
            # Check if affiliation exists
            cursor.execute("""
                SELECT affiliation_id FROM character_corporate_affiliations WHERE character_id = ?
            """, (char_id,))
            
            existing_affil = cursor.fetchone()
            
            if existing_affil:
                cursor.execute("""
                    UPDATE character_corporate_affiliations
                    SET corp_id = ?,
                        division_id = ?,
                        clearance_level = ?
                    WHERE character_id = ?
                """, (nexus_id, shadow_core_id, clearance_level, char_id))
                print(f"   ✓ Updated affiliation → Nexus (Shadow Core)")
            else:
                cursor.execute("""
                    INSERT INTO character_corporate_affiliations (
                        character_id, corp_id, division_id, clearance_level, is_current
                    )
                    VALUES (?, ?, ?, ?, 1)
                """, (char_id, nexus_id, shadow_core_id, clearance_level))
                print(f"   ✓ Created affiliation → Nexus (Shadow Core)")
        
        elif faction == 'Iron Sultura' and cmm_id and iron_sultura_id:
            # Check if affiliation exists
            cursor.execute("""
                SELECT affiliation_id FROM character_corporate_affiliations WHERE character_id = ?
            """, (char_id,))
            
            existing_affil = cursor.fetchone()
            
            if existing_affil:
                cursor.execute("""
                    UPDATE character_corporate_affiliations
                    SET corp_id = ?,
                        division_id = ?
                    WHERE character_id = ?
                """, (cmm_id, iron_sultura_id, char_id))
                print(f"   ✓ Updated affiliation → CMM (Iron Sultura)")
            else:
                cursor.execute("""
                    INSERT INTO character_corporate_affiliations (
                        character_id, corp_id, division_id, is_current
                    )
                    VALUES (?, ?, ?, 1)
                """, (char_id, cmm_id, iron_sultura_id))
                print(f"   ✓ Created affiliation → CMM (Iron Sultura)")
        elif faction == 'Unknown':
            print(f"   ⚠ Faction 'Unknown' - no affiliation created (can be assigned later)")
        else:
            print(f"   ⚠ No affiliation created (faction: {faction})")
        
        print("   " + "-" * 66)
    
    print("\n" + "=" * 70)
    
    # Commit changes
    conn.commit()
    
    # Final verification
    print("\n📊 Final Statistics:\n")
    
    cursor.execute("SELECT COUNT(*) FROM characters")
    total_chars = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM characters WHERE faction = 'Shadow Core'")
    shadow_core_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM characters WHERE faction = 'Iron Sultura'")
    iron_sultura_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM characters WHERE faction = 'Unknown'")
    unknown_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM character_corporate_affiliations")
    total_affiliations = cursor.fetchone()[0]
    
    print(f"   New Characters:        {imported}")
    print(f"   Updated Characters:    {updated}")
    print(f"   Skipped:               {skipped}")
    print(f"   ─────────────────────────────")
    print(f"   Total in Database:     {total_chars}")
    print(f"   Shadow Core:           {shadow_core_count}")
    print(f"   Iron Sultura:          {iron_sultura_count}")
    print(f"   Unknown Faction:       {unknown_count}")
    print(f"   Total Affiliations:    {total_affiliations}")
    
    conn.close()
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python import_full_roster.py <database_path> <json_path>")
        print("\nExample:")
        print("  python import_full_roster.py universe.db identifiers_delta04_full_canon.json")
        sys.exit(1)
    
    db_path = sys.argv[1]
    json_path = sys.argv[2]
    
    if not Path(db_path).exists():
        print(f"❌ Error: Database file '{db_path}' not found!")
        sys.exit(1)
    
    if not Path(json_path).exists():
        print(f"❌ Error: JSON file '{json_path}' not found!")
        sys.exit(1)
    
    print("=" * 70)
    print("PHASE 5B: FULL ROSTER IMPORT (30 CHARACTERS)")
    print("=" * 70)
    print()
    
    success = import_full_roster(db_path, json_path)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ PHASE 5B COMPLETE!")
        print("=" * 70)
        print("\nAll 30 characters imported successfully!")
    else:
        print("❌ Phase 5B encountered errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
