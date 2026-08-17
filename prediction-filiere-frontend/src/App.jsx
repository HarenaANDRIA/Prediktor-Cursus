import React, { useState } from 'react';
import axios from 'axios';

const MATIERES = [
  { id: 'mathematiques', label: 'Mathématiques' },
  { id: 'physique', label: 'Physique' },
  { id: 'chimie', label: 'Chimie' },
  { id: 'science_de_la_vie_et_de_la_terre', label: 'Science de la vie et de la terre' },
  { id: 'statistiques_et_probabilites', label: 'Statistiques et Probabilités' },
  { id: 'francais', label: 'Français' },
  { id: 'anglais', label: 'Anglais' },
  { id: 'philosophie', label: 'Philosophie' },
  { id: 'histoire_et_geographie', label: 'Histoire et Géographie' },
  { id: 'test_psychotechnique', label: 'Test Psychotechnique' }
];

const FILIERES_CONFIG = {
  'science_des_donnees_et_intelligence_artificielle': {
    label: 'Science des Données & IA',
    modules: [
      { id: 'algorithmique_python', label: 'Algorithmique & Python' },
      { id: 'sql_bases_de_donnees', label: 'SQL & Bases de Données' },
      { id: 'algebre_et_analyse', label: 'Algèbre & Analyse' },
      { id: 'langages_web', label: 'Langages Web' },
      { id: 'linux', label: 'Systèmes Linux' },
      { id: 'codage', label: 'Théorie du Codage' },
      { id: 'cryptographie', label: 'Cryptographie' },
      { id: 'reseaux informatiques', label: 'Réseaux Informatiques' }
    ]
  },
  'medecine_et_pharmacie': {
    label: 'Médecine & Pharmacie',
    modules: [
      { id: 'anatomie', label: 'Anatomie' },
      { id: 'physiologie', label: 'Physiologie' },
      { id: 'biochimie', label: 'Biochimie' },
      { id: 'histologie', label: 'Histologie' },
      { id: 'anatomie_pathologique', label: 'Anatomie Pathologique' }
    ]
  },
  'agronomie_et_biotechnologie': {
    label: 'Agronomie & Biotechnologie',
    modules: [
      { id: 'genetique_biologie_moleculaire', label: 'Génétique & Biologie Moléculaire' },
      { id: 'physiologie_ecologie', label: 'Physiologie & Écologie' },
      { id: 'biochimie', label: 'Biochimie' },
      { id: 'statistiques_agricoles_et_modelisation', label: 'Statistiques Agricoles' }
    ]
  },
  'sciences_environnementales_et_science_marine': {
    label: 'Sciences Environnementales & Marine',
    modules: [
      { id: 'oceanographie_et_climatologie', label: 'Océanographie & Climatologie' },
      { id: 'ecologie_marine', label: 'Écologie Marine' },
      { id: 'geologie_sedimentaire_et_hydrologie', label: 'Géologie & Hydrologie' }
    ]
  },
  'tourisme_et_hotellerie': {
    label: 'Tourisme & Hôtellerie',
    modules: [
      { id: 'management_interculturel', label: 'Management Interculturel' },
      { id: 'comptabilite', label: 'Comptabilité' },
      { id: 'geographie', label: 'Géographie' },
      { id: 'droit', label: 'Droit' },
      { id: 'anglais', label: 'Anglais' },
      { id: 'francais', label: 'Français' },
      { id: 'allemand', label: 'Allemand' },
      { id: 'espagnol', label: 'Espagnol' }
    ]
  },
  'langues_et_communication': {
    label: 'Langues & Communication',
    modules: [
      { id: 'langues_etrangeres', label: 'Langues Étrangères' },
      { id: 'semiologie', label: 'Sémiologie' },
      { id: 'journalisme_et_redaction_web', label: 'Journalisme & Rédaction Web' },
      { id: 'audiovisuel_et_multimedia', label: 'Audiovisuel & Multimédia' }
    ]
  },
  'sociologie': {
    label: 'Sociologie',
    modules: [
      { id: 'theories_sociologiques_et_philosophie_sociale', label: 'Théories Sociologiques' },
      { id: 'statistiques_methodologie_quantitative', label: 'Méthodologie Quantitative' },
      { id: 'demographie_sociologie_famille', label: 'Démographie & Famille' }
    ]
  },
  'droit_et_sciences_politiques': {
    label: 'Droit & Sciences Politiques',
    modules: [
      { id: 'droit_civil_et_procedure_civile', label: 'Droit Civil & Procédure' },
      { id: 'droit_penal_procedure_penale', label: 'Droit Pénal' },
      { id: 'droit_administratif_constitutionnel', label: 'Droit Administratif & Const.' },
      { id: 'droit_commercial', label: 'Droit Commercial' }
    ]
  },
  'sciences_actuarielles': {
    label: 'Sciences Actuarielles',
    modules: [
      { id: 'probabilites_statistiques_appliquees', label: 'Probabilités Appliquées' },
      { id: 'mathematiques_financieres_finance_marche', label: 'Mathématiques Financières' },
      { id: 'droit_assurances_reglementation', label: 'Droit des Assurances' }
    ]
  },
  'ingenierie_et_science_generale': {
    label: 'Ingénierie & Science Générale',
    modules: [
      { id: 'resistance_des_materiaux', label: 'Résistance des Matériaux (RDM)' },
      { id: 'mecanique_des_fluides', label: 'Mécanique des Fluides' },
      { id: 'thermodynamique_energetique', label: 'Thermodynamique' },
      { id: 'electronique', label: 'Électronique' },
      { id: 'automatique', label: 'Automatique' },
      { id: 'electricite', label: 'Électricité' },
      { id: 'mathematiques_discretes_et_algorithmique', label: 'Maths Discrètes & Algo' }
    ]
  },
  'psychologie': {
    label: 'Psychologie',
    modules: [
      { id: 'psychopathologie_clinique', label: 'Psychopathologie Clinique' },
      { id: 'neurosciences_sociales', label: 'Neurosciences Sociales' }
    ]
  },
  'anthropologie_ou_archeologie': {
    label: 'Anthropologie ou Archéologie',
    modules: [
      { id: 'paleoanthropologie_et_osteologie', label: 'Paléoanthropologie & Ostéologie' },
      { id: 'prehistoire_geoarcheologie', label: 'Préhistoire & Géoarchéologie' },
      { id: 'ethnologie', label: 'Ethnologie' },
      { id: 'anthropologie_culturelle', label: 'Anthropologie Culturelle' }
    ]
  }
};

