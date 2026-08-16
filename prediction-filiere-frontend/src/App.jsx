import React, { useState } from 'react';
import axios from 'axios';

const MATIERES = [
  { id: 'mathematiques', label: 'Mathématiques' },
  { id: 'physique', label: 'Physique' },
  { id: 'chimie', label: 'Chimie' },
  { id: 'science_de_la_vie_et_de_la_terre', label: 'SVT' },
  { id: 'informatique', label: 'Informatique' },
  { id: 'statistiques_et_probabilites', label: 'Statistiques & Probabilités' },
  { id: 'biologie_appliquee_et_biotechnologie', label: 'Biologie Appliquée' },
  { id: 'francais', label: 'Français' },
  { id: 'anglais', label: 'Anglais' },
  { id: 'philosophie', label: 'Philosophie' },
  { id: 'histoire_et_geographie', label: 'Histoire - Géographie' },
  { id: 'economie_generale', label: 'Économie Générale' },
  { id: 'test_psychotechnique', label: 'Test Psychotechnique' },
  { id: 'dessin_technique_et_arts_appliques', label: 'Dessin Technique & Arts' },
  { id: 'education_physique_et_sportive', label: 'EPS' }
];

const DEFAULT_NOTES = MATIERES.reduce((acc, m) => ({ ...acc, [m.id]: 10 }), {});

const INK = '#1E2A3A';
const INK_SOFT = '#55606B';
const PAPER = '#FFFFFF';
const LINE = '#D9DCD2';
const ACCENT = '#9C3B2E';
const ACCENT_SOFT = '#F3E5E1';

