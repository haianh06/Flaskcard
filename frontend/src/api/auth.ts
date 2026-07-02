import { api } from './axios';

export const authAPI = {
  login: async (email: string, password: string) => {
    // OAuth2PasswordRequestForm expects form-data
    const formData = new URLSearchParams();
    formData.append('username', email); // backend uses username field for email in OAuth2PasswordRequestForm
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
  
  register: async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  forgotPassword: async (email: string) => {
    const response = await api.post('/auth/forgot-password', { email });
    return response.data;
  },

  resetPassword: async (reset_token: string, new_password: string) => {
    const response = await api.post('/auth/reset-password', { reset_token, new_password });
    return response.data;
  }
};
