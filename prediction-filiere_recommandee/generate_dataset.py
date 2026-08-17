"""
Génération du dataset synthétique 'dataset_note_etudiant_bac.csv'
selon les conditions strictes définies dans conditions.pdf.

Architecture STRICTEMENT identique à celle du dataset importé par l'utilisateur :
12 matières + 1 colonne cible (filiere_recommandee), sep=';', decimal=','.
"""

import numpy as np
import pandas as pd
import os

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

FEATURE_COLS = [
    'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
    'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
    'statistiques_et_probabilites'
]

FILIERES = {
    'science_des_donnees_et_intelligence_artificielle': {
        'required': ['mathematiques', 'statistiques_et_probabilites', 'test_psychotechnique'],
        'flavor': [],
        'single_rule': None,
    },
    'medecine_et_pharmacie': {
        'required': ['science_de_la_vie_et_de_la_terre', 'chimie'],
        'flavor': [],
        'single_rule': ['science_de_la_vie_et_de_la_terre', 'chimie'],
    },
    'agronomie_et_biotechnologie': {
        'required': ['mathematiques', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre'],
        'flavor': [],
        'single_rule': None,
    },
    'sciences_environnementales_et_science_marine': {
        'required': ['mathematiques', 'science_de_la_vie_et_de_la_terre'],
        'flavor': [],
        'single_rule': None,
    },
    'tourisme_et_hotellerie': {
        'required': ['histoire_et_geographie', 'francais', 'anglais'],
        'flavor': [],
        'single_rule': None,
    },
    'langues_et_communication': {
        'required': ['francais', 'anglais'],
        'flavor': [],
        'single_rule': ['francais', 'anglais'],
    },
    'sociologie': {
        'required': ['philosophie', 'anglais', 'francais'],
        'flavor': [],
        'single_rule': ['philosophie'],
    },
    'sciences_actuarielles': {
        'required': ['francais', 'anglais', 'statistiques_et_probabilites'],
        'flavor': [],
        'single_rule': ['statistiques_et_probabilites'],
    },
    'ingenierie_et_science_generale': {
        'required': ['mathematiques', 'physique', 'chimie', 'test_psychotechnique'],
        'flavor': [],
        'single_rule': ['mathematiques', 'physique'],
    },
    'droit_et_sciences_politiques': {
        'required': ['histoire_et_geographie', 'francais', 'anglais', 'test_psychotechnique'],
        'flavor': [],
        'single_rule': None,
    },
    'psychologie': {
        'required': ['philosophie', 'test_psychotechnique'],
        'flavor': [],
        'single_rule': ['test_psychotechnique'],
    },
    'anthropologie_ou_archeologie': {
        'required': ['science_de_la_vie_et_de_la_terre', 'histoire_et_geographie'],
        'flavor': [],
        'single_rule': None,
    },
}

N_PER_CLASS = 300  # 10 filières x 300 = 3000 lignes
NOISE_STD = 1.6


def clip_round(x):
    return float(np.clip(round(x, 2), 0, 20))


def baseline_note():
    return clip_round(rng.normal(loc=9.5, scale=NOISE_STD))


def make_row(filiere, profile):
    """Construit une ligne de notes selon le profil ('extreme', 'moderate', 'single', 'borderline')."""
    info = FILIERES[filiere]
    required = info['required']
    flavor = info['flavor']

    notes = {col: baseline_note() for col in FEATURE_COLS}

    if profile == 'extreme':
        for col in required:
            notes[col] = clip_round(rng.uniform(15.0, 20.0))

    elif profile == 'moderate':
        for col in required:
            notes[col] = clip_round(rng.uniform(12.0, 16.5))

    elif profile == 'single':
        chosen = rng.choice(info['single_rule'])
        notes[chosen] = clip_round(rng.uniform(15.0, 20.0))

    elif profile == 'borderline':
        for col in FEATURE_COLS:
            notes[col] = clip_round(rng.normal(loc=10.0, scale=0.8))
        for col in required:
            notes[col] = clip_round(notes[col] + rng.uniform(0.5, 2.0))

    for col in flavor:
        if rng.random() < 0.4:
            notes[col] = clip_round(notes[col] + rng.uniform(1.0, 3.0))

    notes['filiere_recommandee'] = filiere
    return notes


rows = []
for filiere, info in FILIERES.items():
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
        rows.append(make_row(filiere, profile))

df = pd.DataFrame(rows)
df = df[FEATURE_COLS + ['filiere_recommandee']]
df = df.sample(frac=1.0, random_state=RNG_SEED).reset_index(drop=True)

os.makedirs('data/raw', exist_ok=True)
out_path = 'data/raw/dataset_note_etudiant_bac.csv'
df.to_csv(out_path, sep=';', decimal=',', index=False)

print(f"✅ Dataset généré : {len(df)} lignes, {len(FEATURE_COLS)} matières, {df['filiere_recommandee'].nunique()} filières.")
print(df['filiere_recommandee'].value_counts())
