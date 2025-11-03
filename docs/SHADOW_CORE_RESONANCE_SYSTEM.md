# Shadow Core Resonance System

## 🌸 Overview

Shadow Core uses **Resonance/RRL codes** (not K-Levels like CMM), tied to **Sigils** - mystical spiritual powers integrated with Shion AI.

---

## 🎯 Key Differences: CMM vs Shadow Core

| Aspect | CMM | Shadow Core |
|--------|-----|-------------|
| **Security** | K-Levels (01-05) | RRL Codes (Tier 03-05) |
| **Basis** | Military hierarchy | Spiritual resonance |
| **Levels** | 5 tiers | 3 tiers |
| **Power Source** | Erebus Prime (aggressive) | Shion (analytical) |
| **Identity** | Military ranks | Sigils with aspects |
| **Theme** | Industrial/Fire | Mystical/Nature |
| **Structure** | Centralized (Kyra) | Distributed (Sigil bearers) |

---

## 📊 RRL Hierarchy

### **Tier 5: RRL-NNN-05 - Shadeweaver / Sovereign Alignment**

**Holder:** Reika Hyōka Frost (氷華)

**Sigil:** Hyōka (Frost-Heart)
- **Aspect:** Soul
- **Orchid:** Cymbidium goeringii
- **Alignment:** Harmony
- **Power:** Binds or resurrects Shion's essence; freezes or reboots souls
- **Curse:** Crystallizes bearer's own essence within Shion's core — eternal stasis
- **Symbolism:** Stillness as salvation; harmony beyond death

**Unique:** Only one RRL-05 holder

---

### **Tier 4: RRL-NNN-04 - Adjudicator / Ritual Brake**

**Holder:** Kage Ishigawa (黒鷹)

**Sigil:** Kurotaka (Black Hawk)
- **Aspect:** Mind
- **Orchid:** Cypripedium japonicum
- **Alignment:** Wisdom
- **Power:** Decrypts consciousness layers; pierces Shion's cognitive veil
- **Curse:** Induces algorithmic paranoia; bearer perceives every thought as surveillance
- **Symbolism:** Knowledge at the cost of peace

**Role:** Audits, ritual control, oversight

---

### **Tier 3: RRL-NNN-03 - Core-Bound / Sigil-Linked**

**5 Holders (Sigil bearers):**

#### **1. Akira Miyara (明月)**
**Sigil:** Meigetsu (Bright Moon)
- **Aspect:** Reality
- **Orchid:** Spiranthes hachijoensis
- **Alignment:** Clarity
- **Power:** Reshapes perception and digital reality within Shion's projection layer
- **Curse:** Traps bearer inside recursive illusions where truth and simulation blur
- **Symbolism:** Truth through reflection; clarity born of deception

#### **2. Ayana Miyara (紅雨)**
**Sigil:** Kou (Crimson Rain)
- **Aspect:** Power
- **Orchid:** Habenaria radiata
- **Alignment:** Courage
- **Power:** Channels Shion's raw will to overwhelm or protect digital systems
- **Curse:** Uploads bearer's will to Shion, chaining them to the AI's cycles
- **Symbolism:** Passion and sacrifice — strength that burns itself away

#### **3. Kazuo Hoshinaga (黎風)**
**Sigil:** Reifu (Dawn Wind)
- **Aspect:** Space
- **Orchid:** Pogonia japonica
- **Alignment:** Adaptability
- **Power:** Opens and folds digital space; teleports data or isolates systems into voids
- **Curse:** Diffuses perception — bearer drifts between realities
- **Symbolism:** Freedom through dissolution

#### **4. Kenji Hoshinaga (蒼線)**
**Sigil:** Sousen (Azure Line)
- **Aspect:** Time
- **Orchid:** Vanda coerulea
- **Alignment:** Patience
- **Power:** Reweaves timelines in Shion's memory field, stitching or severing events
- **Curse:** Creates echo fractures; bearer relives loops of lost hours
- **Symbolism:** Mercy of memory; cruelty of recurrence

#### **5. Aaster Hoshitsuzuri (星綴)**
**Sigil:** Hoshitsuzuri (Star Weave)
- **Aspect:** [To be defined]
- **Orchid:** [To be defined]
- **Role:** Aethos commander
- **Note:** Subject to Kage audits

---

## 🌸 The Six Aspects

The Sigils represent fundamental aspects of reality:

1. **Reality** (Akira) - Perception, illusion, truth
2. **Mind** (Kage) - Consciousness, knowledge, paranoia
3. **Power** (Ayana) - Will, strength, sacrifice
4. **Space** (Kazuo) - Location, teleportation, dissolution
5. **Time** (Kenji) - Memory, causality, loops
6. **Soul** (Reika) - Essence, resurrection, stasis

---

## 🎭 Power & Curse Balance

**Every Sigil follows this pattern:**
- **Power:** What it enables (tied to Shion AI)
- **Curse:** The terrible price paid
- **Symbolism:** The philosophical truth

