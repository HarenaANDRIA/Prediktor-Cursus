import os
import pandas as pd
import numpy as np

# 1. Chargement des données brutes
data_path = 'data/raw/dataset_note_etudiant_bac.csv'
df = pd.read_csv(data_path, sep=';')

# Nettoyage des doublons
df = df.drop_duplicates()

# Les 12 matières réelles du dataset
feature_cols = [
    'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
    'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
    'statistiques_et_probabilites'
]

# Conversion numérique
for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

df = df.dropna().reset_index(drop=True)

# 2. Sauvegarde du dataset nettoyé
os.makedirs('data/processed', exist_ok=True)
df.to_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',', index=False)
print(f"✅ Dataset nettoyé ({len(df)} lignes) sauvegardé.")