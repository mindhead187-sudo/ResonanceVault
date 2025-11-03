#!/usr/bin/env python3
"""
Universe Database - Sample Data Insertion Script
Phase 3: Database Implementation

This script loads sample data from sample_data.sql into the database.

Usage:
    python insert_sample_data.py [database_name] [data_file]
    
Default database: universe.db
Default data file: sample_data.sql
"""

import sqlite3
import sys
import os
from datetime import datetime


class DataInserter:
    """Handles insertion of sample data into database"""
    
    def __init__(self, db_path="universe.db", data_file="sample_data.sql"):
        self.db_path = db_path
        self.data_file = data_file
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            if not os.path.exists(self.db_path):
                print(f"✗ Database '{self.db_path}' does not exist!")
                print("  Run 'python initialize_database.py' first.")
                return False
            
            self.conn = sqlite3.connect(self.db_path)
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
            print("✓ Database connection closed")
    
    def load_sql_file(self):
        """Load and execute SQL from data file"""
        try:
            if not os.path.exists(self.data_file):
                print(f"✗ Data file '{self.data_file}' not found!")
                return False
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Use connection.executescript which handles multi-line statements
            self.conn.executescript(sql_script)
            self.conn.commit()
            print(f"✓ Successfully loaded and executed SQL script")
            return True
            
        except Exception as e:
            print(f"✗ Error loading SQL file: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_data(self):
        """Verify that data was inserted correctly"""
        print("\n" + "="*60)
        print("DATA VERIFICATION")
        print("="*60)
        
        tables = {
            'locations': 'location_name',
            'corporations': 'corp_name',
            'characters': 'character_name',
            'character_events': 'event_id',
            'character_corporate_affiliations': 'affiliation_id'
        }
        
        for table, display_col in tables.items():
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                print(f"✓ {table:40} {count:3} rows")
                
                # Show sample data
                if display_col != 'event_id' and display_col != 'affiliation_id':
                    self.cursor.execute(f"SELECT {display_col} FROM {table} LIMIT 3")
                    samples = [row[0] for row in self.cursor.fetchall()]
                    for sample in samples:
                        print(f"    • {sample}")
            else:
                print(f"⚠ {table:40} {count:3} rows (empty)")
        
        print("="*60)
    
    def insert_data(self):
        """Main data insertion routine"""
        print("\n" + "="*60)
        print("UNIVERSE DATABASE - SAMPLE DATA INSERTION")
        print("="*60)
        print(f"Database: {self.db_path}")
        print(f"Data file: {self.data_file}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        # Check if database exists
        if not os.path.exists(self.db_path):
            print(f"✗ Database '{self.db_path}' does not exist!")
            print("  Run 'python initialize_database.py' first.")
            return False
        
        # Connect
        if not self.connect():
            return False
        
        # Check if data already exists
        self.cursor.execute("SELECT COUNT(*) FROM characters")
        existing_count = self.cursor.fetchone()[0]
        
        if existing_count > 0:
            response = input(f"\n⚠️  Database already contains {existing_count} characters. Continue? (y/N): ")
            if response.lower() != 'y':
                print("Data insertion cancelled.")
                self.close()
                return False
        
        # Load and execute SQL
        print("\nInserting sample data...")
        if not self.load_sql_file():
            print("\n✗ Failed to load sample data")
            self.close()
            return False
        
        # Verify
        self.verify_data()
        
        print("\n" + "="*60)
        print("✓ SAMPLE DATA INSERTION COMPLETE")
        print("="*60)
        print("\nYou can now:")
        print("  • Run query_examples.py to see sample queries")
        print("  • Explore the data using SQLite browser")
        print("  • Add your own characters and corporations")
        print("="*60)
        
        self.close()
        return True


def main():
    """Main entry point"""
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    data_file = sys.argv[2] if len(sys.argv) > 2 else "sample_data.sql"
    
    inserter = DataInserter(db_path, data_file)
    success = inserter.insert_data()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
