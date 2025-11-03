#!/usr/bin/env python3
"""Shadow Core Resonance System Import"""
import sqlite3, csv, sys, json
from pathlib import Path

def read_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def main():
    if len(sys.argv) != 3:
        print("Usage: python import_shadow_core_resonance.py <db> <csv_dir>")
        sys.exit(1)
    
    db_path, csv_dir = sys.argv[1], Path(sys.argv[2])
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("SHADOW CORE RESONANCE SYSTEM IMPORT")
    print("=" * 70)
    
    # Load CSVs
    levels = read_csv(csv_dir / 'resonance_levels.csv')
    holders = read_csv(csv_dir / 'resonance_level_holders.csv')
    sigils = read_csv(csv_dir / 'sigils_codex.csv')
    
    print(f"\n✓ Loaded {len(levels)} tiers, {len(holders)} holders, {len(sigils)} Sigils\n")
    
    # Get IDs
    cursor.execute("SELECT corp_id FROM corporations WHERE corp_name = 'Nexus Enraenra'")
    nexus_id = cursor.fetchone()[0]
    cursor.execute("SELECT division_id FROM divisions WHERE division_name = 'Shadow Core'")
    shadow_id = cursor.fetchone()[0]
    
    # Create Sigil lookup
    sigils_by_bearer = {s['bearer_id']: s for s in sigils}
    
    # Process holders
    for h in holders:
        holder_id = h['holder_id']
        name = ' '.join(w.capitalize() for w in holder_id.split('_'))
        tier = int(h['tier'])  # Convert to int for formatting
        rrl = h['rrl_code']
        
        # Get tier definition (convert back to string for lookup)
        tier_def = next((r for r in levels if r['tier'] == str(tier)), None)
        title = tier_def['title'] if tier_def else ''
        
        # Get Sigil
        sigil = sigils_by_bearer.get(holder_id, {})
        
        print(f"🌸 {name} - RRL Tier {tier}")
        if sigil:
            print(f"   Sigil: {sigil.get('id')} ({sigil.get('kanji')})")
            print(f"   Aspect: {sigil.get('aspect')}")
        
        # Update character
        cursor.execute("SELECT character_id, character_secrets FROM characters WHERE character_name = ?", (name,))
        result = cursor.fetchone()
        if not result:
            print(f"   ⚠ Not found - run Phase 5B first\n")
            continue
        
        char_id, secrets = result
        secrets_dict = json.loads(secrets) if secrets else {}
        
        # Add RRL + Sigil data
        secrets_dict.update({
            'rrl_tier': tier,
            'rrl_code': rrl,
            'rrl_title': title
        })
        
        if sigil:
            secrets_dict['sigil'] = {
                'id': sigil.get('id'),
                'kanji': sigil.get('kanji'),
                'aspect': sigil.get('aspect'),
                'orchid': sigil.get('orchid'),
                'power': sigil.get('power'),
                'curse': sigil.get('curse')
            }
        
        cursor.execute("UPDATE characters SET character_secrets = ? WHERE character_id = ?",
                      (json.dumps(secrets_dict), char_id))
        
        # Update affiliation
        cursor.execute("UPDATE character_corporate_affiliations SET clearance_level = ? WHERE character_id = ?",
                      (f"{tier:02d}", char_id))
        
        print(f"   ✓ Updated\n")
    
    conn.commit()
    print("=" * 70)
    print("✅ COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
