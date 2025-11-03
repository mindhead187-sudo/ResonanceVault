#!/usr/bin/env python3
"""
Universe Database Initialization Script
Phase 3: Database Implementation

This script creates the SQLite database and initializes all tables
based on the Phase 2 schema design.

Usage:
    python initialize_database.py [database_name]
    
Default database name: universe.db
"""

import sqlite3
import sys
import os
from datetime import datetime
from pathlib import Path


class DatabaseInitializer:
    """Handles database creation and table initialization"""
    
    def __init__(self, db_path="universe.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            # Enable foreign key constraints
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
            print("✓ Database connection closed")
    
    def create_locations_table(self):
        """Create locations table"""
        sql = """
        CREATE TABLE IF NOT EXISTS locations (
          location_id INTEGER PRIMARY KEY AUTOINCREMENT,
          location_name VARCHAR(200) NOT NULL,
          location_type VARCHAR(50),
          parent_location_id INTEGER,
          city VARCHAR(100),
          state_province VARCHAR(100),
          country VARCHAR(100),
          latitude DECIMAL(10, 8),
          longitude DECIMAL(11, 8),
          description TEXT,
          significance TEXT,
          status VARCHAR(50) DEFAULT 'Active',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (parent_location_id) REFERENCES locations(location_id)
        );
        """
        try:
            self.cursor.execute(sql)
            print("✓ Created table: locations")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating locations table: {e}")
            return False
    
    def create_corporations_table(self):
        """Create corporations table"""
        sql = """
        CREATE TABLE IF NOT EXISTS corporations (
          corp_id INTEGER PRIMARY KEY AUTOINCREMENT,
          corp_name VARCHAR(200) NOT NULL UNIQUE,
          legal_name VARCHAR(200),
          industry VARCHAR(100),
          sector VARCHAR(100),
          net_worth_range VARCHAR(50),
          market_cap_usd DECIMAL(20, 2),
          annual_revenue_usd DECIMAL(20, 2),
          nasdaq_symbol VARCHAR(10),
          stock_exchange VARCHAR(20),
          is_public BOOLEAN DEFAULT 0,
          parent_corp_id INTEGER,
          acquired_by_corp_id INTEGER,
          acquisition_date DATE,
          employee_count INTEGER,
          founding_date DATE,
          headquarters_location_id INTEGER,
          mission_statement TEXT,
          public_reputation VARCHAR(50),
          secret_agenda TEXT,
          website_url VARCHAR(255),
          logo_description TEXT,
          status VARCHAR(50) DEFAULT 'Active',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (parent_corp_id) REFERENCES corporations(corp_id),
          FOREIGN KEY (acquired_by_corp_id) REFERENCES corporations(corp_id),
          FOREIGN KEY (headquarters_location_id) REFERENCES locations(location_id)
        );
        """
        try:
            self.cursor.execute(sql)
            print("✓ Created table: corporations")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating corporations table: {e}")
            return False
    
    def create_characters_table(self):
        """Create characters table"""
        sql = """
        CREATE TABLE IF NOT EXISTS characters (
          character_id INTEGER PRIMARY KEY AUTOINCREMENT,
          character_name VARCHAR(200) NOT NULL,
          legal_name VARCHAR(200),
          codename VARCHAR(100),
          aliases TEXT,
          pronouns VARCHAR(50),
          date_of_birth DATE,
          age INTEGER,
          place_of_birth_id INTEGER,
          current_residence_id INTEGER,
          nationality VARCHAR(100),
          ethnicity VARCHAR(100),
          languages_spoken TEXT,
          height_cm INTEGER,
          weight_kg INTEGER,
          build VARCHAR(50),
          hair_color VARCHAR(50),
          hair_style VARCHAR(100),
          eye_color VARCHAR(50),
          skin_tone VARCHAR(50),
          distinguishing_features TEXT,
          physical_description TEXT,
          primary_role VARCHAR(100),
          faction VARCHAR(100),
          allegiance TEXT,
          personality_summary TEXT,
          core_values TEXT,
          fears TEXT,
          motivations TEXT,
          flaws TEXT,
          strengths TEXT,
          skill_set TEXT,
          special_abilities TEXT,
          education_background TEXT,
          certifications TEXT,
          backstory TEXT,
          current_arc TEXT,
          character_secrets TEXT,
          goals TEXT,
          medical_history TEXT,
          current_medications TEXT,
          allergies TEXT,
          blood_type VARCHAR(10),
          cybernetic_implants TEXT,
          genetic_modifications TEXT,
          mental_health_notes TEXT,
          criminal_record TEXT,
          legal_status VARCHAR(100),
          crimes_committed TEXT,
          online_handles TEXT,
          digital_footprint TEXT,
          hacker_reputation VARCHAR(100),
          social_media_presence VARCHAR(50),
          email_addresses TEXT,
          family_notes TEXT,
          relationship_status VARCHAR(50),
          emergency_contact TEXT,
          status VARCHAR(50) DEFAULT 'Active',
          date_of_death DATE,
          cause_of_death TEXT,
          current_location_id INTEGER,
          portrait_description TEXT,
          voice_description TEXT,
          fashion_style TEXT,
          narrative_importance VARCHAR(50),
          character_archetype VARCHAR(100),
          story_tags TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (place_of_birth_id) REFERENCES locations(location_id),
          FOREIGN KEY (current_residence_id) REFERENCES locations(location_id),
          FOREIGN KEY (current_location_id) REFERENCES locations(location_id)
        );
        """
        try:
            self.cursor.execute(sql)
            print("✓ Created table: characters")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating characters table: {e}")
            return False
    
    def create_character_events_table(self):
        """Create character_events table"""
        sql = """
        CREATE TABLE IF NOT EXISTS character_events (
          event_id INTEGER PRIMARY KEY AUTOINCREMENT,
          character_id INTEGER NOT NULL,
          event_year INTEGER NOT NULL,
          event_date TEXT,
          event_type VARCHAR(50),
          description TEXT NOT NULL,
          location_id INTEGER,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (character_id) REFERENCES characters(character_id),
          FOREIGN KEY (location_id) REFERENCES locations(location_id)
        );
        """
        try:
            self.cursor.execute(sql)
            print("✓ Created table: character_events")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating character_events table: {e}")
            return False
    
    def create_character_corporate_affiliations_table(self):
        """Create character_corporate_affiliations table"""
        sql = """
        CREATE TABLE IF NOT EXISTS character_corporate_affiliations (
          affiliation_id INTEGER PRIMARY KEY AUTOINCREMENT,
          character_id INTEGER NOT NULL,
          corp_id INTEGER NOT NULL,
          affiliation_type VARCHAR(50),
          position_title VARCHAR(200),
          department VARCHAR(100),
          clearance_level VARCHAR(100),
          access_codes TEXT,
          military_rank VARCHAR(100),
          sigil_emblem_description TEXT,
          start_date DATE,
          end_date DATE,
          is_current BOOLEAN DEFAULT 1,
          equity_percentage DECIMAL(5, 2),
          salary_range VARCHAR(50),
          affiliation_notes TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (character_id) REFERENCES characters(character_id),
          FOREIGN KEY (corp_id) REFERENCES corporations(corp_id)
        );
        """
        try:
            self.cursor.execute(sql)
            print("✓ Created table: character_corporate_affiliations")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating character_corporate_affiliations table: {e}")
            return False
    
    def create_indexes(self):
        """Create all performance indexes"""
        indexes = [
            ("idx_locations_parent", "locations(parent_location_id)"),
            ("idx_locations_type", "locations(location_type)"),
            ("idx_corporations_name", "corporations(corp_name)"),
            ("idx_corporations_parent", "corporations(parent_corp_id)"),
            ("idx_corporations_industry", "corporations(industry)"),
            ("idx_characters_name", "characters(character_name)"),
            ("idx_characters_codename", "characters(codename)"),
            ("idx_characters_faction", "characters(faction)"),
            ("idx_characters_status", "characters(status)"),
            ("idx_events_character", "character_events(character_id)"),
            ("idx_events_year", "character_events(event_year)"),
            ("idx_events_type", "character_events(event_type)"),
            ("idx_affiliations_character", "character_corporate_affiliations(character_id)"),
            ("idx_affiliations_corp", "character_corporate_affiliations(corp_id)"),
            ("idx_affiliations_current", "character_corporate_affiliations(is_current)"),
        ]
        
        success_count = 0
        for idx_name, idx_cols in indexes:
            try:
                sql = f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_cols};"
                self.cursor.execute(sql)
                success_count += 1
            except sqlite3.Error as e:
                print(f"✗ Error creating index {idx_name}: {e}")
        
        print(f"✓ Created {success_count}/{len(indexes)} indexes")
        return success_count == len(indexes)
    
    def verify_tables(self):
        """Verify all tables were created successfully"""
        expected_tables = [
            'locations',
            'corporations',
            'characters',
            'character_events',
            'character_corporate_affiliations'
        ]
        
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        existing_tables = [row[0] for row in self.cursor.fetchall()]
        
        print("\n" + "="*60)
        print("DATABASE VERIFICATION")
        print("="*60)
        
        all_present = True
        for table in expected_tables:
            if table in existing_tables:
                # Count rows
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                print(f"✓ {table:40} ({count} rows)")
            else:
                print(f"✗ {table:40} MISSING!")
                all_present = False
        
        print("="*60)
        return all_present
    
    def initialize(self):
        """Main initialization routine"""
        print("\n" + "="*60)
        print("UNIVERSE DATABASE INITIALIZATION")
        print("="*60)
        print(f"Database: {self.db_path}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        # Check if database already exists
        db_exists = os.path.exists(self.db_path)
        if db_exists:
            response = input(f"⚠️  Database '{self.db_path}' already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Initialization cancelled.")
                return False
            os.remove(self.db_path)
            print(f"✓ Removed existing database\n")
        
        # Connect to database
        if not self.connect():
            return False
        
        # Create all tables
        print("\nCreating tables...")
        success = (
            self.create_locations_table() and
            self.create_corporations_table() and
            self.create_characters_table() and
            self.create_character_events_table() and
            self.create_character_corporate_affiliations_table()
        )
        
        if not success:
            print("\n✗ Failed to create all tables")
            self.close()
            return False
        
        # Create indexes
        print("\nCreating indexes...")
        self.create_indexes()
        
        # Commit changes
        self.conn.commit()
        print("\n✓ Changes committed to database")
        
        # Verify
        if not self.verify_tables():
            print("\n✗ Verification failed")
            self.close()
            return False
        
        print("\n" + "="*60)
        print("✓ DATABASE INITIALIZATION COMPLETE")
        print("="*60)
        
        self.close()
        return True


def main():
    """Main entry point"""
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    
    # Initialize database
    initializer = DatabaseInitializer(db_path)
    success = initializer.initialize()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
