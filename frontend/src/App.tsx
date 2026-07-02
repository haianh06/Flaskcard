import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ForgotPassword } from './pages/ForgotPassword';
import { ResetPassword } from './pages/ResetPassword';
import { Dashboard } from './pages/Dashboard';
import { DeckDetails } from './pages/DeckDetails';
import { Study } from './pages/Study';
import { Dictionary } from './pages/Dictionary';

// Protected Route wrapper
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div className="flex-center" style={{ minHeight: '100vh' }}>Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        
        <Route path="/" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        
        <Route path="/dictionary" element={
          <ProtectedRoute>
            <Dictionary />
          </ProtectedRoute>
        } />
        
        <Route path="/decks/:id" element={
          <ProtectedRoute>
            <DeckDetails />
          </ProtectedRoute>
        } />
        
        <Route path="/decks/:id/study" element={
          <ProtectedRoute>
            <Study />
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
