# ==============================================================================
# NOTEBOOK 2 : ANALYSE EXPLORATOIRE DES DONNÉES (EDA) - CORRIGÉ (15 MATIÈRES)
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration du style graphique
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette("husl")

# Chargement du dataset nettoyé
df = pd.read_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',')
feature_cols = [col for col in df.columns if col != "filiere_recommandee"]

# Force la conversion des colonnes de notes en valeurs numériques
for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

# 1. Statistiques descriptives globales
print("--- Statistiques descriptives des notes sur 20 ---")
print(df[feature_cols].describe().loc[['mean', 'std', 'min', '50%', 'max']])

# 2. Distribution des 15 notes par matière (Grille 4x4)
plt.figure(figsize=(16, 12))
for i, col in enumerate(feature_cols, 1):
    plt.subplot(4, 4, i)  # Adapté pour contenir jusqu'à 16 sous-graphiques
    sns.histplot(df[col], kde=True, color="skyblue")
    plt.title(f"{col}", fontsize=9)
    plt.xlabel("Note / 20", fontsize=8)
    plt.ylabel("Effectif", fontsize=8)

plt.tight_layout()
plt.savefig("eda_distributions_notes.png", dpi=150)
plt.show()

# 3. Matrice de corrélation (15x15)
plt.figure(figsize=(12, 10))
corr = df[feature_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, annot_kws={"size": 8})
plt.title("Matrice de Corrélation entre les 15 Matières")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig("eda_matrice_correlation.png", dpi=150)
plt.show()

# 4. Profil moyen des notes par filière recommandée
plt.figure(figsize=(16, 10))
filiere_means = df.groupby("filiere_recommandee")[feature_cols].mean()
sns.heatmap(filiere_means, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Note moyenne / 20'}, annot_kws={"size": 7})
plt.title("Moyenne des Notes obtenues par Filière Recommandée")
plt.ylabel("Filière Recommandée")
plt.xlabel("Matières")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig("eda_profil_moyen_filieres.png", dpi=150)
plt.show()