#!/usr/bin/env python3
"""
Universe Database Validation Script
Phase 3: Database Implementation

This script validates that the database schema was created correctly
and tests foreign key constraints, indexes, and table structures.

Usage:
    python validate_schema.py [database_name]
    
Default database name: universe.db
"""

import sqlite3
import sys
from datetime import datetime


class SchemaValidator:
    """Validates database schema and integrity"""
    
    def __init__(self, db_path="universe.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.errors = []
        self.warnings = []
        
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            self.errors.append(f"Failed to connect to database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def validate_tables_exist(self):
        """Check that all expected tables exist"""
        print("\n" + "="*60)
        print("VALIDATING TABLES")
        print("="*60)
        
        expected_tables = {
            'locations': 14,  # expected number of columns
            'corporations': 24,
            'characters': 70,
            'character_events': 9,
            'character_corporate_affiliations': 17
        }
        
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        existing_tables = {row[0] for row in self.cursor.fetchall()}
        
        all_valid = True
        for table, expected_cols in expected_tables.items():
            if table in existing_tables:
                # Check column count
                self.cursor.execute(f"PRAGMA table_info({table})")
                actual_cols = len(self.cursor.fetchall())
                
                if actual_cols == expected_cols:
                    print(f"✓ {table:40} ({actual_cols} columns)")
                else:
                    print(f"⚠ {table:40} ({actual_cols} columns, expected {expected_cols})")
                    self.warnings.append(f"Table {table} has {actual_cols} columns, expected {expected_cols}")
                    all_valid = False
            else:
                print(f"✗ {table:40} MISSING!")
                self.errors.append(f"Table {table} is missing")
                all_valid = False
        
        return all_valid
    
    def validate_indexes_exist(self):
        """Check that all indexes were created"""
        print("\n" + "="*60)
        print("VALIDATING INDEXES")
        print("="*60)
        
        expected_indexes = [
            'idx_locations_parent',
            'idx_locations_type',
            'idx_corporations_name',
            'idx_corporations_parent',
            'idx_corporations_industry',
            'idx_characters_name',
            'idx_characters_codename',
            'idx_characters_faction',
            'idx_characters_status',
            'idx_events_character',
            'idx_events_year',
            'idx_events_type',
            'idx_affiliations_character',
            'idx_affiliations_corp',
            'idx_affiliations_current'
        ]
        
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';"
        )
        existing_indexes = {row[0] for row in self.cursor.fetchall()}
        
        all_valid = True
        for index in expected_indexes:
            if index in existing_indexes:
                print(f"✓ {index}")
            else:
                print(f"✗ {index} MISSING!")
                self.errors.append(f"Index {index} is missing")
                all_valid = False
        
        return all_valid
    
    def validate_foreign_keys(self):
        """Test that foreign key constraints work"""
        print("\n" + "="*60)
        print("VALIDATING FOREIGN KEY CONSTRAINTS")
        print("="*60)
        
        # Check if foreign keys are enabled
        self.cursor.execute("PRAGMA foreign_keys")
        fk_enabled = self.cursor.fetchone()[0]
        
        if fk_enabled:
            print("✓ Foreign keys are ENABLED")
        else:
            print("✗ Foreign keys are DISABLED")
            self.errors.append("Foreign keys are disabled")
            return False
        
        # Test foreign key constraint (try to insert invalid reference)
        try:
            self.cursor.execute(
                "INSERT INTO characters (character_name, current_location_id) VALUES (?, ?)",
                ("Test Character", 9999)  # Non-existent location
            )
            self.conn.rollback()
            print("✗ Foreign key constraint NOT working (invalid insert succeeded)")
            self.errors.append("Foreign key constraints are not being enforced")
            return False
        except sqlite3.IntegrityError:
            print("✓ Foreign key constraints are working")
            return True
    
    def validate_default_values(self):
        """Test that default values are set correctly"""
        print("\n" + "="*60)
        print("VALIDATING DEFAULT VALUES")
        print("="*60)
        
        try:
            # Insert minimal record to test defaults
            self.cursor.execute(
                "INSERT INTO locations (location_name) VALUES (?)",
                ("Test Location",)
            )
            
            # Check if defaults were applied
            self.cursor.execute(
                "SELECT status, created_at FROM locations WHERE location_name = 'Test Location'"
            )
            row = self.cursor.fetchone()
            
            if row:
                status, created_at = row
                if status == 'Active' and created_at:
                    print("✓ Default values working (status='Active', created_at set)")
                else:
                    print(f"⚠ Default values may not be working (status={status})")
                    self.warnings.append("Default values may not be applied correctly")
            
            # Rollback test insert
            self.conn.rollback()
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Error testing default values: {e}")
            self.errors.append(f"Failed to test default values: {e}")
            self.conn.rollback()
            return False
    
    def validate_unique_constraints(self):
        """Test unique constraints"""
        print("\n" + "="*60)
        print("VALIDATING UNIQUE CONSTRAINTS")
        print("="*60)
        
        try:
            # Try to insert duplicate corp_name
            self.cursor.execute(
                "INSERT INTO corporations (corp_name) VALUES (?)",
                ("Test Corp",)
            )
            self.cursor.execute(
                "INSERT INTO corporations (corp_name) VALUES (?)",
                ("Test Corp",)
            )
            
            self.conn.rollback()
            print("✗ UNIQUE constraint NOT working (duplicate insert succeeded)")
            self.errors.append("UNIQUE constraints are not being enforced")
            return False
            
        except sqlite3.IntegrityError:
            self.conn.rollback()
            print("✓ UNIQUE constraints are working")
            return True
    
    def run_validation(self):
        """Run all validation tests"""
        print("\n" + "="*60)
        print("UNIVERSE DATABASE SCHEMA VALIDATION")
        print("="*60)
        print(f"Database: {self.db_path}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        if not self.connect():
            print("\n✗ VALIDATION FAILED: Could not connect to database")
            return False
        
        # Run all validation checks
        checks = [
            ("Tables", self.validate_tables_exist),
            ("Indexes", self.validate_indexes_exist),
            ("Foreign Keys", self.validate_foreign_keys),
            ("Default Values", self.validate_default_values),
            ("Unique Constraints", self.validate_unique_constraints),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            if not check_func():
                all_passed = False
        
        # Summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if all_passed and not self.errors:
            print("\n✓ ALL VALIDATION CHECKS PASSED")
            print("="*60)
        else:
            print("\n✗ VALIDATION FAILED")
            print("="*60)
        
        self.close()
        return all_passed and not self.errors


def main():
    """Main entry point"""
    db_path = sys.argv[1] if len(sys.argv) > 1 else "universe.db"
    
    validator = SchemaValidator(db_path)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
