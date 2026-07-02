import React from 'react';
import { Link } from 'react-router-dom';
import { Book, Play, Edit2, Trash2 } from 'lucide-react';

interface DeckProps {
  deck: {
    id: string;
    title: string;
    description: string;
  };
  onEdit: (deck: any) => void;
  onDelete: (deckId: string) => void;
}

export const DeckCard: React.FC<DeckProps> = ({ deck, onEdit, onDelete }) => {
  return (
    <div className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', transition: 'transform 0.2s', cursor: 'pointer' }} 
         onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-4px)'}
         onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
      <div className="flex-between">
        <h3 style={{ fontSize: '1.25rem', color: 'var(--primary)' }}>{deck.title}</h3>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn" style={{ padding: '0.25rem', background: 'transparent', color: 'var(--text-muted)' }} onClick={() => onEdit(deck)}>
            <Edit2 size={16} />
          </button>
          <button className="btn" style={{ padding: '0.25rem', background: 'transparent', color: 'var(--accent)' }} onClick={() => onDelete(deck.id)}>
            <Trash2 size={16} />
          </button>
        </div>
      </div>
      <p style={{ color: 'var(--text-muted)', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical' }}>
        {deck.description}
      </p>
      <div className="flex-between" style={{ marginTop: '1rem' }}>
        <Link to={`/decks/${deck.id}`} className="btn btn-outline" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
          Manage Words
        </Link>
        <Link to={`/decks/${deck.id}/study`} className="btn btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
          <Play size={14} /> Study
        </Link>
      </div>
    </div>
  );
};
