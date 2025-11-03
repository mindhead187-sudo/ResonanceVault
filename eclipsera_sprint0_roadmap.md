# Eclipsera Character Database - Sprint 0 Roadmap
**Project**: Desktop Character Database Application  
**Universe**: Eclipsera (Nexus Enraenra vs Constantine Meridian Media)  
**Started**: November 1, 2025  
**Methodology**: Agile Development

---

## Project Overview

### Goal
Build a local desktop application for storing, referencing, and searching character data from the Eclipsera fictional universe, featuring 30+ characters across two rival corporate empires.

### Scope
- **Characters**: ~30-50 (currently ~30 defined)
- **Corporations**: 2 main (Nexus Enraenra, Constantine Meridian Media)
- **Divisions**: 8 total (4 per corporation)
- **Holdings**: 9 subsidiaries
- **Relationships**: Character connections, rivalries, romantic ties
- **Timeline**: Chronological events per character

### Technical Stack (Proposed)
- **Database**: SQLite (file-based, no server needed)
- **Desktop App**: Electron (HTML/CSS/JS)
- **Platform**: MacOS exclusively
- **Data Format**: PDF → Structured Data → SQLite
- **Version Control**: GitHub (optional)

---

## Sprint 0: Design & Planning

### Phase 1: Requirements & Data Analysis ✅
**Status**: COMPLETE  
**Deliverables**:
- [✅] Identified primary data entities
- [✅] Analyzed source PDF structure
- [✅] Determined scope (30 characters, 2 factions)
- [✅] Confirmed technical preferences (Electron, SQLite, Python comfort)

---

## ✅ Phase 2 Checklist - COMPLETE

- [✅] **Corporations Table** - Fully designed with 22 fields
- [✅] **Characters Table** - Comprehensive with 68 fields
- [✅] **Locations Table** - Hierarchical with 13 fields
- [✅] **Character_Events Table** - Timeline system with 9 fields
- [✅] **Character_Corporate_Affiliations** - Security-focused with 17 fields
- [✅] **Indexes** - 11 performance indexes created
- [✅] **Documentation** - Complete with examples

---
📊 What We Just Accomplished
✅ Stashed your roadmap changes
✅ Created phase-3-database-implementation branch
✅ Added all 11 Phase 3 files
✅ Committed with proper message (2,918 lines!)
✅ Pushed branch to GitHub
✅ Merged to main
✅ Pushed main to GitHub
✅ Deleted local branch
✅ Restored your roadmap changes
Phase 3 is live and your repo is clean! 🚀
---

---

### Phase 2: Database Schema Design
**Status**: IN PROGRESS  
**Goal**: Design complete SQLite schema before any coding

#### 2.1 Core Entity Design
- [x] **Corporations Table**
  - [ ] Define fields (name, industry, net_worth, nasdaq_symbol, employees, location, founding_date, mission)
  - [ ] Decide on additional metadata fields
  
- [x] **Characters Table**
  - [ ] Core identity fields (name, age, pronouns, codename, faction)
  - [ ] Physical description fields
  - [ ] Role/position fields
  - [ ] Backstory/narrative field (TEXT)
  - [ ] Medical history field
  - [ ] Criminal record field
  - [ ] Online presence field
  
- [x] **Divisions Table**
  - [ ] Link to corporation
  - [ ] Type, location, employee count
  - [ ] Rationale, discipline, dynamics
  - [ ] Key projects
  
- [x] **Holdings Table**
  - [ ] Name, location, employee count
  - [ ] Parent corporation link
  - [ ] Purpose/description
  
- [x] **Locations Table**
  - [ ] City, country, description
  - [ ] Link to divisions/headquarters

#### 2.2 Relationship Tables
- [x] **Character_Relationships**
  - [ ] character_id_1, character_id_2
  - [ ] relationship_type (enemy, ally, romantic, family, mentor, rival)
  - [ ] description
  - [ ] status (active, past, complicated)
  
