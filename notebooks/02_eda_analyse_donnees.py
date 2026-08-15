# ==============================================================================
# NOTEBOOK 2 : ANALYSE EXPLORATOIRE DES DONNÉES (EDA)
# Objectif : Analyser les statistiques, la distribution des notes, les corrélations
#            et les profils de notes par filière avec des visualisations.
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration du style graphique
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette("husl")

# Chargement avec gestion des virgules décimales
df = pd.read_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',')
feature_cols = [col for col in df.columns if col != "filiere_recommandee"]

# Force la conversion des colonnes de notes en valeurs numériques
for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

# 1. Statistiques descriptives globales
print("--- Statistiques descriptives des notes sur 20 ---")
print(df[feature_cols].describe().loc[['mean', 'std', 'min', '50%', 'max']])

# 2. Distribution des notes par matière (Histogrammes & KDE)
plt.figure(figsize=(14, 10))
for i, col in enumerate(feature_cols, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df[col], kde=True, color="skyblue")
    plt.title(f"Distribution : {col}")
    plt.xlabel("Note / 20")
    plt.ylabel("Effectif")
plt.tight_layout()
plt.savefig("eda_distributions_notes.png", dpi=150)
plt.show()

# 3. Matrice de corrélation entre les matières
plt.figure(figsize=(10, 8))
corr = df[feature_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
plt.title("Matrice de Corrélation entre les Matières au Bac")
plt.tight_layout()
plt.savefig("eda_matrice_correlation.png", dpi=150)
plt.show()

# 4. Profil moyen des notes par filière recommandée
plt.figure(figsize=(14, 8))
filiere_means = df.groupby("filiere_recommandee")[feature_cols].mean()
sns.heatmap(filiere_means, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Note moyenne / 20'})
plt.title("Moyenne des Notes obtenues par Filière Recommandée")
plt.ylabel("Filière Recommandée")
plt.xlabel("Matières")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("eda_profil_moyen_filieres.png", dpi=150)
plt.show()

# 5. Boxplot : Distribution de Mathématiques par Filière
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="filiere_recommandee", y="mathematiques")
plt.xticks(rotation=45, ha="right")
plt.title("Distribution des notes en Mathématiques par Filière")
plt.tight_layout()
plt.savefig("eda_boxplot_maths_par_filiere.png", dpi=150)
plt.show()