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

const DEFAULT_NOTES = MATIERES.reduce((acc, m) => ({ ...acc, [m.id]: 10 }), {});

const SERIES = {
  aucune: { label: 'Aucune', coef5: [], coef4: [], coef3: [] },
  scientifique: {
    label: 'Scientifique',
    coef5: ['mathematiques', 'physique', 'chimie','statistiques_et_probabilites', 
            'science_de_la_vie_et_de_la_terre'],
    coef4: ['test_psychotechnique'],
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
  const [notes, setNotes] = useState(DEFAULT_NOTES);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showBacQuestion, setShowBacQuestion] = useState(false);
  const [rejected, setRejected] = useState(false);
  const [serie, setSerie] = useState('aucune');
  const [isFlatProfile, setIsFlatProfile] = useState(false);

  const handleInputChange = (id, value) => {
    const val = parseFloat(value);
    setNotes(prev => ({
      ...prev,
      [id]: isNaN(val) ? '' : Math.min(20, Math.max(0, val))
    }));
  };

  const handleReset = () => {
    setNotes(DEFAULT_NOTES);
    setResults(null);
    setError(null);
    setShowBacQuestion(false);
    setRejected(false);
    setSerie('aucune');
    setIsFlatProfile(false);
  };

  const values = Object.values(notes).filter(v => typeof v === 'number');
  const moyNum = values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0;
  const moyenne = values.length ? moyNum.toFixed(2) : '0.00';

  const weightedTotals = MATIERES.reduce((acc, m) => {
    const note = notes[m.id];
    if (typeof note !== 'number') return acc;
    const coef = getCoefficient(m.id, serie);
    return { sumNotes: acc.sumNotes + note * coef, sumCoefs: acc.sumCoefs + coef };
  }, { sumNotes: 0, sumCoefs: 0 });
  const moyennePondereeNum = weightedTotals.sumCoefs ? weightedTotals.sumNotes / weightedTotals.sumCoefs : 0;
  const moyennePonderee = weightedTotals.sumCoefs ? moyennePondereeNum.toFixed(2) : '0.00';

  const checkIfFlatProfile = (currentNotes) => {
    const vals = Object.values(currentNotes);
    if (vals.length === 0) return false;
    const firstVal = vals[0];
    return vals.every(v => v === firstVal);
  };

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    setShowBacQuestion(false);
    setRejected(false);

    const flat = checkIfFlatProfile(notes);
    setIsFlatProfile(flat);

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

  const handleSubmit = (e) => {
    e.preventDefault();
    setResults(null);
    setError(null);
    setRejected(false);

    if (moyNum < 10) {
      setShowBacQuestion(true);
    } else {
      fetchRecommendations();
    }
  };

  return (
    <div className="min-h-screen font-sans pb-16" style={{ backgroundColor: PAPER, color: INK }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
        .font-display { font-family: 'Fraunces', serif; font-feature-settings: 'ss01' 1; }
        .font-mono { font-family: 'IBM Plex Mono', monospace; }
        .font-sans { font-family: 'IBM Plex Sans', sans-serif; }

        @keyframes popIn {
          0% { transform: scale(0.96); opacity: 0; }
          60% { transform: scale(1.02); opacity: 1; }
          100% { transform: scale(1); opacity: 1; }
        }

        @keyframes pulseGlow {
          0%, 100% { box-shadow: 0 4px 20px -2px rgba(156, 59, 46, 0.25); }
          50% { box-shadow: 0 6px 28px 4px rgba(156, 59, 46, 0.45); }
        }

        /* Continuous bounce animation for Top-1 */
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

      <header className="sticky top-0 z-50 border-b" style={{ backgroundColor: PAPER, borderColor: LINE }}>
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="font-display text-2xl font-medium tracking-tight" style={{ color: INK }}>
              Prédiktor Cursus
            </h1>
            <p className="font-mono text-[10px] uppercase tracking-[0.15em] mt-1" style={{ color: INK_SOFT }}>
              Système d'orientation · 12 matières · 10 filières
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="font-mono text-[10px] uppercase tracking-[0.15em] text-right leading-tight" style={{ color: INK_SOFT }}>
              Moyenne<br />générale
            </span>
            <div
              className="min-w-14 h-14 px-3 rounded-full flex items-center justify-center border-2 font-mono font-semibold text-sm whitespace-nowrap"
              style={{ borderColor: INK, color: INK }}
            >
              {moyenne}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 pt-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <section className="lg:col-span-7 space-y-6">
            <div className="bg-white rounded-lg p-6 border" style={{ borderColor: LINE }}>
              <div className="flex items-start justify-between mb-6 pb-5 border-b" style={{ borderColor: LINE }}>
                <div>
                  <h2 className="font-display text-lg font-medium" style={{ color: INK }}>Bulletin de notes</h2>
                  <p className="font-sans text-sm mt-1" style={{ color: INK_SOFT }}>Saisissez chaque note sur 20 points.</p>
                </div>
                <button
                  type="button"
                  onClick={handleReset}
                  className="font-mono text-[10px] uppercase tracking-[0.1em] px-3 py-2 rounded border transition-colors"
                  style={{ borderColor: LINE, color: INK_SOFT }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = ACCENT; e.currentTarget.style.color = ACCENT; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = LINE; e.currentTarget.style.color = INK_SOFT; }}
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
                    {serie !== 'aucune' && (
                      <span className="font-sans text-xs" style={{ color: INK_SOFT }}>
                        Moyenne pondérée : <span className="font-mono font-semibold" style={{ color: ACCENT }}>{moyennePonderee}/20</span>
                      </span>
                    )}
                  </div>
                  <div className="flex gap-2">
                    {Object.entries(SERIES).map(([key, s]) => {
                      const isActive = serie === key;
                      return (
                        <button
                          key={key}
                          type="button"
                          onClick={() => setSerie(key)}
                          className="flex-1 py-2 px-3 rounded font-mono text-[10px] uppercase tracking-[0.1em] font-medium border transition-colors"
                          style={
                            isActive
                              ? { backgroundColor: INK, color: PAPER, borderColor: INK }
                              : { backgroundColor: 'transparent', color: INK_SOFT, borderColor: LINE }
                          }
                        >
                          {s.label}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                  {MATIERES.map(m => {
                    const coef = getCoefficient(m.id, serie);
                    return (
                      <div
                        key={m.id}
                        className="flex items-baseline justify-between py-2.5 border-b"
                        style={{ borderColor: LINE, borderBottomStyle: 'dotted' }}
                      >
                        <div className="flex items-center gap-2 pr-2 min-w-0">
                          <label htmlFor={m.id} className="font-sans text-sm truncate" style={{ color: INK }}>
                            {m.label}
                          </label>
                          {serie !== 'aucune' && (
                            <span
                              className="font-mono text-[9px] px-1.5 py-0.5 rounded-full border shrink-0 inline-flex items-center justify-center min-w-[24px] h-[18px]"
                              style={
                                coef >= 4
                                  ? { color: ACCENT, borderColor: ACCENT, backgroundColor: ACCENT_SOFT }
                                  : { color: INK_SOFT, borderColor: LINE }
                              }
                            >
                              ×{coef}
                            </span>
                          )}
                        </div>
                        <input
                          id={m.id}
                          type="number"
                          min="0"
                          max="20"
                          step="0.25"
                          value={notes[m.id]}
                          onChange={e => handleInputChange(m.id, e.target.value)}
                          className="font-mono text-base font-semibold text-right min-w-[4.5rem] w-auto bg-transparent border-0 border-b-2 focus:outline-none px-1"
                          style={{ color: INK, borderColor: 'transparent' }}
                          onFocus={e => { e.currentTarget.style.borderColor = ACCENT; }}
                          onBlur={e => { e.currentTarget.style.borderColor = 'transparent'; }}
                          required
                        />
                      </div>
                    );
                  })}
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-4 px-6 rounded font-mono text-xs uppercase tracking-[0.15em] font-medium transition-colors disabled:opacity-50 text-center"
                  style={{ backgroundColor: loading ? INK_SOFT : INK, color: PAPER }}
                  onMouseEnter={e => { if (!loading) e.currentTarget.style.backgroundColor = ACCENT; }}
                  onMouseLeave={e => { if (!loading) e.currentTarget.style.backgroundColor = INK; }}
                >
                  {loading ? "Analyse en cours..." : "Découvrir mes filières"}
                </button>
              </form>
            </div>
          </section>

          <section className="lg:col-span-5 space-y-6">
            {error && (
              <div className="rounded-lg p-4 text-sm font-sans" style={{ backgroundColor: ACCENT_SOFT, color: ACCENT, border: `1px solid ${ACCENT}` }}>
                {error}
              </div>
            )}

            {!results && !loading && !error && !showBacQuestion && !rejected && (
              <div
                className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border border-dashed"
                style={{ borderColor: LINE }}
              >
                <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>Analyse</span>
                <h3 className="font-display text-lg font-medium mt-2" style={{ color: INK }}>En attente de saisie</h3>
                <p className="font-sans text-sm mt-2 max-w-xs" style={{ color: INK_SOFT }}>
                  Complétez le bulletin pour calculer vos affinités parmi les 10 filières recommandées.
                </p>
              </div>
            )}

            {showBacQuestion && (
              <div
                className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border space-y-6"
                style={{ borderColor: ACCENT }}
              >
                <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: ACCENT }}>Vérification</span>
                <h3 className="font-display text-lg font-medium" style={{ color: INK }}>
                  Êtes-vous sûr que vous avez été admis(es) au bac ?
                </h3>
                <p className="font-sans text-sm max-w-xs" style={{ color: INK_SOFT }}>
                  Votre moyenne actuelle est de <span className="font-semibold" style={{ color: ACCENT }}>{moyenne}/20</span>.
                </p>
                <div className="flex gap-4 w-full max-w-xs pt-2">
                  <button
                    type="button"
                    onClick={() => fetchRecommendations()}
                    className="flex-1 py-3 px-4 rounded font-mono text-xs uppercase tracking-[0.1em] font-medium transition-colors"
                    style={{ backgroundColor: INK, color: PAPER }}
                  >
                    OUI
                  </button>
                  <button
                    type="button"
                    onClick={() => { setShowBacQuestion(false); setRejected(true); }}
                    className="flex-1 py-3 px-4 rounded font-mono text-xs uppercase tracking-[0.1em] font-medium border transition-colors"
                    style={{ borderColor: LINE, color: INK }}
                  >
                    NON
                  </button>
                </div>
              </div>
            )}

            {rejected && (
              <div className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border" style={{ borderColor: LINE }}>
                <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>Résultat</span>
                <h3 className="font-display text-xl font-medium mt-3" style={{ color: ACCENT }}>
                  Réessayez l'année prochaine, bon courage !
                </h3>
              </div>
            )}

            {loading && !results && (
              <div className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border" style={{ borderColor: LINE }}>
                <div className="w-10 h-10 rounded-full border-2 animate-spin" style={{ borderColor: LINE, borderTopColor: ACCENT }} />
                <p className="font-mono text-[10px] uppercase tracking-[0.15em] mt-4" style={{ color: INK_SOFT }}>
                  Calcul des affinités selon les conditions...
                </p>
              </div>
            )}

            {results && (
              <div className="bg-white rounded-lg p-6 border space-y-6" style={{ borderColor: LINE }}>
                <div className="pb-4 border-b" style={{ borderColor: LINE }}>
                  <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>
                    Top 3 · Recommandations de filières
                  </span>
                  <h2 className="font-display text-lg font-medium mt-1" style={{ color: INK }}>Recommandations</h2>
                </div>

                {isFlatProfile && (
                  <div className="p-3 rounded text-xs border" style={{ backgroundColor: '#FFFBEB', borderColor: '#F59E0B', color: '#B45309' }}>
                    <strong>Note :</strong> Profil uniforme (notes identiques sur toutes les matières). La prédiction du modèle est indicative, car aucun domaine de force spécifique n'émerge.
                  </div>
                )}

                <div className="space-y-4">
                  {results.map((rec, index) => {
                    const isTop1 = index === 0;
                    return (
                      <div
                        key={rec.rang || index}
                        className={`p-4 rounded-lg border relative transition-all duration-300 ${
                          isTop1 ? 'animate-top1' : 'hover:translate-x-1'
                        }`}
                        style={{
                          backgroundColor: isTop1 ? ACCENT_SOFT : '#FFFFFF',
                          borderColor: isTop1 ? ACCENT : LINE,
                          borderWidth: isTop1 ? '2px' : '1px'
                        }}
                      >
                        {isTop1 && (
                          <div className="absolute -top-3 right-4 bg-white border border-red-800 px-2.5 py-0.5 rounded-full flex items-center gap-1.5 shadow-sm z-10">
                            <span className="w-1.5 h-1.5 rounded-full animate-ping" style={{ backgroundColor: ACCENT }} />
                            <span className="font-mono text-[9px] uppercase tracking-[0.12em] font-semibold" style={{ color: ACCENT }}>
                              Meilleur Choix
                            </span>
                          </div>
                        )}

                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center gap-3">
                            <div
                              className="w-7 h-7 rounded-full flex items-center justify-center font-mono text-[11px] font-semibold shrink-0 transition-transform hover:scale-110"
                              style={
                                isTop1
                                  ? { backgroundColor: ACCENT, color: PAPER }
                                  : { border: `1px solid ${LINE}`, color: INK_SOFT }
                              }
                            >
                              {rec.rang || index + 1}
                            </div>
                            <h3 className={`font-sans font-medium text-sm ${isTop1 ? 'font-semibold text-base' : ''}`} style={{ color: INK }}>
                              {rec.filiere}
                            </h3>
                          </div>
                          <span
                            className={`font-mono font-semibold shrink-0 pl-2 ${isTop1 ? 'text-2xl' : 'text-lg'}`}
                            style={{ color: isTop1 ? ACCENT : INK }}
                          >
                            {rec.probabilite}%
                          </span>
                        </div>

                        <div className="w-full h-1.5 rounded-full overflow-hidden relative" style={{ backgroundColor: LINE }}>
                          <div
                            className={`h-full rounded-full transition-all duration-1000 ease-out relative overflow-hidden ${
                              isTop1 ? 'shine-effect' : ''
                            }`}
                            style={{ width: `${rec.probabilite}%`, backgroundColor: isTop1 ? ACCENT : INK_SOFT }}
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
      </main>
    </div>
  );
}