import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { deckAPI } from '../api/deck';
import { Flashcard } from '../components/Flashcard';
import { ArrowLeft, ArrowRight, X } from 'lucide-react';

export const Study: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [deck, setDeck] = useState<any>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDeck = async () => {
      if (!id) return;
      setLoading(true);
      try {
        const data = await deckAPI.getDeck(id);
        setDeck(data);
      } catch (error) {
        console.error("Failed to fetch deck for study", error);
      }
      setLoading(false);
    };
    fetchDeck();
  }, [id]);

  if (loading) return <div className="container flex-center" style={{ minHeight: '60vh' }}>Loading...</div>;
  if (!deck) return <div className="container flex-center" style={{ minHeight: '60vh' }}>Deck not found</div>;
  
  if (deck.words.length === 0) {
    return (
      <div className="container flex-center" style={{ minHeight: '60vh', flexDirection: 'column', gap: '2rem' }}>
        <h2>No words in this deck.</h2>
        <Link to={`/decks/${id}`} className="btn btn-primary">Go add some words</Link>
      </div>
    );
  }

  const nextCard = () => {
    if (currentIndex < deck.words.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const prevCard = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const progress = ((currentIndex + 1) / deck.words.length) * 100;

  return (
    <div className="container flex-center" style={{ minHeight: '80vh', flexDirection: 'column' }}>
      <div style={{ width: '100%', maxWidth: '600px', marginBottom: '2rem' }}>
        <div className="flex-between" style={{ marginBottom: '1rem' }}>
          <h2 style={{ fontSize: '1.25rem', color: 'var(--text-muted)' }}>{deck.title}</h2>
          <Link to="/" className="btn btn-outline" style={{ padding: '0.4rem 0.8rem' }}>
            <X size={16} /> Exit
          </Link>
        </div>
        
        {/* Progress Bar */}
        <div style={{ width: '100%', height: '6px', background: 'var(--surface)', borderRadius: '3px', overflow: 'hidden' }}>
          <div style={{ height: '100%', width: `${progress}%`, background: 'var(--primary-gradient)', transition: 'width 0.3s ease' }}></div>
        </div>
        <div style={{ textAlign: 'center', marginTop: '0.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          {currentIndex + 1} / {deck.words.length}
        </div>
      </div>

      <Flashcard key={deck.words[currentIndex].id} word={deck.words[currentIndex]} />

      <div className="flex-center" style={{ gap: '2rem', marginTop: '3rem' }}>
        <button 
          className="btn btn-outline" 
          onClick={prevCard} 
          disabled={currentIndex === 0}
          style={{ width: '120px', opacity: currentIndex === 0 ? 0.5 : 1 }}
        >
          <ArrowLeft size={18} /> Prev
        </button>
        <button 
          className="btn btn-primary" 
          onClick={nextCard} 
          disabled={currentIndex === deck.words.length - 1}
          style={{ width: '120px', opacity: currentIndex === deck.words.length - 1 ? 0.5 : 1 }}
        >
          Next <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
};