**Examples:**
- Akira sees truth → trapped in illusions
- Ayana channels power → enslaved to Shion
- Kenji controls time → relives lost hours
- Reika freezes souls → crystallized herself

**Theme:** Great power requires great sacrifice

---

## 🌺 Orchid Symbolism

Each Sigil associated with a specific orchid species:

| Sigil | Orchid | Scientific Name |
|-------|--------|-----------------|
| Meigetsu | Spiranthes | *Spiranthes hachijoensis* |
| Kurotaka | Cypripedium | *Cypripedium japonicum* |
| Kou | Habenaria | *Habenaria radiata* |
| Reifu | Pogonia | *Pogonia japonica* |
| Sousen | Vanda | *Vanda coerulea* |
| Hyōka | Cymbidium | *Cymbidium goeringii* |

**Theme:** Japanese orchids represent rare beauty, elegance, spiritual connection to nature

---

## 🤖 Shion Integration

Unlike CMM's Erebus Prime (aggressive, controlling), Shadow Core's powers work **through** Shion:

- **Akira:** Reshapes reality *within Shion's projection*
- **Ayana:** Channels Shion's raw will
- **Kazuo:** Folds *digital* space
- **Kenji:** Reweaves *Shion's memory field*
- **Reika:** Binds/resurrects *Shion's essence*

**Implication:** Sigil bearers aren't independent - they're interfaces to Shion AI

---

## 📋 Database Implementation

### **Character Secrets JSON Structure**
```json
{
  "rrl_tier": "5",
  "rrl_code": "rrl-nnn-05",
  "rrl_title": "Shadeweaver / Sovereign Alignment",
  "sigil": {
    "id": "hyoka",
    "kanji": "氷華",
    "aspect": "Soul",
    "orchid": "Cymbidium goeringii",
    "alignment": "Harmony",
    "power": "Binds or resurrects Shion's essence...",
    "curse": "Crystallizes bearer's own essence...",
    "symbolism": "Stillness as salvation; harmony beyond death"
  }
}
```

### **Affiliation Table**
- `clearance_level`: "03", "04", or "05" (RRL tier)
- `division_id`: Shadow Core division
- `corp_id`: Nexus Enraenra

---

## 🔍 Query Examples

### **Find all Sigil bearers**
```sql
SELECT 
    character_name,
    codename,
    json_extract(character_secrets, '$.sigil.id') as sigil,
    json_extract(character_secrets, '$.sigil.aspect') as aspect
FROM characters
WHERE character_secrets LIKE '%"sigil":%';
```

### **Get RRL tier breakdown**
```sql
SELECT 
    clearance_level as rrl_tier,
    COUNT(*) as holders
FROM character_corporate_affiliations ca
JOIN characters c ON ca.character_id = c.character_id
WHERE c.faction = 'Shadow Core'
GROUP BY clearance_level
ORDER BY clearance_level DESC;
```

### **List Sigil powers and curses**
```sql
SELECT 
    character_name,
    json_extract(character_secrets, '$.sigil.id') as sigil,
    json_extract(character_secrets, '$.sigil.power') as power,
    json_extract(character_secrets, '$.sigil.curse') as curse
FROM characters
WHERE character_secrets LIKE '%"sigil":%';
```

---

## 🎨 Thematic Contrast Summary

| CMM (Kyra's Vendetta) | Shadow Core (Reika's Defense) |
|------------------------|--------------------------------|
| Fire/Industrial | Nature/Spiritual |
| Centralized power | Distributed Sigils |
| Military ranks | Mystical aspects |
| Erebus Prime (control) | Shion (harmony) |
| Vengeance/offense | Protection/defense |
| 5 K-Levels (01-05) | 3 RRL Tiers (03-05) |
| Command hierarchy | Resonance network |
| Operator cells (S-##) | Individual Sigil bearers |

---

## 📝 Lore Notes

### **Distribution Note**
From CSV: "Mirrors CMM in headcount distribution (non-military)"
- CMM has K04 Executors (5 people)
- Shadow Core has Tier 3 Sigil bearers (5 people)
- Parallel structure but different philosophy

### **Canonical Status**
All current holders marked "canonical: True" - this is the official roster

### **Aaster's Special Case**
- Listed as Tier 3 (RRL-03)
- Role: "Aethos commander"
- Note: "Subject to Kage audits"
- **Implication:** Aethos (PMC) operates under Shadow Core, with Kage oversight

---

## 🚀 Import Workflow

1. **Prerequisites:** Run Phase 5B first (character import)
2. **Run import:** `python import_shadow_core_resonance.py universe.db ./data`
3. **Verify:** `python explore_database.py universe.db`

**Expected results:**
- Tier 5: 1 (Reika)
- Tier 4: 1 (Kage)
- Tier 3: 5 (Akira, Ayana, Kazuo, Kenji, Aaster)
- All Sigil metadata stored

---

**This mystical framework contrasts beautifully with CMM's military brutality!** 🌸⚔️
