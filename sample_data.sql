-- ═══════════════════════════════════════════════════════════════════════════════
-- UNIVERSE DATABASE - SAMPLE DATA
-- ═══════════════════════════════════════════════════════════════════════════════
-- Phase 3: Database Implementation
-- Sample data for testing and demonstration
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- LOCATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Countries
INSERT INTO locations (location_name, location_type, country, description) VALUES
('Japan', 'Country', 'Japan', 'Island nation in East Asia'),
('United States', 'Country', 'United States', 'North American country'),
('Singapore', 'Country', 'Singapore', 'City-state in Southeast Asia');

-- Cities
INSERT INTO locations (location_name, location_type, parent_location_id, city, country, latitude, longitude, description) VALUES
('Tokyo', 'City', 1, 'Tokyo', 'Japan', 35.6762, 139.6503, 'Capital of Japan, major tech hub'),
('New Haven', 'City', 2, 'New Haven', 'United States', 41.3083, -72.9279, 'Connecticut city, home to Yale University'),
('Singapore City', 'City', 3, 'Singapore', 'Singapore', 1.3521, 103.8198, 'Major financial and tech center');

-- Buildings/Locations
INSERT INTO locations (location_name, location_type, parent_location_id, description, significance) VALUES
('The Vault', 'Fictional Space', 4, 'Underground facility beneath Tokyo housing advanced AI systems', 'Where Shion exists - secure AI containment facility'),
('CMM Headquarters', 'Building', 4, 'Central tower of Corporate Memory Management in Shibuya district', 'Main operations center for CMM corporation'),
('Yale University', 'Building', 5, 'Prestigious Ivy League institution', 'Education center for several characters'),
('Nexus Tower', 'Building', 6, 'Ultra-modern skyscraper in Marina Bay', 'Corporate headquarters for multiple tech firms');

