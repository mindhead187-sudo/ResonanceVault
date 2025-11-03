#!/usr/bin/env python3
"""
ResonanceVault Database Explorer
=================================
Query and explore your world!

Usage:
    python explore_database.py universe.db
"""

import sqlite3
import sys
from pathlib import Path


def print_header(title):
    """Print a nice header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def query_character_roster(cursor):
    """Show all characters by faction"""
    print_header("CHARACTER ROSTER BY FACTION")
    
    # Get faction counts
    cursor.execute("""
        SELECT faction, COUNT(*) as count
        FROM characters
        GROUP BY faction
        ORDER BY count DESC
    """)
    
    faction_counts = cursor.fetchall()
    
    print("📊 Faction Summary:")
    for faction, count in faction_counts:
        print(f"   • {faction}: {count} characters")
    
    print()
    
    # Show characters by faction
    for faction, _ in faction_counts:
        print(f"\n🔷 {faction}")
        print("-" * 70)
        
        cursor.execute("""
            SELECT 
                character_name,
                codename,
                primary_role,
                status,
                character_secrets
            FROM characters
            WHERE faction = ?
            ORDER BY character_name
        """, (faction,))
        
        chars = cursor.fetchall()
        
        for name, codename, role, status, secrets in chars:
            status_icon = "✓" if status == "Active" else "✗"
            
            # Handle None values
            codename = codename or "N/A"
            role = role or "N/A"
            
            # Parse K-Level from secrets if available
            klevel = ""
            if secrets:
                try:
                    import json
                    secrets_dict = json.loads(secrets)
                    klevel = secrets_dict.get('klevel', '')
                    if klevel:
                        klevel = f" [K{klevel}]"
                except:
                    pass
            
            print(f"   {status_icon} {name:25s} | {codename:20s} | {role}{klevel}")


def query_corporate_structure(cursor):
    """Show corporations and their divisions"""
    print_header("CORPORATE STRUCTURE")
    
    cursor.execute("""
        SELECT 
            corp_id,
            corp_name,
            industry,
            sector,
            status
        FROM corporations
        ORDER BY corp_name
    """)
    
    corps = cursor.fetchall()
    
    for corp_id, corp_name, industry, sector, status in corps:
        print(f"\n🏢 {corp_name}")
        print(f"   Industry: {industry}")
        print(f"   Sector: {sector}")
        print(f"   Status: {status}")
        
        # Get divisions
        cursor.execute("""
            SELECT 
                division_name,
                description,
                headquarters
            FROM divisions
            WHERE corp_id = ?
            ORDER BY division_name
        """, (corp_id,))
        
        divisions = cursor.fetchall()
        
        if divisions:
            print(f"\n   Divisions:")
            for div_name, desc, hq in divisions:
                print(f"      🔹 {div_name}")
                if hq:
                    print(f"         HQ: {hq}")
                if desc:
                    desc_short = desc[:80] + "..." if len(desc) > 80 else desc
                    print(f"         {desc_short}")
                
                # Count members
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM character_corporate_affiliations ca
                    JOIN divisions d ON ca.division_id = d.division_id
                    WHERE d.division_name = ? AND d.corp_id = ?
                """, (div_name, corp_id))
                
                member_count = cursor.fetchone()[0]
                print(f"         Members: {member_count}")
        else:
            print("   No divisions")


def query_affiliations_detail(cursor):
    """Show detailed affiliation information"""
    print_header("CHARACTER AFFILIATIONS & CLEARANCE")
    
    cursor.execute("""
        SELECT 
            c.character_name,
            c.codename,
            corp.corp_name,
            d.division_name,
            ca.clearance_level,
            ca.position_title,
            ca.military_rank,
            ca.is_current
        FROM characters c
        LEFT JOIN character_corporate_affiliations ca ON c.character_id = ca.character_id
        LEFT JOIN corporations corp ON ca.corp_id = corp.corp_id
        LEFT JOIN divisions d ON ca.division_id = d.division_id
        ORDER BY corp.corp_name, d.division_name, c.character_name
    """)
    
    affiliations = cursor.fetchall()
    
    current_corp = None
    current_div = None
    
    for name, codename, corp, div, clearance, position, rank, is_current in affiliations:
        # Handle None values
        codename = codename or "N/A"
        corp = corp or "No Corporation"
        
        if corp != current_corp:
            current_corp = corp
            current_div = None
            print(f"\n🏢 {current_corp}")
            print("-" * 70)
        
        if div != current_div:
            current_div = div
            if div:
                print(f"\n   🔹 {div}")
        
        status = "✓" if is_current else "✗"
        clearance_str = f"K{clearance}" if clearance else "N/A"
        
        line = f"   {status} {name:25s} ({codename:15s})"
        
        if clearance:
            line += f" | Clearance: {clearance_str}"
        if position:
            line += f" | {position}"
        if rank:
            line += f" | Rank: {rank}"
        
        print(line)


