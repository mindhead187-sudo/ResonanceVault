#!/usr/bin/env python3
"""
Universe Database - Utility Functions
Phase 3: Database Implementation

This module provides helper functions for common database operations.

Usage:
    from database_utils import DatabaseConnection, add_character, search_characters, etc.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class DatabaseConnection:
    """Context manager for database connections"""
    
    def __init__(self, db_path="universe.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
    
    def execute(self, query, params=None):
        """Execute a query and return cursor"""
        if params:
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)
    
    def fetchall(self):
        """Fetch all results"""
        return self.cursor.fetchall()
    
    def fetchone(self):
        """Fetch one result"""
        return self.cursor.fetchone()


# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def add_character(
    db_path: str,
    character_name: str,
    **kwargs
) -> Optional[int]:
    """
    Add a new character to the database.
    
    Args:
        db_path: Path to database
        character_name: Name of the character (required)
        **kwargs: Any other character fields (codename, age, faction, etc.)
    
    Returns:
        character_id if successful, None otherwise
    """
    with DatabaseConnection(db_path) as db:
        # Build INSERT statement dynamically
        fields = ['character_name'] + list(kwargs.keys())
        placeholders = ','.join(['?' for _ in fields])
        field_names = ','.join(fields)
        
        query = f"INSERT INTO characters ({field_names}) VALUES ({placeholders})"
        values = [character_name] + list(kwargs.values())
        
        try:
            db.execute(query, values)
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding character: {e}")
            return None


def get_character(db_path: str, character_name: str) -> Optional[Dict[str, Any]]:
    """
    Get a character by name.
    
    Args:
        db_path: Path to database
        character_name: Name of the character
    
    Returns:
        Dictionary of character data or None if not found
    """
    with DatabaseConnection(db_path) as db:
        db.execute(
            "SELECT * FROM characters WHERE character_name = ?",
            (character_name,)
        )
        row = db.fetchone()
        return dict(row) if row else None


def search_characters(
    db_path: str,
    **filters
) -> List[Dict[str, Any]]:
    """
    Search for characters by various criteria.
    
    Args:
        db_path: Path to database
        **filters: Field names and values to filter by
            Examples: faction="Corporate", status="Active", primary_role="Hacker"
    
    Returns:
        List of matching characters
    """
    with DatabaseConnection(db_path) as db:
        if not filters:
            query = "SELECT * FROM characters"
            db.execute(query)
        else:
            conditions = [f"{field} = ?" for field in filters.keys()]
            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM characters WHERE {where_clause}"
            db.execute(query, tuple(filters.values()))
        
        return [dict(row) for row in db.fetchall()]


def update_character(
    db_path: str,
    character_name: str,
    **updates
) -> bool:
    """
    Update a character's fields.
    
    Args:
        db_path: Path to database
        character_name: Name of the character to update
        **updates: Fields to update
    
    Returns:
        True if successful, False otherwise
    """
    with DatabaseConnection(db_path) as db:
        if not updates:
            return False
        
        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])
        query = f"UPDATE characters SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE character_name = ?"
        values = list(updates.values()) + [character_name]
        
        try:
            db.execute(query, values)
            return db.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating character: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# EVENT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def add_event(
    db_path: str,
    character_name: str,
    event_year: int,
    description: str,
    event_type: Optional[str] = None,
    event_date: Optional[str] = None,
    location_name: Optional[str] = None
) -> Optional[int]:
    """
    Add an event to a character's timeline.
    
    Args:
        db_path: Path to database
        character_name: Name of the character
        event_year: Year the event occurred
        description: Description of the event
        event_type: Type of event (birth, education, career, etc.)
        event_date: Full date in YYYY-MM-DD format
        location_name: Name of location where event occurred
    
    Returns:
        event_id if successful, None otherwise
    """
    with DatabaseConnection(db_path) as db:
        # Get character_id
        db.execute("SELECT character_id FROM characters WHERE character_name = ?", (character_name,))
        char_row = db.fetchone()
        if not char_row:
            print(f"Character '{character_name}' not found")
            return None
        character_id = char_row['character_id']
        
        # Get location_id if location provided
        location_id = None
        if location_name:
            db.execute("SELECT location_id FROM locations WHERE location_name = ?", (location_name,))
            loc_row = db.fetchone()
            if loc_row:
                location_id = loc_row['location_id']
        
        try:
            db.execute(
                """INSERT INTO character_events 
                   (character_id, event_year, event_date, event_type, description, location_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (character_id, event_year, event_date, event_type, description, location_id)
            )
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding event: {e}")
            return None


def get_character_timeline(
    db_path: str,
    character_name: str
) -> List[Dict[str, Any]]:
    """
    Get all events for a character in chronological order.
    
    Args:
        db_path: Path to database
        character_name: Name of the character
    
    Returns:
        List of events
    """
    with DatabaseConnection(db_path) as db:
        query = """
        SELECT 
            e.*,
            l.location_name
        FROM character_events e
        JOIN characters c ON e.character_id = c.character_id
        LEFT JOIN locations l ON e.location_id = l.location_id
        WHERE c.character_name = ?
        ORDER BY e.event_year, e.event_date
        """
        db.execute(query, (character_name,))
        return [dict(row) for row in db.fetchall()]


