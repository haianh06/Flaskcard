import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { authAPI } from '../api/auth';

export const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setLoading(true);
    try {
      const data = await authAPI.forgotPassword(email);
      setMessage(data.detail || 'If the email exists, a reset link has been sent.');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process request.');
    }
    setLoading(false);
  };

  return (
    <div className="container flex-center" style={{ minHeight: '80vh' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '1rem', fontSize: '2rem' }}>Reset Password</h2>
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', marginBottom: '2rem' }}>
          Enter your email address and we'll send you a link to reset your password.
        </p>
        
        {error && <div style={{ color: 'var(--accent)', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        {message && <div style={{ color: 'var(--primary)', marginBottom: '1rem', textAlign: 'center' }}>{message}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label className="input-label">Email</label>
            <input 
              type="email" 
              className="input-field" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              placeholder="you@example.com" 
              required 
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }} disabled={loading}>
            {loading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-muted)' }}>
          Remember your password? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};
