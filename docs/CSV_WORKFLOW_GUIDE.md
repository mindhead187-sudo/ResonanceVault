# CSV-Based Detail Updates Workflow

## 🎯 Purpose

This document shows how to incorporate detailed changes during Phase 5+ using the **CSV approach** demonstrated with CMM k-levels.

---

## 📊 Why CSV Works Best

### **Advantages:**
1. ✅ **Bulk updates** - change 30 characters at once
2. ✅ **Version control** - easy to track changes with git
3. ✅ **Spreadsheet friendly** - edit in Excel/Google Sheets
4. ✅ **Fast processing** - programmatic import
5. ✅ **Multiple aspects** - separate files for different data types
6. ✅ **Easy to verify** - human-readable

### **When to Use CSV:**
- K-level assignments
- Military ranks/designations
- Service periods (epochs)
- Bulk character updates
- Affiliation changes
- Status updates (active/inactive/exposed)

### **When NOT to Use CSV:**
- Narrative backstories → Use PDF
- Complex nested data → Use JSON
- Single character update → Direct SQL

---

## 📋 CSV Structure Pattern

### **Core Pattern: Multiple CSVs for Different Aspects**

```
identities.csv        - Main character data (name, codename, role)
identities_levels.csv - K-level assignments
identities_epochs.csv - Service periods
identities_crossrefs.csv - Reference IDs
```

**Why separate files?**
- Each file serves one purpose
- Easy to update just one aspect
- Clean data model
- No duplicate information

---

## 🔧 Standard CSV Structures

### **1. Main Identity File**
```csv
id,name,codename,faction,role,status,notes,military_rank,designation,command_priority
cmm-kyra,Kyra Constantine,Matriarch,CMM,Sovereign,active,Notes here,Supreme Sovereign Commander,CMM-00,0
```

**Fields:**
- `id`: Unique identifier (faction-name pattern)
- `name`: Full character name
- `codename`: Operational codename
- `faction`: Faction/organization
- `role`: Primary role
- `status`: active/inactive/exposed/provisional/deceased
- `notes`: Freeform notes
- `military_rank`: (Optional) Military title
- `designation`: (Optional) Special designation
- `command_priority`: (Optional) Numeric hierarchy

### **2. Levels File**
```csv
identity_id,klevel
cmm-kyra,05
cmm-aegis,04
```

**Fields:**
- `identity_id`: Links to main identity
- `klevel`: Clearance level (01-05)

### **3. Epochs File**
```csv
identity_id,epoch_range
cmm-kyra,2022-2025
```

**Fields:**
- `identity_id`: Links to main identity
- `epoch_range`: Service period

### **4. Crossrefs File**
```csv
identity_id,ref
cmm-kyra,cmm_klevel_protocol:05
```

**Fields:**
- `identity_id`: Links to main identity
- `ref`: Reference string (for documentation)

---

## 🚀 Implementation Workflow

### **Step 1: Prepare CSV Files**
1. Create/update CSV files in spreadsheet
2. Export as CSV (UTF-8 encoding)
3. Verify structure with sample script

### **Step 2: Run Import Script**
```bash
python import_cmm_klevels.py universe.db ./data
```

### **Step 3: Verify Results**
```bash
python explore_database.py universe.db
```

### **Step 4: Query for Specific Data**
```sql
SELECT character_name, clearance_level 
FROM characters c
JOIN character_corporate_affiliations ca ON c.character_id = ca.character_id
WHERE faction = 'CMM'
ORDER BY clearance_level DESC;
```

---

## 📝 Creating Import Scripts

### **Template Pattern:**
```python
# 1. Load CSV files
identities = read_csv_file('identities.csv')
levels = read_csv_file('identities_levels.csv')

# 2. Create lookup dictionaries
levels_dict = {row['identity_id']: row['klevel'] for row in levels}

# 3. Process each identity
for identity in identities:
    # Check if exists
    # Update or insert character
    # Update or insert affiliation
    # Store metadata in character_secrets JSON
```

