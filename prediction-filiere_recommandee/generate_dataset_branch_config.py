"""
Génération du dataset synthétique 'dataset_branch_config.csv'
BRANCH_CONFIG dérivé du guide PDF 'Filières, Modules et Spécialisations Recommandées'.
Chaque module de filière correspond à une spécialisation recommandée si l'étudiant y excelle.
"""

import numpy as np
import pandas as pd
import os

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

BRANCH_CONFIG = {
    'science_des_donnees_et_intelligence_artificielle': {
        'label': "Science des Données et Intelligence Artificielle",
        'modules': ['mathematiques_algebre_lineaire_calcul_di', 'probabilites_et_statistiques', 'programmation_python_r_c', 'structures_de_donnees_et_algorithmes', 'bases_de_donnees_et_gestion_de_l_informa', 'apprentissage_automatique_machine_learni', 'apprentissage_profond_deep_learning', 'traitement_du_langage_naturel_nlp', 'vision_par_ordinateur', 'big_data_et_cloud_computing', 'visualisation_de_donnees_et_business_int', 'ethique_et_gouvernance_de_l_ia', 'systemes_distribues_et_infrastructure_it'],
        'branches': {
            'recherche_en_ia_specialiste_en_modelisation_mathem': {'label': "Recherche en IA, spécialiste en modélisation mathématique avancée", 'required': ['mathematiques_algebre_lineaire_calcul_di'], 'single_rule': ['mathematiques_algebre_lineaire_calcul_di']},
            'data_scientist_statisticien_analyste_quantitatif': {'label': "Data Scientist, Statisticien, Analyste quantitatif", 'required': ['probabilites_et_statistiques'], 'single_rule': ['probabilites_et_statistiques']},
            'ingenieur_machine_learning_developpeur_ia': {'label': "Ingénieur Machine Learning, développeur IA", 'required': ['programmation_python_r_c'], 'single_rule': ['programmation_python_r_c']},
            'ingenieur_logiciel_specialise_en_ia_algorithmicien': {'label': "Ingénieur logiciel spécialisé en IA, algorithmicien", 'required': ['structures_de_donnees_et_algorithmes'], 'single_rule': ['structures_de_donnees_et_algorithmes']},
            'data_engineer_architecte_de_donnees': {'label': "Data Engineer, architecte de données", 'required': ['bases_de_donnees_et_gestion_de_l_informa'], 'single_rule': ['bases_de_donnees_et_gestion_de_l_informa']},
            'ingenieur_ml_chercheur_en_apprentissage_automatiqu': {'label': "Ingénieur ML, chercheur en apprentissage automatique", 'required': ['apprentissage_automatique_machine_learni'], 'single_rule': ['apprentissage_automatique_machine_learni']},
            'chercheur_en_ia_specialiste_reseaux_de_neurones': {'label': "Chercheur en IA, spécialiste réseaux de neurones", 'required': ['apprentissage_profond_deep_learning'], 'single_rule': ['apprentissage_profond_deep_learning']},
            'ingenieur_nlp_concepteur_de_modeles_de_langage_llm': {'label': "Ingénieur NLP, concepteur de modèles de langage (LLM)", 'required': ['traitement_du_langage_naturel_nlp'], 'single_rule': ['traitement_du_langage_naturel_nlp']},
            'ingenieur_computer_vision_robotique_intelligente': {'label': "Ingénieur Computer Vision, robotique intelligente", 'required': ['vision_par_ordinateur'], 'single_rule': ['vision_par_ordinateur']},
            'data_engineer_architecte_big_data_cloud': {'label': "Data Engineer, architecte Big Data / Cloud", 'required': ['big_data_et_cloud_computing'], 'single_rule': ['big_data_et_cloud_computing']},
            'analyste_business_intelligence_data_analyst': {'label': "Analyste Business Intelligence, Data Analyst", 'required': ['visualisation_de_donnees_et_business_int'], 'single_rule': ['visualisation_de_donnees_et_business_int']},
            'consultant_en_ethique_de_l_ia_gouvernance_des_donn': {'label': "Consultant en éthique de l\'IA, gouvernance des données", 'required': ['ethique_et_gouvernance_de_l_ia'], 'single_rule': ['ethique_et_gouvernance_de_l_ia']},
            'ingenieur_devops_mlops': {'label': "Ingénieur DevOps / MLOps", 'required': ['systemes_distribues_et_infrastructure_it'], 'single_rule': ['systemes_distribues_et_infrastructure_it']},
        }
    },
    'tourisme_et_hotellerie': {
        'label': "Tourisme et Hôtellerie",
        'modules': ['gestion_hoteliere_et_gestion_de_la_resta', 'marketing_touristique_et_revenue_managem', 'gestion_des_evenements_mice', 'langues_etrangeres_appliquees', 'communication_et_relation_client', 'geographie_et_culture_touristique', 'droit_du_tourisme_et_de_l_hotellerie', 'comptabilite_et_finance_hoteliere', 'gestion_des_ressources_humaines_en_hotel', 'developpement_durable_et_ecotourisme', 'technologies_de_l_information_touristiqu'],
        'branches': {
            'directeur_d_hotel_manager_de_restauration': {'label': "Directeur d\'hôtel, manager de restauration", 'required': ['gestion_hoteliere_et_gestion_de_la_resta'], 'single_rule': ['gestion_hoteliere_et_gestion_de_la_resta']},
            'responsable_marketing_touristique_revenue_manager': {'label': "Responsable marketing touristique, Revenue Manager", 'required': ['marketing_touristique_et_revenue_managem'], 'single_rule': ['marketing_touristique_et_revenue_managem']},
            'event_manager_organisateur_de_congres_et_seminaire': {'label': "Event Manager, organisateur de congrès et séminaires", 'required': ['gestion_des_evenements_mice'], 'single_rule': ['gestion_des_evenements_mice']},
            'guide_touristique_international_agent_de_voyage': {'label': "Guide touristique international, agent de voyage", 'required': ['langues_etrangeres_appliquees'], 'single_rule': ['langues_etrangeres_appliquees']},
            'responsable_relation_clientele_charge_d_accueil_vi': {'label': "Responsable relation clientèle, chargé d\'accueil VIP", 'required': ['communication_et_relation_client'], 'single_rule': ['communication_et_relation_client']},
            'concepteur_de_circuits_touristiques_tour_operateur': {'label': "Concepteur de circuits touristiques, tour-opérateur", 'required': ['geographie_et_culture_touristique'], 'single_rule': ['geographie_et_culture_touristique']},
            'juriste_specialise_tourisme_responsable_conformite': {'label': "Juriste spécialisé tourisme, responsable conformité", 'required': ['droit_du_tourisme_et_de_l_hotellerie'], 'single_rule': ['droit_du_tourisme_et_de_l_hotellerie']},
            'controleur_de_gestion_hoteliere_directeur_financie': {'label': "Contrôleur de gestion hôtelière, directeur financier d\'établissement", 'required': ['comptabilite_et_finance_hoteliere'], 'single_rule': ['comptabilite_et_finance_hoteliere']},
            'responsable_rh_hotelier_formateur': {'label': "Responsable RH hôtelier, formateur", 'required': ['gestion_des_ressources_humaines_en_hotel'], 'single_rule': ['gestion_des_ressources_humaines_en_hotel']},
            'consultant_en_tourisme_durable_responsable_ecotour': {'label': "Consultant en tourisme durable, responsable écotourisme", 'required': ['developpement_durable_et_ecotourisme'], 'single_rule': ['developpement_durable_et_ecotourisme']},
            'responsable_e_tourisme_gestion_des_plateformes_de_': {'label': "Responsable e-tourisme, gestion des plateformes de réservation", 'required': ['technologies_de_l_information_touristiqu'], 'single_rule': ['technologies_de_l_information_touristiqu']},
        }
    },
    'science_actuarielle': {
        'label': "Science Actuarielle",
        'modules': ['mathematiques_financieres', 'probabilites_et_statistiques', 'theorie_du_risque_et_modeles_de_survie', 'econometrie', 'droit_des_assurances_et_reglementation', 'comptabilite_actuarielle_et_finance_d_en', 'programmation_actuarielle_r_python_sas_v', 'gestion_des_risques_erm', 'actuariat_vie', 'actuariat_non_vie_iard'],
        'branches': {
            'actuaire_en_investissement_gestion_d_actifs': {'label': "Actuaire en investissement, gestion d\'actifs", 'required': ['mathematiques_financieres'], 'single_rule': ['mathematiques_financieres']},
            'actuaire_tarification_modelisation_du_risque': {'label': "Actuaire tarification, modélisation du risque", 'required': ['probabilites_et_statistiques'], 'single_rule': ['probabilites_et_statistiques']},
            'actuaire_vie_actuaire_prevoyance': {'label': "Actuaire vie, actuaire prévoyance", 'required': ['theorie_du_risque_et_modeles_de_survie'], 'single_rule': ['theorie_du_risque_et_modeles_de_survie']},
            'analyste_quantitatif_chercheur_en_finance': {'label': "Analyste quantitatif, chercheur en finance", 'required': ['econometrie'], 'single_rule': ['econometrie']},
            'actuaire_reglementaire_responsable_conformite_solv': {'label': "Actuaire réglementaire, responsable conformité (Solvabilité)", 'required': ['droit_des_assurances_et_reglementation'], 'single_rule': ['droit_des_assurances_et_reglementation']},
            'actuaire_en_gestion_financiere_controleur_de_gesti': {'label': "Actuaire en gestion financière, contrôleur de gestion assurance", 'required': ['comptabilite_actuarielle_et_finance_d_en'], 'single_rule': ['comptabilite_actuarielle_et_finance_d_en']},
            'data_scientist_actuariel_modelisateur_quantitatif': {'label': "Data Scientist actuariel, modélisateur quantitatif", 'required': ['programmation_actuarielle_r_python_sas_v'], 'single_rule': ['programmation_actuarielle_r_python_sas_v']},
            'risk_manager_actuaire_en_gestion_globale_des_risqu': {'label': "Risk Manager, actuaire en gestion globale des risques", 'required': ['gestion_des_risques_erm'], 'single_rule': ['gestion_des_risques_erm']},
            'actuaire_specialise_assurance_vie_et_retraite': {'label': "Actuaire spécialisé assurance-vie et retraite", 'required': ['actuariat_vie'], 'single_rule': ['actuariat_vie']},
            'actuaire_specialise_assurance_dommages_iard': {'label': "Actuaire spécialisé assurance dommages / IARD", 'required': ['actuariat_non_vie_iard'], 'single_rule': ['actuariat_non_vie_iard']},
        }
    },
    'droit_et_science_politique': {
        'label': "Droit et Science Politique",
        'modules': ['droit_civil', 'droit_penal', 'droit_constitutionnel', 'droit_administratif', 'droit_international_public_et_prive', 'droit_des_affaires_et_droit_commercial', 'institutions_politiques_comparees', 'relations_internationales', 'sociologie_politique', 'economie_politique', 'histoire_du_droit_et_methodologie_juridi'],
        'branches': {
            'avocat_en_droit_civil_notaire': {'label': "Avocat en droit civil, notaire", 'required': ['droit_civil'], 'single_rule': ['droit_civil']},
            'avocat_penaliste_magistrat': {'label': "Avocat pénaliste, magistrat", 'required': ['droit_penal'], 'single_rule': ['droit_penal']},
            'constitutionnaliste_conseiller_juridique_instituti': {'label': "Constitutionnaliste, conseiller juridique institutionnel", 'required': ['droit_constitutionnel'], 'single_rule': ['droit_constitutionnel']},
            'juriste_dans_la_fonction_publique_contentieux_admi': {'label': "Juriste dans la fonction publique, contentieux administratif", 'required': ['droit_administratif'], 'single_rule': ['droit_administratif']},
            'diplomate_juriste_des_organisations_internationale': {'label': "Diplomate, juriste des organisations internationales", 'required': ['droit_international_public_et_prive'], 'single_rule': ['droit_international_public_et_prive']},
            'juriste_d_entreprise_avocat_d_affaires': {'label': "Juriste d\'entreprise, avocat d\'affaires", 'required': ['droit_des_affaires_et_droit_commercial'], 'single_rule': ['droit_des_affaires_et_droit_commercial']},
            'analyste_politique_conseiller_institutionnel': {'label': "Analyste politique, conseiller institutionnel", 'required': ['institutions_politiques_comparees'], 'single_rule': ['institutions_politiques_comparees']},
            'diplomatie_expert_en_geopolitique_ong_internationa': {'label': "Diplomatie, expert en géopolitique, ONG internationales", 'required': ['relations_internationales'], 'single_rule': ['relations_internationales']},
            'politologue_chercheur_en_science_politique': {'label': "Politologue, chercheur en science politique", 'required': ['sociologie_politique'], 'single_rule': ['sociologie_politique']},
            'conseiller_en_politiques_publiques_economiste_poli': {'label': "Conseiller en politiques publiques, économiste politique", 'required': ['economie_politique'], 'single_rule': ['economie_politique']},
            'recherche_academique_enseignement_du_droit': {'label': "Recherche académique, enseignement du droit", 'required': ['histoire_du_droit_et_methodologie_juridi'], 'single_rule': ['histoire_du_droit_et_methodologie_juridi']},
        }
    },
    'science_environnementale': {
        'label': "Science Environnementale",
        'modules': ['ecologie_generale', 'biologie_et_sciences_de_la_vie', 'chimie_de_l_environnement', 'geologie_et_sciences_de_la_terre', 'climatologie_et_sciences_du_climat', 'gestion_des_ressources_naturelles', 'droit_de_l_environnement', 'systemes_d_information_geographique_sig', 'economie_de_l_environnement', 'toxicologie_et_pollution'],
        'branches': {
            'ecologue_specialiste_de_la_conservation_de_la_biod': {'label': "Écologue, spécialiste de la conservation de la biodiversité", 'required': ['ecologie_generale'], 'single_rule': ['ecologie_generale']},
            'biologiste_environnemental_chercheur_en_ecologie': {'label': "Biologiste environnemental, chercheur en écologie", 'required': ['biologie_et_sciences_de_la_vie'], 'single_rule': ['biologie_et_sciences_de_la_vie']},
            'analyste_environnemental_expert_en_gestion_des_dec': {'label': "Analyste environnemental, expert en gestion des déchets et pollution", 'required': ['chimie_de_l_environnement'], 'single_rule': ['chimie_de_l_environnement']},
            'geologue_environnemental_expert_en_risques_naturel': {'label': "Géologue environnemental, expert en risques naturels", 'required': ['geologie_et_sciences_de_la_terre'], 'single_rule': ['geologie_et_sciences_de_la_terre']},
            'climatologue_expert_en_changement_climatique': {'label': "Climatologue, expert en changement climatique", 'required': ['climatologie_et_sciences_du_climat'], 'single_rule': ['climatologie_et_sciences_du_climat']},
            'gestionnaire_de_ressources_naturelles_forestier': {'label': "Gestionnaire de ressources naturelles, forestier", 'required': ['gestion_des_ressources_naturelles'], 'single_rule': ['gestion_des_ressources_naturelles']},
            'consultant_en_conformite_environnementale_juriste_': {'label': "Consultant en conformité environnementale, juriste de l\'environnement", 'required': ['droit_de_l_environnement'], 'single_rule': ['droit_de_l_environnement']},
            'cartographe_environnemental_analyste_sig_amenageme': {'label': "Cartographe environnemental, analyste SIG, aménagement du territoire", 'required': ['systemes_d_information_geographique_sig'], 'single_rule': ['systemes_d_information_geographique_sig']},
            'economiste_environnemental_consultant_en_developpe': {'label': "Économiste environnemental, consultant en développement durable", 'required': ['economie_de_l_environnement'], 'single_rule': ['economie_de_l_environnement']},
            'expert_en_evaluation_des_risques_sanitaires_et_env': {'label': "Expert en évaluation des risques sanitaires et environnementaux", 'required': ['toxicologie_et_pollution'], 'single_rule': ['toxicologie_et_pollution']},
        }
    },
    'science_marine': {
        'label': "Science Marine",
        'modules': ['oceanographie_physique_et_chimique', 'biologie_marine', 'ecologie_marine_et_conservation', 'chimie_marine', 'geologie_marine', 'gestion_des_peches_et_ressources_halieut', 'aquaculture', 'droit_maritime_et_gestion_des_zones_coti', 'cartographie_et_technologies_marines_sig'],
        'branches': {
            'oceanographe_chercheur_en_dynamique_oceanique': {'label': "Océanographe, chercheur en dynamique océanique", 'required': ['oceanographie_physique_et_chimique'], 'single_rule': ['oceanographie_physique_et_chimique']},
            'biologiste_marin_specialiste_de_la_faune_et_flore_': {'label': "Biologiste marin, spécialiste de la faune et flore marines", 'required': ['biologie_marine'], 'single_rule': ['biologie_marine']},
            'expert_en_conservation_marine_gestionnaire_d_aires': {'label': "Expert en conservation marine, gestionnaire d\'aires marines protégées", 'required': ['ecologie_marine_et_conservation'], 'single_rule': ['ecologie_marine_et_conservation']},
            'chercheur_en_chimie_des_oceans_analyste_environnem': {'label': "Chercheur en chimie des océans, analyste environnemental marin", 'required': ['chimie_marine'], 'single_rule': ['chimie_marine']},
            'geologue_marin_exploration_des_fonds_marins': {'label': "Géologue marin, exploration des fonds marins", 'required': ['geologie_marine'], 'single_rule': ['geologie_marine']},
            'gestionnaire_des_peches_expert_en_ressources_halie': {'label': "Gestionnaire des pêches, expert en ressources halieutiques", 'required': ['gestion_des_peches_et_ressources_halieut'], 'single_rule': ['gestion_des_peches_et_ressources_halieut']},
            'aquaculteur_ingenieur_en_production_aquacole': {'label': "Aquaculteur, ingénieur en production aquacole", 'required': ['aquaculture'], 'single_rule': ['aquaculture']},
            'juriste_maritime_gestionnaire_du_littoral': {'label': "Juriste maritime, gestionnaire du littoral", 'required': ['droit_maritime_et_gestion_des_zones_coti'], 'single_rule': ['droit_maritime_et_gestion_des_zones_coti']},
            'hydrographe_cartographe_marin': {'label': "Hydrographe, cartographe marin", 'required': ['cartographie_et_technologies_marines_sig'], 'single_rule': ['cartographie_et_technologies_marines_sig']},
        }
    },
    'anthropologie': {
        'label': "Anthropologie",
        'modules': ['anthropologie_sociale_et_culturelle', 'anthropologie_physique_biologique', 'ethnographie_et_methodes_de_terrain', 'linguistique_anthropologique', 'anthropologie_de_la_parente_et_des_struc', 'anthropologie_religieuse', 'anthropologie_economique_et_du_developpe', 'histoire_de_l_anthropologie_et_theories'],
        'branches': {
            'chercheur_en_anthropologie_sociale_consultant_cult': {'label': "Chercheur en anthropologie sociale, consultant culturel", 'required': ['anthropologie_sociale_et_culturelle'], 'single_rule': ['anthropologie_sociale_et_culturelle']},
            'paleoanthropologue_anthropologue_legiste': {'label': "Paléoanthropologue, anthropologue légiste", 'required': ['anthropologie_physique_biologique'], 'single_rule': ['anthropologie_physique_biologique']},
            'ethnographe_chercheur_de_terrain': {'label': "Ethnographe, chercheur de terrain", 'required': ['ethnographie_et_methodes_de_terrain'], 'single_rule': ['ethnographie_et_methodes_de_terrain']},
            'anthropologue_linguiste_documentation_des_langues_': {'label': "Anthropologue linguiste, documentation des langues menacées", 'required': ['linguistique_anthropologique'], 'single_rule': ['linguistique_anthropologique']},
            'chercheur_en_etudes_sociales_expert_en_mediation_c': {'label': "Chercheur en études sociales, expert en médiation culturelle", 'required': ['anthropologie_de_la_parente_et_des_struc'], 'single_rule': ['anthropologie_de_la_parente_et_des_struc']},
            'chercheur_en_anthropologie_des_religions': {'label': "Chercheur en anthropologie des religions", 'required': ['anthropologie_religieuse'], 'single_rule': ['anthropologie_religieuse']},
            'expert_en_developpement_international_consultant_o': {'label': "Expert en développement international, consultant ONG", 'required': ['anthropologie_economique_et_du_developpe'], 'single_rule': ['anthropologie_economique_et_du_developpe']},
            'enseignant_chercheur_museologie': {'label': "Enseignant-chercheur, muséologie", 'required': ['histoire_de_l_anthropologie_et_theories'], 'single_rule': ['histoire_de_l_anthropologie_et_theories']},
        }
    },
    'archeologie': {
        'label': "Archéologie",
        'modules': ['prehistoire_et_protohistoire', 'archeologie_classique_et_antique', 'methodes_de_fouille_et_prospection', 'ceramologie_et_etude_du_mobilier', 'epigraphie_et_paleographie', 'anthropologie_physique_appliquee_a_l_arc', 'conservation_restauration_du_patrimoine', 'archeometrie_et_datation_c14_dendrochron', 'histoire_de_l_art_ancien'],
        'branches': {
            'archeologue_prehistorien_chercheur_en_evolution_hu': {'label': "Archéologue préhistorien, chercheur en évolution humaine", 'required': ['prehistoire_et_protohistoire'], 'single_rule': ['prehistoire_et_protohistoire']},
            'archeologue_specialise_civilisations_antiques': {'label': "Archéologue spécialisé civilisations antiques", 'required': ['archeologie_classique_et_antique'], 'single_rule': ['archeologie_classique_et_antique']},
            'archeologue_de_terrain_chef_de_chantier_archeologi': {'label': "Archéologue de terrain, chef de chantier archéologique", 'required': ['methodes_de_fouille_et_prospection'], 'single_rule': ['methodes_de_fouille_et_prospection']},
            'specialiste_du_mobilier_archeologique_ceramologue': {'label': "Spécialiste du mobilier archéologique, céramologue", 'required': ['ceramologie_et_etude_du_mobilier'], 'single_rule': ['ceramologie_et_etude_du_mobilier']},
            'epigraphiste_chercheur_en_textes_anciens': {'label': "Épigraphiste, chercheur en textes anciens", 'required': ['epigraphie_et_paleographie'], 'single_rule': ['epigraphie_et_paleographie']},
            'bioarcheologue_archeo_anthropologue': {'label': "Bioarchéologue, archéo-anthropologue", 'required': ['anthropologie_physique_appliquee_a_l_arc'], 'single_rule': ['anthropologie_physique_appliquee_a_l_arc']},
            'conservateur_restaurateur_expert_en_patrimoine': {'label': "Conservateur-restaurateur, expert en patrimoine", 'required': ['conservation_restauration_du_patrimoine'], 'single_rule': ['conservation_restauration_du_patrimoine']},
            'archeologue_scientifique_specialiste_de_laboratoir': {'label': "Archéologue scientifique, spécialiste de laboratoire", 'required': ['archeometrie_et_datation_c14_dendrochron'], 'single_rule': ['archeometrie_et_datation_c14_dendrochron']},
            'historien_de_l_art_conservateur_de_musee': {'label': "Historien de l\'art, conservateur de musée", 'required': ['histoire_de_l_art_ancien'], 'single_rule': ['histoire_de_l_art_ancien']},
        }
    },
    'agronomie_et_biotechnologie': {
        'label': "Agronomie et Biotechnologie",
        'modules': ['biologie_vegetale_et_physiologie_des_pla', 'genetique_et_genie_genetique', 'microbiologie', 'sciences_du_sol_pedologie', 'phytopathologie', 'zootechnie_et_production_animale', 'biotechnologie_vegetale_et_animale', 'agroeconomie_et_gestion_d_exploitation', 'agroalimentaire_et_transformation', 'machinisme_et_technologies_agricoles'],
        'branches': {
            'agronome_phytotechnicien': {'label': "Agronome, phytotechnicien", 'required': ['biologie_vegetale_et_physiologie_des_pla'], 'single_rule': ['biologie_vegetale_et_physiologie_des_pla']},
            'ingenieur_en_biotechnologie_selectionneur_vegetal': {'label': "Ingénieur en biotechnologie, sélectionneur végétal", 'required': ['genetique_et_genie_genetique'], 'single_rule': ['genetique_et_genie_genetique']},
            'chercheur_en_microbiologie_agricole_biotechnologue': {'label': "Chercheur en microbiologie agricole, biotechnologue", 'required': ['microbiologie'], 'single_rule': ['microbiologie']},
            'pedologue_expert_en_fertilite_des_sols': {'label': "Pédologue, expert en fertilité des sols", 'required': ['sciences_du_sol_pedologie'], 'single_rule': ['sciences_du_sol_pedologie']},
            'expert_en_protection_des_cultures_phytopathologist': {'label': "Expert en protection des cultures, phytopathologiste", 'required': ['phytopathologie'], 'single_rule': ['phytopathologie']},
            'zootechnicien_ingenieur_en_elevage': {'label': "Zootechnicien, ingénieur en élevage", 'required': ['zootechnie_et_production_animale'], 'single_rule': ['zootechnie_et_production_animale']},
            'ingenieur_biotechnologue_chercheur_en_r_d_agricole': {'label': "Ingénieur biotechnologue, chercheur en R&D agricole", 'required': ['biotechnologie_vegetale_et_animale'], 'single_rule': ['biotechnologie_vegetale_et_animale']},
            'gestionnaire_d_exploitation_agricole_conseiller_ag': {'label': "Gestionnaire d\'exploitation agricole, conseiller agricole", 'required': ['agroeconomie_et_gestion_d_exploitation'], 'single_rule': ['agroeconomie_et_gestion_d_exploitation']},
            'ingenieur_agroalimentaire_responsable_qualite': {'label': "Ingénieur agroalimentaire, responsable qualité", 'required': ['agroalimentaire_et_transformation'], 'single_rule': ['agroalimentaire_et_transformation']},
            'ingenieur_en_mecanisation_agricole': {'label': "Ingénieur en mécanisation agricole", 'required': ['machinisme_et_technologies_agricoles'], 'single_rule': ['machinisme_et_technologies_agricoles']},
        }
    },
    'ingenierie_et_science_generale': {
        'label': "Ingénierie et Science Générale",
        'modules': ['mathematiques_appliquees', 'physique_generale_et_appliquee', 'mecanique_et_resistance_des_materiaux', 'electricite_et_electronique', 'thermodynamique_et_energetique', 'informatique_et_programmation', 'genie_civil_et_structures', 'genie_electrique_et_telecommunications', 'chimie_industrielle', 'gestion_de_projet_et_methodologie_indust'],
        'branches': {
            'ingenieur_en_modelisation_recherche_operationnelle': {'label': "Ingénieur en modélisation, recherche opérationnelle", 'required': ['mathematiques_appliquees'], 'single_rule': ['mathematiques_appliquees']},
            'ingenieur_r_d_physicien_applique': {'label': "Ingénieur R&D, physicien appliqué", 'required': ['physique_generale_et_appliquee'], 'single_rule': ['physique_generale_et_appliquee']},
            'ingenieur_mecanicien_ingenieur_en_structures': {'label': "Ingénieur mécanicien, ingénieur en structures", 'required': ['mecanique_et_resistance_des_materiaux'], 'single_rule': ['mecanique_et_resistance_des_materiaux']},
            'ingenieur_electricien_ingenieur_en_electronique': {'label': "Ingénieur électricien, ingénieur en électronique", 'required': ['electricite_et_electronique'], 'single_rule': ['electricite_et_electronique']},
            'ingenieur_energeticien_ingenieur_en_systemes_therm': {'label': "Ingénieur énergéticien, ingénieur en systèmes thermiques", 'required': ['thermodynamique_et_energetique'], 'single_rule': ['thermodynamique_et_energetique']},
            'ingenieur_logiciel_ingenieur_systemes_embarques': {'label': "Ingénieur logiciel, ingénieur systèmes embarqués", 'required': ['informatique_et_programmation'], 'single_rule': ['informatique_et_programmation']},
            'ingenieur_btp_ingenieur_structures': {'label': "Ingénieur BTP, ingénieur structures", 'required': ['genie_civil_et_structures'], 'single_rule': ['genie_civil_et_structures']},
            'ingenieur_telecoms_ingenieur_reseaux': {'label': "Ingénieur télécoms, ingénieur réseaux", 'required': ['genie_electrique_et_telecommunications'], 'single_rule': ['genie_electrique_et_telecommunications']},
            'ingenieur_chimiste_ingenieur_des_procedes': {'label': "Ingénieur chimiste, ingénieur des procédés", 'required': ['chimie_industrielle'], 'single_rule': ['chimie_industrielle']},
            'chef_de_projet_industriel_ingenieur_qualite': {'label': "Chef de projet industriel, ingénieur qualité", 'required': ['gestion_de_projet_et_methodologie_indust'], 'single_rule': ['gestion_de_projet_et_methodologie_indust']},
        }
    },
    'sociologie': {
        'label': "Sociologie",
        'modules': ['theories_sociologiques', 'methodes_quantitatives_et_statistiques_s', 'methodes_qualitatives_entretiens_observa', 'sociologie_urbaine', 'sociologie_du_travail_et_des_organisatio', 'sociologie_de_la_famille', 'sociologie_politique', 'demographie', 'sociologie_de_l_education'],
        'branches': {
            'chercheur_en_sociologie_enseignant_chercheur': {'label': "Chercheur en sociologie, enseignant-chercheur", 'required': ['theories_sociologiques'], 'single_rule': ['theories_sociologiques']},
            'sociologue_statisticien_demographe': {'label': "Sociologue statisticien, démographe", 'required': ['methodes_quantitatives_et_statistiques_s'], 'single_rule': ['methodes_quantitatives_et_statistiques_s']},
            'charge_d_etudes_sociales_chercheur_qualitatif': {'label': "Chargé d\'études sociales, chercheur qualitatif", 'required': ['methodes_qualitatives_entretiens_observa'], 'single_rule': ['methodes_qualitatives_entretiens_observa']},
            'urbaniste_social_charge_de_developpement_communaut': {'label': "Urbaniste social, chargé de développement communautaire", 'required': ['sociologie_urbaine'], 'single_rule': ['sociologie_urbaine']},
            'consultant_rh_sociologue_des_organisations': {'label': "Consultant RH, sociologue des organisations", 'required': ['sociologie_du_travail_et_des_organisatio'], 'single_rule': ['sociologie_du_travail_et_des_organisatio']},
            'chercheur_en_politiques_familiales_travailleur_soc': {'label': "Chercheur en politiques familiales, travailleur social", 'required': ['sociologie_de_la_famille'], 'single_rule': ['sociologie_de_la_famille']},
            'analyste_politique_charge_d_etudes_en_opinion_publ': {'label': "Analyste politique, chargé d\'études en opinion publique", 'required': ['sociologie_politique'], 'single_rule': ['sociologie_politique']},
            'demographe_analyste_population_et_statistiques_pub': {'label': "Démographe, analyste population et statistiques publiques", 'required': ['demographie'], 'single_rule': ['demographie']},
            'chercheur_en_politiques_educatives_conseiller_peda': {'label': "Chercheur en politiques éducatives, conseiller pédagogique", 'required': ['sociologie_de_l_education'], 'single_rule': ['sociologie_de_l_education']},
        }
    },
    'langues_et_communication': {
        'label': "Langues et Communication",
        'modules': ['linguistique_generale', 'litterature', 'traduction_et_interpretation', 'communication_interculturelle', 'journalisme', 'communication_digitale_et_reseaux_sociau', 'redaction_professionnelle_et_technique', 'medias_et_audiovisuel', 'relations_publiques'],
        'branches': {
            'chercheur_en_linguistique_enseignant_de_langues': {'label': "Chercheur en linguistique, enseignant de langues", 'required': ['linguistique_generale'], 'single_rule': ['linguistique_generale']},
            'enseignant_critique_litteraire_edition': {'label': "Enseignant, critique littéraire, édition", 'required': ['litterature'], 'single_rule': ['litterature']},
            'traducteur_professionnel_interprete_de_conference': {'label': "Traducteur professionnel, interprète de conférence", 'required': ['traduction_et_interpretation'], 'single_rule': ['traduction_et_interpretation']},
            'consultant_en_communication_interculturelle_diplom': {'label': "Consultant en communication interculturelle, diplomatie culturelle", 'required': ['communication_interculturelle'], 'single_rule': ['communication_interculturelle']},
            'journaliste_presentateur_reporter': {'label': "Journaliste, présentateur, reporter", 'required': ['journalisme'], 'single_rule': ['journalisme']},
            'community_manager_specialiste_marketing_digital': {'label': "Community Manager, spécialiste marketing digital", 'required': ['communication_digitale_et_reseaux_sociau'], 'single_rule': ['communication_digitale_et_reseaux_sociau']},
            'redacteur_technique_content_manager': {'label': "Rédacteur technique, content manager", 'required': ['redaction_professionnelle_et_technique'], 'single_rule': ['redaction_professionnelle_et_technique']},
            'realisateur_producteur_de_contenu_audiovisuel': {'label': "Réalisateur, producteur de contenu audiovisuel", 'required': ['medias_et_audiovisuel'], 'single_rule': ['medias_et_audiovisuel']},
            'attache_de_presse_responsable_des_relations_publiq': {'label': "Attaché de presse, responsable des relations publiques", 'required': ['relations_publiques'], 'single_rule': ['relations_publiques']},
        }
    },
    'psychologie': {
        'label': "Psychologie",
        'modules': ['psychologie_generale', 'psychologie_du_developpement', 'psychologie_clinique_et_psychopathologie', 'psychologie_sociale', 'psychologie_cognitive', 'neuropsychologie', 'psychologie_du_travail_et_des_organisati', 'psychometrie_et_methodologie_de_recherch'],
        'branches': {
            'chercheur_en_psychologie_enseignant_chercheur': {'label': "Chercheur en psychologie, enseignant-chercheur", 'required': ['psychologie_generale'], 'single_rule': ['psychologie_generale']},
            'psychologue_de_l_enfant_specialiste_du_developpeme': {'label': "Psychologue de l\'enfant, spécialiste du développement", 'required': ['psychologie_du_developpement'], 'single_rule': ['psychologie_du_developpement']},
            'psychologue_clinicien_psychotherapeute': {'label': "Psychologue clinicien, psychothérapeute", 'required': ['psychologie_clinique_et_psychopathologie'], 'single_rule': ['psychologie_clinique_et_psychopathologie']},
            'chercheur_en_psychologie_sociale_consultant_en_com': {'label': "Chercheur en psychologie sociale, consultant en communication/marketing", 'required': ['psychologie_sociale'], 'single_rule': ['psychologie_sociale']},
            'chercheur_en_sciences_cognitives_ergonome_cognitif': {'label': "Chercheur en sciences cognitives, ergonome cognitif", 'required': ['psychologie_cognitive'], 'single_rule': ['psychologie_cognitive']},
            'neuropsychologue_clinicien_ou_de_recherche': {'label': "Neuropsychologue clinicien ou de recherche", 'required': ['neuropsychologie'], 'single_rule': ['neuropsychologie']},
            'psychologue_du_travail_consultant_rh': {'label': "Psychologue du travail, consultant RH", 'required': ['psychologie_du_travail_et_des_organisati'], 'single_rule': ['psychologie_du_travail_et_des_organisati']},
            'chercheur_en_evaluation_psychologique_concepteur_d': {'label': "Chercheur en évaluation psychologique, concepteur de tests", 'required': ['psychometrie_et_methodologie_de_recherch'], 'single_rule': ['psychometrie_et_methodologie_de_recherch']},
        }
    },
    'medecine_et_pharmacie': {
        'label': "Médecine et Pharmacie",
        'modules': ['anatomie', 'physiologie', 'biochimie', 'microbiologie_et_immunologie', 'pharmacologie', 'pathologie_generale', 'semiologie_et_pratique_clinique', 'pharmacie_galenique', 'chimie_therapeutique', 'toxicologie', 'sante_publique_et_epidemiologie', 'stages_cliniques_pratiques'],
        'branches': {
            'chirurgien_specialites_chirurgicales': {'label': "Chirurgien, spécialités chirurgicales", 'required': ['anatomie'], 'single_rule': ['anatomie']},
            'medecine_du_sport_physiologie_clinique': {'label': "Médecine du sport, physiologie clinique", 'required': ['physiologie'], 'single_rule': ['physiologie']},
            'biologie_medicale_recherche_biomedicale': {'label': "Biologie médicale, recherche biomédicale", 'required': ['biochimie'], 'single_rule': ['biochimie']},
            'medecine_des_maladies_infectieuses_biologiste_medi': {'label': "Médecine des maladies infectieuses, biologiste médical", 'required': ['microbiologie_et_immunologie'], 'single_rule': ['microbiologie_et_immunologie']},
            'pharmacien_chercheur_en_developpement_de_medicamen': {'label': "Pharmacien, chercheur en développement de médicaments", 'required': ['pharmacologie'], 'single_rule': ['pharmacologie']},
            'anatomopathologiste_medecine_de_laboratoire': {'label': "Anatomopathologiste, médecine de laboratoire", 'required': ['pathologie_generale'], 'single_rule': ['pathologie_generale']},
            'medecine_generale_specialites_cliniques': {'label': "Médecine générale, spécialités cliniques", 'required': ['semiologie_et_pratique_clinique'], 'single_rule': ['semiologie_et_pratique_clinique']},
            'pharmacien_industriel_formulation_pharmaceutique': {'label': "Pharmacien industriel, formulation pharmaceutique", 'required': ['pharmacie_galenique'], 'single_rule': ['pharmacie_galenique']},
            'chercheur_en_chimie_medicinale_industrie_pharmaceu': {'label': "Chercheur en chimie médicinale, industrie pharmaceutique", 'required': ['chimie_therapeutique'], 'single_rule': ['chimie_therapeutique']},
            'toxicologue_expert_en_pharmacovigilance': {'label': "Toxicologue, expert en pharmacovigilance", 'required': ['toxicologie'], 'single_rule': ['toxicologie']},
            'medecin_de_sante_publique_epidemiologiste': {'label': "Médecin de santé publique, épidémiologiste", 'required': ['sante_publique_et_epidemiologie'], 'single_rule': ['sante_publique_et_epidemiologie']},
            'orientation_vers_la_specialite_clinique_correspond': {'label': "Orientation vers la spécialité clinique correspondante", 'required': ['stages_cliniques_pratiques'], 'single_rule': ['stages_cliniques_pratiques']},
        }
    },
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

    required = branch_info.get('required', [])
    single_rule = branch_info.get('single_rule', None)

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

    for filiere_key, filiere_info in BRANCH_CONFIG.items():
        filiere_label = filiere_info['label']
        filiere_modules = filiere_info['modules']
        branches = filiere_info['branches']

        for branch_key, branch_info in branches.items():
            branch_label = branch_info['label']
            for _ in range(N_PER_BRANCH):
                # On écrit les VRAIS LABELS accentués (pas les clés techniques snake_case)
                row = make_row(filiere_label, branch_label, branch_info, filiere_modules)
                all_rows.append(row)

    df = pd.DataFrame(all_rows)
    # Réorganisation des colonnes : d'abord tous les modules, puis filiere et branche_recommandee
    columns_order = ALL_MODULES + ['filiere', 'branche_recommandee']
    df = df[columns_order]

    df = df.sample(frac=1.0, random_state=RNG_SEED).reset_index(drop=True)

    os.makedirs('data/raw', exist_ok=True)
    out_path = 'data/raw/dataset_branch_config.csv'
    df.to_csv(out_path, sep=';', decimal=',', index=False)

    print(f"Dataset des branches généré : {len(df)} lignes, {len(ALL_MODULES)} modules, {df['branche_recommandee'].nunique()} branches uniques.")
    return df


if __name__ == '__main__':
    generate_branch_dataset()
