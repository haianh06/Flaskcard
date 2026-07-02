import React, { useEffect, useState } from 'react';
import { wordAPI } from '../api/word';
import { Edit2, Trash2, Search, Plus } from 'lucide-react';

export const Dictionary: React.FC = () => {
  const [words, setWords] = useState<any[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  
  // Pagination
  const [page, setPage] = useState(1);
  const [limit] = useState(50); // Show 50 words per page
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');

  // Modals
  const [showModal, setShowModal] = useState(false);
  const [editingWord, setEditingWord] = useState<any>(null);
  
  const [kanji, setKanji] = useState('');
  const [yomikata, setYomikata] = useState('');
  const [meaning, setMeaning] = useState('');
  const [jlptLevel, setJlptLevel] = useState('N5');

  // Debounce search term
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchTerm);
      setPage(1); // Reset page when search changes
    }, 300);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const fetchWords = async () => {
    setLoading(true);
    try {
      const data = await wordAPI.getWords(page, limit, debouncedSearch);
      setWords(data.items || []);
      setTotalCount(data.total || 0);
    } catch (error) {
      console.error("Failed to fetch words", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchWords();
  }, [page, debouncedSearch]);

  const handleOpenModal = (word?: any) => {
    if (word) {
      setEditingWord(word);
      setKanji(word.kanji || '');
      setYomikata(word.yomikata || '');
      setMeaning(word.meaning || '');
      setJlptLevel(word.jlpt_level || 'N5');
    } else {
      setEditingWord(null);
      setKanji('');
      setYomikata('');
      setMeaning('');
      setJlptLevel('N5');
    }
    setShowModal(true);
  };

  const handleSaveWord = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      kanji: kanji || undefined,
      yomikata,
      meaning,
      jlpt_level: jlptLevel
    };

    try {
      if (editingWord) {
        await wordAPI.updateWord(editingWord.id, payload);
      } else {
        await wordAPI.createWord(payload);
      }
      setShowModal(false);
      fetchWords();
    } catch (error) {
      console.error("Failed to save word", error);
    }
  };

  const handleDeleteWord = async (id: string) => {
    if (window.confirm("Are you sure you want to delete this word permanently?")) {
      try {
        await wordAPI.deleteWord(id);
        fetchWords();
      } catch (error) {
        console.error("Failed to delete word", error);
      }
    }
  };

  const totalPages = Math.ceil(totalCount / limit);

  return (
    <div className="container" style={{ padding: '2rem 1.5rem' }}>
      <div className="flex-between" style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem' }}>Dictionary <span style={{fontSize: '1rem', color: 'var(--text-muted)'}}>({totalCount.toLocaleString()} words)</span></h1>
        <button className="btn btn-primary" onClick={() => handleOpenModal()}>
          <Plus size={18} /> New Word
        </button>
      </div>

      <div className="input-group" style={{ marginBottom: '2rem', position: 'relative' }}>
        <Search size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
        <input 
          type="text" 
          className="input-field" 
          placeholder="Search by kanji, reading, or meaning (server-side)..." 
          style={{ paddingLeft: '3rem' }}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {loading && words.length === 0 ? (
        <div className="flex-center" style={{ minHeight: '30vh' }}>Loading dictionary...</div>
      ) : (
        <>
          <div className="glass-panel" style={{ padding: 0, overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: 'rgba(255,255,255,0.05)', textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                  <th style={{ padding: '1rem 1.5rem' }}>Kanji</th>
                  <th style={{ padding: '1rem 1.5rem' }}>Reading</th>
                  <th style={{ padding: '1rem 1.5rem' }}>Meaning</th>
                  <th style={{ padding: '1rem 1.5rem' }}>JLPT</th>
                  <th style={{ padding: '1rem 1.5rem', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody style={{ opacity: loading ? 0.5 : 1, transition: 'opacity 0.2s' }}>
                {words.map(word => (
                  <tr key={word.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '1rem 1.5rem', fontSize: '1.25rem', fontWeight: 'bold' }}>{word.kanji || '-'}</td>
                    <td style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)' }}>{word.yomikata}</td>
                    <td style={{ padding: '1rem 1.5rem' }}>{word.meaning}</td>
                    <td style={{ padding: '1rem 1.5rem' }}>
                      <span style={{ fontSize: '0.8rem', background: 'var(--primary)', color: 'white', padding: '0.2rem 0.6rem', borderRadius: '4px', fontWeight: 'bold' }}>
                        {word.jlpt_level}
                      </span>
                    </td>
                    <td style={{ padding: '1rem 1.5rem', textAlign: 'right' }}>
                      <button className="btn" style={{ padding: '0.25rem', background: 'transparent', color: 'var(--text-muted)' }} onClick={() => handleOpenModal(word)}>
                        <Edit2 size={16} />
                      </button>
                      <button className="btn" style={{ padding: '0.25rem', background: 'transparent', color: 'var(--accent)' }} onClick={() => handleDeleteWord(word.id)}>
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {words.length === 0 && (
              <div className="flex-center" style={{ padding: '3rem', color: 'var(--text-muted)' }}>No words found.</div>
            )}
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex-center" style={{ marginTop: '2rem', gap: '1rem' }}>
              <button 
                className="btn btn-outline" 
                disabled={page === 1} 
                onClick={() => setPage(p => p - 1)}
              >
                Previous
              </button>
              <span style={{ color: 'var(--text-muted)' }}>Page {page} of {totalPages.toLocaleString()}</span>
              <button 
                className="btn btn-outline" 
                disabled={page === totalPages} 
                onClick={() => setPage(p => p + 1)}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

      {showModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 50 }} className="flex-center">
          <div className="glass-panel" style={{ width: '100%', maxWidth: '500px' }}>
            <h2 style={{ marginBottom: '1.5rem' }}>{editingWord ? 'Edit Word' : 'Create New Word'}</h2>
            <form onSubmit={handleSaveWord}>
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
                <button type="submit" className="btn btn-primary">{editingWord ? 'Update' : 'Create'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
