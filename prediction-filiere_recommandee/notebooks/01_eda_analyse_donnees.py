import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuration du style des graphiques
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10, 'figure.titlesize': 14})

def generer_graphiques_eda(df, prefix_name, feature_cols, target_col):
    """Génère et sauvegarde des représentations graphiques pour l'analyse exploratoire."""
    output_dir = 'reports/figures'
    os.makedirs(output_dir, exist_ok=True)
    valid_features = [col for col in feature_cols if col in df.columns]

    # 1. Histogramme & KDE des distributions des notes / modules
    if valid_features:
        n_cols = 3
        n_rows = int(np.ceil(len(valid_features) / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 3 * n_rows))
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        for i, col in enumerate(valid_features):
            sns.histplot(df[col], kde=True, ax=axes[i], color='skyblue', bins=15)
            axes[i].set_title(f"Distribution : {col}")
            axes[i].set_xlim(0, 20)
            axes[i].set_xlabel("Note (/20)")
            axes[i].set_ylabel("Fréquence")

        # Cacher les sous-graphiques inutilisés
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        fig_path = os.path.join(output_dir, f"{prefix_name}_distributions.png")
        plt.savefig(fig_path, dpi=300)
        plt.close()
        print(f"Graphique généré : '{fig_path}'")

    # 2. Boxplot général (Détection des outliers & dispersion)
    if valid_features:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df[valid_features], palette="Set3")
        plt.xticks(rotation=45, ha='right')
        plt.title(f"Boxplot des notes - {prefix_name}")
        plt.ylabel("Notes (/20)")
        plt.ylim(0, 20.5)
        plt.tight_layout()
        fig_path = os.path.join(output_dir, f"{prefix_name}_boxplots.png")
        plt.savefig(fig_path, dpi=300)
        plt.close()
        print(f"Graphique généré : '{fig_path}'")

    # 3. Matrice de Corrélation (Heatmap)
    if len(valid_features) > 1:
        plt.figure(figsize=(10, 8))
        corr = df[valid_features].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True)
        plt.title(f"Matrice de Corrélation - {prefix_name}")
        plt.tight_layout()
        fig_path = os.path.join(output_dir, f"{prefix_name}_correlation.png")
        plt.savefig(fig_path, dpi=300)
        plt.close()
        print(f"Graphique généré : '{fig_path}'")

    # 4. Distribution de la variable cible (Barplot)
    if target_col in df.columns:
        plt.figure(figsize=(12, 6))
        order = df[target_col].value_counts().index
        sns.countplot(data=df, y=target_col, order=order, palette="viridis")
        plt.title(f"Répartition des Recommandations ('{target_col}') - {prefix_name}")
        plt.xlabel("Nombre d'étudiants")
        plt.ylabel("Branche / Filière")
        plt.tight_layout()
        fig_path = os.path.join(output_dir, f"{prefix_name}_target_distribution.png")
        plt.savefig(fig_path, dpi=300)
        plt.close()
        print(f"Graphique généré : '{fig_path}'")


def analyser_exploratoire(df, title, prefix_name, feature_cols, target_col):
    """Effectue une analyse exploratoire (EDA) textuelle et graphique d'un dataset."""
    print("=" * 70)
    print(f"EDA & ANALYSE EXPLORATOIRE : {title}")
    print("=" * 70)
    
    print(f"• Dimensions (lignes, colonnes) : {df.shape}")
    print(f"• Liste des colonnes            : {list(df.columns)}")
    
    print("\n--- Diagnostic des Valeurs Manquantes ---")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "Aucune valeur manquante détectée.")
    
    print("\n--- Statistiques Descriptives ---")
    valid_features = [col for col in feature_cols if col in df.columns]
    if valid_features:
        stats = df[valid_features].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']]
        print(stats.round(2))
        
    if target_col in df.columns:
        print(f"\n--- Distribution de la Cible ('{target_col}') ---")
        print(df[target_col].value_counts())
    print("\n--- Génération des représentations graphiques ---")
    generer_graphiques_eda(df, prefix_name, feature_cols, target_col)
    print("\n")


# -------------------------------------------------------------------------
# 1. Analyse exploratoire du premier dataset : dataset_note_etudiant_bac.csv
# -------------------------------------------------------------------------
data_path_bac = 'data/raw/dataset_note_etudiant_bac.csv'

if os.path.exists(data_path_bac):
    df_bac = pd.read_csv(data_path_bac, sep=';')
    feature_cols_bac = [
        'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
        'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
        'statistiques_et_probabilites'
    ]
    # Conversion numérique pour les graphiques
    for col in feature_cols_bac:
        if col in df_bac.columns:
            df_bac[col] = pd.to_numeric(df_bac[col].astype(str).str.replace(',', '.'), errors='coerce')
            
    analyser_exploratoire(
        df=df_bac, 
        title="dataset_note_etudiant_bac.csv", 
        prefix_name="bac",
        feature_cols=feature_cols_bac, 
        target_col='filiere_recommandee'
    )
else:
    print(f"Fichier introuvable : {data_path_bac}")


# -------------------------------------------------------------------------
# 2. Analyse exploratoire du second dataset : dataset_branch_config.csv
# -------------------------------------------------------------------------
data_path_branch = 'data/raw/dataset_branch_config.csv'

if os.path.exists(data_path_branch):
    df_branch = pd.read_csv(data_path_branch, sep=';')
    non_features = ['filiere', 'branche_recommandee']
    feature_cols_branch = [col for col in df_branch.columns if col not in non_features]
    
    # Conversion numérique pour les graphiques
    for col in feature_cols_branch:
        df_branch[col] = pd.to_numeric(df_branch[col].astype(str).str.replace(',', '.'), errors='coerce')
        
    analyser_exploratoire(
        df=df_branch, 
        title="dataset_branch_config.csv", 
        prefix_name="branch",
        feature_cols=feature_cols_branch, 
        target_col='branche_recommandee'
    )
else:
    print(f"Fichier introuvable : {data_path_branch}")