# ═══════════════════════════════════════════════════════════════════════════════
# CORPORATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def add_corporation(
    db_path: str,
    corp_name: str,
    **kwargs
) -> Optional[int]:
    """
    Add a new corporation to the database.
    
    Args:
        db_path: Path to database
        corp_name: Name of the corporation (required, must be unique)
        **kwargs: Any other corporation fields
    
    Returns:
        corp_id if successful, None otherwise
    """
    with DatabaseConnection(db_path) as db:
        fields = ['corp_name'] + list(kwargs.keys())
        placeholders = ','.join(['?' for _ in fields])
        field_names = ','.join(fields)
        
        query = f"INSERT INTO corporations ({field_names}) VALUES ({placeholders})"
        values = [corp_name] + list(kwargs.values())
        
        try:
            db.execute(query, values)
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding corporation: {e}")
            return None


def get_corporation_employees(
    db_path: str,
    corp_name: str,
    current_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Get all employees (past and/or current) of a corporation.
    
    Args:
        db_path: Path to database
        corp_name: Name of the corporation
        current_only: If True, only return current employees
    
    Returns:
        List of employees with affiliation details
    """
    with DatabaseConnection(db_path) as db:
        query = """
        SELECT 
            c.character_name,
            a.*
        FROM character_corporate_affiliations a
        JOIN characters c ON a.character_id = c.character_id
        JOIN corporations corp ON a.corp_id = corp.corp_id
        WHERE corp.corp_name = ?
        """
        params = [corp_name]
        
        if current_only:
            query += " AND a.is_current = 1"
        
        query += " ORDER BY a.is_current DESC, a.start_date"
        
        db.execute(query, params)
        return [dict(row) for row in db.fetchall()]


# ═══════════════════════════════════════════════════════════════════════════════
# LOCATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def add_location(
    db_path: str,
    location_name: str,
    **kwargs
) -> Optional[int]:
    """
    Add a new location to the database.
    
    Args:
        db_path: Path to database
        location_name: Name of the location (required)
        **kwargs: Any other location fields
    
    Returns:
        location_id if successful, None otherwise
    """
    with DatabaseConnection(db_path) as db:
        fields = ['location_name'] + list(kwargs.keys())
        placeholders = ','.join(['?' for _ in fields])
        field_names = ','.join(fields)
        
        query = f"INSERT INTO locations ({field_names}) VALUES ({placeholders})"
        values = [location_name] + list(kwargs.values())
        
        try:
            db.execute(query, values)
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding location: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# AFFILIATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def add_affiliation(
    db_path: str,
    character_name: str,
    corp_name: str,
    affiliation_type: str = "Employee",
    **kwargs
) -> Optional[int]:
    """
    Add a corporate affiliation for a character.
    
    Args:
        db_path: Path to database
        character_name: Name of the character
        corp_name: Name of the corporation
        affiliation_type: Type of affiliation (Employee, Founder, etc.)
        **kwargs: Any other affiliation fields
    
    Returns:
        affiliation_id if successful, None otherwise
    """
    with DatabaseConnection(db_path) as db:
        # Get character_id
        db.execute("SELECT character_id FROM characters WHERE character_name = ?", (character_name,))
        char_row = db.fetchone()
        if not char_row:
            print(f"Character '{character_name}' not found")
            return None
        character_id = char_row['character_id']
        
        # Get corp_id
        db.execute("SELECT corp_id FROM corporations WHERE corp_name = ?", (corp_name,))
        corp_row = db.fetchone()
        if not corp_row:
            print(f"Corporation '{corp_name}' not found")
            return None
        corp_id = corp_row['corp_id']
        
        # Insert affiliation
        fields = ['character_id', 'corp_id', 'affiliation_type'] + list(kwargs.keys())
        placeholders = ','.join(['?' for _ in fields])
        field_names = ','.join(fields)
        
        query = f"INSERT INTO character_corporate_affiliations ({field_names}) VALUES ({placeholders})"
        values = [character_id, corp_id, affiliation_type] + list(kwargs.values())
        
        try:
            db.execute(query, values)
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding affiliation: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_database_stats(db_path: str) -> Dict[str, int]:
    """
    Get statistics about the database.
    
    Args:
        db_path: Path to database
    
    Returns:
        Dictionary with counts for each table
    """
    tables = [
        'locations',
        'corporations',
        'characters',
        'character_events',
        'character_corporate_affiliations'
    ]
    
    stats = {}
    with DatabaseConnection(db_path) as db:
        for table in tables:
            db.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = db.fetchone()['count']
    
    return stats


if __name__ == "__main__":
    # Example usage
    db_path = "universe.db"
    
    # Get stats
    print("Database Statistics:")
    stats = get_database_stats(db_path)
    for table, count in stats.items():
        print(f"  {table}: {count} rows")
    
    # Search for characters by faction
    print("\nCorporate faction characters:")
    corporate_chars = search_characters(db_path, faction="Corporate")
    for char in corporate_chars:
        print(f"  - {char['character_name']} ({char['primary_role']})")
