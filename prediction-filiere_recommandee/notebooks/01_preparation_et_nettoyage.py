# ==============================================================================
# NOTEBOOK 1 : PRÉPARATION, NETTOYAGE ET AUGMENTATION DES DONNÉES
# Objectif : Charger le CSV brut, nettoyer les types/anomalies, appliquer une
#            augmentation statistique conditionnelle par filière et exporter
#            le jeu de données enrichi pour la modélisation.
# ==============================================================================

import os
import pandas as pd
import numpy as np

# ------------------------------------------------------------------------------
# 1. Chargement des données brutes
# ------------------------------------------------------------------------------
data_path = 'data/raw/dataset_note_etudiant_bac.csv'
df = pd.read_csv(data_path, sep=';')

print("--- Informations générales sur le Dataset Brut ---")
print(f"Dimensions : {df.shape[0]} lignes, {df.shape[1]} colonnes")
print("\nAperçu des 5 premières lignes :")
print(df.head())

# ------------------------------------------------------------------------------
# 2. Nettoyage initial des données
# ------------------------------------------------------------------------------
# Détection des doublons
num_duplicates = df.duplicated().sum()
if num_duplicates > 0:
    df = df.drop_duplicates()
    print(f"\n[INFO] {num_duplicates} doublons supprimés.")

# Saisie des colonnes de caractéristiques
feature_cols = [col for col in df.columns if col != "filiere_recommandee"]

# Conversion forcée des notes en type flottant (remplacement des virgules)
for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

# Suppression des éventuelles lignes contenant des valeurs manquantes
df = df.dropna().reset_index(drop=True)

print("\n--- Répartition initiale de la variable cible ---")
print(df["filiere_recommandee"].value_counts())

# ------------------------------------------------------------------------------
# 3. Augmentation Statistique Conditionnelle par Filière
# ------------------------------------------------------------------------------
def augmenter_dataset_par_filiere(df_in, n_samples_par_filiere=250, noise_factor=0.05, random_state=42):
    """
    Génère de nouveaux profils d'étudiants cohérents en se basant sur 
    la distribution statistique (moyenne et covariance) de chaque filière.
    """
    np.random.seed(random_state)
    augmented_dfs = []
    
    for filiere, group in df_in.groupby("filiere_recommandee"):
        X_group = group[feature_cols]
        
        # Statistiques de la filière
        mean_vector = X_group.mean()
        cov_matrix = X_group.cov()
        
        # Régularisation de la matrice de covariance pour assurer la stabilité
        cov_matrix += np.eye(len(feature_cols)) * noise_factor
        
        # Génération multivariée selon la loi normale
        synthetic_data = np.random.multivariate_normal(
            mean=mean_vector, 
            cov=cov_matrix, 
            size=n_samples_par_filiere
        )
        
        # Création du DataFrame, bornage des notes entre 0.0 et 20.0, et arrondi
        df_synth = pd.DataFrame(synthetic_data, columns=feature_cols)
        df_synth = df_synth.clip(lower=0.0, upper=20.0).round(2)
        df_synth["filiere_recommandee"] = filiere
        
        augmented_dfs.append(df_synth)
        
    # Fusion et mélange (shuffle) du jeu de données final
    df_aug = pd.concat(augmented_dfs, ignore_index=True)
    return df_aug.sample(frac=1, random_state=random_state).reset_index(drop=True)

print("\n--- Génération des données synthétiques ---")
# Génération de 250 exemples par filière (16 filières = 4 000 exemples au total)
df_augmented = augmenter_dataset_par_filiere(df, n_samples_par_filiere=250)

print(f"Taille initiale du dataset : {df.shape[0]} lignes")
print(f"Taille après augmentation  : {df_augmented.shape[0]} lignes")

# ------------------------------------------------------------------------------
# 4. Sauvegarde des Données Traitées
# ------------------------------------------------------------------------------
os.makedirs('data/processed', exist_ok=True)
output_path = 'data/processed/dataset_cleaned.csv'

df_augmented.to_csv(output_path, sep=';', decimal=',', index=False)
print(f"\n[OK] Dataset augmenté et nettoyé sauvegardé avec succès dans '{output_path}'")