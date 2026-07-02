import React, { useState } from 'react';
import './Flashcard.css';

interface Word {
  id: string;
  kanji?: string;
  yomikata: string;
  meaning: string;
  jlpt_level: string;
}

interface FlashcardProps {
  word: Word;
}

export const Flashcard: React.FC<FlashcardProps> = ({ word }) => {
  const [flipped, setFlipped] = useState(false);

  return (
    <div className={`flashcard-container ${flipped ? 'flipped' : ''}`} onClick={() => setFlipped(!flipped)}>
      <div className="flashcard">
        {/* Front */}
        <div className="flashcard-face flashcard-front">
          <div className="jlpt-badge">{word.jlpt_level}</div>
          <div className="main-text">
            {word.kanji || word.yomikata}
          </div>
          {word.kanji && <div className="sub-text">Click to reveal reading and meaning</div>}
          {!word.kanji && <div className="sub-text">Click to reveal meaning</div>}
        </div>
        
        {/* Back */}
        <div className="flashcard-face flashcard-back">
          <div className="jlpt-badge">{word.jlpt_level}</div>
          {word.kanji && (
            <div className="reading-text">{word.yomikata}</div>
          )}
          <div className="meaning-text">{word.meaning}</div>
        </div>
      </div>
    </div>
  );
};