def query_character_secrets(cursor):
    """Show character metadata (colors, sigils, etc.)"""
    print_header("CHARACTER METADATA (Colors, Sigils, K-Levels)")
    
    cursor.execute("""
        SELECT 
            character_name,
            codename,
            faction,
            character_secrets
        FROM characters
        WHERE character_secrets IS NOT NULL
        ORDER BY faction, character_name
    """)
    
    chars = cursor.fetchall()
    
    import json
    
    current_faction = None
    
    for name, codename, faction, secrets in chars:
        # Handle None values
        codename = codename or "N/A"
        
        if faction != current_faction:
            current_faction = faction
            print(f"\n🔷 {faction}")
            print("-" * 70)
        
        try:
            secrets_dict = json.loads(secrets)
            
            colors = secrets_dict.get('colors', {})
            primary = colors.get('primary', 'N/A')
            accent = colors.get('accent', 'N/A')
            
            klevel = secrets_dict.get('klevel', 'N/A')
            verified = secrets_dict.get('verified_by', 'N/A')
            sigils = secrets_dict.get('sigils', [])
            
            print(f"\n   {name} ({codename})")
            print(f"      K-Level: {klevel}")
            print(f"      Colors: {primary} / {accent}")
            print(f"      Verified: {verified}")
            if sigils:
                print(f"      Sigils: {', '.join(sigils) if sigils else 'None'}")
        except:
            print(f"\n   {name} ({codename}): [Unable to parse secrets]")


def query_statistics(cursor):
    """Show database statistics"""
    print_header("DATABASE STATISTICS")
    
    # Character count
    cursor.execute("SELECT COUNT(*) FROM characters")
    char_count = cursor.fetchone()[0]
    
    # Corporation count
    cursor.execute("SELECT COUNT(*) FROM corporations")
    corp_count = cursor.fetchone()[0]
    
    # Division count
    cursor.execute("SELECT COUNT(*) FROM divisions")
    div_count = cursor.fetchone()[0]
    
    # Affiliation count
    cursor.execute("SELECT COUNT(*) FROM character_corporate_affiliations")
    affil_count = cursor.fetchone()[0]
    
    # Active vs inactive
    cursor.execute("SELECT status, COUNT(*) FROM characters GROUP BY status")
    status_counts = cursor.fetchall()
    
    print(f"📊 Total Characters:     {char_count}")
    print(f"🏢 Total Corporations:   {corp_count}")
    print(f"🔹 Total Divisions:      {div_count}")
    print(f"🔗 Total Affiliations:   {affil_count}")
    print()
    print("Character Status:")
    for status, count in status_counts:
        print(f"   • {status}: {count}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python explore_database.py <database_path>")
        print("\nExample:")
        print("  python explore_database.py universe.db")
        sys.exit(1)
    
    db_path = sys.argv[1]
    
    if not Path(db_path).exists():
        print(f"❌ Error: Database file '{db_path}' not found!")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("  RESONANCEVAULT DATABASE EXPLORER")
    print("=" * 70)
    
    # Run all queries
    query_statistics(cursor)
    query_character_roster(cursor)
    query_corporate_structure(cursor)
    query_affiliations_detail(cursor)
    query_character_secrets(cursor)
    
    print("\n" + "=" * 70)
    print("  EXPLORATION COMPLETE!")
    print("=" * 70 + "\n")
    
    conn.close()


if __name__ == "__main__":
    main()
