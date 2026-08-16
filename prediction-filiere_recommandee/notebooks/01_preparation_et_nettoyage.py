import os
import pandas as pd
import numpy as np

# 1. Chargement des données brutes
data_path = 'data/raw/dataset_note_etudiant_bac.csv'
df = pd.read_csv(data_path, sep=';')

# Nettoyage des doublons
df = df.drop_duplicates()

# Les 15 matières réelles du dataset
feature_cols = [
    'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
    'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
    'informatique', 'economie_generale', 'education_physique_et_sportive',
    'dessin_technique_et_arts_appliques', 'statistiques_et_probabilites',
    'biologie_appliquee_et_biotechnologie'
]

# Conversion numérique
for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

df = df.dropna().reset_index(drop=True)

# 2. Augmentation conditionnelle sur les 25 filières
def augmenter_dataset_par_filiere(df_in, n_samples_par_filiere=200, noise_factor=0.05, random_state=42):
    np.random.seed(random_state)
    augmented_dfs = []
    
    for filiere, group in df_in.groupby("filiere_recommandee"):
        X_group = group[feature_cols]
        mean_vector = X_group.mean()
        cov_matrix = X_group.cov() + np.eye(len(feature_cols)) * noise_factor
        
        synthetic_data = np.random.multivariate_normal(
            mean=mean_vector, cov=cov_matrix, size=n_samples_par_filiere
        )
        
        df_synth = pd.DataFrame(synthetic_data, columns=feature_cols)
        df_synth = df_synth.clip(lower=0.0, upper=20.0).round(2)
        df_synth["filiere_recommandee"] = filiere
        augmented_dfs.append(df_synth)
        
    df_aug = pd.concat(augmented_dfs, ignore_index=True)
    return df_aug.sample(frac=1, random_state=random_state).reset_index(drop=True)

df_augmented = augmenter_dataset_par_filiere(df, n_samples_par_filiere=200)

os.makedirs('data/processed', exist_ok=True)
df_augmented.to_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',', index=False)
print(f"✅ Dataset augmenté ({len(df_augmented)} lignes) sauvegardé pour les 25 filières.")