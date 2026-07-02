import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { authAPI } from '../api/auth';

export const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      setError('Invalid or missing reset token.');
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!token) return;

    try {
      await authAPI.resetPassword(token, password);
      setMessage('Password updated successfully! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reset password.');
    }
  };

  return (
    <div className="container flex-center" style={{ minHeight: '80vh' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '2rem' }}>Set New Password</h2>
        
        {error && <div style={{ color: 'var(--accent)', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        {message && <div style={{ color: 'var(--primary)', marginBottom: '1rem', textAlign: 'center' }}>{message}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label className="input-label">New Password</label>
            <input 
              type="password" 
              className="input-field" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="•••••••• (Min 8 chars)" 
              required 
              minLength={8}
              disabled={!token}
            />
          </div>
          <div className="input-group">
            <label className="input-label">Confirm Password</label>
            <input 
              type="password" 
              className="input-field" 
              value={confirmPassword} 
              onChange={(e) => setConfirmPassword(e.target.value)} 
              placeholder="••••••••" 
              required 
              minLength={8}
              disabled={!token}
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }} disabled={!token}>
            Update Password
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-muted)' }}>
          Back to <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};