- [x] **Character_Corporations**
  - [ ] character_id, corporation_id
  - [ ] division_id (optional)
  - [ ] role/title
  - [ ] start_date, end_date (for timeline)
  
- [x] **Character_Events** (Timeline)
  - [ ] character_id
  - [ ] event_date (year or full date)
  - [ ] event_type (education, career, personal, major_event)
  - [ ] description
  - [ ] location_id (optional)
  
- [x] **Attachments**
  - [ ] attached_to_type (character, corporation, location)
  - [ ] attached_to_id
  - [ ] file_path
  - [ ] file_type (image, document, note)
  - [ ] description

#### 2.3 Lookup/Tag Tables
- [x] **Tags** (flexible categorization)
  - [ ] tag_name (e.g., "Shadow Core", "Iron Sultura", "Executive")
  - [ ] tag_type (group, role, faction, specialty)
  
- [x] **Character_Tags**
  - [ ] character_id, tag_id

#### 2.4 Secret Assets Tables
- [x] **Secret_Assets**
  - [ ] corporation_id
  - [ ] name (Shion, Erebus, Aethos, Erebus Vanguard)
  - [ ] type (AI, paramilitary, intelligence)
  - [ ] description
  - [ ] location_id
  - [ ] employee_count (if applicable)

---

### Phase 3: Data Structure Decisions

#### 3.1 Character Physical Description
**Decision Needed**: Store as structured fields or single TEXT blob?

**Option A: Structured Fields**
```sql
height VARCHAR(10)
weight VARCHAR(10)
eye_color VARCHAR(50)
hair_color VARCHAR(50)
hair_style VARCHAR(100)
tattoos TEXT
piercings TEXT
```
**Pros**: Searchable, queryable  
**Cons**: More fields to manage

**Option B: Single TEXT Field**
```sql
physical_description TEXT
```
**Pros**: Flexible, easy to write  
**Cons**: Harder to search

- [ ] **Decision Made**: _________
- [ ] **Rationale**: _________

#### 3.2 Timeline Events Storage
**Decision Needed**: Separate table or JSON field?

**Option A: Separate Table** (Recommended)
```sql
CREATE TABLE character_events (
  event_id INTEGER PRIMARY KEY,
  character_id INTEGER,
  event_year INTEGER,
  event_date TEXT, -- optional full date
  event_type VARCHAR(50),
  description TEXT,
  location_id INTEGER
);
```

**Option B: JSON Field in Characters Table**
```sql
timeline_events JSON
```

- [ ] **Decision Made**: _________
- [ ] **Rationale**: _________

#### 3.3 Accomplishments Storage
**Decision Needed**: How to store character accomplishments?

**Options**:
- Separate table (structured, searchable)
- TEXT field with bullet points (simple)
- JSON array (flexible)

- [ ] **Decision Made**: _________
- [ ] **Rationale**: _________

---

### Phase 4: Complete Schema Draft

#### 4.1 Write Full SQL Schema
- [ ] Create schema.sql file with all CREATE TABLE statements
- [ ] Include foreign key constraints
- [ ] Add indexes for performance (character names, corporation names)
- [ ] Include sample INSERT statements for testing

#### 4.2 Schema Review Checklist
- [ ] All entities from PDF represented
- [ ] Relationships properly linked (foreign keys)
- [ ] No redundant data storage
- [ ] Flexible enough for future expansion
- [ ] Searchable fields identified
- [ ] Required vs optional fields defined

---

### Phase 5: Data Extraction Plan

#### 5.1 Extraction Strategy
**Decision Needed**: Manual vs automated extraction?

- [ ] **Manual Entry**: Copy/paste from PDF into structured format
  - Pros: Accurate, can clean data as you go
  - Cons: Time-consuming
  
- [ ] **Semi-Automated**: Use Python script to parse PDF
  - Pros: Faster for bulk data
  - Cons: May need manual cleanup
  
