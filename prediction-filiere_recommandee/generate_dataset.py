"""
Génération synthétique des 4 datasets Bac par Série :
- dataset_bac_aucune.csv
- dataset_bac_scientifique.csv
- dataset_bac_litteraire.csv
- dataset_bac_ose.csv
"""

import numpy as np
import pandas as pd
import os

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

ALL_FEATURE_COLS = [
    'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
    'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
    'statistiques_et_probabilites'
]

SERIES_CONFIG = {
    'aucune': {
        'features': ALL_FEATURE_COLS,
        'filieres': [
            'science_des_donnees_et_intelligence_artificielle', 'medecine_et_pharmacie',
            'agronomie_et_biotechnologie', 'sciences_environnementales', 'science_marine',
            'tourisme_et_hotellerie', 'langues_et_communication', 'sociologie',
            'sciences_actuarielles', 'ingenierie_et_science_generale',
            'droit_et_sciences_politiques', 'psychologie', 'anthropologie', 'archeologie'
        ]
    },
    'scientifique': {
        'features': ALL_FEATURE_COLS,
        'filieres': [
            'science_des_donnees_et_intelligence_artificielle', 'medecine_et_pharmacie',
            'agronomie_et_biotechnologie', 'sciences_environnementales', 'science_marine',
            'tourisme_et_hotellerie', 'langues_et_communication', 'sociologie',
            'sciences_actuarielles', 'ingenierie_et_science_generale',
            'droit_et_sciences_politiques', 'psychologie', 'anthropologie', 'archeologie'
        ]
    },
    'litteraire': {
        'features': [
            'francais', 'histoire_et_geographie', 'philosophie', 'anglais',
            'test_psychotechnique', 'statistiques_et_probabilites'
        ],
        'filieres': [
            'tourisme_et_hotellerie', 'langues_et_communication', 'sociologie',
            'droit_et_sciences_politiques', 'psychologie', 'anthropologie', 'archeologie'
        ]
    },
    'ose': {
        'features': [
            'mathematiques', 'francais', 'histoire_et_geographie', 'philosophie',
            'anglais', 'test_psychotechnique', 'statistiques_et_probabilites'
        ],
        'filieres': [
            'tourisme_et_hotellerie', 'langues_et_communication', 'sociologie',
            'droit_et_sciences_politiques', 'psychologie', 'anthropologie', 'archeologie',
            'sciences_actuarielles', 'science_des_donnees_et_intelligence_artificielle'
        ]
    }
}

