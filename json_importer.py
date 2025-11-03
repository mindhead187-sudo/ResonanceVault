#!/usr/bin/env python3
"""
Universe Database - JSON Character Importer
Phase 4: Data Population

This script imports characters from your identifiers JSON format
into the universe database.

Usage:
    python json_importer.py [json_file] [database_name]
    
Default: identifiers_delta04_full_canon.json → universe.db
"""

import json
import sqlite3
import sys
from datetime import datetime
from typing import Dict, List, Optional


class CharacterImporter:
    """Imports characters from JSON into database"""
    
    def __init__(self, json_file="identifiers_delta04_full_canon.json", db_path="universe.db"):
        self.json_file = json_file
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.data = None
        
        # Field mapping: JSON → Database
        self.field_map = {
            'name': 'character_name',
            'codename': 'codename',
            'faction': 'faction',
            'role': 'primary_role',
            'status': 'status',
        }
        
        # Statistics
        self.imported_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.errors = []
        
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
            print(f"✓ Connected to database: {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def load_json(self):
        """Load JSON data"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✓ Loaded JSON: {self.json_file}")
            print(f"  Total identities: {self.data['summary']['total_identities']}")
            return True
        except Exception as e:
            print(f"✗ Error loading JSON: {e}")
            return False
    
    def character_exists(self, name: str) -> bool:
        """Check if character already exists"""
        self.cursor.execute(
            "SELECT character_id FROM characters WHERE character_name = ?",
            (name,)
        )
        return self.cursor.fetchone() is not None
    
    def get_corporation_id(self, corp_name: str) -> Optional[int]:
        """Get corporation ID by name"""
        self.cursor.execute(
            "SELECT corp_id FROM corporations WHERE corp_name = ?",
            (corp_name,)
        )
        row = self.cursor.fetchone()
        return row['corp_id'] if row else None
    
    def map_faction_to_corporation(self, faction: str) -> Optional[str]:
        """Map faction to corporation name"""
        faction_corp_map = {
            'Shadow Core': 'Nexus Enraenra',
            'Iron Sultura': 'Corporate Memory Management',
            'Unknown': None
        }
        return faction_corp_map.get(faction)
    
    def import_character(self, char_data: Dict, preview_only: bool = False) -> bool:
        """Import a single character"""
        try:
            name = char_data.get('name', '')
            char_id = char_data.get('id', '')
            
            # If name is just the ID (lowercase_underscore), convert to proper name
            if name == char_id and '_' in name:
                # Convert snake_case to Title Case
                name = ' '.join(word.capitalize() for word in name.split('_'))
                char_data = char_data.copy()  # Don't modify original
                char_data['name'] = name
            
            # Skip if no proper name
            if not name:
                self.skipped_count += 1
                return False
            
            # Check if already exists
            if self.character_exists(name):
                print(f"  ⚠ Skipping {name} (already exists)")
                self.skipped_count += 1
                return False
            
            # Build character fields
            character_fields = {
                'character_name': name,
                'codename': char_data.get('codename') or None,
                'faction': char_data.get('faction'),
                'primary_role': char_data.get('role'),
                'status': char_data.get('status', 'Active'),
                'aliases': ', '.join(char_data.get('aliases', [])) if char_data.get('aliases') else None,
                'story_tags': ', '.join(char_data.get('tags', [])) if char_data.get('tags') else None,
            }
            
            # Add custom JSON data as structured text
            security = char_data.get('security', {})
            colors = char_data.get('colors', {})
            
            # Store clearance in notes for now (or we can add to affiliations)
            if security:
                character_fields['character_secrets'] = json.dumps({
                    'klevel': security.get('klevel'),
                    'verified_by': security.get('verified_by'),
                    'colors': colors
                })
            
            if preview_only:
                print(f"\n  Preview: {name}")
                print(f"    Codename: {character_fields['codename']}")
                print(f"    Faction: {character_fields['faction']}")
                print(f"    Role: {character_fields['primary_role']}")
                print(f"    Status: {character_fields['status']}")
                return True
            
            # Build INSERT statement
            fields = list(character_fields.keys())
            placeholders = ','.join(['?' for _ in fields])
            field_names = ','.join(fields)
            
            query = f"INSERT INTO characters ({field_names}) VALUES ({placeholders})"
            values = [character_fields[f] for f in fields]
            
            self.cursor.execute(query, values)
            character_id = self.cursor.lastrowid
            
            # Add corporate affiliation if faction maps to corporation
            corp_name = self.map_faction_to_corporation(character_fields['faction'])
            if corp_name:
                corp_id = self.get_corporation_id(corp_name)
                if corp_id:
                    # Get clearance level
                    klevel = security.get('klevel', '01')
                    clearance_desc = f"K-Level {klevel}"
                    
                    # Insert affiliation
                    self.cursor.execute(
                        """INSERT INTO character_corporate_affiliations 
                           (character_id, corp_id, affiliation_type, clearance_level, is_current)
                           VALUES (?, ?, ?, ?, ?)""",
                        (character_id, corp_id, 'Operative', clearance_desc, 1)
                    )
            
            print(f"  ✓ Imported: {name}")
            self.imported_count += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Error importing {name}: {e}")
            self.errors.append(f"{name}: {e}")
            self.error_count += 1
            return False
    
    def import_selected_characters(self, names: List[str], preview: bool = False):
        """Import only selected characters by name"""
        print("\n" + "="*60)
        if preview:
            print("PREVIEW MODE - No data will be imported")
        else:
            print("IMPORTING SELECTED CHARACTERS")
        print("="*60 + "\n")
        
        # Find characters in JSON
        characters_to_import = []
        for identity in self.data['identities']:
            char_name = identity.get('name', '')
            # Match by name (case-insensitive)
            for target_name in names:
                if char_name.lower() == target_name.lower() or \
                   identity.get('id', '').lower() == target_name.lower().replace(' ', '_'):
                    characters_to_import.append(identity)
                    break
        
        print(f"Found {len(characters_to_import)}/{len(names)} characters in JSON\n")
        
        # Import each character
        for char_data in characters_to_import:
            self.import_character(char_data, preview_only=preview)
        
        if not preview:
            self.conn.commit()
            print("\n✓ Changes committed to database")
    
    def import_all(self, preview: bool = False):
        """Import all characters from JSON"""
        print("\n" + "="*60)
        if preview:
            print("PREVIEW MODE - No data will be imported")
        else:
            print("IMPORTING ALL CHARACTERS")
        print("="*60 + "\n")
        
        for identity in self.data['identities']:
            self.import_character(identity, preview_only=preview)
        
        if not preview:
            self.conn.commit()
            print("\n✓ Changes committed to database")
    
    def print_summary(self):
        """Print import summary"""
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"✓ Imported: {self.imported_count}")
        print(f"⚠ Skipped:  {self.skipped_count}")
        print(f"✗ Errors:   {self.error_count}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  • {error}")
        
        print("="*60)
    
    def run_import(self, selected_names: Optional[List[str]] = None, preview: bool = False):
        """Main import routine"""
        print("\n" + "="*60)
        print("UNIVERSE DATABASE - CHARACTER IMPORT")
        print("="*60)
        print(f"JSON File: {self.json_file}")
        print(f"Database: {self.db_path}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Load data
        if not self.load_json():
            return False
        
        # Connect to database
        if not self.connect():
            return False
        
        # Import
        if selected_names:
            self.import_selected_characters(selected_names, preview)
        else:
            self.import_all(preview)
        
        # Summary
        self.print_summary()
        
        self.close()
        return True


def main():
    """Main entry point"""
    json_file = sys.argv[1] if len(sys.argv) > 1 else "identifiers_delta04_full_canon.json"
    db_path = sys.argv[2] if len(sys.argv) > 2 else "universe.db"
    
    # Top 10 priority characters
    top_10 = [
        "Reika Hyōka Frost",  # Using full name from JSON
        "Kage Ishigawa",
        "Akira Miyara",
        "Ayana Miyara",
        "Kazuo Hoshinaga",
        "Kenji Hoshinaga",
        "Aaster Mythril",
        "Ren Kael",
        "Haruto Frost",
        # Mitsuko Frost not in JSON yet
    ]
    
    importer = CharacterImporter(json_file, db_path)
    
    # Preview first
    print("\n" + "="*60)
    print("STEP 1: PREVIEW")
    print("="*60)
    importer.run_import(selected_names=top_10, preview=True)
    
    # Ask for confirmation
    print("\n" + "="*60)
    response = input("\nImport these characters? (y/N): ")
    if response.lower() != 'y':
        print("Import cancelled.")
        return
    
    # Actually import
    print("\n" + "="*60)
    print("STEP 2: IMPORT")
    print("="*60)
    importer = CharacterImporter(json_file, db_path)
    importer.run_import(selected_names=top_10, preview=False)
    
    print("\n" + "="*60)
    print("✓ CHARACTER IMPORT COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