- [ ] **Hybrid Approach**: Script for bulk, manual for details
  - Recommended for this project

#### 5.2 Data Staging Format
**Before loading into SQLite, structure data as:**
- [ ] JSON files (one per character/corporation)
- [ ] CSV files (for bulk loading)
- [ ] Python dictionaries (for scripting)

**Decision**: _________

#### 5.3 Extraction Order
- [ ] **Phase 1**: Nexus Enraenra corporation data
- [ ] **Phase 2**: Nexus Enraenra Shadow Core characters (7 people)
- [ ] **Phase 3**: Nexus Enraenra middle management (6 people)
- [ ] **Phase 4**: Constantine Meridian Media corporation data
- [ ] **Phase 5**: CMM Iron Sultura characters (7 people)
- [ ] **Phase 6**: Divisions and holdings
- [ ] **Phase 7**: Relationships mapping
- [ ] **Phase 8**: Timeline events

---

### Phase 6: Application Architecture Design

#### 6.1 Electron App Structure
```
eclipsera-app/
├── main.js                 # Electron main process
├── package.json           # Dependencies
├── src/
│   ├── database/
│   │   ├── schema.sql     # Database schema
│   │   ├── db.js          # SQLite connection handler
│   │   └── queries.js     # Prepared SQL queries
│   ├── ui/
│   │   ├── index.html     # Main window
│   │   ├── styles.css     # UI styles
│   │   └── app.js         # Frontend logic
│   └── assets/
│       └── images/        # Character images, logos
└── data/
    └── eclipsera.db       # SQLite database file
```

#### 6.2 Core Features (MVP)
- [ ] **Feature 1: Character List View**
  - Display all characters in scrollable list
  - Filter by faction/corporation
  - Search by name
  
- [ ] **Feature 2: Character Detail View**
  - Full character profile
  - Tabbed sections (Bio, Timeline, Relationships, etc.)
  - Image display
  
- [ ] **Feature 3: Search Functionality**
  - Full-text search across all fields
  - Filter by: faction, division, role, tags
  - Cross-reference search (e.g., "all characters in Shadow Core")
  
- [ ] **Feature 4: Relationship Viewer**
  - Show character connections
  - Visual relationship map (future enhancement)
  
- [ ] **Feature 5: Data Entry/Edit**
  - Add new characters
  - Edit existing entries
  - Import from JSON

#### 6.3 UI Mockup Decisions
- [ ] Color scheme (match corporate aesthetics?)
  - Nexus Enraenra: Cool tones (ice blue, silver)
  - CMM: Dark/aggressive (crimson, black, steel)
  
- [ ] Layout preference:
  - [ ] Sidebar navigation + detail panel
  - [ ] Tab-based navigation
  - [ ] Split-pane (list on left, detail on right)
  
- [ ] Font choices for readability

---

## Implementation Phases (Post-Sprint 0)

### Sprint 1: Database Foundation
**Goal**: Create and populate database with Nexus Enraenra data

- [ ] 1.1: Implement schema.sql
- [ ] 1.2: Create Python script for data loading
- [ ] 1.3: Extract & load Nexus Enraenra corporation data
- [ ] 1.4: Extract & load Shadow Core characters (7)
- [ ] 1.5: Extract & load middle management (6)
- [ ] 1.6: Validate data integrity
- [ ] 1.7: Test queries (search by name, filter by division)

**Success Criteria**: Database contains all Nexus Enraenra data, searchable

---

### Sprint 2: Basic Electron App
**Goal**: Working desktop app with read-only character viewing

- [ ] 2.1: Set up Electron boilerplate
- [ ] 2.2: Implement SQLite connection from Electron
- [ ] 2.3: Build character list view
- [ ] 2.4: Build character detail view
- [ ] 2.5: Implement basic search
- [ ] 2.6: Style UI with CSS

**Success Criteria**: App launches, displays characters, search works

---

### Sprint 3: CMM Integration
**Goal**: Add Constantine Meridian Media data

