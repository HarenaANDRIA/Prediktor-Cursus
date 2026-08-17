"""
Génération du dataset synthétique 'dataset_branch_config.csv'
Corrigé : Génère des notes réalistes pour TOUS les modules (comme generate_dataset.py),
évitant ainsi les valeurs à 0 dans le fichier CSV final.
"""

import numpy as np
import pandas as pd
import os

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

BRANCH_CONFIG = {
    'science_des_donnees_et_intelligence_artificielle': {
        'modules': ['algorithmique_python', 'sql_bases_de_donnees', 'algebre_et_analyse', 'langages_web', 'linux', 'codage', 'cryptographie', 'reseaux informatiques'],
        'branches': {
            'machine_learning_deep_learning': {'required': ['algorithmique_python'], 'single_rule': ['algorithmique_python']},
            'data_engineer': {'required': ['sql_bases_de_donnees'], 'single_rule': ['sql_bases_de_donnees']},
            'data_scientist_data_analyst': {'required': ['algebre_et_analyse'], 'single_rule': ['algebre_et_analyse']},
            'developpeur_frontend_backend_fullstack': {'required': ['langages_web'], 'single_rule': ['langages_web']},
            'cybersecurite': {'required': ['linux', 'codage', 'cryptographie', 'reseaux informatiques'], 'single_rule': ['linux', 'codage', 'cryptographie', 'reseaux informatiques']},
            'product_owner_data': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'medecine_et_pharmacie': {
        'modules': ['anatomie', 'physiologie', 'biochimie', 'histologie', 'anatomie_pathologique'],
        'branches': {
            'chirurgie_orthopedie_neurochirurgie': {'required': ['anatomie'], 'single_rule': ['anatomie']},
            'medecine_interne_cardiologie': {'required': ['physiologie'], 'single_rule': ['physiologie']},
            'pharmacie_hospitaliere': {'required': ['biochimie'], 'single_rule': ['biochimie']},
            'cancerologie_radiologie': {'required': ['histologie', 'anatomie_pathologique'], 'single_rule': ['histologie', 'anatomie_pathologique']},
            'medecine_generale_et_sante_publique': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'agronomie_et_biotechnologie': {
        'modules': ['genetique_biologie_moleculaire', 'physiologie_ecologie', 'biochimie', 'statistiques_agricoles_et_modelisation'],
        'branches': {
            'biotechnologie_vegetale_amelioration_des_especes': {'required': ['genetique_biologie_moleculaire'], 'single_rule': ['genetique_biologie_moleculaire']},
            'agronomie_durable': {'required': ['physiologie_ecologie'], 'single_rule': ['physiologie_ecologie']},
            'agroalimentaire_qualite_sanitaire_et_fermentations': {'required': ['biochimie'], 'single_rule': ['biochimie']},
            'agrometeorologie': {'required': ['statistiques_agricoles_et_modelisation'], 'single_rule': ['statistiques_agricoles_et_modelisation']},
            'gestion_d_exploitation_et_zootechnie': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'sciences_environnementales_et_science_marine': {
        'modules': ['oceanographie_et_climatologie', 'ecologie_marine', 'geologie_sedimentaire_et_hydrologie'],
        'branches': {
            'meteo_marine_et_peche': {'required': ['oceanographie_et_climatologie'], 'single_rule': ['oceanographie_et_climatologie']},
            'biodiversite': {'required': ['ecologie_marine'], 'single_rule': ['ecologie_marine']},
            'geosciences_marine': {'required': ['geologie_sedimentaire_et_hydrologie'], 'single_rule': ['geologie_sedimentaire_et_hydrologie']},
            'gestion_d_exploitation_et_zootechnie': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'tourisme_et_hotellerie': {
        'modules': ['management_interculturel', 'comptabilite', 'geographie', 'droit', 'anglais', 'francais', 'allemand', 'espagnol'],
        'branches': {
            'marketing_hotelier_international_branding': {'required': ['management_interculturel'], 'single_rule': ['management_interculturel']},
            'direction_d_hotel_chaines_hotelieres': {'required': ['comptabilite'], 'single_rule': ['comptabilite']},
            'tourisme_durable_ecotourisme_patrimoine_unesco': {'required': ['geographie', 'droit'], 'single_rule': ['geographie', 'droit']},
            'relations_internationales_tourisme_d_affaires': {'required': ['anglais', 'francais', 'allemand', 'espagnol'], 'single_rule': ['anglais', 'francais', 'allemand', 'espagnol']},
            'agence_de_voyage_et_animation_touristique': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'langues_et_communication': {
        'modules': ['langues_etrangeres', 'semiologie', 'journalisme_et_redaction_web', 'audiovisuel_et_multimedia'],
        'branches': {
            'interpretation_traduction_technique_et_juridique': {'required': ['langues_etrangeres'], 'single_rule': ['langues_etrangeres']},
            'communication_strategique_publicite': {'required': ['semiologie'], 'single_rule': ['semiologie']},
            'content_marketing_journalisme_d_enquete_redacteur_seo': {'required': ['journalisme_et_redaction_web'], 'single_rule': ['journalisme_et_redaction_web']},
            'production_audiovisuelle_community_management': {'required': ['audiovisuel_et_multimedia'], 'single_rule': ['audiovisuel_et_multimedia']},
            'assistant_de_communication': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'sociologie': {
        'modules': ['theories_sociologiques_et_philosophie_sociale', 'statistiques_methodologie_quantitative', 'demographie_sociologie_famille'],
        'branches': {
            'sociologie_theorique_et_enseignant_chercheur': {'required': ['theories_sociologiques_et_philosophie_sociale'], 'single_rule': ['theories_sociologiques_et_philosophie_sociale']},
            'data_sociologue': {'required': ['statistiques_methodologie_quantitative'], 'single_rule': ['statistiques_methodologie_quantitative']},
            'politiques_publiques_et_gerontologie': {'required': ['demographie_sociologie_famille'], 'single_rule': ['demographie_sociologie_famille']},
            'rh_et_mediation_sociale': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'droit_et_sciences_politiques': {
        'modules': ['droit_civil_et_procedure_civile', 'droit_penal_procedure_penale', 'droit_administratif_constitutionnel', 'droit_commercial'],
        'branches': {
            'avocat_droit_des_affaires_droit_immobilier': {'required': ['droit_civil_et_procedure_civile'], 'single_rule': ['droit_civil_et_procedure_civile']},
            'magistrature': {'required': ['droit_penal_procedure_penale'], 'single_rule': ['droit_penal_procedure_penale']},
            'conseil_d_etat_fonction_publique_droit_public_affaires': {'required': ['droit_administratif_constitutionnel'], 'single_rule': ['droit_administratif_constitutionnel']},
            'juriste_d_entreprise': {'required': ['droit_commercial'], 'single_rule': ['droit_commercial']},
            'rh_fonction_publique_territoriale': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'sciences_actuarielles': {
        'modules': ['probabilites_statistiques_appliquees', 'mathematiques_financieres_finance_marche', 'droit_assurances_reglementation'],
        'branches': {
            'prevoyance_actuaire_vie': {'required': ['probabilites_statistiques_appliquees'], 'single_rule': ['probabilites_statistiques_appliquees']},
            'banque_risk_manager_financier': {'required': ['mathematiques_financieres_finance_marche'], 'single_rule': ['mathematiques_financieres_finance_marche']},
            'actuaire_conseil_juridique_reassurance': {'required': ['droit_assurances_reglementation'], 'single_rule': ['droit_assurances_reglementation']},
            'gestionnaire_de_sinistres': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'ingenierie_et_science_generale': {
        'modules': ['resistance_des_materiaux', 'mecanique_des_fluides', 'thermodynamique_energetique', 'electronique', 'automatique', 'electricite', 'mathematiques_discretes_et_algorithmique'],
        'branches': {
            'genie_civil_architecture_hydraulique': {'required': ['resistance_des_materiaux', 'mecanique_des_fluides'], 'single_rule': ['resistance_des_materiaux', 'mecanique_des_fluides']},
            'energie_nucleaire_propulsion': {'required': ['thermodynamique_energetique'], 'single_rule': ['thermodynamique_energetique']},
            'genie_electrique_robotique_et_mecatronique': {'required': ['electronique', 'automatique', 'electricite'], 'single_rule': ['electronique', 'automatique', 'electricite']},
            'telecommunication_et_genie_logiciel': {'required': ['mathematiques_discretes_et_algorithmique'], 'single_rule': ['mathematiques_discretes_et_algorithmique']},
            'bureau_d_etudes_et_maintenance': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'psychologie': {
        'modules': ['psychopathologie_clinique', 'neurosciences_sociales'],
        'branches': {
            'psychotherapeute': {'required': ['psychopathologie_clinique'], 'single_rule': ['psychopathologie_clinique']},
            'psychologie_du_travail_rh': {'required': ['neurosciences_sociales'], 'single_rule': ['neurosciences_sociales']},
            'psychologue_scolaire_conseiller_orientation': {'required': [], 'single_rule': None, 'is_default': True}
        }
    },
    'anthropologie_ou_archeologie': {
        'modules': ['paleoanthropologie_et_osteologie', 'prehistoire_geoarcheologie', 'ethnologie', 'anthropologie_culturelle'],
        'branches': {
            'anthropologie_biologique': {'required': ['paleoanthropologie_et_osteologie'], 'single_rule': ['paleoanthropologie_et_osteologie']},
            'archeologie_paleoenvironnement': {'required': ['prehistoire_geoarcheologie'], 'single_rule': ['prehistoire_geoarcheologie']},
            'patrimoine_et_ethnologie_de_terrain': {'required': ['ethnologie', 'anthropologie_culturelle'], 'single_rule': ['ethnologie', 'anthropologie_culturelle']},
            'technicien_fouilles_archeologiques_museographie_et_mediation': {'required': [], 'single_rule': None, 'is_default': True}
        }
    }
}

# 1. Extrait la liste globale unique de TOUS les modules
ALL_MODULES = sorted(list({mod for cfg in BRANCH_CONFIG.values() for mod in cfg['modules']}))

N_PER_BRANCH = 300
NOISE_STD = 1.6


def clip_round(x):
    return float(np.clip(round(x, 2), 0, 20))


def baseline_note():
    return clip_round(rng.normal(loc=9.5, scale=NOISE_STD))


def make_row(filiere_name, branch_name, branch_info, filiere_modules):
    """Initialise toutes les notes de tous les modules puis applique les règles de la branche."""
    # Note de base générée pour TOUS les modules du dataset (alignement avec generate_dataset.py)
    notes = {m: baseline_note() for m in ALL_MODULES}

    is_default = branch_info.get('is_default', False)
    required = branch_info.get('required', [])
    single_rule = branch_info.get('single_rule', None)

    if is_default:
        for m in filiere_modules:
            notes[m] = clip_round(rng.normal(loc=11.0, scale=0.8))
    else:
        if single_rule is not None and rng.random() < 0.2:
            profile = 'single'
        else:
            profile = rng.choice(['extreme', 'moderate', 'borderline'], p=[0.60, 0.35, 0.05])

        if profile == 'extreme':
            for col in required:
                notes[col] = clip_round(rng.uniform(15.0, 20.0))
        elif profile == 'moderate':
            for col in required:
                notes[col] = clip_round(rng.uniform(12.5, 16.5))
        elif profile == 'single':
            chosen = rng.choice(single_rule)
            notes[chosen] = clip_round(rng.uniform(15.0, 20.0))
        elif profile == 'borderline':
            for col in filiere_modules:
                notes[col] = clip_round(rng.normal(loc=10.5, scale=0.8))
            for col in required:
                notes[col] = clip_round(notes[col] + rng.uniform(0.5, 2.0))

    notes['filiere'] = filiere_name
    notes['branche_recommandee'] = branch_name
    return notes


def generate_branch_dataset():
    all_rows = []

    for filiere_name, filiere_info in BRANCH_CONFIG.items():
        filiere_modules = filiere_info['modules']
        branches = filiere_info['branches']

        for branch_name, branch_info in branches.items():
            for _ in range(N_PER_BRANCH):
                row = make_row(filiere_name, branch_name, branch_info, filiere_modules)
                all_rows.append(row)

    df = pd.DataFrame(all_rows)
    # Réorganisation des colonnes : d'abord tous les modules, puis filiere et branche_recommandee
    columns_order = ALL_MODULES + ['filiere', 'branche_recommandee']
    df = df[columns_order]
    
    df = df.sample(frac=1.0, random_state=RNG_SEED).reset_index(drop=True)

    os.makedirs('data/raw', exist_ok=True)
    out_path = 'data/raw/dataset_branch_config.csv'
    df.to_csv(out_path, sep=';', decimal=',', index=False)

    print(f"✅ Dataset des branches généré : {len(df)} lignes, {len(ALL_MODULES)} modules, {df['branche_recommandee'].nunique()} branches uniques.")
    return df


if __name__ == '__main__':
    generate_branch_dataset()