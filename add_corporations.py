#!/usr/bin/env python3
"""
Add Missing Corporations
Adds Nexus Enraenra and Aethos Military Group to the database
"""

import sqlite3
import sys


def add_corporations(db_path="universe.db"):
    """Add the missing corporations"""
    
    print("\n" + "="*60)
    print("ADDING MISSING CORPORATIONS")
    print("="*60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Get Tokyo location ID (for headquarters)
    cursor.execute("SELECT location_id FROM locations WHERE location_name = 'Tokyo'")
    tokyo_row = cursor.fetchone()
    tokyo_id = tokyo_row[0] if tokyo_row else None
    
    corporations = [
        {
            'corp_name': 'Nexus Enraenra',
            'legal_name': 'Nexus Enraenra Corporation',
            'industry': 'Technology',
            'sector': 'Advanced Defense Systems',
            'net_worth_range': '$200B-$300B',
            'is_public': 0,
            'headquarters_location_id': tokyo_id,
            'mission_statement': 'Pioneering next-generation defense and intelligence solutions',
            'public_reputation': 'Elite Defense Contractor',
            'secret_agenda': 'Operating Shadow Core as covert reaction force beneath corporate facade',
            'status': 'Active'
        },
        {
            'corp_name': 'Aethos Military Group',
            'legal_name': 'Aethos Military Group Ltd.',
            'industry': 'Military',
            'sector': 'Private Military Contractor',
            'net_worth_range': '$50B-$100B',
            'is_public': 0,
            'headquarters_location_id': tokyo_id,
            'mission_statement': 'Providing elite tactical and security solutions worldwide',
            'public_reputation': 'Secretive PMC',
            'secret_agenda': 'Subsidiary force operating under Nexus Enraenra umbrella',
            'status': 'Active'
        }
    ]
    
    for corp in corporations:
        # Check if exists
        cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = ?", (corp['corp_name'],))
        if cursor.fetchone():
            print(f"  ⚠ {corp['corp_name']} already exists")
            continue
        
        # Insert
        fields = list(corp.keys())
        placeholders = ','.join(['?' for _ in fields])
        field_names = ','.join(fields)
        
        query = f"INSERT INTO corporations ({field_names}) VALUES ({placeholders})"
        values = [corp[f] for f in fields]
        
        cursor.execute(query, values)
        print(f"  ✓ Added: {corp['corp_name']}")
    
    conn.commit()
    conn.close()
    
    print("\n✓ Corporations added successfully")
    print("="*60)


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    add_corporations(db_path)