const DEFAULT_NOTES = MATIERES.reduce((acc, m) => ({ ...acc, [m.id]: 10 }), {});

const createDefaultModuleNotes = (filiereKey) => {
  const modules = FILIERES_CONFIG[filiereKey]?.modules || [];
  return modules.reduce((acc, mod) => ({ ...acc, [mod.id]: 10 }), {});
};

const SERIES = {
  aucune: { label: 'Aucune', coef5: [], coef4: [], coef3: [] },
  scientifique: {
    label: 'Scientifique',
    coef5: ['mathematiques', 'physique', 'chimie', 'statistiques_et_probabilites'],
    coef4: ['test_psychotechnique', 'science_de_la_vie_et_de_la_terre'],
    coef3: [],
  },
  litteraire: {
    label: 'Littéraire',
    coef5: ['francais', 'anglais'],
    coef4: ['philosophie', 'histoire_et_geographie'],
    coef3: ['statistiques_et_probabilites', 'test_psychotechnique'],
  },
};

function getCoefficient(subjectId, serieKey) {
  const serie = SERIES[serieKey];
  if (!serie || serieKey === 'aucune') return 1;
  if (serie.coef5.includes(subjectId)) return 5;
  if (serie.coef4.includes(subjectId)) return 4;
  if (serie.coef3.includes(subjectId)) return 3;
  return 2;
}

function computeNotesForModel(notes, serieKey) {
  const coefs = MATIERES.map(m => getCoefficient(m.id, serieKey));
  const meanCoef = coefs.reduce((a, b) => a + b, 0) / coefs.length;

  const adjusted = {};
  MATIERES.forEach(m => {
    const note = typeof notes[m.id] === 'number' ? notes[m.id] : 0;
    const coef = getCoefficient(m.id, serieKey);
    const raw = meanCoef > 0 ? (note * coef) / meanCoef : note;
    adjusted[m.id] = Math.max(0, Math.min(20, Math.round(raw * 100) / 100));
  });
  return adjusted;
}

const INK = '#1E2A3A';
const INK_SOFT = '#55606B';
const PAPER = '#FFFFFF';
const LINE = '#D9DCD2';
const ACCENT = '#9C3B2E';
const ACCENT_SOFT = '#F3E5E1';

