import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verifica se há usuário logado apenas uma vez
    let isMounted = true;
    
    const verifyAuth = async () => {
      try {
        const response = await api.get('/api/auth/user/');
        if (isMounted) {
          setUser(response.data);
        }
      } catch (error) {
        // Não fazer nada se o erro for 401 (usuário não autenticado)
        if (error.response?.status !== 401 && isMounted) {
          console.error('Erro ao verificar autenticação:', error);
        }
        if (isMounted) {
          setUser(null);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    
    verifyAuth();
    
    return () => {
      isMounted = false;
    };
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get('/api/auth/user/');
      setUser(response.data);
      setLoading(false);
    } catch (error) {
      // Não fazer nada se o erro for 401 (usuário não autenticado)
      if (error.response?.status !== 401) {
        console.error('Erro ao verificar autenticação:', error);
      }
      setUser(null);
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      const response = await api.post('/api/auth/login/', {
        username,
        password,
      });
      setUser(response.data.user);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Erro ao fazer login',
      };
    }
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout/');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    } finally {
      setUser(null);
    }
  };

  // Memoiza o valor do contexto para evitar re-renders desnecessários
  const value = React.useMemo(
    () => ({ user, loading, login, logout, checkAuth }),
    [user, loading]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

