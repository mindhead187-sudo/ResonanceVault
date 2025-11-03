-- ResonanceVault Quick Query Reference
-- =======================================
-- Copy and paste these into your SQLite client (DB Browser, sqlite3 CLI, etc.)

-- ===========================
-- CHARACTER QUERIES
-- ===========================

-- 1. All characters with basic info
SELECT 
    character_name,
    codename,
    faction,
    primary_role,
    status
FROM characters
ORDER BY faction, character_name;

-- 2. Shadow Core members only
SELECT 
    character_name,
    codename,
    primary_role
FROM characters
WHERE faction = 'Shadow Core'
ORDER BY character_name;

-- 3. Iron Sultura members only
SELECT 
    character_name,
    codename,
    primary_role
FROM characters
WHERE faction = 'Iron Sultura'
ORDER BY character_name;

-- 4. Characters with Unknown faction
SELECT 
    character_name,
    codename,
    primary_role
FROM characters
WHERE faction = 'Unknown'
ORDER BY character_name;

-- 5. Find specific character by name
SELECT * FROM characters 
WHERE character_name LIKE '%Reika%';

-- ===========================
-- CORPORATE STRUCTURE
-- ===========================

-- 6. All corporations
SELECT 
    corp_id,
    corp_name,
    industry,
    sector,
    status
FROM corporations
ORDER BY corp_name;

-- 7. All divisions with their parent corporations
SELECT 
    c.corp_name,
    d.division_name,
    d.headquarters,
    d.description
FROM divisions d
JOIN corporations c ON d.corp_id = c.corp_id
ORDER BY c.corp_name, d.division_name;

-- 8. Count members per division
SELECT 
    c.corp_name,
    d.division_name,
    COUNT(ca.character_id) as member_count
FROM divisions d
JOIN corporations c ON d.corp_id = c.corp_id
LEFT JOIN character_corporate_affiliations ca ON d.division_id = ca.division_id
GROUP BY c.corp_name, d.division_name
ORDER BY c.corp_name, d.division_name;

-- ===========================
-- AFFILIATIONS & CLEARANCE
-- ===========================

-- 9. Full affiliation details
SELECT 
    ch.character_name,
    ch.codename,
    corp.corp_name,
    d.division_name,
    ca.clearance_level,
    ca.position_title,
    ca.military_rank,
    ca.is_current
FROM characters ch
JOIN character_corporate_affiliations ca ON ch.character_id = ca.character_id
JOIN corporations corp ON ca.corp_id = corp.corp_id
LEFT JOIN divisions d ON ca.division_id = d.division_id
ORDER BY corp.corp_name, d.division_name, ch.character_name;

-- 10. Shadow Core members with K-Levels
SELECT 
    ch.character_name,
    ch.codename,
    ca.clearance_level as k_level
FROM characters ch
JOIN character_corporate_affiliations ca ON ch.character_id = ca.character_id
JOIN divisions d ON ca.division_id = d.division_id
WHERE d.division_name = 'Shadow Core'
ORDER BY ca.clearance_level, ch.character_name;

-- 11. Iron Sultura members with ranks
SELECT 
    ch.character_name,
    ch.codename,
    ca.military_rank,
    ca.position_title
FROM characters ch
JOIN character_corporate_affiliations ca ON ch.character_id = ca.character_id
JOIN divisions d ON ca.division_id = d.division_id
WHERE d.division_name = 'Iron Sultura'
ORDER BY ch.character_name;

-- 12. Characters without affiliations
SELECT 
    character_name,
    codename,
    faction
FROM characters
WHERE character_id NOT IN (
    SELECT character_id FROM character_corporate_affiliations
)
ORDER BY character_name;

-- ===========================
-- STATISTICS
-- ===========================

-- 13. Character count by faction
SELECT 
    faction,
    COUNT(*) as count
FROM characters
GROUP BY faction
ORDER BY count DESC;

-- 14. Character count by status
SELECT 
    status,
    COUNT(*) as count
FROM characters
GROUP BY status
ORDER BY count DESC;

-- 15. Division member counts
SELECT 
    d.division_name,
    c.corp_name,
    COUNT(ca.character_id) as members
FROM divisions d
JOIN corporations c ON d.corp_id = c.corp_id
LEFT JOIN character_corporate_affiliations ca ON d.division_id = ca.division_id
GROUP BY d.division_name, c.corp_name
ORDER BY members DESC;

-- ===========================
-- ADVANCED QUERIES
-- ===========================

-- 16. Characters with their full corporate hierarchy
SELECT 
    ch.character_name,
    ch.codename,
    ch.faction,
    corp.corp_name as corporation,
    d.division_name as division,
    ca.clearance_level,
    ch.status
FROM characters ch
LEFT JOIN character_corporate_affiliations ca ON ch.character_id = ca.character_id
LEFT JOIN corporations corp ON ca.corp_id = corp.corp_id
LEFT JOIN divisions d ON ca.division_id = d.division_id
ORDER BY corp.corp_name, d.division_name, ch.character_name;

-- 17. Nexus Enraenra full roster (both Shadow Core and Aethos)
SELECT 
    ch.character_name,
    ch.codename,
    d.division_name,
    ca.clearance_level,
    ch.primary_role
FROM characters ch
JOIN character_corporate_affiliations ca ON ch.character_id = ca.character_id
JOIN corporations corp ON ca.corp_id = corp.corp_id
LEFT JOIN divisions d ON ca.division_id = d.division_id
WHERE corp.corp_name = 'Nexus Enraenra'
ORDER BY d.division_name, ch.character_name;

-- 18. Constantine Meridian Media full roster
SELECT 
    ch.character_name,
    ch.codename,
    d.division_name,
    ca.military_rank,
    ch.primary_role
FROM characters ch
JOIN character_corporate_affiliations ca ON ch.character_id = ca.character_id
JOIN corporations corp ON ca.corp_id = corp.corp_id
LEFT JOIN divisions d ON ca.division_id = d.division_id
WHERE corp.corp_name = 'Constantine Meridian Media'
ORDER BY d.division_name, ch.character_name;

-- ===========================
-- CHARACTER SEARCH
-- ===========================

-- 19. Search characters by name pattern
-- Replace 'pattern' with your search term
SELECT 
    character_name,
    codename,
    faction,
    primary_role
FROM characters
WHERE character_name LIKE '%pattern%'
   OR codename LIKE '%pattern%'
ORDER BY character_name;

-- 20. Find twins (Hoshinaga, Miyara)
SELECT 
    character_name,
    codename,
    faction,
    primary_role
FROM characters
WHERE character_name LIKE '%Hoshinaga%'
   OR character_name LIKE '%Miyara%'
ORDER BY character_name;

-- ===========================
-- METADATA EXPLORATION
-- ===========================

-- 21. All table names in database
SELECT name FROM sqlite_master 
WHERE type='table' 
ORDER BY name;

-- 22. Schema for characters table
PRAGMA table_info(characters);

-- 23. Schema for corporations table
PRAGMA table_info(corporations);

-- 24. Schema for divisions table
PRAGMA table_info(divisions);

-- 25. Schema for affiliations table
PRAGMA table_info(character_corporate_affiliations);

-- ===========================
-- NOTES
-- ===========================
-- 
-- To run these queries:
-- 1. Open your SQLite client (DB Browser, DBeaver, sqlite3 CLI, etc.)
-- 2. Connect to universe.db
-- 3. Copy and paste any query
-- 4. Execute!
--
-- Tip: Modify the WHERE clauses to filter for specific characters,
--      factions, or divisions you're interested in.
