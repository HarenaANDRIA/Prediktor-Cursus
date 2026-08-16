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

export default function App() {
  const [notes, setNotes] = useState(DEFAULT_NOTES);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/predict', notes);
      setResults(response.data.recommandations);
    } catch (err) {
      setError("Impossible de contacter le serveur d'IA (http://localhost:8000).");
    } finally {
      setLoading(false);
    }
  };

  const values = Object.values(notes).filter(v => typeof v === 'number');
  const moyenne = values.length ? (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2) : 0;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans pb-12">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Prédiktor Cursus AI</h1>
            <p className="text-xs text-slate-500">Système d'Orientation Universitaire (15 Matières)</p>
          </div>
          <div className="bg-slate-100 border border-slate-200 px-4 py-2 rounded-lg">
            <span className="text-xs text-slate-500">Moyenne globale : </span>
            <span className="text-sm font-semibold text-slate-900">{moyenne} / 20</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 pt-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <section className="lg:col-span-7 space-y-6">
            <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-100">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">Notes par Matière</h2>
                  <p className="text-sm text-slate-500 mt-1">Saisissez les notes obtenues sur 20.</p>
                </div>
                <button
                  type="button"
                  onClick={handleReset}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 border border-slate-200 rounded-lg transition-colors font-medium"
                >
                  Réinitialiser
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {MATIERES.map(m => (
                    <div key={m.id} className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                      <div className="flex items-center justify-between mb-1.5">
                        <label htmlFor={m.id} className="text-xs font-medium text-slate-700 truncate pr-2">
                          {m.label}
                        </label>
                        <span className="text-[10px] text-slate-400 font-mono">/20</span>
                      </div>
                      <input
                        id={m.id}
                        type="number"
                        min="0"
                        max="20"
                        step="0.25"
                        value={notes[m.id]}
                        onChange={e => handleInputChange(m.id, e.target.value)}
                        className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 text-sm font-semibold focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
                        required
                      />
                    </div>
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3.5 px-6 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg shadow-sm disabled:opacity-50 transition-colors text-center"
                >
                  {loading ? "Analyse en cours..." : "Générer mes Recommandations IA"}
                </button>
              </form>
            </div>
          </section>

          <section className="lg:col-span-5 space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 text-sm">
                {error}
              </div>
            )}

            {!results && !loading && !error && (
              <div className="bg-white border border-slate-200 rounded-xl p-8 text-center flex flex-col items-center justify-center min-h-[380px] shadow-sm">
                <h3 className="text-base font-medium text-slate-800">En attente d'analyse</h3>
                <p className="text-sm text-slate-500 mt-2 max-w-xs">
                  Saisissez vos notes pour calculer les affinités parmi les 25 filières universitaires.
                </p>
              </div>
            )}

            {results && (
              <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-6">
                <div className="pb-4 border-b border-slate-100">
                  <h2 className="text-lg font-semibold text-slate-900">Top 3 Recommandations</h2>
                  <p className="text-xs text-slate-500 mt-1">Classé parmi 25 filières potentielles</p>
                </div>

                <div className="space-y-4">
                  {results.map((rec, index) => {
                    const isTop1 = index === 0;
                    return (
                      <div 
                        key={rec.rang}
                        className={`p-4 rounded-lg border ${
                          isTop1 ? "bg-slate-50 border-blue-600" : "bg-white border-slate-200"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-3">
                            <span className="px-2 py-0.5 text-xs font-semibold text-slate-700 bg-slate-200 rounded">
                              #{rec.rang}
                            </span>
                            <h3 className="font-medium text-slate-900 text-sm">
                              {rec.filiere}
                            </h3>
                          </div>
                          <span className="text-sm font-semibold text-blue-600 font-mono">
                            {rec.probabilite}%
                          </span>
                        </div>

                        <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden mt-3">
                          <div 
                            className={`h-full ${isTop1 ? "bg-blue-600" : "bg-slate-600"}`}
                            style={{ width: `${rec.probabilite}%` }}
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