import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, BookOpen } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="glass" style={{ margin: '1rem', padding: '1rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Link to="/" className="flex-center" style={{ gap: '0.5rem', fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--text-main)' }}>
        <BookOpen size={28} color="var(--primary)" />
        <span>Flaskcard</span>
      </Link>
      
      <div className="flex-center" style={{ gap: '1.5rem' }}>
        {isAuthenticated ? (
          <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'var(--text-main)', fontWeight: 500 }}>Dashboard</Link>
            <Link to="/dictionary" style={{ textDecoration: 'none', color: 'var(--text-main)', fontWeight: 500 }}>Dictionary</Link>
            <span style={{ color: 'var(--text-muted)' }}>Hello, {user?.username}</span>
            <button className="btn btn-outline" onClick={handleLogout}>
              <LogOut size={18} /> Logout
            </button>
          </div>
        ) : (
          <>
            <Link to="/login" className="btn btn-outline">Login</Link>
            <Link to="/register" className="btn btn-primary">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
};