- [ ] 3.1: Extract & load CMM corporation data
- [ ] 3.2: Extract & load Iron Sultura characters (7)
- [ ] 3.3: Load divisions and holdings
- [ ] 3.4: Update UI to filter by faction
- [ ] 3.5: Test cross-faction searches

**Success Criteria**: Full dataset loaded, faction filtering works

---

### Sprint 4: Relationships & Timeline
**Goal**: Add advanced features

- [ ] 4.1: Load character relationships
- [ ] 4.2: Build relationship viewer
- [ ] 4.3: Load timeline events
- [ ] 4.4: Build timeline view (chronological)
- [ ] 4.5: Implement relationship filtering

**Success Criteria**: Can view character connections and life events

---

### Sprint 5: Polish & Enhancement
**Goal**: Refinement and quality-of-life features

- [ ] 5.1: Add image support
- [ ] 5.2: Implement data export (JSON/PDF)
- [ ] 5.3: Add notes feature
- [ ] 5.4: Build advanced search
- [ ] 5.5: UI polish and bug fixes
- [ ] 5.6: Create user documentation

**Success Criteria**: Production-ready app for personal use

---

## Key Decisions Log

### Decision 1: Desktop vs Web App
**Chosen**: Desktop (Electron)  
**Rationale**: Local-only, no need for server, matches user request  
**Date**: 2025-11-01

### Decision 2: Database Technology
**Chosen**: SQLite  
**Rationale**: File-based, no server, portable, perfect for personal use  
**Date**: 2025-11-01

### Decision 3: Starting Faction
**Chosen**: Nexus Enraenra first  
**Rationale**: "Hero" organization, allows validation before adding antagonist  
**Date**: 2025-11-01

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| PDF data extraction is time-consuming | High | Use semi-automated approach, prioritize key characters |
| Schema doesn't fit all character types | Medium | Design flexible schema with optional fields |
| Relationship data becomes complex | Medium | Use junction table, keep it simple initially |
| App performance with 50+ characters | Low | SQLite handles this easily, add indexes if needed |
| Lost progress due to session disconnect | Medium | **THIS DOCUMENT + Git commits** |

---

## Milestones

### Milestone 1: Schema Design Complete ⬜
**Target**: End of Sprint 0  
**Deliverables**:
- Complete schema.sql file
- Data extraction plan
- Architecture document

### Milestone 2: MVP Database Populated ⬜
**Target**: End of Sprint 1  
**Deliverables**:
- Working SQLite database
- Nexus Enraenra data loaded
- Basic queries tested

### Milestone 3: Working Desktop App ⬜
**Target**: End of Sprint 2  
**Deliverables**:
- Launchable Electron app
- Character viewing works
- Search functionality implemented

### Milestone 4: Complete Dataset ⬜
**Target**: End of Sprint 3  
**Deliverables**:
- Both factions loaded
- All divisions and holdings added
- Faction filtering works

### Milestone 5: Production Ready ⬜
**Target**: End of Sprint 5  
**Deliverables**:
- Relationships and timeline complete
- Polished UI
- Documentation written

---

## Notes & Decisions

### Session 1 (2025-11-01)
- Analyzed Eclipsera.pdf
- Identified ~30 characters across 2 factions
- Chose Electron + SQLite stack
- Established Sprint 0 roadmap approach

---

## Next Actions
1. [ ] Review this roadmap and confirm approach
2. [ ] Make key decisions in Phase 3 (data structure)
3. [ ] Begin schema design (Phase 4)
4. [ ] Create schema.sql file
5. [ ] Test schema with sample data

---

## Contact & Reconnection Protocol
If we need to reconnect:
1. Upload this document
2. Upload any schema.sql file created
3. Upload any sample data files
4. Reference specific milestone/phase we were working on

**Current Status**: Sprint 0, Phase 2 (Schema Design)
**Last Updated**: 2025-11-01
