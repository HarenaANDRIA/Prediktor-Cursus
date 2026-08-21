import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuration globale du style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.titlesize': 14
})

def nettoyer_et_convertir(df, feature_cols):
    """Convertit proprement les colonnes numériques en nettoyant les décimales avec virgule."""
    df_clean = df.copy()
    for col in feature_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(
                df_clean[col].astype(str).str.replace(',', '.'), 
                errors='coerce'
            )
    return df_clean


def generer_statistiques_avancees(df, feature_cols):
    """Génère un tableau récapitulatif complet des métriques statistiques."""
    valid_features = [c for c in feature_cols if c in df.columns]
    if not valid_features:
        return pd.DataFrame()

    stats_list = []
    for col in valid_features:
        series = df[col].dropna()
        q25, q75 = series.quantile(0.25), series.quantile(0.75)
        iqr = q75 - q25
        outliers_count = ((series < (q25 - 1.5 * iqr)) | (series > (q75 + 1.5 * iqr))).sum()
        
        stats_list.append({
            'Variable': col,
            'Effectif': series.count(),
            'Manquants (%)': round((df[col].isnull().sum() / len(df)) * 100, 2),
            'Moyenne': round(series.mean(), 2),
            'Écart-type': round(series.std(), 2),
            'Médiane': round(series.median(), 2),
            'Min': round(series.min(), 2),
            'Max': round(series.max(), 2),
            'Skewness': round(series.skew(), 2),
            'Outliers (IQR)': outliers_count
        })
    
    return pd.DataFrame(stats_list).set_index('Variable')


def generer_graphiques_eda(df, prefix_name, feature_cols, target_col):
    """Génère et sauvegarde des visualisations haute résolution pour l'EDA."""
    output_dir = 'reports/figures'
    os.makedirs(output_dir, exist_ok=True)
    valid_features = [col for col in feature_cols if col in df.columns and df[col].notnull().any()]

    if not valid_features:
        print(f"Aucune caractéristique valide à afficher pour {prefix_name}.")
        return

    # 1. Distributions (Histogame + KDE)
    n_cols = 3
    n_rows = int(np.ceil(len(valid_features) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 3.2 * n_rows))
    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for i, col in enumerate(valid_features):
        sns.histplot(df[col], kde=True, ax=axes[i], color='#3498db', bins=15, stat="density", alpha=0.6)
        axes[i].set_title(f"Distribution : {col}")
        axes[i].set_xlim(0, 20)
        axes[i].set_xlabel("Note (/20)")
        axes[i].set_ylabel("Densité")

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    fig_path = os.path.join(output_dir, f"{prefix_name}_distributions.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  [✓] Graphique généré : '{fig_path}'")

    # 2. Boxplot interactif & dispersion
    plt.figure(figsize=(max(10, len(valid_features) * 0.8), 6))
    sns.boxplot(data=df[valid_features], palette="Blues_r", flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 5})
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Dispersion et Détection des Outliers - {prefix_name}")
    plt.ylabel("Notes (/20)")
    plt.ylim(0, 20.5)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, f"{prefix_name}_boxplots.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  [✓] Graphique généré : '{fig_path}'")

    # 3. Matrice de Corrélation (Heatmap optimisée)
    if len(valid_features) > 1:
        corr = df[valid_features].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        
        plt.figure(figsize=(max(8, len(valid_features) * 0.7), max(6, len(valid_features) * 0.6)))
        annot_size = 8 if len(valid_features) > 12 else 10
        
        sns.heatmap(
            corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", 
            vmin=-1, vmax=1, square=True, linewidths=.5,
            annot_kws={"size": annot_size}, cbar_kws={"shrink": .8}
        )
        plt.title(f"Matrice de Corrélation - {prefix_name}")
        plt.tight_layout()
        fig_path = os.path.join(output_dir, f"{prefix_name}_correlation.png")
        plt.savefig(fig_path, dpi=300)
        plt.close()
        print(f"  [✓] Graphique généré : '{fig_path}'")

    # 4. Distribution de la variable cible (Barplot annoté)
    if target_col in df.columns:
        plt.figure(figsize=(10, max(5, df[target_col].nunique() * 0.4)))
        target_counts = df[target_col].value_counts().reset_index()
        target_counts.columns = [target_col, 'count']
        
        ax = sns.barplot(
            data=target_counts, y=target_col, x='count', 
            hue=target_col, palette="mako", legend=False
        )
        
        # Ajout des annotations avec pourcentage
        total = len(df)
        for p in ax.patches:
            width = p.get_width()
            percentage = f"{width:.0f} ({(width / total)*100:.1f}%)"
            ax.annotate(
                percentage, 
                (width + (total * 0.01), p.get_y() + p.get_height() / 2.),
                ha='left', va='center', fontsize=9, color='black'
            )

        plt.title(f"Répartition de la Cible ('{target_col}') - {prefix_name}")
        plt.xlabel("Nombre d'étudiants")
        plt.ylabel("Recommandation")
        plt.xlim(0, max(target_counts['count']) * 1.18)
        plt.tight_layout()
        fig_path = os.path.join(output_dir, f"{prefix_name}_target_distribution.png")
        plt.savefig(fig_path, dpi=300)
        plt.close()
        print(f"  [✓] Graphique généré : '{fig_path}'")


