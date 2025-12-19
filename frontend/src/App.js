import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { SidebarProvider, useSidebar } from './contexts/SidebarContext';
import Sidebar from './components/Layout/Sidebar';
import Login from './components/Auth/Login';
import Dashboard from './components/Dashboard/Dashboard';
import Produtos from './components/Estoque/Produtos';
import Categorias from './components/Estoque/Categorias';
import Movimentacoes from './components/Estoque/Movimentacoes';
import Vendas from './components/Financeiro/Vendas';
import Compras from './components/Financeiro/Compras';
import ContasPagar from './components/Financeiro/ContasPagar';
import ContasReceber from './components/Financeiro/ContasReceber';
import Relatorios from './components/Financeiro/Relatorios';
import Clientes from './components/Financeiro/Clientes';
import PrivateRoute from './components/Auth/PrivateRoute';
import './App.css';

const AppContent = () => {
  const { collapsed } = useSidebar();
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  
  return (
    <div className="App">
      {!isLoginPage && <Sidebar />}
      <div className={`main-content ${collapsed && !isLoginPage ? 'sidebar-collapsed' : ''} ${isLoginPage ? 'login-page' : ''}`}>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/"
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                }
              />
              <Route
                path="/produtos"
                element={
                  <PrivateRoute>
                    <Produtos />
                  </PrivateRoute>
                }
              />
              <Route
                path="/categorias"
                element={
                  <PrivateRoute>
                    <Categorias />
                  </PrivateRoute>
                }
              />
              <Route
                path="/movimentacoes"
                element={
                  <PrivateRoute>
                    <Movimentacoes />
                  </PrivateRoute>
                }
              />
              <Route
                path="/vendas"
                element={
                  <PrivateRoute>
                    <Vendas />
                  </PrivateRoute>
                }
              />
              <Route
                path="/compras"
                element={
                  <PrivateRoute>
                    <Compras />
                  </PrivateRoute>
                }
              />
              <Route
                path="/contas-pagar"
                element={
                  <PrivateRoute>
                    <ContasPagar />
                  </PrivateRoute>
                }
              />
              <Route
                path="/contas-receber"
                element={
                  <PrivateRoute>
                    <ContasReceber />
                  </PrivateRoute>
                }
              />
              <Route
                path="/relatorios"
                element={
                  <PrivateRoute>
                    <Relatorios />
                  </PrivateRoute>
                }
              />
              <Route
                path="/clientes"
                element={
                  <PrivateRoute>
                    <Clientes />
                  </PrivateRoute>
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <SidebarProvider>
        <Router>
          <AppContent />
        </Router>
      </SidebarProvider>
    </AuthProvider>
  );
}

export default App;

