#!/usr/bin/env python3
"""
Script pour analyser la taxonomie IAB
"""

import pandas as pd

def analyze_taxonomy():
    print("🔍 Analyse de la taxonomie IAB...")
    
    # Charger le fichier
    df = pd.read_csv('data/Content Taxonomy 3.1.tsv', sep='\t', skiprows=3, engine='python')
    df.columns = ['Unique ID', 'Parent', 'Name', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Extension']
    
    print(f"📊 Total d'entrées: {len(df)}")
    
    # Analyser les tiers
    tier1_count = df['Tier 1'].notna().sum()
    tier2_count = df['Tier 2'].notna().sum()
    tier3_count = df['Tier 3'].notna().sum()
    tier4_count = df['Tier 4'].notna().sum()
    
    print(f"📈 Répartition des tiers:")
    print(f"  Tier 1: {tier1_count} entrées")
    print(f"  Tier 2: {tier2_count} entrées") 
    print(f"  Tier 3: {tier3_count} entrées")
    print(f"  Tier 4: {tier4_count} entrées")
    
    # Analyser les catégories Tier 1 (racines)
    tier1_only = df[df['Tier 2'].isna()]
    print(f"\n🌳 Catégories Tier 1 seulement (racines): {len(tier1_only)}")
    
    # Créer le label_text comme dans le notebook
    df['label_text'] = (
        df[['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4']]
        .fillna('')
        .agg(' '.join, axis=1)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
    )
    
    # Mapping ID -> label
    id2label = {str(r['Unique ID']).strip(): r['label_text']
                for _, r in df.iterrows()
                if pd.notna(r['Unique ID']) and str(r['Unique ID']).strip()}
    
    print(f"\n🗂️ Mappings créés: {len(id2label)}")
    
    # Vérifier IAB422
    if '422' in id2label:
        print(f"🔍 IAB422 = '{id2label['422']}'")
    else:
        print("❌ IAB422 non trouvé!")
    
    # Chercher les catégories liées aux voyages
    print(f"\n✈️ Catégories liées aux voyages:")
    travel_found = False
    for code, label in id2label.items():
        if any(keyword in label.lower() for keyword in ['travel', 'vacation', 'tourism', 'trip', 'journey', 'holiday']):
            print(f"  IAB{code}: {label}")
            travel_found = True
    
    if not travel_found:
        print("  ❌ Aucune catégorie voyage trouvée!")
    
    # Catégories Tier 1 uniques
    tier1_labels = df.loc[df['Tier 2'].isna(), 'label_text'].tolist()
    print(f"\n📋 Les {len(tier1_labels)} catégories Tier 1:")
    for i, label in enumerate(tier1_labels, 1):
        print(f"  {i:2d}. {label}")
    
    # Quelques exemples de mappings
    print(f"\n📝 Exemples de mappings (10 premiers):")
    for i, (code, label) in enumerate(list(id2label.items())[:10]):
        print(f"  IAB{code}: {label}")

if __name__ == "__main__":
    analyze_taxonomy()
