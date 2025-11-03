# Phase 4: Import Workflow - Quick Guide

**ONE COMMAND TO RULE THEM ALL** 🚀

---

## ⚡ Fastest Way (Recommended)

```bash
# Step 1: Copy Phase 4 files to your repo
# (json_importer.py, master_import.py, add_corporations.py, 
#  post_import_adjustments.py, identifiers_delta04_full_canon.json)

# Step 2: Run master import
python3 master_import.py universe.db

# Step 3: Verify
python query_examples.py universe.db
```

**That's it!** ✅

---

## 📋 What Happens When You Run master_import.py

### Automatic Steps:
1. ✅ Adds Nexus Enraenra corporation
2. ✅ Adds Aethos Military Group corporation
3. ✅ Shows preview of 9 characters from JSON
4. ⏸️ **PAUSES FOR YOUR CONFIRMATION**
5. ✅ Imports all 9 characters
6. ✅ Links them to corporations
7. ✅ Applies special adjustments:
   - Haruto Frost → Deceased
   - Ren Kael → Iron Sultura/CMM
   - Reika Frost → Protagonist
8. ✅ Adds Mitsuko Frost (not in JSON)
9. ✅ Shows final results

---

## 🎯 Your Top 10 Characters

**Will be imported:**
1. Reika Hyōka Frost (Protagonist) ⭐
2. Kage Ishigawa
3. Akira Miyara
4. Ayana Miyara
5. Kazuo Hoshinaga
6. Kenji Hoshinaga
7. Aaster Mythril
8. Ren Kael (CMM)
9. Haruto Frost (Deceased)
10. Mitsuko Frost (Missing)

---

## 📸 Expected Output

```
============================================================
PHASE 4: MASTER CHARACTER IMPORT
============================================================
Database: universe.db
JSON File: identifiers_delta04_full_canon.json
============================================================

============================================================
STEP: Add Missing Corporations
============================================================
  ✓ Added: Nexus Enraenra
  ✓ Added: Aethos Military Group

✓ Corporations added successfully

============================================================
STEP: Import Top 10 Characters
============================================================

[Shows preview of all 9 characters]

Import these characters? (y/N): y

  ✓ Imported: Aaster Mythril
  ✓ Imported: Akira Miyara
  ✓ Imported: Ayana Miyara
  [... etc ...]

✓ Imported: 9
⚠ Skipped:  0
✗ Errors:   0

============================================================
STEP: Apply Post-Import Adjustments
============================================================
  ✓ Updated Haruto Frost: Deceased, Shadow Core Founder
  ✓ Updated Ren Kael: Iron Sultura faction, CMM affiliation
  ✓ Updated Reika Frost: Marked as Protagonist
  ✓ Added Mitsuko Frost (Missing status)

============================================================
VERIFYING IMPORT RESULTS
============================================================
✓ Characters: 10
✓ Corporations: 5 (3 from Phase 3 + 2 new)
✓ Affiliations: 8

[Shows list of all imported characters]

============================================================
✓ PHASE 4 MASTER IMPORT COMPLETE
============================================================
```

---

## 🔧 Manual Step-by-Step (If You Want Control)

### Step 1: Add Corporations
```bash
python add_corporations.py universe.db
```

### Step 2: Import Characters
```bash
python json_importer.py identifiers_delta04_full_canon.json universe.db
```
*(This will show preview and ask for confirmation)*

### Step 3: Apply Adjustments
```bash
python post_import_adjustments.py universe.db
```

### Step 4: Verify
```bash
python query_examples.py universe.db
```

---

## 🎮 After Import - What You Can Do

### View All Characters
```bash
python query_examples.py universe.db
```

### Search Characters
```python
from database_utils import search_characters

# Find all Shadow Core members
shadow_core = search_characters("universe.db", faction="Shadow Core")
for char in shadow_core:
    print(f"{char['character_name']} - {char['codename']}")
```

### Get Character Timeline
```python
from database_utils import get_character_timeline

timeline = get_character_timeline("universe.db", "Reika Hyōka Frost")
for event in timeline:
    print(f"{event['event_year']}: {event['description']}")
```

### Check Corporate Affiliations
```python
from database_utils import get_corporation_employees

employees = get_corporation_employees("universe.db", "Nexus Enraenra", current_only=True)
for emp in employees:
    print(f"{emp['character_name']} - Clearance: {emp['clearance_level']}")
```

---

## ⚠️ Important Notes

### Before Running:
- ✅ Make sure `universe.db` exists (from Phase 3)
- ✅ All Phase 4 scripts in same directory
- ✅ JSON file present

### After Running:
- Characters are linked to corporations automatically
- Clearance levels (K-Level) preserved
- Special statuses applied
- Ready to add more data!

### If Something Goes Wrong:
```bash
# Reset and try again
python reset_database.py universe.db
python initialize_database.py universe.db
python master_import.py universe.db
```

---

## 💡 Pro Tips

1. **Preview First**: master_import.py shows preview before importing
2. **Check Results**: Always run query_examples.py after import
3. **Backup**: Copy universe.db before major imports
4. **Iterate**: Import, test, adjust, repeat
5. **Expand**: After top 10, import remaining 20 characters

---

## 🎯 Success Checklist

After running master_import.py, verify:
- [ ] 10 characters imported
- [ ] Nexus Enraenra corporation exists
- [ ] Aethos Military Group exists
- [ ] Shadow Core members linked to Nexus Enraenra
- [ ] Ren Kael linked to CMM
- [ ] Haruto Frost status = Deceased
- [ ] Mitsuko Frost status = Missing
- [ ] Reika marked as Protagonist
- [ ] query_examples.py shows all characters

---

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python master_import.py universe.db` | Run complete import |
| `python query_examples.py universe.db` | View results |
| `python add_corporations.py universe.db` | Just add corps |
| `python json_importer.py <json> <db>` | Just import chars |
| `python post_import_adjustments.py <db>` | Just apply fixes |

---

**Ready? Run the master import and bring your universe to life!** 🌟

```bash
python master_import.py universe.db
```
