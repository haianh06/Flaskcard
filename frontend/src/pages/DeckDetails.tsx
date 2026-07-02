import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { deckAPI } from '../api/deck';
import { wordAPI } from '../api/word';
import { ArrowLeft, Plus, Trash2 } from 'lucide-react';

export const DeckDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [deck, setDeck] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  // Word Modal State (Create New)
  const [showModal, setShowModal] = useState(false);
  const [kanji, setKanji] = useState('');
  const [yomikata, setYomikata] = useState('');
  const [meaning, setMeaning] = useState('');
  const [jlptLevel, setJlptLevel] = useState('N5');

  // Dictionary Pick State
  const [showDictModal, setShowDictModal] = useState(false);
  const [allWords, setAllWords] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchDeck = async () => {
    if (!id) return;
    setLoading(true);
    try {
      const data = await deckAPI.getDeck(id);
      setDeck(data);
    } catch (error) {
      console.error("Failed to fetch deck details", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchDeck();
    fetchDictionary();
  }, [id]);

  const fetchDictionary = async () => {
    try {
      const data = await wordAPI.getWords();
      setAllWords(data);
    } catch (error) {
      console.error("Failed to fetch dictionary", error);
    }
  };

  const handleAddWord = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    
    try {
      // 1. Create word
      const newWord = await wordAPI.createWord({
        kanji: kanji || undefined,
        yomikata,
        meaning,
        jlpt_level: jlptLevel
      });
      // 2. Add word to deck
      await deckAPI.addWordToDeck(id, newWord.id);
      
      // Cleanup and refresh
      setShowModal(false);
      setKanji(''); setYomikata(''); setMeaning(''); setJlptLevel('N5');
      fetchDeck();
    } catch (error) {
      console.error("Failed to add word", error);
    }
  };

  const handleRemoveWord = async (wordId: string) => {
    if (!id) return;
    try {
      await deckAPI.removeWordFromDeck(id, wordId);
      fetchDeck();
    } catch (error) {
      console.error("Failed to remove word", error);
    }
  };

  const handlePickWord = async (wordId: string) => {
    if (!id) return;
    try {
      await deckAPI.addWordToDeck(id, wordId);
      setShowDictModal(false);
      fetchDeck();
    } catch (error) {
      console.error("Failed to pick word", error);
    }
  };

  if (loading) return <div className="container flex-center" style={{ minHeight: '60vh' }}>Loading...</div>;
  if (!deck) return <div className="container flex-center" style={{ minHeight: '60vh' }}>Deck not found</div>;

  return (
    <div className="container" style={{ padding: '2rem 1.5rem' }}>
      <Link to="/" className="btn btn-outline" style={{ display: 'inline-flex', marginBottom: '2rem' }}>
        <ArrowLeft size={18} /> Back to Dashboard
      </Link>
      
      <div className="flex-between" style={{ marginBottom: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', color: 'var(--primary)' }}>{deck.title}</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', marginTop: '0.5rem' }}>{deck.description}</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-outline" onClick={() => setShowDictModal(true)}>
            Browse Dictionary
          </button>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <Plus size={18} /> Add New Word
          </button>
        </div>
      </div>
      
      <div style={{ marginTop: '3rem' }}>
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>Words ({deck.words.length})</h2>
        {deck.words.length === 0 ? (
          <div className="glass flex-center" style={{ padding: '3rem', color: 'var(--text-muted)' }}>
            This deck is empty. Add some words to start studying!
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {deck.words.map((word: any) => (
              <div key={word.id} className="glass flex-between" style={{ padding: '1rem 1.5rem' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '1rem' }}>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{word.kanji || word.yomikata}</span>
                    {word.kanji && <span style={{ color: 'var(--text-muted)' }}>{word.yomikata}</span>}
                    <span style={{ fontSize: '0.8rem', background: 'var(--primary-hover)', color: '#000', padding: '0.1rem 0.5rem', borderRadius: '4px', fontWeight: 'bold' }}>
                      {word.jlpt_level}
                    </span>
                  </div>
                  <div style={{ color: 'var(--text-main)', marginTop: '0.25rem' }}>{word.meaning}</div>
                </div>
                <button className="btn btn-outline" style={{ padding: '0.5rem', borderColor: 'var(--accent)', color: 'var(--accent)' }} onClick={() => handleRemoveWord(word.id)}>
                  <Trash2 size={18} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 50 }} className="flex-center">
          <div className="glass-panel" style={{ width: '100%', maxWidth: '500px' }}>
            <h2 style={{ marginBottom: '1.5rem' }}>Add New Word</h2>
            <form onSubmit={handleAddWord}>
              <div className="input-group">
                <label className="input-label">Kanji (Optional)</label>
                <input type="text" className="input-field" value={kanji} onChange={(e) => setKanji(e.target.value)} />
              </div>
              <div className="input-group">
                <label className="input-label">Yomikata (Reading)</label>
                <input type="text" className="input-field" value={yomikata} onChange={(e) => setYomikata(e.target.value)} required />
              </div>
              <div className="input-group">
                <label className="input-label">Meaning</label>
                <input type="text" className="input-field" value={meaning} onChange={(e) => setMeaning(e.target.value)} required />
              </div>
              <div className="input-group">
                <label className="input-label">JLPT Level</label>
                <select className="input-field" value={jlptLevel} onChange={(e) => setJlptLevel(e.target.value)}>
                  <option value="N5">N5</option>
                  <option value="N4">N4</option>
                  <option value="N3">N3</option>
                  <option value="N2">N2</option>
                  <option value="N1">N1</option>
                </select>
              </div>
              <div className="flex-between" style={{ marginTop: '2rem' }}>
                <button type="button" className="btn btn-outline" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Add Word</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Pick from Dictionary Modal */}
      {showDictModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 50, padding: '2rem' }} className="flex-center">
          <div className="glass-panel" style={{ width: '100%', maxWidth: '700px', maxHeight: '80vh', display: 'flex', flexDirection: 'column' }}>
            <div className="flex-between" style={{ marginBottom: '1.5rem' }}>
              <h2>Pick from Dictionary</h2>
              <button className="btn btn-outline" onClick={() => setShowDictModal(false)}>Close</button>
            </div>
            <input 
              type="text" 
              className="input-field" 
              placeholder="Search words..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ marginBottom: '1rem' }}
            />
            <div style={{ overflowY: 'auto', flex: 1, paddingRight: '0.5rem' }}>
              {allWords
                .filter(w => 
                  (w.kanji && w.kanji.toLowerCase().includes(searchTerm.toLowerCase())) ||
                  w.yomikata.toLowerCase().includes(searchTerm.toLowerCase()) ||
                  w.meaning.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .filter(w => !deck.words.some((dw: any) => dw.id === w.id)) // Hide words already in deck
                .slice(0, 50) // Show only 50 results to prevent lag
                .map(word => (
                  <div key={word.id} className="flex-between" style={{ padding: '0.75rem', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                    <div>
                      <strong>{word.kanji || word.yomikata}</strong> <span style={{ color: 'var(--text-muted)' }}>{word.meaning}</span>
                    </div>
                    <button className="btn btn-primary" style={{ padding: '0.25rem 0.75rem' }} onClick={() => handlePickWord(word.id)}>
                      Add
                    </button>
                  </div>
                ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
