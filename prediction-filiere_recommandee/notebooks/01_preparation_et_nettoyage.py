import os
import pandas as pd

# 1. Chargement des données brutes
data_path = 'data/raw/dataset_note_etudiant_bac.csv'
df = pd.read_csv(data_path, sep=';')

# Nettoyage des doublons
df = df.drop_duplicates()

# Les 15 matières du dataset
notes_cols = [
    'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
    'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
    'informatique', 'economie_generale', 'education_physique_et_sportive',
    'dessin_technique_et_arts_appliques', 'statistiques_et_probabilites',
    'biologie_appliquee_et_biotechnologie'
]

# Conversion numérique des notes (gestion du séparateur décimal)
for col in notes_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

# Suppression des valeurs manquantes et réinitialisation de l'index
df = df.dropna().reset_index(drop=True)

# Sauvegarde du dataset nettoyé (sans aucune augmentation synthétique)
os.makedirs('data/processed', exist_ok=True)
df.to_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',', index=False)

print(f"✅ Dataset réel nettoyé ({len(df)} lignes) sauvegardé sans augmentation synthétique.")