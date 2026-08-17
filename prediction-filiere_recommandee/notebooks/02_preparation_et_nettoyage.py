import os
import pandas as pd
import numpy as np

os.makedirs('data/processed', exist_ok=True)

# =========================================================================
# 1. Traitement de dataset_note_etudiant_bac.csv (Fonctionnalités préservées)
# =========================================================================
data_path_bac = 'data/raw/dataset_note_etudiant_bac.csv'

if os.path.exists(data_path_bac):
    df_bac = pd.read_csv(data_path_bac, sep=';')

    # Nettoyage des doublons
    df_bac = df_bac.drop_duplicates()

    # Les 12 matières réelles du dataset
    feature_cols_bac = [
        'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
        'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
        'statistiques_et_probabilites'
    ]

    # Conversion numérique
    for col in feature_cols_bac:
        if col in df_bac.columns:
            df_bac[col] = pd.to_numeric(df_bac[col].astype(str).str.replace(',', '.'), errors='coerce')

    df_bac = df_bac.dropna().reset_index(drop=True)

    # Sauvegarde du dataset nettoyé
    df_bac.to_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',', index=False)
    print(f"✅ Dataset Bac nettoyé ({len(df_bac)} lignes) sauvegardé dans 'data/processed/dataset_cleaned.csv'.")
else:
    print(f"⚠️ Fichier introuvable : {data_path_bac}")


# =========================================================================
# 2. Traitement de dataset_branch_config.csv (Correction du dropna)
# =========================================================================
data_path_branch = 'data/raw/dataset_branch_config.csv'

if os.path.exists(data_path_branch):
    # Detection automatique du séparateur (';' ou ',')
    try:
        df_branch = pd.read_csv(data_path_branch, sep=';')
        if len(df_branch.columns) <= 1:
            df_branch = pd.read_csv(data_path_branch, sep=',')
    except Exception:
        df_branch = pd.read_csv(data_path_branch, sep=',')

    # Nettoyage des doublons
    df_branch = df_branch.drop_duplicates()

    # Détection dynamique des colonnes de notes (features)
    non_feature_cols = ['filiere', 'branche_recommandee']
    feature_cols_branch = [col for col in df_branch.columns if col not in non_feature_cols]

    # Conversion numérique et nettoyage
    for col in feature_cols_branch:
        df_branch[col] = pd.to_numeric(
            df_branch[col].astype(str).str.replace(',', '.'), 
            errors='coerce'
        )

    # Si une valeur manque accidentellement, on la comble par la moyenne globale du module
    df_branch[feature_cols_branch] = df_branch[feature_cols_branch].fillna(df_branch[feature_cols_branch].mean())

    # Supprimer uniquement si 'filiere' ou 'branche_recommandee' est manquante
    df_branch = df_branch.dropna(subset=non_feature_cols).reset_index(drop=True)

    # Sauvegarde dans data/processed
    out_path_branch = 'data/processed/dataset_branch_cleaned.csv'
    df_branch.to_csv(out_path_branch, sep=';', decimal=',', index=False)
    print(f"✅ Dataset Branch nettoyé ({len(df_branch)} lignes) sauvegardé dans '{out_path_branch}'.")
else:
    print(f"⚠️ Fichier introuvable : {data_path_branch}")