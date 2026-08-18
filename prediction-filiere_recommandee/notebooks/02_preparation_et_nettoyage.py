import os
import pandas as pd
import numpy as np

os.makedirs('data/processed', exist_ok=True)

series_list = ['aucune', 'scientifique', 'litteraire', 'ose']

for serie in series_list:
    data_path_bac = f'data/raw/dataset_bac_{serie}.csv'

    if os.path.exists(data_path_bac):
        df_bac = pd.read_csv(data_path_bac, sep=';')
        df_bac = df_bac.drop_duplicates()

        feature_cols_bac = [col for col in df_bac.columns if col != 'filiere_recommandee']

        for col in feature_cols_bac:
            df_bac[col] = pd.to_numeric(df_bac[col].astype(str).str.replace(',', '.'), errors='coerce')

        df_bac = df_bac.dropna().reset_index(drop=True)
        out_bac = f'data/processed/cleaned_bac_{serie}.csv'
        df_bac.to_csv(out_bac, sep=';', decimal=',', index=False)
        print(f"✅ Dataset Bac ({serie}) nettoyé ({len(df_bac)} lignes) -> '{out_bac}'.")

# Traitement du dataset branches universitaires
data_path_branch = 'data/raw/dataset_branch_config.csv'

if os.path.exists(data_path_branch):
    try:
        df_branch = pd.read_csv(data_path_branch, sep=';')
        if len(df_branch.columns) <= 1:
            df_branch = pd.read_csv(data_path_branch, sep=',')
    except Exception:
        df_branch = pd.read_csv(data_path_branch, sep=',')

    df_branch = df_branch.drop_duplicates()
    non_feature_cols = ['filiere', 'branche_recommandee']
    feature_cols_branch = [col for col in df_branch.columns if col not in non_feature_cols]

    for col in feature_cols_branch:
        df_branch[col] = pd.to_numeric(df_branch[col].astype(str).str.replace(',', '.'), errors='coerce')

    df_branch[feature_cols_branch] = df_branch[feature_cols_branch].fillna(df_branch[feature_cols_branch].mean())
    df_branch = df_branch.dropna(subset=non_feature_cols).reset_index(drop=True)

    out_path_branch = 'data/processed/dataset_branch_cleaned.csv'
    df_branch.to_csv(out_path_branch, sep=';', decimal=',', index=False)
    print(f"✅ Dataset Branch nettoyé ({len(df_branch)} lignes) -> '{out_path_branch}'.")