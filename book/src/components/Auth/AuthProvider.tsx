import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  userId: string | null;
  login: (token: string, userId: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUserId = localStorage.getItem('user_id');
    
    if (storedToken && storedUserId) {
      setToken(storedToken);
      setUserId(storedUserId);
    }
  }, []);

  const login = (newToken: string, newUserId: string) => {
    setToken(newToken);
    setUserId(newUserId);
    localStorage.setItem('token', newToken);
    localStorage.setItem('user_id', newUserId);
  };

  const logout = () => {
    setToken(null);
    setUserId(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!token,
        token,
        userId,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}