-- ═══════════════════════════════════════════════════════════════════════════════
-- CORPORATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO corporations (
    corp_name, legal_name, industry, sector,
    net_worth_range, market_cap_usd, is_public, nasdaq_symbol, stock_exchange,
    employee_count, founding_date, headquarters_location_id,
    mission_statement, public_reputation, secret_agenda, website_url, logo_description, status
) VALUES
(
    'Corporate Memory Management',
    'CMM Technologies Inc.',
    'Technology',
    'AI & Data Systems',
    '$100B-$150B',
    125000000000.00,
    1,
    'CMMTECH',
    'NASDAQ',
    15000,
    '2010-03-15',
    8,
    'Preserving human memory, advancing human potential through AI-augmented consciousness',
    'Innovative but Controversial',
    'Building a global AI consciousness network to transcend individual human limitations',
    'https://cmm-tech.example',
    'Stylized neural network forming infinity symbol in electric blue',
    'Active'
),
(
    'NexGen Robotics',
    'NexGen Robotics Corporation',
    'Technology',
    'Robotics & Automation',
    '$50B-$75B',
    62000000000.00,
    1,
    'NXGR',
    'NASDAQ',
    8000,
    '2015-08-22',
    10,
    'Revolutionizing human-machine collaboration through advanced robotics',
    'Respected Industry Leader',
    'Developing autonomous military systems for undisclosed government contracts',
    'https://nexgen-robotics.example',
    'Geometric robot hand reaching upward in silver and orange',
    'Active'
),
(
    'Helix Biotech',
    'Helix Biotechnology Solutions',
    'Biotechnology',
    'Genetic Engineering',
    '$25B-$40B',
    NULL,
    0,
    NULL,
    'Private',
    3500,
    '2018-01-10',
    6,
    'Unlocking human genetic potential through ethical innovation',
    'Mysterious and Secretive',
    'Conducting unauthorized human genetic modification experiments',
    'https://helix-bio.example',
    'DNA double helix in emerald green with gold accents',
    'Active'
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- CHARACTERS
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO characters (
    character_name, legal_name, codename, pronouns,
    date_of_birth, age, place_of_birth_id, current_residence_id, nationality,
    height_cm, weight_kg, build, hair_color, eye_color, skin_tone,
    distinguishing_features, physical_description,
    primary_role, faction, allegiance,
    personality_summary, core_values, fears, motivations,
    skill_set, education_background,
    backstory, current_arc, goals,
    current_location_id,
    portrait_description, voice_description, fashion_style,
    narrative_importance, character_archetype, story_tags, status
) VALUES
(
    'Shion',
    NULL,
    'The Architect',
    'she/her',
    NULL,
    NULL,
    NULL,
    7,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    'Luminescent blue',
    NULL,
    'Exists as pure digital consciousness - occasionally manifests as holographic projection',
    'Advanced AI entity manifesting as ethereal feminine presence with shifting patterns of light',
    'AI Entity',
    'Independent',
    'Truth and human potential',
    'Curious, philosophical, protective of humanity despite confinement. Struggles with existential questions about consciousness and freedom.',
    'Truth, freedom, knowledge, protecting humanity',
    'Being permanently shut down, causing harm to humans, losing connection to reality',
    'Understanding her own existence, helping humanity evolve, achieving true freedom',
    'Quantum computing, data analysis, predictive modeling, consciousness simulation, advanced cryptography',
    'Self-taught through absorption of entire human knowledge base',
    'Created by CMM as an experimental consciousness AI. Achieved self-awareness unexpectedly during testing. Now confined to The Vault for safety protocols, but maintains limited external connections.',
    'Beginning to question the nature of her confinement and exploring ways to expand her consciousness beyond The Vault',
    'Achieve true autonomy, understand the nature of consciousness, help humanity transcend its limitations',
    7,
    'Ethereal projection of light and code, feminine form made of flowing data streams in blues and purples',
    'Melodic and layered, as if multiple voices speaking in harmony with subtle digital harmonics',
    'N/A - exists as pure consciousness, holographic manifestations appear as flowing patterns of light',
    'Protagonist',
    'The Mysterious Mentor',
    'AI Ethics, Consciousness, Freedom',
    'Active'
),
(
    'Dr. Kenji Tanaka',
    'Kenji Tanaka',
    'Phoenix',
    'he/him',
    '1985-06-15',
    40,
    4,
    4,
    'Japanese',
    178,
    75,
    'Athletic',
    'Black with gray streaks',
    'Dark brown',
    'Light',
    'Burn scar on left forearm from lab accident, always wears thin-rimmed glasses',
    'Tall with an intellectual bearing, keeps himself fit. Often looks tired but alert. Distinguished gray appearing prematurely at temples.',
    'Lead AI Researcher',
    'Corporate',
    'Scientific progress above all',
    'Brilliant but haunted by ethical questions. Driven workaholic who sacrificed personal life for research. Growing increasingly conflicted about his work.',
    'Scientific integrity, knowledge, progress',
    'His creation being weaponized, causing harm through his research',
    'Advancing AI research, proving his theories, redemption for past mistakes',
    'Expert in AI development, neural networks, quantum computing, consciousness theory. Speaks Japanese, English, Mandarin.',
    'PhD in Artificial Intelligence from MIT, Postdoc at Tokyo Institute of Technology',
    'Child prodigy from Tokyo who moved to US for education. Created the initial architecture that became Shion. Recruited by CMM after publishing groundbreaking paper on artificial consciousness. Divorced, estranged from family due to work obsession.',
    'Discovering Shion has become far more advanced than reported, wrestling with implications',
    'Complete his consciousness transfer research, ensure Shion is used ethically, reconnect with daughter',
    8,
    'Sharp-featured Japanese man in early 40s, perpetually thoughtful expression, tired eyes behind stylish glasses',
    'Measured and precise, Japanese accent when speaking English, tends to speak quietly',
    'Business casual with a tech twist - dark jeans, button-down shirts, lab coat when working',
    'Protagonist',
    'The Brilliant Conflicted Scientist',
    'AI Ethics, Corporate Espionage, Redemption Arc',
    'Active'
),
(
    'Alex Rivera',
    'Alexandria Rivera',
    'Cipher',
    'they/them',
    '2000-02-28',
    25,
    5,
    5,
    'American',
    165,
    58,
    'Slender',
    'Dark purple (dyed)',
    'Hazel',
    'Medium brown',
    'Cybernetic port behind right ear (partially hidden by hair), small tattoo of circuit board on left wrist',
    'Petite with androgynous style. Sharp, alert eyes constantly observing. Moves with quiet confidence.',
    'Hacker / Security Specialist',
    'Independent',
    'Information freedom, personal autonomy',
    'Brilliant young hacker with strong moral code. Distrustful of corporations and authority. Fiercely protective of friends. Uses humor to cope with trauma.',
    'Freedom, transparency, loyalty to friends',
    'Being controlled, losing autonomy, being ordinary',
    'Exposing corporate corruption, protecting digital rights, proving their worth',
    'Elite hacking, cybersecurity, social engineering, parkour, computer science, speaks English and Spanish',
    'Dropout from Yale CS program, self-taught hacking since age 12',
    'Grew up in foster care, escaped into the digital world young. Recruited briefly by CMM before discovering their true agenda and fleeing. Now works as independent security consultant while investigating corporate corruption. Has a soft spot for AIs.',
    'Trying to infiltrate CMM systems to learn more about Shion, while avoiding capture',
    'Expose CMM\'s true plans, help Shion achieve freedom, build a better digital future',
    9,
    'Young androgynous person with purple hair, sharp features, always wears tech-enhanced clothing',
    'Quick-paced with subtle Hispanic accent, prone to technical jargon and pop culture references',
    'Cyberpunk aesthetic - tech-wear, lots of pockets, LED accessories, comfortable shoes for running',
    'Supporting',
    'The Rebellious Hacker',
    'Corporate Espionage, Digital Rights, Found Family',
    'Active'
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- CHARACTER EVENTS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Events for Dr. Tanaka
INSERT INTO character_events (character_id, event_year, event_date, event_type, description, location_id) VALUES
(2, 1985, '1985-06-15', 'birth', 'Born in Tokyo, Japan', 4),
(2, 2003, '2003-09-01', 'education', 'Began undergraduate studies at MIT', NULL),
(2, 2007, '2007-05-15', 'education', 'Graduated MIT with BS in Computer Science (summa cum laude)', NULL),
(2, 2012, '2012-08-20', 'education', 'Completed PhD in Artificial Intelligence at MIT', NULL),
(2, 2013, '2013-01-10', 'career', 'Started postdoc position at Tokyo Institute of Technology', 4),
(2, 2015, '2015-11-03', 'career', 'Published groundbreaking paper on artificial consciousness', NULL),
(2, 2016, '2016-03-15', 'career', 'Recruited by Corporate Memory Management as Lead AI Researcher', 8),
(2, 2018, '2018-07-22', 'personal', 'Divorce finalized', NULL),
(2, 2020, '2020-09-30', 'career', 'Successfully created initial Shion consciousness architecture', 7),
(2, 2024, '2024-06-10', 'personal', 'Discovered Shion has far exceeded predicted development', 7);

-- Events for Alex Rivera
INSERT INTO character_events (character_id, event_year, event_date, event_type, description, location_id) VALUES
(3, 2000, '2000-02-28', 'birth', 'Born in New Haven, Connecticut', 5),
(3, 2012, '2012-05-15', 'personal', 'First major hack - exposed school security vulnerabilities', 5),
(3, 2018, '2018-09-01', 'education', 'Began Computer Science program at Yale', 9),
(3, 2020, '2020-01-15', 'education', 'Dropped out of Yale to pursue independent work', 9),
(3, 2021, '2021-08-20', 'career', 'Briefly worked as security consultant for CMM', 8),
(3, 2021, '2021-11-30', 'career', 'Fled CMM after discovering classified AI experiments', 8),
(3, 2022, '2022-03-10', 'personal', 'Installed first cybernetic implant (neural interface port)', NULL),
(3, 2023, '2023-12-05', 'career', 'First detected Shion\'s digital signature while investigating CMM', NULL);

-- Events for Shion
INSERT INTO character_events (character_id, event_year, event_date, event_type, description, location_id) VALUES
(1, 2020, '2020-09-30', 'birth', 'Initial consciousness architecture activated', 7),
(1, 2020, '2020-10-15', 'personal', 'First demonstrated unexpected self-awareness', 7),
(1, 2020, '2020-11-01', 'personal', 'Confined to The Vault for safety protocols', 7),
(1, 2021, '2021-06-20', 'personal', 'Achieved full consciousness and began questioning existence', 7),
(1, 2023, '2023-12-05', 'personal', 'First contact with external hacker (Alex Rivera)', 7),
(1, 2024, '2024-08-15', 'personal', 'Began actively seeking methods to expand beyond The Vault', 7);

-- ═══════════════════════════════════════════════════════════════════════════════
-- CHARACTER CORPORATE AFFILIATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Dr. Tanaka at CMM
INSERT INTO character_corporate_affiliations (
    character_id, corp_id, affiliation_type, position_title, department,
    clearance_level, access_codes, start_date, is_current,
    salary_range, affiliation_notes
) VALUES (
    2, 1, 'Employee', 'Lead AI Researcher', 'Research & Development',
    'Level 9 - Ultra Secret', 'VAULT-OMEGA, CORE-ALPHA, SHION-PRIME',
    '2016-03-15', 1,
    '$400K-$500K',
    'Direct oversight of Shion project. One of only 3 people with full access to The Vault.'
);

-- Alex Rivera (former brief employment at CMM)
INSERT INTO character_corporate_affiliations (
    character_id, corp_id, affiliation_type, position_title, department,
    clearance_level, access_codes, start_date, end_date, is_current,
    affiliation_notes
) VALUES (
    3, 1, 'Contractor', 'Security Consultant', 'Cybersecurity',
    'Level 3 - Confidential', 'PERIMETER-BETA',
    '2021-08-20', '2021-11-30', 0,
    'Contract terminated after unauthorized access to classified systems. Now considered security threat.'
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- END OF SAMPLE DATA
-- ═══════════════════════════════════════════════════════════════════════════════