### **Key Components:**
- CSV reader (built-in Python `csv` module)
- SQLite connection
- Existence checks (UPDATE vs INSERT)
- JSON storage for metadata
- Transaction commit
- Verification queries

---

## 🎯 Use Cases for This Approach

### **CMM K-Levels** ✅ (Test case)
- 31 characters
- 5 K-levels
- Military ranks
- Designations
- Command priorities

### **Shadow Core K-Levels** (Next)
- ~18 characters
- 3 K-levels
- Sigil assignments
- Essence types
- Spiritual designations

### **Location Assignments**
```csv
identity_id,primary_location,secondary_location
cmm-kyra,Chicago,Los Angeles
sc-reika,Tokyo,Matsumoto
```

### **Relationship Matrix**
```csv
identity_a,identity_b,relationship_type,status
cmm-aegis,sc-kenji,romantic,strained
sc-akira,sc-ayana,sibling,twin
```

### **Timeline Events** (Phase 5D)
```csv
identity_id,event_date,event_type,location,description
cmm-aegis,2025-03-15,mission_victory,Shenzhen,Defeated Aaster
```

---

## 📊 Data Format Decision Tree

```
Need to update character data?
├─ Single character? → Direct SQL or Python script
├─ Multiple characters, structured data? → CSV
├─ Narrative backstory? → PDF
└─ Complex nested structure? → JSON
```

---

## 🔄 Iteration Pattern

### **First Time:**
1. Create CSV structure
2. Write import script
3. Test on database
4. Verify results

### **Subsequent Updates:**
1. Update CSV files
2. Re-run import script (updates existing)
3. Verify changes

**Benefit:** Script can be re-run safely, will UPDATE existing records!

---

## ✅ Best Practices

### **CSV Creation:**
- ✅ Use consistent ID patterns (faction-name)
- ✅ UTF-8 encoding always
- ✅ Include header row
- ✅ No spaces in column names (use underscores)
- ✅ Empty fields okay (will be NULL)
- ✅ Quote fields with commas

### **Import Scripts:**
- ✅ Check file existence first
- ✅ Use transactions (commit at end)
- ✅ UPDATE existing, INSERT new
- ✅ Store metadata in JSON fields
- ✅ Print progress and verification
- ✅ Handle errors gracefully

### **Verification:**
- ✅ Count before/after
- ✅ Check for duplicates
- ✅ Verify relationships
- ✅ Sample random records

---

## 🎨 Example: Shadow Core K-Levels (Template)

If you want to do Shadow Core next, structure would be:

### **identities_shadowcore.csv**
```csv
id,name,codename,sigil,essence,role,status
sc-reika,Reika Frost,Frost-Heart,Frost-Heart,Ice,Commander,active
sc-kenji,Kenji Hoshinaga,Azure Line,Azure Line,Water,Operative,active
```

### **identities_shadowcore_levels.csv**
```csv
identity_id,klevel
sc-reika,03
sc-kenji,01
```

### **identities_shadowcore_sigils.csv**
```csv
identity_id,sigil_name,sigil_type,verified_by
sc-reika,Frost-Heart,Ice,Shion
sc-kenji,Azure Line,Water,Shion
```

---

## 📝 Summary

**CSV approach is perfect for:**
- ✅ Bulk character updates
- ✅ K-level systems
- ✅ Affiliation changes
- ✅ Structured metadata
- ✅ Version-controlled data

**This pattern scales to:**
- Shadow Core k-levels
- Location assignments
- Relationship matrices
- Timeline events (Phase 5D)
- Any structured bulk update

**CMM test case proves the workflow - ready to apply to Shadow Core immediately if needed!**

---

## 🚀 Next Steps

1. **Run CMM import** to test the pattern
2. **Verify results** with explore_database.py
3. **Prepare Shadow Core CSVs** (if ready)
4. **Adapt import script** for Shadow Core
5. **Rinse and repeat** for other data types

**The infrastructure is ready - just need the data files!** 🎯
