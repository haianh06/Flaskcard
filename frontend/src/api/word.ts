import { api } from './axios';

export const wordAPI = {
  getWords: async (page: number = 1, limit: number = 50, search: string = "") => {
    const offset = (page - 1) * limit;
    const response = await api.get('/words/', { params: { offset, limit, search } });
    return response.data;
  },

  getWord: async (id: string) => {
    const response = await api.get(`/words/${id}`);
    return response.data;
  },
  
  createWord: async (wordData: { kanji?: string; yomikata: string; meaning: string; jlpt_level: string }) => {
    const response = await api.post('/words/', wordData);
    return response.data;
  },
  
  updateWord: async (id: string, wordData: any) => {
    const response = await api.put(`/words/${id}`, wordData);
    return response.data;
  },
  
  deleteWord: async (id: string) => {
    const response = await api.delete(`/words/${id}`);
    return response.data;
  }
};