export default function App() {
  const [activeTab, setActiveTab] = useState('bac');

  // États Post-Bac
  const [notes, setNotes] = useState(DEFAULT_NOTES);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showBacQuestion, setShowBacQuestion] = useState(false);
  const [rejected, setRejected] = useState(false);
  const [serie, setSerie] = useState('aucune');

  // États Branches Universitaires
  const initialFiliereKey = Object.keys(FILIERES_CONFIG)[0];
  const [selectedFiliereKey, setSelectedFiliereKey] = useState(initialFiliereKey);
  const [moduleNotes, setModuleNotes] = useState(() => createDefaultModuleNotes(initialFiliereKey));
  const [branchResults, setBranchResults] = useState(null);
  const [branchLoading, setBranchLoading] = useState(false);
  const [branchError, setBranchError] = useState(null);

  const handleInputChange = (id, value) => {
    const val = parseFloat(value);
    setNotes(prev => ({
      ...prev,
      [id]: isNaN(val) ? '' : Math.min(20, Math.max(0, val))
    }));
  };

  const handleModuleNoteChange = (modId, value) => {
    const val = parseFloat(value);
    setModuleNotes(prev => ({
      ...prev,
      [modId]: isNaN(val) ? '' : Math.min(20, Math.max(0, val))
    }));
  };

  const handleFiliereChange = (newFiliereKey) => {
    setSelectedFiliereKey(newFiliereKey);
    setModuleNotes(createDefaultModuleNotes(newFiliereKey));
    setBranchResults(null);
    setBranchError(null);
  };

  const handleResetBac = () => {
    setNotes(DEFAULT_NOTES);
    setResults(null);
    setError(null);
    setShowBacQuestion(false);
    setRejected(false);
    setSerie('aucune');
  };

  const handleResetBranch = () => {
    setModuleNotes(createDefaultModuleNotes(selectedFiliereKey));
    setBranchResults(null);
    setBranchError(null);
  };

  // Calculs Moyenne Post-Bac
  const valuesBac = Object.values(notes).filter(v => typeof v === 'number');
  const moyNumBac = valuesBac.length ? valuesBac.reduce((a, b) => a + b, 0) / valuesBac.length : 0;
  const moyenneBac = valuesBac.length ? moyNumBac.toFixed(2) : '0.00';

  const weightedTotals = MATIERES.reduce((acc, m) => {
    const note = notes[m.id];
    if (typeof note !== 'number') return acc;
    const coef = getCoefficient(m.id, serie);
    return { sumNotes: acc.sumNotes + note * coef, sumCoefs: acc.sumCoefs + coef };
  }, { sumNotes: 0, sumCoefs: 0 });
  const moyennePondereeNum = weightedTotals.sumCoefs ? weightedTotals.sumNotes / weightedTotals.sumCoefs : 0;
  const moyennePonderee = weightedTotals.sumCoefs ? moyennePondereeNum.toFixed(2) : '0.00';

  // Calculs Moyenne Modules Universitaires
  const currentModules = FILIERES_CONFIG[selectedFiliereKey]?.modules || [];
  const moduleValues = currentModules
    .map(mod => moduleNotes[mod.id])
    .filter(val => typeof val === 'number');
  const moyNumModules = moduleValues.length ? moduleValues.reduce((a, b) => a + b, 0) / moduleValues.length : 0;
  const moyenneModules = moduleValues.length ? moyNumModules.toFixed(2) : '0.00';

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    setShowBacQuestion(false);
    setRejected(false);

    try {
      const notesForModel = computeNotesForModel(notes, serie);
      const response = await axios.post('http://localhost:8000/predict', notesForModel);
      setResults(response.data.recommandations);
    } catch (err) {
      setError("Impossible de contacter le serveur d'IA (http://localhost:8000).");
    } finally {
      setLoading(false);
    }
  };

  const fetchBranchRecommendations = async (e) => {
    e.preventDefault();
    setBranchLoading(true);
    setBranchError(null);

    try {
      const response = await axios.post('http://localhost:8000/predict-branch', {
        filiere: selectedFiliereKey,
        notes_modules: moduleNotes
      });
      setBranchResults(response.data.recommandations);
    } catch (err) {
      setBranchError("Impossible de contacter le serveur de recommandation de branche.");
    } finally {
      setBranchLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setResults(null);
    setError(null);
    setRejected(false);

    if (moyNumBac < 10) {
      setShowBacQuestion(true);
    } else {
      fetchRecommendations();
    }
  };

  return (
    <div className="min-h-screen font-sans pb-16 animate-fadeIn" style={{ backgroundColor: PAPER, color: INK }}>
      {/* Styles des animations provenant de Exemple.jsx */}
      <style>{`
        @keyframes popIn {
          0% { transform: scale(0.96); opacity: 0; }
          60% { transform: scale(1.02); opacity: 1; }
          100% { transform: scale(1); opacity: 1; }
        }

        @keyframes pulseGlow {
          0%, 100% { box-shadow: 0 4px 20px -2px rgba(156, 59, 46, 0.25); }
          50% { box-shadow: 0 6px 28px 4px rgba(156, 59, 46, 0.45); }
        }

        /* Effet de bounce récupéré depuis Exemple.jsx */
        @keyframes continuousBounce {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-6px);
          }
        }

        @keyframes shine {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }

        .animate-top1 {
          animation: 
            popIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards,
            pulseGlow 3s infinite ease-in-out,
            continuousBounce 2.5s infinite ease-in-out;
        }

        .shine-effect::after {
          content: '';
          position: absolute;
          top: 0; right: 0; bottom: 0; left: 0;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
          transform: translateX(-100%);
          animation: shine 2s infinite 0.8s;
        }
      `}</style>

      <header className="sticky top-0 z-50 border-b backdrop-blur-md bg-white/80" style={{ borderColor: LINE }}>
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="font-display text-2xl font-medium tracking-tight" style={{ color: INK }}>
              Prédiktor Cursus
            </h1>
            <p className="font-mono text-[10px] uppercase tracking-[0.15em] mt-1" style={{ color: INK_SOFT }}>
              Système d'orientation · Filières & Branches
            </p>
          </div>
          
          <div className="flex gap-2 bg-slate-100 p-1 rounded-lg border shadow-inner" style={{ borderColor: LINE }}>
            <button
              onClick={() => setActiveTab('bac')}
              className={`px-4 py-2 rounded text-xs font-mono transition-all duration-200 ${
                activeTab === 'bac' ? 'bg-slate-800 text-white shadow-md scale-[1.02]' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Orientation Post-Bac
            </button>
            <button
              onClick={() => setActiveTab('branche')}
              className={`px-4 py-2 rounded text-xs font-mono transition-all duration-200 ${
                activeTab === 'branche' ? 'bg-slate-800 text-white shadow-md scale-[1.02]' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Spécialisation Branche
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 pt-10">
        {activeTab === 'bac' ? (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <section className="lg:col-span-7 space-y-6">
              <div className="bg-white rounded-lg p-6 border shadow-sm" style={{ borderColor: LINE }}>
                <div className="flex items-start justify-between mb-6 pb-5 border-b" style={{ borderColor: LINE }}>
                  <div>
                    <h2 className="font-display text-lg font-medium" style={{ color: INK }}>Bulletin de notes</h2>
                    <p className="font-sans text-sm mt-1" style={{ color: INK_SOFT }}>Saisissez chaque note sur 20 points.</p>
                  </div>
                  <button
                    type="button"
                    onClick={handleResetBac}
                    className="font-mono text-[10px] uppercase tracking-[0.1em] px-3 py-2 rounded border transition-colors hover:bg-slate-50"
                    style={{ borderColor: LINE, color: INK_SOFT }}
                  >
                    Réinitialiser
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-8">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>
                        Série du bac (Madagascar)
                      </span>
                    </div>
                    <div className="flex gap-2">
                      {Object.entries(SERIES).map(([key, s]) => (
                        <button
                          key={key}
                          type="button"
                          onClick={() => setSerie(key)}
                          className="flex-1 py-2 px-3 rounded font-mono text-[10px] uppercase tracking-[0.1em] font-medium border transition-all duration-150"
                          style={
                            serie === key
                              ? { backgroundColor: INK, color: PAPER, borderColor: INK, transform: 'scale(1.02)' }
                              : { backgroundColor: 'transparent', color: INK_SOFT, borderColor: LINE }
                          }
                        >
                          {s.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                    {MATIERES.map(m => (
                      <div key={m.id} className="flex items-baseline justify-between py-2.5 border-b" style={{ borderColor: LINE }}>
                        <label htmlFor={m.id} className="font-sans text-sm">{m.label}</label>
                        <input
                          id={m.id}
                          type="number"
                          min="0"
                          max="20"
                          step="0.25"
                          value={notes[m.id]}
                          onChange={e => handleInputChange(m.id, e.target.value)}
                          className="font-mono text-base font-semibold text-right w-16 bg-transparent border-b-2 focus:outline-none transition-colors focus:border-slate-800"
                          required
                        />
                      </div>
                    ))}
                  </div>

                  <div className="p-4 rounded border flex items-center justify-between" style={{ borderColor: LINE, backgroundColor: '#FAFAFA' }}>
                    <div>
                      <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>Moyenne Générale</span>
                      <div className="font-mono text-xl font-bold mt-0.5">{moyenneBac} <span className="text-xs font-normal text-slate-400">/20</span></div>
                    </div>
                    {serie !== 'aucune' && (
                      <div className="text-right">
                        <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>Moyenne Pondérée</span>
                        <div className="font-mono text-xl font-bold mt-0.5" style={{ color: ACCENT }}>{moyennePonderee} <span className="text-xs font-normal text-slate-400">/20</span></div>
                      </div>
                    )}
                  </div>

                  {showBacQuestion && !rejected && (
                    <div className="p-4 rounded border-l-4 animate-slideDown" style={{ backgroundColor: ACCENT_SOFT, borderColor: ACCENT }}>
                      <p className="text-sm font-medium mb-3" style={{ color: INK }}>
                        Votre moyenne générale est inférieure à 10 ({moyenneBac}/20). Avez-vous quand même réussi votre examen du Bac ?
                      </p>
                      <div className="flex gap-3">
                        <button
                          type="button"
                          onClick={() => { setShowBacQuestion(false); fetchRecommendations(); }}
                          className="px-4 py-2 rounded font-mono text-xs uppercase tracking-wider font-semibold text-white shadow-sm"
                          style={{ backgroundColor: ACCENT }}
                        >
                          Oui, j'ai mon Bac
                        </button>
                        <button
                          type="button"
                          onClick={() => setRejected(true)}
                          className="px-4 py-2 rounded font-mono text-xs uppercase tracking-wider font-semibold border bg-white"
                          style={{ borderColor: LINE, color: INK_SOFT }}
                        >
                          Non
                        </button>
                      </div>
                    </div>
                  )}

                  {rejected && (
                    <div className="p-4 rounded border bg-slate-50 text-center text-sm font-medium text-slate-600 animate-fadeIn">
                      Il est recommandé de redoubler d'efforts ou de se préparer pour une session de rattrapage avant d'envisager une orientation supérieure.
                    </div>
                  )}

                  {error && <p className="text-red-600 text-xs font-mono">{error}</p>}

                  {!showBacQuestion && !rejected && (
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full py-4 px-6 rounded font-mono text-xs uppercase tracking-[0.15em] font-medium text-center transition-all shadow-md hover:shadow-lg"
                      style={{ backgroundColor: INK, color: PAPER }}
                    >
                      {loading ? "Analyse en cours..." : "Découvrir mes filières"}
                    </button>
                  )}
                </form>
              </div>
            </section>

            <section className="lg:col-span-5 space-y-6">
              {results && (
                <div className="bg-white rounded-2xl p-6 border shadow-sm space-y-6 animate-fadeIn" style={{ borderColor: LINE }}>
                  <div>
                    <p className="font-mono text-[10px] uppercase tracking-[0.2em] font-semibold text-slate-400">
                      TOP 3 · RECOMMANDATIONS DE FILIÈRES
                    </p>
                    <h2 className="font-serif text-2xl font-bold mt-1" style={{ color: INK }}>
                      Recommandations
                    </h2>
                    <hr className="mt-4" style={{ borderColor: LINE }} />
                  </div>

                  <div className="space-y-5">
                    {results.map((rec, index) => {
                      const isTop1 = index === 0;
                      const prob = parseFloat(rec.probabilite);

                      if (isTop1) {
                        return (
                          <div
                            key={index}
                            className="relative rounded-2xl p-5 border-2 transition-all duration-300 shadow-lg animate-top1"
                            style={{
                              backgroundColor: '#FDF8F6',
                              borderColor: ACCENT
                            }}
                          >
                            <div 
                              className="absolute -top-3.5 right-6 px-3 py-0.5 rounded-full border text-[10px] font-mono font-bold tracking-widest uppercase flex items-center gap-1.5 shadow-sm bg-white z-10"
                              style={{ borderColor: ACCENT, color: ACCENT }}
                            >
                              <span className="w-1.5 h-1.5 rounded-full animate-ping" style={{ backgroundColor: ACCENT }} />
                              MEILLEUR CHOIX
                            </div>

                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center gap-3">
                                <span 
                                  className="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm text-white shadow-sm"
                                  style={{ backgroundColor: ACCENT }}
                                >
                                  1
                                </span>
                                <h3 className="font-bold text-lg leading-snug" style={{ color: INK }}>
                                  {rec.filiere}
                                </h3>
                              </div>
                              <span className="font-mono text-2xl font-black tracking-tight" style={{ color: ACCENT }}>
                                {rec.probabilite}%
                              </span>
                            </div>

                            <div className="w-full bg-slate-200/70 h-2.5 rounded-full overflow-hidden relative">
                              <div
                                className="h-full rounded-full transition-all duration-1000 ease-out shine-effect"
                                style={{
                                  width: `${prob}%`,
                                  backgroundColor: ACCENT
                                }}
                              />
                            </div>
                          </div>
                        );
                      }

                      return (
                        <div
                          key={index}
                          className="rounded-2xl p-5 border bg-white transition-all duration-200 hover:border-slate-400 shadow-sm"
                          style={{ borderColor: LINE }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center gap-3">
                              <span className="w-8 h-8 rounded-full border flex items-center justify-center font-semibold text-sm text-slate-600 bg-slate-50" style={{ borderColor: LINE }}>
                                {rec.rang}
                              </span>
                              <h3 className="font-semibold text-base" style={{ color: INK }}>
                                {rec.filiere}
                              </h3>
                            </div>
                            <span className="font-mono text-xl font-bold" style={{ color: INK }}>
                              {rec.probabilite}%
                            </span>
                          </div>

                          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                            <div
                              className="h-full rounded-full transition-all duration-1000 ease-out"
                              style={{
                                width: `${prob}%`,
                                backgroundColor: INK
                              }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </section>
          </div>
        ) : (
          /* SECTION SPÉCIALISATION BRANCHE UNIVERSITAIRE */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <section className="lg:col-span-7 space-y-6">
              <div className="bg-white rounded-lg p-6 border shadow-sm" style={{ borderColor: LINE }}>
                <div className="flex items-start justify-between mb-6 pb-5 border-b" style={{ borderColor: LINE }}>
                  <div>
                    <h2 className="font-display text-lg font-medium" style={{ color: INK }}>Bulletin de modules universitaires</h2>
                    <p className="font-sans text-sm mt-1" style={{ color: INK_SOFT }}>Sélectionnez votre filière et renseignez vos notes sur 20 points.</p>
                  </div>
                  <button
                    type="button"
                    onClick={handleResetBranch}
                    className="font-mono text-[10px] uppercase tracking-[0.1em] px-3 py-2 rounded border transition-colors hover:bg-slate-50"
                    style={{ borderColor: LINE, color: INK_SOFT }}
                  >
                    Réinitialiser
                  </button>
                </div>

                <form onSubmit={fetchBranchRecommendations} className="space-y-8">
                  <div>
                    <span className="font-mono text-[10px] uppercase tracking-[0.15em] block mb-2" style={{ color: INK_SOFT }}>
                      Filière universitaire
                    </span>
                    <select
                      value={selectedFiliereKey}
                      onChange={e => handleFiliereChange(e.target.value)}
                      className="w-full p-3 border rounded font-sans text-sm bg-white focus:outline-none focus:border-slate-800 transition-colors"
                      style={{ borderColor: LINE, color: INK }}
                    >
                      {Object.entries(FILIERES_CONFIG).map(([key, config]) => (
                        <option key={key} value={key}>{config.label}</option>
                      ))}
                    </select>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                    {currentModules.map(mod => (
                      <div key={mod.id} className="flex items-baseline justify-between py-2.5 border-b" style={{ borderColor: LINE }}>
                        <label htmlFor={mod.id} className="font-sans text-sm">{mod.label}</label>
                        <input
                          id={mod.id}
                          type="number"
                          min="0"
                          max="20"
                          step="0.25"
                          value={moduleNotes[mod.id] ?? ''}
                          onChange={e => handleModuleNoteChange(mod.id, e.target.value)}
                          className="font-mono text-base font-semibold text-right w-16 bg-transparent border-b-2 focus:outline-none transition-colors focus:border-slate-800"
                          required
                        />
                      </div>
                    ))}
                  </div>

                  <div className="p-4 rounded border flex items-center justify-between" style={{ borderColor: LINE, backgroundColor: '#FAFAFA' }}>
                    <div>
                      <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>Moyenne Générale des Modules</span>
                      <div className="font-mono text-xl font-bold mt-0.5">{moyenneModules} <span className="text-xs font-normal text-slate-400">/20</span></div>
                    </div>
                  </div>

                  {branchError && <p className="text-red-600 text-xs font-mono">{branchError}</p>}

                  <button
                    type="submit"
                    disabled={branchLoading}
                    className="w-full py-4 px-6 rounded font-mono text-xs uppercase tracking-[0.15em] font-medium text-center transition-all shadow-md hover:shadow-lg"
                    style={{ backgroundColor: INK, color: PAPER }}
                  >
                    {branchLoading ? "Analyse en cours..." : "Découvrir ma branche idéale"}
                  </button>
                </form>
              </div>
            </section>

            <section className="lg:col-span-5 space-y-6">
              {branchResults && (
                <div className="bg-white rounded-2xl p-6 border shadow-sm space-y-6 animate-fadeIn" style={{ borderColor: LINE }}>
                  <div>
                    <p className="font-mono text-[10px] uppercase tracking-[0.2em] font-semibold text-slate-400">
                      TOP 3 · RECOMMANDATIONS DE BRANCHES
                    </p>
                    <h2 className="font-serif text-2xl font-bold mt-1" style={{ color: INK }}>
                      Recommandations
                    </h2>
                    <hr className="mt-4" style={{ borderColor: LINE }} />
                  </div>

                  <div className="space-y-5">
                    {branchResults.map((rec, index) => {
                      const isTop1 = index === 0;
                      const prob = parseFloat(rec.probabilite);

                      if (isTop1) {
                        return (
                          <div
                            key={index}
                            className="relative rounded-2xl p-5 border-2 transition-all duration-300 shadow-lg animate-top1"
                            style={{
                              backgroundColor: '#FDF8F6',
                              borderColor: ACCENT
                            }}
                          >
                            <div 
                              className="absolute -top-3.5 right-6 px-3 py-0.5 rounded-full border text-[10px] font-mono font-bold tracking-widest uppercase flex items-center gap-1.5 shadow-sm bg-white z-10"
                              style={{ borderColor: ACCENT, color: ACCENT }}
                            >
                              <span className="w-1.5 h-1.5 rounded-full animate-ping" style={{ backgroundColor: ACCENT }} />
                              MEILLEUR CHOIX
                            </div>

                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center gap-3">
                                <span 
                                  className="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm text-white shadow-sm"
                                  style={{ backgroundColor: ACCENT }}
                                >
                                  1
                                </span>
                                <h3 className="font-bold text-lg leading-snug" style={{ color: INK }}>
                                  {rec.branche}
                                </h3>
                              </div>
                              <span className="font-mono text-2xl font-black tracking-tight" style={{ color: ACCENT }}>
                                {rec.probabilite}%
                              </span>
                            </div>

                            <div className="w-full bg-slate-200/70 h-2.5 rounded-full overflow-hidden relative">
                              <div
                                className="h-full rounded-full transition-all duration-1000 ease-out shine-effect"
                                style={{
                                  width: `${prob}%`,
                                  backgroundColor: ACCENT
                                }}
                              />
                            </div>
                          </div>
                        );
                      }

                      return (
                        <div
                          key={index}
                          className="rounded-2xl p-5 border bg-white transition-all duration-200 hover:border-slate-400 shadow-sm"
                          style={{ borderColor: LINE }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center gap-3">
                              <span className="w-8 h-8 rounded-full border flex items-center justify-center font-semibold text-sm text-slate-600 bg-slate-50" style={{ borderColor: LINE }}>
                                {rec.rang}
                              </span>
                              <h3 className="font-semibold text-base" style={{ color: INK }}>
                                {rec.branche}
                              </h3>
                            </div>
                            <span className="font-mono text-xl font-bold" style={{ color: INK }}>
                              {rec.probabilite}%
                            </span>
                          </div>

                          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                            <div
                              className="h-full rounded-full transition-all duration-1000 ease-out"
                              style={{
                                width: `${prob}%`,
                                backgroundColor: INK
                              }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}