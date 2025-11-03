# Phase 5: Foundation Build

**Goal:** Get the world spinning with proper corporate structure and full character roster, before tackling timeline mechanics.

---

## 🎯 What Phase 5 Does

### Phase 5A: Fix Corporate Structure ✅
**Fixes the lore issues:**
- ❌ **OLD:** "Corporate Memory Management" as main corp
- ✅ **NEW:** "Constantine Meridian Media (CMM)" as main corp
- ❌ **OLD:** Iron Sultura as separate faction
- ✅ **NEW:** Iron Sultura as **division** under CMM
- Updates all character affiliations accordingly

### Phase 5B: Import Full 30-Character Roster ✅
**Imports all characters:**
- **Shadow Core** (Nexus Enraenra) - ~23 characters
- **Iron Sultura** (CMM division) - ~7 characters
- Preserves K-Levels, codenames, colors
- Creates proper corporate affiliations with divisions

---

## 🚀 Quick Start

### One-Command Install
```bash
python3 run_phase_5.py universe.db identifiers_delta04_full_canon.json
```
---

### Hotfix-Command Install
```bash
python3 check_schema.py universe.db
```
---

This runs both Phase 5A and 5B automatically!

### Or Run Separately
```bash
# Step 1: Fix corporate structure
python fix_corporate_structure.py universe.db

# Step 2: Import all 30 characters
python import_full_roster.py universe.db identifiers_delta04_full_canon.json
```

---

## 📦 Files Included

### Scripts (3)
1. **`fix_corporate_structure.py`** - Phase 5A corporate fixes
2. **`import_full_roster.py`** - Phase 5B character import
3. **`run_phase_5.py`** - Master script (runs both)

### Documentation (1)
4. **`PHASE_5_GUIDE.md`** - This file!

---

## ✅ What Gets Changed

### Phase 5A Changes

**Corporations Table:**
- Renames "Corporate Memory Management" → "Constantine Meridian Media"
- Updates description with Chicago founding, Kyra's vendetta

**Divisions Table:**
- Creates "Iron Sultura" as division under CMM
- Assigns Kyra Constantine as leader
- Adds military emblems (Skull, Trident, Shield, Talon, Crescent, Blade)
- Sets headquarters: Chicago, USA

**Character Affiliations:**
- Migrates Iron Sultura characters to CMM (with Iron Sultura division link)
- Adds `division_id` column if not exists

### Phase 5B Changes

**Characters Table:**
- Imports/updates all 30 characters from JSON
- Converts lowercase names → Title Case
- Sets codename, faction, role, status
- Preserves K-Level as `clearance_level`

**Character Secrets:**
- Stores primary/secondary colors
- Stores verification metadata
- Tracks import source

**Character Affiliations:**
- Links Shadow Core → Nexus Enraenra (with Shadow Core division)
- Links Iron Sultura → CMM (with Iron Sultura division)

---

## 📊 Expected Results

After running Phase 5, your database should have:

```
✅ Corporations:
   • Constantine Meridian Media (CMM) - renamed, lore-corrected
   • Nexus Enraenra
   • Aethos Military Group
   • [any others from Phase 4]

✅ Divisions:
   • Shadow Core (under Nexus Enraenra)
   • Iron Sultura (under CMM) ← NEW!
   • [any others]

✅ Characters: 30 total
   • ~23 Shadow Core (Nexus Enraenra)
   • ~7 Iron Sultura (CMM)

✅ Affiliations: 30+ links
   • All characters properly linked to corporations AND divisions
```

---

## 🔍 Verification Queries

Check if Phase 5 worked:

### 1. Check CMM Exists
```sql
SELECT * FROM corporations WHERE name = 'Constantine Meridian Media';
```

### 2. Check Iron Sultura Division
```sql
SELECT d.*, c.name as corporation 
FROM divisions d
JOIN corporations c ON d.corporation_id = c.id
WHERE d.name = 'Iron Sultura';
```

### 3. Count Characters by Faction
```sql
SELECT faction, COUNT(*) as count
FROM characters
GROUP BY faction
ORDER BY count DESC;
```

### 4. Check Iron Sultura Character Affiliations
```sql
SELECT 
    ch.name,
    ch.codename,
    c.name as corporation,
    d.name as division
FROM characters ch
JOIN character_affiliations ca ON ch.id = ca.character_id
JOIN corporations c ON ca.corporation_id = c.id
LEFT JOIN divisions d ON ca.division_id = d.id
WHERE ch.faction = 'Iron Sultura';
```

### 5. Total Character Count
```sql
SELECT COUNT(*) FROM characters;
-- Should be 30+
```

---

## 🐛 Troubleshooting

### "Corporate Memory Management not found"
- You may have already fixed it, or haven't run Phase 4
- Phase 5A will skip if CMM already exists

### "Not all 30 characters imported"
- Check your JSON file has all 30 entries
- Verify file path is correct
- Check for JSON formatting errors

### "Division not created"
- Make sure Phase 5A runs before 5B
- Check that CMM corporation exists first
- Verify divisions table was created

### "Affiliations not linking"
- Run Phase 5A before 5B (division must exist first)
- Check corporation IDs exist for Nexus/CMM
- Check division IDs exist for Shadow Core/Iron Sultura

---

## 🎯 Next Steps

After Phase 5 completes:

### ⏸️ POSTPONED (Later)
- **Phase 5C:** AETP Epoch System (timeline mechanics)
- **Phase 5D:** Detailed Backstories & Timelines (PDF imports)
- **Phase 5E:** Relationship System (character connections)
- **Phase 5F:** Location Expansion (cities, headquarters)

### ✅ READY NOW
Your database has:
- ✅ Proper corporate structure
- ✅ All 30 characters loaded
- ✅ Correct faction affiliations
- ✅ Preserved metadata (colors, K-Levels, codenames)

**Time to query and explore your world!** 🚀

---

## 📝 Notes

### Why This Approach?
- **Get world spinning first** - proper foundation before complex timeline mechanics
- **Fix lore issues early** - don't want to migrate 30 characters twice
- **Postpone complexity** - AETP epochs are cool, but not blocking basic queries

### What Changed from Original Plan?
- Originally planned to do 5A → 5C (epochs) → 5B (import)
- **New pragmatic approach:** 5A → 5B → world is usable → 5C later
- Timeline mechanics are important but not required to start building stories

### Design Decisions
- **Iron Sultura as division, not corp** - matches your lore
- **CMM proper name** - Constantine Meridian Media
- **Division support** - added `division_id` to affiliations for hierarchy
- **Metadata preservation** - colors, K-Levels stored for future use

---

## 🎉 Success Criteria

You'll know Phase 5 worked if:

1. ✅ CMM exists with correct name
2. ✅ Iron Sultura is a division under CMM (not a separate corp)
3. ✅ 30 characters in database
4. ✅ All Shadow Core characters link to Nexus Enraenra
5. ✅ All Iron Sultura characters link to CMM
6. ✅ K-Levels, codenames, colors preserved
7. ✅ You can query character rosters by faction/corporation/division

**Ready to build your narrative world!** 🌟

---

*Phase 5 Complete - Foundation solid. Time to tell some stories!*
