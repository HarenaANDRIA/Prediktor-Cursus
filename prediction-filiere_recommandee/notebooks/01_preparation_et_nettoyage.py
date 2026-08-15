# ==============================================================================
# NOTEBOOK 1 : PRÉPARATION ET NETTOYAGE DES DONNÉES
# Objectif : Charger le CSV, vérifier les types, traiter les anomalies/manquants
#            et préparer les ensembles X (features) et y (target).
# ==============================================================================

import os
import pandas as pd
import numpy as np

# 1. Chargement des données brutes
data_path = 'data/raw/dataset_note_etudiant_bac.csv'
df = pd.read_csv(data_path, sep=';')

print("--- Informations générales sur le Dataset ---")
print(f"Dimensions du dataset : {df.shape[0]} lignes, {df.shape[1]} colonnes")
print("\n--- Aperçu des 5 premières lignes ---")
print(df.head())

# 2. Vérification de la structure et des types
print("\n--- Types de données et valeurs non nulles ---")
print(df.info())

# 3. Détection des valeurs manquantes et doublons
print("\n--- Nombre de valeurs manquantes par colonne ---")
print(df.isnull().sum())

num_duplicates = df.duplicated().sum()
print(f"\nNombre de lignes en doublon : {num_duplicates}")

if num_duplicates > 0:
    df = df.drop_duplicates()
    print("Doublons supprimés avec succès.")

# 4. Séparation Features (X) et Cible (y)
X = df.drop(columns=["filiere_recommandee"])
y = df["filiere_recommandee"]

print("\n--- Liste des matières (Features / X) ---")
print(list(X.columns))

print("\n--- Répartition de la variable cible (Filières / y) ---")
print(y.value_counts())

# 5. Sauvegarde des données nettoyées dans data/processed/
df.to_csv('data/processed/dataset_cleaned.csv', sep=';', index=False)
print("\n[OK] Données nettoyées et sauvegardées dans 'data/processed/dataset_cleaned.csv'")