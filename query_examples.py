#!/usr/bin/env python3
"""
Universe Database - Query Examples
Phase 3: Database Implementation

This script demonstrates useful queries for the Universe database.

Usage:
    python query_examples.py [database_name]
    
Default database: universe.db
"""

import sqlite3
import sys
from datetime import datetime


class QueryExamples:
    """Demonstrates common database queries"""
    
    def __init__(self, db_path="universe.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "="*60)
        print(title.upper())
        print("="*60 + "\n")
    
    def query_all_characters(self):
        """Get all characters with basic info"""
        self.print_header("All Characters")
        
        query = """
        SELECT 
            character_name,
            codename,
            age,
            primary_role,
            faction,
            status
        FROM characters
        ORDER BY character_name
        """
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        if rows:
            for row in rows:
                print(f"Name: {row['character_name']}")
                if row['codename']:
                    print(f"  Codename: {row['codename']}")
                if row['age']:
                    print(f"  Age: {row['age']}")
                print(f"  Role: {row['primary_role']}")
                print(f"  Faction: {row['faction']}")
                print(f"  Status: {row['status']}")
                print()
        else:
            print("No characters found.")
    
    def query_character_timeline(self, character_name=None):
        """Get timeline of events for a character"""
        if character_name:
            self.print_header(f"Timeline for {character_name}")
            query = """
            SELECT 
                e.event_year,
                e.event_date,
                e.event_type,
                e.description,
                l.location_name
            FROM character_events e
            JOIN characters c ON e.character_id = c.character_id
            LEFT JOIN locations l ON e.location_id = l.location_id
            WHERE c.character_name = ?
            ORDER BY e.event_year, e.event_date
            """
            self.cursor.execute(query, (character_name,))
        else:
            self.print_header("Cross-Character Timeline")
            query = """
            SELECT 
                c.character_name,
                e.event_year,
                e.event_date,
                e.event_type,
                e.description,
                l.location_name
            FROM character_events e
            JOIN characters c ON e.character_id = c.character_id
            LEFT JOIN locations l ON e.location_id = l.location_id
            ORDER BY e.event_year, e.event_date
            """
            self.cursor.execute(query)
        
        rows = self.cursor.fetchall()
        
        if rows:
            current_year = None
            for row in rows:
                if row['event_year'] != current_year:
                    current_year = row['event_year']
                    print(f"\n━━━ {current_year} ━━━")
                
                if character_name is None:
                    print(f"\n[{row['character_name']}]")
                
                date_str = row['event_date'] if row['event_date'] else "Unknown date"
                print(f"  {date_str} ({row['event_type']})")
                print(f"  {row['description']}")
                if row['location_name']:
                    print(f"  Location: {row['location_name']}")
        else:
            print("No events found.")
    
    def query_corporation_employees(self, corp_name):
        """Get all employees of a corporation"""
        self.print_header(f"Employees at {corp_name}")
        
        query = """
        SELECT 
            c.character_name,
            a.position_title,
            a.department,
            a.clearance_level,
            a.start_date,
            a.is_current
        FROM character_corporate_affiliations a
        JOIN characters c ON a.character_id = c.character_id
        JOIN corporations corp ON a.corp_id = corp.corp_id
        WHERE corp.corp_name = ?
        ORDER BY a.is_current DESC, a.start_date
        """
        
        self.cursor.execute(query, (corp_name,))
        rows = self.cursor.fetchall()
        
        if rows:
            for row in rows:
                status = "✓ Current" if row['is_current'] else "✗ Former"
                print(f"{status} - {row['character_name']}")
                print(f"  Position: {row['position_title']}")
                if row['department']:
                    print(f"  Department: {row['department']}")
                if row['clearance_level']:
                    print(f"  Clearance: {row['clearance_level']}")
                print(f"  Started: {row['start_date']}")
                print()
        else:
            print(f"No employees found for {corp_name}.")
    
    def query_character_full_profile(self, character_name):
        """Get complete profile for a character"""
        self.print_header(f"Full Profile: {character_name}")
        
        # Basic info
        query = """
        SELECT 
            c.*,
            birth_loc.location_name as birth_location,
            res_loc.location_name as residence_location,
            curr_loc.location_name as current_location
        FROM characters c
        LEFT JOIN locations birth_loc ON c.place_of_birth_id = birth_loc.location_id
        LEFT JOIN locations res_loc ON c.current_residence_id = res_loc.location_id
        LEFT JOIN locations curr_loc ON c.current_location_id = curr_loc.location_id
        WHERE c.character_name = ?
        """
        
        self.cursor.execute(query, (character_name,))
        char = self.cursor.fetchone()
        
        if not char:
            print(f"Character '{character_name}' not found.")
            return
        
        # Print profile sections
        print("━━━ IDENTITY ━━━")
        print(f"Name: {char['character_name']}")
        if char['legal_name']:
            print(f"Legal Name: {char['legal_name']}")
        if char['codename']:
            print(f"Codename: {char['codename']}")
        if char['pronouns']:
            print(f"Pronouns: {char['pronouns']}")
        
        if char['age'] or char['date_of_birth']:
            print("\n━━━ BIOGRAPHICAL ━━━")
            if char['age']:
                print(f"Age: {char['age']}")
            if char['date_of_birth']:
                print(f"Date of Birth: {char['date_of_birth']}")
            if char['birth_location']:
                print(f"Place of Birth: {char['birth_location']}")
            if char['nationality']:
                print(f"Nationality: {char['nationality']}")
        
        if char['physical_description']:
            print("\n━━━ PHYSICAL DESCRIPTION ━━━")
            print(char['physical_description'])
        
        if char['primary_role'] or char['faction']:
            print("\n━━━ ROLE & FACTION ━━━")
            if char['primary_role']:
                print(f"Role: {char['primary_role']}")
            if char['faction']:
                print(f"Faction: {char['faction']}")
            if char['allegiance']:
                print(f"Allegiance: {char['allegiance']}")
        
        if char['personality_summary']:
            print("\n━━━ PERSONALITY ━━━")
            print(char['personality_summary'])
        
        if char['backstory']:
            print("\n━━━ BACKSTORY ━━━")
            print(char['backstory'])
        
        if char['current_arc']:
            print("\n━━━ CURRENT ARC ━━━")
            print(char['current_arc'])
        
        if char['goals']:
            print("\n━━━ GOALS ━━━")
            print(char['goals'])
        
        # Get affiliations
        aff_query = """
        SELECT 
            corp.corp_name,
            a.position_title,
            a.affiliation_type,
            a.is_current
        FROM character_corporate_affiliations a
        JOIN corporations corp ON a.corp_id = corp.corp_id
        WHERE a.character_id = ?
        """
        self.cursor.execute(aff_query, (char['character_id'],))
        affiliations = self.cursor.fetchall()
        
        if affiliations:
            print("\n━━━ CORPORATE AFFILIATIONS ━━━")
            for aff in affiliations:
                status = "Current" if aff['is_current'] else "Former"
                print(f"• {aff['corp_name']} ({status})")
                print(f"  {aff['position_title']} - {aff['affiliation_type']}")
    
    def query_events_in_year(self, year):
        """Get all events that happened in a specific year"""
        self.print_header(f"Events in {year}")
        
        query = """
        SELECT 
            c.character_name,
            e.event_date,
            e.event_type,
            e.description,
            l.location_name
        FROM character_events e
        JOIN characters c ON e.character_id = c.character_id
        LEFT JOIN locations l ON e.location_id = l.location_id
        WHERE e.event_year = ?
        ORDER BY e.event_date
        """
        
        self.cursor.execute(query, (year,))
        rows = self.cursor.fetchall()
        
        if rows:
            for row in rows:
                print(f"[{row['character_name']}]")
                date_str = row['event_date'] if row['event_date'] else "Unknown date"
                print(f"  {date_str} ({row['event_type']})")
                print(f"  {row['description']}")
                if row['location_name']:
                    print(f"  Location: {row['location_name']}")
                print()
        else:
            print(f"No events found in {year}.")
    
    def query_location_hierarchy(self):
        """Show location hierarchy"""
        self.print_header("Location Hierarchy")
        
        # Get top-level locations (no parent)
        query = """
        SELECT location_id, location_name, location_type
        FROM locations
        WHERE parent_location_id IS NULL
        ORDER BY location_name
        """
        
        self.cursor.execute(query)
        top_level = self.cursor.fetchall()
        
        for loc in top_level:
            print(f"📍 {loc['location_name']} ({loc['location_type']})")
            self._print_child_locations(loc['location_id'], indent=1)
    
    def _print_child_locations(self, parent_id, indent=0):
        """Recursively print child locations"""
        query = """
        SELECT location_id, location_name, location_type
        FROM locations
        WHERE parent_location_id = ?
        ORDER BY location_name
        """
        
        self.cursor.execute(query, (parent_id,))
        children = self.cursor.fetchall()
        
        for child in children:
            print("  " * indent + f"  └─ {child['location_name']} ({child['location_type']})")
            self._print_child_locations(child['location_id'], indent + 1)
    
    def run_examples(self):
        """Run all example queries"""
        print("\n" + "="*60)
        print("UNIVERSE DATABASE - QUERY EXAMPLES")
        print("="*60)
        print(f"Database: {self.db_path}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        if not self.connect():
            return False
        
        # Run example queries
        self.query_all_characters()
        self.query_location_hierarchy()
        self.query_character_timeline("Dr. Kenji Tanaka")
        self.query_character_full_profile("Shion")
        self.query_corporation_employees("Corporate Memory Management")
        self.query_events_in_year(2020)
        
        print("\n" + "="*60)
        print("✓ QUERY EXAMPLES COMPLETE")
        print("="*60)
        
        self.close()
        return True


def main():
    """Main entry point"""
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    
    examples = QueryExamples(db_path)
    success = examples.run_examples()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
