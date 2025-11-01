-- ═══════════════════════════════════════════════════════════════════════════════
-- UNIVERSE DATABASE SCHEMA - PHASE 2 COMPLETE
-- ═══════════════════════════════════════════════════════════════════════════════
-- SQLite Schema for Character/Corporation/Location Management System
-- Created: 2025-11-01
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE 1: LOCATIONS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Purpose: Store all geographic and fictional locations
-- Usage: Referenced by corporations, characters, and events
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE locations (
  -- Primary Key
  location_id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Basic Identity
  location_name VARCHAR(200) NOT NULL,
  location_type VARCHAR(50),  -- "City", "Building", "Room", "Country", "Fictional Space"
  
  -- Geographic Hierarchy
  parent_location_id INTEGER,  -- "The Vault" -> "Tokyo" -> "Japan"
  
  -- Address Details (flexible - use what you need)
  city VARCHAR(100),
  state_province VARCHAR(100),
  country VARCHAR(100),
  
  -- Coordinates (optional)
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  
  -- Narrative/Story Elements
  description TEXT,  -- "Underground AI server room beneath CMM headquarters"
  significance TEXT,  -- "Where Shion exists", "Site of the ritual"
  
  -- Metadata
  status VARCHAR(50) DEFAULT 'Active',
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Foreign Keys
  FOREIGN KEY (parent_location_id) REFERENCES locations(location_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE 2: CORPORATIONS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Purpose: Store all corporate entities in the universe
-- Usage: Companies, organizations, conglomerates
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE corporations (
  -- Primary Key
  corp_id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Basic Identity
  corp_name VARCHAR(200) NOT NULL UNIQUE,
  legal_name VARCHAR(200),
  industry VARCHAR(100),
  sector VARCHAR(100),
  
  -- Financial Data
  net_worth_range VARCHAR(50),  -- "$500B-$600B" or "Under $1B"
  market_cap_usd DECIMAL(20, 2),
  annual_revenue_usd DECIMAL(20, 2),
  nasdaq_symbol VARCHAR(10),
  stock_exchange VARCHAR(20),
  is_public BOOLEAN DEFAULT 0,
  
  -- Corporate Structure
  parent_corp_id INTEGER,  -- NULL if independent
  acquired_by_corp_id INTEGER,  -- NULL if never acquired
  acquisition_date DATE,  -- When acquired (if applicable)
  
  -- Operational Info
  employee_count INTEGER,
  founding_date DATE,
  headquarters_location_id INTEGER,
  
  -- Narrative/Story Elements
  mission_statement TEXT,
  public_reputation VARCHAR(50),  -- "Beloved Tech Giant", "Feared Monopoly", etc.
  secret_agenda TEXT,
  
  -- Visual/Branding
  website_url VARCHAR(255),
  logo_description TEXT,
  status VARCHAR(50) DEFAULT 'Active',
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Foreign Keys
  FOREIGN KEY (parent_corp_id) REFERENCES corporations(corp_id),
  FOREIGN KEY (acquired_by_corp_id) REFERENCES corporations(corp_id),
  FOREIGN KEY (headquarters_location_id) REFERENCES locations(location_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE 3: CHARACTERS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Purpose: Store all characters (human, AI, hybrid) in the universe
-- Usage: Main character database with comprehensive fields
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE characters (
  -- ═══════════════════════════════════════════════════════════
  -- PRIMARY KEY
  -- ═══════════════════════════════════════════════════════════
  character_id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- ═══════════════════════════════════════════════════════════
  -- CORE IDENTITY
  -- ═══════════════════════════════════════════════════════════
  character_name VARCHAR(200) NOT NULL,
  legal_name VARCHAR(200),  -- Birth name if different
  codename VARCHAR(100),  -- "Agent Phoenix", "The Architect"
  aliases TEXT,  -- Other names they go by (JSON or comma-separated)
  pronouns VARCHAR(50),  -- "she/her", "they/them", "he/him"
  
  -- ═══════════════════════════════════════════════════════════
  -- BIOGRAPHICAL
  -- ═══════════════════════════════════════════════════════════
  date_of_birth DATE,
  age INTEGER,
  place_of_birth_id INTEGER,  -- FK to locations
  current_residence_id INTEGER,  -- FK to locations
  nationality VARCHAR(100),
  ethnicity VARCHAR(100),
  languages_spoken TEXT,  -- "English, Japanese, Mandarin"
  
  -- ═══════════════════════════════════════════════════════════
  -- PHYSICAL DESCRIPTION
  -- ═══════════════════════════════════════════════════════════
  height_cm INTEGER,
  weight_kg INTEGER,
  build VARCHAR(50),  -- "Athletic", "Slender", "Muscular", "Average"
  hair_color VARCHAR(50),
  hair_style VARCHAR(100),
  eye_color VARCHAR(50),
  skin_tone VARCHAR(50),
  distinguishing_features TEXT,  -- "Scar on left cheek", "Tattoo of dragon on back"
  physical_description TEXT,  -- Full prose description
  
  -- ═══════════════════════════════════════════════════════════
  -- ROLE & FACTION
  -- ═══════════════════════════════════════════════════════════
  primary_role VARCHAR(100),  -- "Hacker", "Executive", "Operative", "AI Entity"
  faction VARCHAR(100),  -- "Corporate", "Independent", "Resistance", "Government"
  allegiance TEXT,  -- Who/what they're loyal to
  
  -- ═══════════════════════════════════════════════════════════
  -- PSYCHOLOGICAL & PERSONALITY
  -- ═══════════════════════════════════════════════════════════
  personality_summary TEXT,  -- "Calculating, empathetic, driven by revenge"
  core_values TEXT,  -- "Justice, loyalty, innovation"
  fears TEXT,  -- "Abandonment, failure, losing control"
  motivations TEXT,  -- What drives them
  flaws TEXT,  -- Character weaknesses
  strengths TEXT,  -- Character strengths
  
  -- ═══════════════════════════════════════════════════════════
  -- SKILLS & ABILITIES
  -- ═══════════════════════════════════════════════════════════
  skill_set TEXT,  -- "Expert hacker, martial arts, social engineering"
  special_abilities TEXT,  -- "Cybernetic enhancements", "Photographic memory"
  education_background TEXT,  -- "PhD Computer Science from MIT", "Self-taught"
  certifications TEXT,  -- Licenses, credentials
  
  -- ═══════════════════════════════════════════════════════════
  -- BACKSTORY & NARRATIVE
  -- ═══════════════════════════════════════════════════════════
  backstory TEXT,  -- Full life story
  current_arc TEXT,  -- Where they are in the story now
  character_secrets TEXT,  -- Hidden truths about them
  goals TEXT,  -- What they're trying to achieve
  
  -- ═══════════════════════════════════════════════════════════
  -- MEDICAL HISTORY
  -- ═══════════════════════════════════════════════════════════
  medical_history TEXT,  -- Conditions, injuries, surgeries
  current_medications TEXT,
  allergies TEXT,
  blood_type VARCHAR(10),
  cybernetic_implants TEXT,  -- "Neural interface, arm prosthetic"
  genetic_modifications TEXT,  -- If applicable
  mental_health_notes TEXT,
  
  -- ═══════════════════════════════════════════════════════════
  -- CRIMINAL & LEGAL
  -- ═══════════════════════════════════════════════════════════
  criminal_record TEXT,  -- Arrests, convictions, warrants
  legal_status VARCHAR(100),  -- "Wanted", "Pardoned", "Clean Record", "Under Investigation"
  crimes_committed TEXT,  -- Known or suspected
  
  -- ═══════════════════════════════════════════════════════════
  -- ONLINE & DIGITAL PRESENCE
  -- ═══════════════════════════════════════════════════════════
  online_handles TEXT,  -- Social media, forum names
  digital_footprint TEXT,  -- How they appear online
  hacker_reputation VARCHAR(100),  -- If applicable
  social_media_presence VARCHAR(50),  -- "High", "Ghost", "Moderate"
  email_addresses TEXT,
  
  -- ═══════════════════════════════════════════════════════════
  -- RELATIONSHIPS & CONNECTIONS
  -- ═══════════════════════════════════════════════════════════
  family_notes TEXT,  -- Parents, siblings, children
  relationship_status VARCHAR(50),  -- "Single", "Married", "Complicated"
  emergency_contact TEXT,
  
  -- ═══════════════════════════════════════════════════════════
  -- STATUS & VITALS
  -- ═══════════════════════════════════════════════════════════
  status VARCHAR(50) DEFAULT 'Active',  -- "Active", "Deceased", "Missing", "Retired"
  date_of_death DATE,
  cause_of_death TEXT,
  current_location_id INTEGER,  -- FK to locations - where they are NOW
  
  -- ═══════════════════════════════════════════════════════════
  -- VISUAL & MEDIA
  -- ═══════════════════════════════════════════════════════════
  portrait_description TEXT,  -- How to visualize them
  voice_description TEXT,  -- "Deep baritone", "Soft with Japanese accent"
  fashion_style TEXT,  -- "Corporate suits", "Streetwear", "Tactical gear"
  
  -- ═══════════════════════════════════════════════════════════
  -- META & NARRATIVE CONTROL
  -- ═══════════════════════════════════════════════════════════
  narrative_importance VARCHAR(50),  -- "Protagonist", "Antagonist", "Supporting", "Minor"
  character_archetype VARCHAR(100),  -- "The Mentor", "The Rebel", "The Fallen Hero"
  story_tags TEXT,  -- "AI Ethics", "Corporate Espionage", "Redemption Arc"
  
  -- ═══════════════════════════════════════════════════════════
  -- TIMESTAMPS
  -- ═══════════════════════════════════════════════════════════
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- ═══════════════════════════════════════════════════════════
  -- FOREIGN KEYS
  -- ═══════════════════════════════════════════════════════════
  FOREIGN KEY (place_of_birth_id) REFERENCES locations(location_id),
  FOREIGN KEY (current_residence_id) REFERENCES locations(location_id),
  FOREIGN KEY (current_location_id) REFERENCES locations(location_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE 4: CHARACTER_EVENTS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Purpose: Timeline system for tracking character life events
-- Usage: Build cross-character timelines, track milestones
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE character_events (
  -- Primary Key
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Links
  character_id INTEGER NOT NULL,
  
  -- Event Details
  event_year INTEGER NOT NULL,
  event_date TEXT,  -- Optional: "2023-05-15"
  event_type VARCHAR(50),  -- "birth", "education", "career", "personal", "criminal", "medical"
  description TEXT NOT NULL,
  
  -- Location
  location_id INTEGER,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Foreign Keys
  FOREIGN KEY (character_id) REFERENCES characters(character_id),
  FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE 5: CHARACTER_CORPORATE_AFFILIATIONS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Purpose: Link characters to corporations (employment, ownership, etc.)
-- Usage: Track who works where, with what access/clearance
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE character_corporate_affiliations (
  -- Primary Key
  affiliation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Links
  character_id INTEGER NOT NULL,
  corp_id INTEGER NOT NULL,
  
  -- Affiliation Details
  affiliation_type VARCHAR(50),  -- "Employee", "Founder", "Board Member", "Investor", "Contractor", "Spy"
  position_title VARCHAR(200),
  department VARCHAR(100),
  
  -- Security & Access
  clearance_level VARCHAR(100),  -- "Top Secret", "Level 5", "Omega Clearance"
  access_codes TEXT,  -- JSON or comma-separated: "VAULT-ALPHA, SERVER-OMEGA"
  military_rank VARCHAR(100),  -- "Captain", "Colonel", NULL if civilian
  sigil_emblem_description TEXT,  -- "Silver eagle with red star", "Infinity symbol badge"
  
  -- Timeline
  start_date DATE,
  end_date DATE,
  is_current BOOLEAN DEFAULT 1,
  
  -- Financial
  equity_percentage DECIMAL(5, 2),
  salary_range VARCHAR(50),
  
  -- Narrative
  affiliation_notes TEXT,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Foreign Keys
  FOREIGN KEY (character_id) REFERENCES characters(character_id),
  FOREIGN KEY (corp_id) REFERENCES corporations(corp_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- INDEXES FOR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════
-- Create indexes on frequently queried fields

-- Locations
CREATE INDEX idx_locations_parent ON locations(parent_location_id);
CREATE INDEX idx_locations_type ON locations(location_type);

-- Corporations
CREATE INDEX idx_corporations_name ON corporations(corp_name);
CREATE INDEX idx_corporations_parent ON corporations(parent_corp_id);
CREATE INDEX idx_corporations_industry ON corporations(industry);

-- Characters
CREATE INDEX idx_characters_name ON characters(character_name);
CREATE INDEX idx_characters_codename ON characters(codename);
CREATE INDEX idx_characters_faction ON characters(faction);
CREATE INDEX idx_characters_status ON characters(status);

-- Events
CREATE INDEX idx_events_character ON character_events(character_id);
CREATE INDEX idx_events_year ON character_events(event_year);
CREATE INDEX idx_events_type ON character_events(event_type);

-- Affiliations
CREATE INDEX idx_affiliations_character ON character_corporate_affiliations(character_id);
CREATE INDEX idx_affiliations_corp ON character_corporate_affiliations(corp_id);
CREATE INDEX idx_affiliations_current ON character_corporate_affiliations(is_current);

-- ═══════════════════════════════════════════════════════════════════════════════
-- EXAMPLE QUERIES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Find all events in 2018 across all characters
-- SELECT c.character_name, e.event_date, e.description, l.location_name
-- FROM character_events e
-- JOIN characters c ON e.character_id = c.character_id
-- LEFT JOIN locations l ON e.location_id = l.location_id
-- WHERE e.event_year = 2018
-- ORDER BY e.event_date;

-- Find all characters working at a specific corporation
-- SELECT c.character_name, a.position_title, a.clearance_level
-- FROM character_corporate_affiliations a
-- JOIN characters c ON a.character_id = c.character_id
-- JOIN corporations corp ON a.corp_id = corp.corp_id
-- WHERE corp.corp_name = 'Your Corporation Name'
-- AND a.is_current = 1;

-- Get complete character profile with current location
-- SELECT c.*, l.location_name as current_location
-- FROM characters c
-- LEFT JOIN locations l ON c.current_location_id = l.location_id
-- WHERE c.character_name = 'Character Name';

-- ═══════════════════════════════════════════════════════════════════════════════
-- END OF SCHEMA
-- ═══════════════════════════════════════════════════════════════════════════════
