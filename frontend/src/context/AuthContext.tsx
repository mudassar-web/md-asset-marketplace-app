import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { api, refreshAccessToken, setAccessToken } from '../api/client';

type User = { id: string; email: string; name: string; role: 'user' | 'admin'; created_at: string };
type AuthContextType = {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>(null!);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const token = await refreshAccessToken();
        if (token) {
          const result = await api<{ user: User }>('/api/users/me');
          setUser(result.user);
        }
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const login = async (email: string, password: string) => {
    const result = await api<{ access_token: string; user: User }>('/api/users/login', {
      method: 'POST', body: JSON.stringify({ email, password }),
    });
    setAccessToken(result.access_token);
    setUser(result.user);
  };

  const register = async (name: string, email: string, password: string) => {
    await api('/api/users/register', { method: 'POST', body: JSON.stringify({ name, email, password }) });
    await login(email, password);
  };

  const logout = async () => {
    try { await api('/api/users/logout', { method: 'POST' }); } finally {
      setAccessToken(null);
      setUser(null);
    }
  };

  return <AuthContext.Provider value={{ user, loading, login, register, logout }}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
