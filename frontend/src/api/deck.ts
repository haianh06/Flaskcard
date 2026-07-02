import { api } from './axios';

export const deckAPI = {
  getDecks: async () => {
    const response = await api.get('/decks/');
    return response.data;
  },
  
  getDeck: async (id: string) => {
    const response = await api.get(`/decks/${id}`);
    return response.data;
  },
  
  createDeck: async (deckData: { title: string; description: string }) => {
    const response = await api.post('/decks/', deckData);
    return response.data;
  },
  
  updateDeck: async (id: string, deckData: { title?: string; description?: string }) => {
    const response = await api.put(`/decks/${id}`, deckData);
    return response.data;
  },
  
  deleteDeck: async (id: string) => {
    const response = await api.delete(`/decks/${id}`);
    return response.data;
  },

  addWordToDeck: async (deckId: string, wordId: string) => {
    const response = await api.post(`/decks/${deckId}/words/${wordId}`);
    return response.data;
  },

  removeWordFromDeck: async (deckId: string, wordId: string) => {
    const response = await api.delete(`/decks/${deckId}/words/${wordId}`);
    return response.data;
  }
};
