import React, { useEffect, useState } from 'react';
import { deckAPI } from '../api/deck';
import { DeckCard } from '../components/DeckCard';
import { Plus } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [decks, setDecks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  
  // Edit & Delete State
  const [editingDeck, setEditingDeck] = useState<any>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDesc, setEditDesc] = useState('');

  const fetchDecks = async () => {
    setLoading(true);
    try {
      const data = await deckAPI.getDecks();
      setDecks(data);
    } catch (error) {
      console.error("Failed to fetch decks", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchDecks();
  }, []);

  const handleCreateDeck = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await deckAPI.createDeck({ title: newTitle, description: newDesc });
      setShowModal(false);
      setNewTitle('');
      setNewDesc('');
      fetchDecks();
    } catch (error) {
      console.error("Failed to create deck", error);
    }
  };

  const handleEditClick = (deck: any) => {
    setEditingDeck(deck);
    setEditTitle(deck.title);
    setEditDesc(deck.description);
    setShowEditModal(true);
  };

  const handleUpdateDeck = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingDeck) return;
    try {
      await deckAPI.updateDeck(editingDeck.id, { title: editTitle, description: editDesc });
      setShowEditModal(false);
      fetchDecks();
    } catch (error) {
      console.error("Failed to update deck", error);
    }
  };

  const handleDeleteDeck = async (id: string) => {
    if (window.confirm("Are you sure you want to delete this deck? All words in it will be removed from the deck.")) {
      try {
        await deckAPI.deleteDeck(id);
        fetchDecks();
      } catch (error) {
        console.error("Failed to delete deck", error);
      }
    }
  };

  if (loading) {
    return <div className="container flex-center" style={{ minHeight: '60vh' }}>Loading decks...</div>;
  }

  return (
    <div className="container" style={{ padding: '2rem 1.5rem' }}>
      <div className="flex-between" style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem' }}>Your Decks</h1>
        <button className="btn btn-primary" style={{ marginLeft: '6rem' }} onClick={() => setShowModal(true)}>
          <Plus size={18} /> New Deck
        </button>
      </div>

      {decks.length === 0 ? (
        <div className="glass-panel flex-center" style={{ minHeight: '300px', flexDirection: 'column', gap: '1rem' }}>
          <h2 style={{ color: 'var(--text-muted)' }}>No decks found.</h2>
          <p>Create your first deck to start learning!</p>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>Create Deck</button>
        </div>
      ) : (
        <div className="grid-cards">
          {decks.map(deck => (
            <DeckCard 
              key={deck.id} 
              deck={deck} 
              onEdit={handleEditClick} 
              onDelete={handleDeleteDeck} 
            />
          ))}
        </div>
      )}

      {showModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 50 }} className="flex-center">
          <div className="glass-panel" style={{ width: '100%', maxWidth: '500px' }}>
            <h2 style={{ marginBottom: '1.5rem' }}>Create New Deck</h2>
            <form onSubmit={handleCreateDeck}>
              <div className="input-group">
                <label className="input-label">Title</label>
                <input type="text" className="input-field" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} required />
              </div>
              <div className="input-group">
                <label className="input-label">Description</label>
                <textarea className="input-field" rows={3} value={newDesc} onChange={(e) => setNewDesc(e.target.value)} required />
              </div>
              <div className="flex-between" style={{ marginTop: '2rem' }}>
                <button type="button" className="btn btn-outline" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showEditModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 50 }} className="flex-center">
          <div className="glass-panel" style={{ width: '100%', maxWidth: '500px' }}>
            <h2 style={{ marginBottom: '1.5rem' }}>Edit Deck</h2>
            <form onSubmit={handleUpdateDeck}>
              <div className="input-group">
                <label className="input-label">Title</label>
                <input type="text" className="input-field" value={editTitle} onChange={(e) => setEditTitle(e.target.value)} required />
              </div>
              <div className="input-group">
                <label className="input-label">Description</label>
                <textarea className="input-field" rows={3} value={editDesc} onChange={(e) => setEditDesc(e.target.value)} required />
              </div>
              <div className="flex-between" style={{ marginTop: '2rem' }}>
                <button type="button" className="btn btn-outline" onClick={() => setShowEditModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Update</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