def analyser_exploratoire(df, title, prefix_name, feature_cols, target_col):
    """Effectue l'analyse exploratoire complète (Console + Graphiques)."""
    print("\n" + "=" * 75)
    print(f"  EDA COMPLET : {title.upper()}")
    print("=" * 75)
    
    print(f"• Dimensions du jeu de données : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    
    print("\n--- Diagnostic des Valeurs Manquantes ---")
    null_counts = df.isnull().sum()
    null_df = pd.DataFrame({'Manquants': null_counts, 'Pourcentage (%)': round((null_counts / len(df)) * 100, 2)})
    print(null_df[null_df['Manquants'] > 0] if null_counts.sum() > 0 else "✓ Aucune valeur manquante détectée.")
    
    print("\n--- Statistiques Descriptives Avancées ---")
    stats_df = generer_statistiques_avancees(df, feature_cols)
    print(stats_df.to_string())
        
    if target_col in df.columns:
        print(f"\n--- Répartition de la Variable Cible ('{target_col}') ---")
        counts = df[target_col].value_counts()
        props = df[target_col].value_counts(normalize=True) * 100
        target_summary = pd.DataFrame({'Effectif': counts, 'Proportion (%)': props.round(2)})
        print(target_summary.to_string())

    print("\n--- Génération des représentations graphiques ---")
    generer_graphiques_eda(df, prefix_name, feature_cols, target_col)


# -------------------------------------------------------------------------
# 1. Analyse du Dataset Baccalauréat
# -------------------------------------------------------------------------
data_path_bac = 'data/raw/dataset_note_etudiant_bac.csv'

if os.path.exists(data_path_bac):
    df_bac = pd.read_csv(data_path_bac, sep=';')
    feature_cols_bac = [
        'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
        'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre'
    ]
    df_bac = nettoyer_et_convertir(df_bac, feature_cols_bac)
    
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
# 2. Analyse du Dataset Spécialisation / Branches
# -------------------------------------------------------------------------
data_path_branch = 'data/raw/dataset_branch_config.csv'

if os.path.exists(data_path_branch):
    df_branch = pd.read_csv(data_path_branch, sep=';')
    non_features = ['filiere', 'branche_recommandee']
    feature_cols_branch = [col for col in df_branch.columns if col not in non_features]
    
    df_branch = nettoyer_et_convertir(df_branch, feature_cols_branch)
        
    analyser_exploratoire(
        df=df_branch, 
        title="dataset_branch_config.csv", 
        prefix_name="branch",
        feature_cols=feature_cols_branch, 
        target_col='branche_recommandee'
    )
else:
    print(f"Fichier introuvable : {data_path_branch}")