export default function App() {
  const [notes, setNotes] = useState(DEFAULT_NOTES);
  const [serie, setSerie] = useState('scientifique');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showBacQuestion, setShowBacQuestion] = useState(false);
  const [rejected, setRejected] = useState(false);

  const handleInputChange = (id, value) => {
    const val = parseFloat(value);
    setNotes(prev => ({
      ...prev,
      [id]: isNaN(val) ? '' : Math.min(20, Math.max(0, val))
    }));
  };

  const handleReset = () => {
    setNotes(DEFAULT_NOTES);
    setSerie('scientifique');
    setResults(null);
    setError(null);
    setShowBacQuestion(false);
    setRejected(false);
  };

  const values = Object.values(notes).filter(v => typeof v === 'number');
  const moyNum = values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0;
  const moyenne = values.length ? moyNum.toFixed(2) : '0.00';

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    setShowBacQuestion(false);
    setRejected(false);

    const payload = { ...notes, serie };

    try {
      const response = await axios.post('http://localhost:8000/predict', payload);
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
      <header className="sticky top-0 z-50 border-b" style={{ backgroundColor: PAPER, borderColor: LINE }}>
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="font-display text-2xl font-medium tracking-tight" style={{ color: INK }}>
              Prédiktor Cursus
            </h1>
            <p className="font-mono text-[10px] uppercase tracking-[0.15em] mt-1" style={{ color: INK_SOFT }}>
              Système d'orientation · Données Réelles
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
                  <p className="font-sans text-sm mt-1" style={{ color: INK_SOFT }}>Sélectionnez votre série et saisissez vos notes sur 20.</p>
                </div>
                <button
                  type="button"
                  onClick={handleReset}
                  className="font-mono text-[10px] uppercase tracking-[0.1em] px-3 py-2 rounded border transition-colors"
                  style={{ borderColor: LINE, color: INK_SOFT }}
                >
                  Réinitialiser
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Nouveau sélecteur de série : deux boutons */}
                <div className="flex flex-col pb-4 border-b" style={{ borderColor: LINE }}>
                  <span className="font-sans text-sm font-semibold mb-2" style={{ color: INK }}>
                    Série du Baccalauréat
                  </span>
                  <div className="flex space-x-2">
                    <button
                      type="button"
                      onClick={() => setSerie('scientifique')}
                      className={`flex-1 py-2 px-4 border rounded font-mono text-xs uppercase tracking-[0.1em] transition-colors ${
                        serie === 'scientifique'
                          ? 'bg-[#1E2A3A] text-white border-[#1E2A3A]'
                          : 'bg-white text-[#1E2A3A] border-[#D9DCD2]'
                      }`}
                    >
                      Scientifique
                    </button>
                    <button
                      type="button"
                      onClick={() => setSerie('litteraire')}
                      className={`flex-1 py-2 px-4 border rounded font-mono text-xs uppercase tracking-[0.1em] transition-colors ${
                        serie === 'litteraire'
                          ? 'bg-[#1E2A3A] text-white border-[#1E2A3A]'
                          : 'bg-white text-[#1E2A3A] border-[#D9DCD2]'
                      }`}
                    >
                      Littéraire
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                  {MATIERES.map(m => (
                    <div
                      key={m.id}
                      className="flex items-baseline justify-between py-2.5 border-b"
                      style={{ borderColor: LINE, borderBottomStyle: 'dotted' }}
                    >
                      <label htmlFor={m.id} className="font-sans text-sm pr-3" style={{ color: INK }}>
                        {m.label}
                      </label>
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
                        required
                      />
                    </div>
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-4 px-6 rounded font-mono text-xs uppercase tracking-[0.15em] font-medium transition-colors disabled:opacity-50 text-center"
                  style={{ backgroundColor: loading ? INK_SOFT : INK, color: PAPER }}
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
              <div className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border border-dashed" style={{ borderColor: LINE }}>
                <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>Analyse</span>
                <h3 className="font-display text-lg font-medium mt-2" style={{ color: INK }}>En attente de saisie</h3>
                <p className="font-sans text-sm mt-2 max-w-xs" style={{ color: INK_SOFT }}>
                  Renseignez vos notes réelles et votre série pour calculer vos affinités.
                </p>
              </div>
            )}

            {showBacQuestion && (
              <div className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border space-y-6" style={{ borderColor: ACCENT }}>
                <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: ACCENT }}>Vérification</span>
                <h3 className="font-display text-lg font-medium" style={{ color: INK }}>Vous êtes sûr que vous avez été admis(e) au bac ?</h3>
                <p className="font-sans text-sm max-w-xs" style={{ color: INK_SOFT }}>
                  Votre moyenne actuelle est de <span className="font-semibold" style={{ color: ACCENT }}>{moyenne}/20</span>.
                </p>
                <div className="flex gap-4 w-full max-w-xs pt-2">
                  <button type="button" onClick={() => fetchRecommendations()} className="flex-1 py-3 px-4 rounded font-mono text-xs uppercase tracking-[0.1em] font-medium transition-colors" style={{ backgroundColor: INK, color: PAPER }}>
                    OUI
                  </button>
                  <button type="button" onClick={() => { setShowBacQuestion(false); setRejected(true); }} className="flex-1 py-3 px-4 rounded font-mono text-xs uppercase tracking-[0.1em] font-medium border transition-colors" style={{ borderColor: LINE, color: INK }}>
                    NON
                  </button>
                </div>
              </div>
            )}

            {rejected && (
              <div className="bg-white rounded-lg p-8 text-center flex flex-col items-center justify-center min-h-[420px] border" style={{ borderColor: LINE }}>
                <h3 className="font-display text-xl font-medium mt-3" style={{ color: ACCENT }}>
                  Réessayez l'année prochaine, bon courage !
                </h3>
              </div>
            )}

            {results && (
              <div className="bg-white rounded-lg p-6 border space-y-6" style={{ borderColor: LINE }}>
                <div className="pb-4 border-b" style={{ borderColor: LINE }}>
                  <span className="font-mono text-[10px] uppercase tracking-[0.15em]" style={{ color: INK_SOFT }}>
                    Top 3 Recommandations
                  </span>
                  <h2 className="font-display text-lg font-medium mt-1" style={{ color: INK }}>Filières suggérées</h2>
                </div>

                <div className="space-y-4">
                  {results.map((rec, index) => {
                    const isTop1 = index === 0;
                    return (
                      <div key={rec.rang} className="p-4 rounded-lg border" style={{ backgroundColor: isTop1 ? ACCENT_SOFT : '#FFFFFF', borderColor: isTop1 ? ACCENT : LINE }}>
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center gap-3">
                            <div className="w-7 h-7 rounded-full flex items-center justify-center font-mono text-[11px] font-semibold shrink-0" style={isTop1 ? { border: `2px solid ${ACCENT}`, color: ACCENT } : { border: `1px solid ${LINE}`, color: INK_SOFT }}>
                              {rec.rang}
                            </div>
                            <h3 className="font-sans font-medium text-sm" style={{ color: INK }}>
                              {rec.filiere}
                            </h3>
                          </div>
                          <span className="font-mono text-lg font-semibold shrink-0 pl-2" style={{ color: isTop1 ? ACCENT : INK }}>
                            {rec.probabilite}%
                          </span>
                        </div>
                        <div className="w-full h-1 rounded-full overflow-hidden" style={{ backgroundColor: LINE }}>
                          <div className="h-full rounded-full" style={{ width: `${rec.probabilite}%`, backgroundColor: isTop1 ? ACCENT : INK_SOFT }} />
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