FILIERES_INFO = {
    'science_des_donnees_et_intelligence_artificielle': {
        'label': "Science des Données et Intelligence Artificielle",
        'required': ['mathematiques', 'statistiques_et_probabilites', 'test_psychotechnique'],
        'single_rule': None,
    },
    'medecine_et_pharmacie': {
        'label': "Médecine et Pharmacie",
        'required': ['science_de_la_vie_et_de_la_terre', 'chimie'],
        'single_rule': ['science_de_la_vie_et_de_la_terre', 'chimie'],
    },
    'agronomie_et_biotechnologie': {
        'label': "Agronomie et Biotechnologie",
        'required': ['mathematiques', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre'],
        'single_rule': None,
    },
    'sciences_environnementales': {
        'label': "Sciences Environnementales",
        'required': ['mathematiques', 'science_de_la_vie_et_de_la_terre'],
        'single_rule': None,
    },
    'science_marine': {
        'label': "Science Marine",
        'required': ['science_de_la_vie_et_de_la_terre', 'mathematiques'],
        'single_rule': ['science_de_la_vie_et_de_la_terre'],
    },
    'tourisme_et_hotellerie': {
        'label': "Tourisme et Hôtellerie",
        'required': ['histoire_et_geographie', 'francais', 'anglais'],
        'single_rule': None,
    },
    'langues_et_communication': {
        'label': "Langues et Communication",
        'required': ['francais', 'anglais'],
        'single_rule': ['francais', 'anglais'],
    },
    'sociologie': {
        'label': "Sociologie",
        'required': ['philosophie', 'anglais', 'francais'],
        'single_rule': ['philosophie'],
    },
    'sciences_actuarielles': {
        'label': "Sciences Actuarielles",
        'required': ['francais', 'anglais', 'statistiques_et_probabilites'],
        'single_rule': ['statistiques_et_probabilites'],
    },
    'ingenierie_et_science_generale': {
        'label': "Ingénierie et Science Générale",
        'required': ['mathematiques', 'physique', 'chimie', 'test_psychotechnique'],
        'single_rule': ['mathematiques', 'physique'],
    },
    'droit_et_sciences_politiques': {
        'label': "Droit et Sciences Politiques",
        'required': ['histoire_et_geographie', 'francais', 'anglais', 'test_psychotechnique'],
        'single_rule': None,
    },
    'psychologie': {
        'label': "Psychologie",
        'required': ['philosophie', 'test_psychotechnique'],
        'single_rule': ['test_psychotechnique'],
    },
    'anthropologie': {
        'label': "Anthropologie",
        'required': ['histoire_et_geographie', 'francais'],
        'single_rule': ['histoire_et_geographie'],
    },
    'archeologie': {
        'label': "Archéologie",
        'required': ['histoire_et_geographie', 'francais'],
        'single_rule': ['histoire_et_geographie'],
    },
}

N_PER_CLASS = 600
NOISE_STD = 1.6

def clip_round(x):
    return float(np.clip(round(x, 2), 0, 20))

def make_row(filiere, profile, feature_cols):
    info = FILIERES_INFO[filiere]
    required = [c for c in info['required'] if c in feature_cols]
    single_rules = [c for c in (info['single_rule'] or []) if c in feature_cols]

    notes = {col: clip_round(rng.normal(loc=9.5, scale=NOISE_STD)) for col in feature_cols}

    if profile == 'extreme':
        for col in required:
            notes[col] = clip_round(rng.uniform(15.0, 20.0))
    elif profile == 'moderate':
        for col in required:
            notes[col] = clip_round(rng.uniform(12.0, 16.5))
    elif profile == 'single' and len(single_rules) > 0:
        chosen = rng.choice(single_rules)
        notes[chosen] = clip_round(rng.uniform(15.0, 20.0))
    elif profile == 'borderline':
        for col in feature_cols:
            notes[col] = clip_round(rng.normal(loc=10.0, scale=0.8))
        for col in required:
            notes[col] = clip_round(notes[col] + rng.uniform(0.5, 2.0))

    notes['filiere_recommandee'] = info['label']
    return notes

def generate_dataset_for_serie(serie_key):
    config = SERIES_CONFIG[serie_key]
    feature_cols = config['features']
    allowed_filieres = config['filieres']

    rows = []
    for filiere in allowed_filieres:
        info = FILIERES_INFO[filiere]
        if info['single_rule'] is None:
            profile_plan = (['extreme'] * int(N_PER_CLASS * 0.62) +
                             ['moderate'] * int(N_PER_CLASS * 0.33) +
                             ['borderline'] * int(N_PER_CLASS * 0.05))
        else:
            profile_plan = (['extreme'] * int(N_PER_CLASS * 0.50) +
                             ['moderate'] * int(N_PER_CLASS * 0.30) +
                             ['single'] * int(N_PER_CLASS * 0.15) +
                             ['borderline'] * int(N_PER_CLASS * 0.05))

        while len(profile_plan) < N_PER_CLASS:
            profile_plan.append('moderate')
        profile_plan = profile_plan[:N_PER_CLASS]
        rng.shuffle(profile_plan)

        for profile in profile_plan:
            rows.append(make_row(filiere, profile, feature_cols))

    df = pd.DataFrame(rows)
    df = df[feature_cols + ['filiere_recommandee']]
    df = df.sample(frac=1.0, random_state=RNG_SEED).reset_index(drop=True)

    os.makedirs('data/raw', exist_ok=True)
    out_path = f'data/raw/dataset_bac_{serie_key}.csv'
    df.to_csv(out_path, sep=';', decimal=',', index=False)
    print(f"✅ Dataset Série {serie_key.upper()} généré : {len(df)} lignes, {len(feature_cols)} matières, {df['filiere_recommandee'].nunique()} filières.")

if __name__ == '__main__':
    for serie in SERIES_CONFIG.keys():
        generate_dataset_for_serie(serie)