#!/usr/bin/env python3
"""
Quick schema diagnostic
"""

import sqlite3
import sys

def check_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("DATABASE SCHEMA CHECK")
    print("=" * 70)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n📊 Found {len(tables)} tables:\n")
    
    for (table_name,) in tables:
        print(f"\n{'='*70}")
        print(f"TABLE: {table_name}")
        print(f"{'='*70}")
        
        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"Columns:")
        for col in columns:
            cid, name, type_, notnull, default, pk = col
            pk_str = " [PRIMARY KEY]" if pk else ""
            null_str = " NOT NULL" if notnull else ""
            default_str = f" DEFAULT {default}" if default else ""
            print(f"  • {name}: {type_}{pk_str}{null_str}{default_str}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\nRows: {count}")
        
        # Show sample data for important tables
        if table_name in ['corporations', 'characters', 'divisions']:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            if rows:
                print(f"\nSample data:")
                for row in rows:
                    print(f"  {row}")
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_schema.py <database_path>")
        sys.exit(1)
    
    check_schema(sys.argv[1])
