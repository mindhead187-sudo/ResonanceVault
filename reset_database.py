#!/usr/bin/env python3
"""
Universe Database - Reset Script
Phase 3: Database Implementation

This script resets the database to a clean state.

Usage:
    python reset_database.py [database_name]
    
WARNING: This will delete ALL data in the database!

Default database: universe.db
"""

import sqlite3
import sys
import os
from datetime import datetime


def reset_database(db_path="universe.db"):
    """Reset the database to clean state"""
    
    print("\n" + "="*60)
    print("UNIVERSE DATABASE RESET")
    print("="*60)
    print(f"Database: {db_path}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    if not os.path.exists(db_path):
        print(f"✗ Database '{db_path}' does not exist!")
        return False
    
    # Confirm with user
    print("⚠️  WARNING: This will DELETE ALL DATA in the database!")
    response = input("Are you absolutely sure you want to reset? (type 'YES' to confirm): ")
    
    if response != 'YES':
        print("Reset cancelled.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("✓ Database is already empty")
            conn.close()
            return True
        
        print(f"\nDeleting data from {len(tables)} tables...")
        
        # Disable foreign keys temporarily
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Delete all data from each table
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"  ✓ Cleared {table}")
        
        # Reset autoincrement counters
        cursor.execute("DELETE FROM sqlite_sequence")
        
        # Re-enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ DATABASE RESET COMPLETE")
        print("="*60)
        print("\nDatabase structure intact, all data removed.")
        print("You can now:")
        print("  • Run insert_sample_data.py to reload sample data")
        print("  • Add your own data from scratch")
        print("="*60)
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n✗ Error resetting database: {e}")
        return False


def main():
    """Main entry point"""
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    
    success = reset_database(db_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
