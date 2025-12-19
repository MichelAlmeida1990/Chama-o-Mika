import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useSidebar } from '../../contexts/SidebarContext';
import {
  FiPackage,
  FiDollarSign,
  FiBarChart2,
  FiLogOut,
  FiHome,
  FiShoppingCart,
  FiFileText,
  FiTrendingUp,
  FiMenu,
  FiChevronDown,
  FiChevronRight,
  FiUser,
} from 'react-icons/fi';
import './Sidebar.css';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { collapsed, toggleSidebar } = useSidebar();
  const [openMenus, setOpenMenus] = useState({
    estoque: false,
    financeiro: false,
  });

  // Verificar se está em mobile - hooks devem estar no topo
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 991);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 991);
      if (window.innerWidth > 991 && collapsed) {
        toggleSidebar(); // Fechar sidebar quando voltar para desktop
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [collapsed, toggleSidebar]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (!user) {
    return null;
  }

  const isActive = (path) => {
    return location.pathname === path;
  };

  const toggleMenu = (menu) => {
    setOpenMenus(prev => ({
      ...prev,
      [menu]: !prev[menu]
    }));
  };

  return (
    <>
      {/* Overlay para mobile */}
      {collapsed && isMobile && (
        <div 
          className="sidebar-overlay active" 
          onClick={toggleSidebar}
        />
      )}
      
      {/* Top Navbar */}
      <nav className="top-navbar">
        <div className="top-navbar-content">
          <button 
            className="sidebar-toggle-btn" 
            onClick={toggleSidebar}
            title={collapsed ? 'Expandir menu' : 'Recolher menu'}
          >
            <FiMenu size={20} />
          </button>
          <div className="navbar-brand-top">
            <img 
              src="/logo-mika.png" 
              alt="Chama o Mika" 
              className="navbar-logo"
              style={{ height: '40px', marginRight: '10px' }}
            />
            <span>Chama o Mika</span>
          </div>
          <div className="navbar-user-top">
            <span className="user-greeting">
              Olá, <span className="user-name">{user.email || user.username || 'Usuário'}</span>
            </span>
            <button 
              className="logout-btn-top" 
              onClick={handleLogout}
              title="Sair"
            >
              <FiLogOut size={18} />
            </button>
          </div>
        </div>
      </nav>

      {/* Sidebar */}
      <div className={`sidebar ${collapsed ? 'collapsed' : ''}`} id="sidebar">
        <div className="sidebar-content">
          <div className="sidebar-header">
            {!collapsed && (
              <div className="sidebar-logo-container">
                <img 
                  src="/logo-mika.png" 
                  alt="Chama o Mika" 
                  className="sidebar-logo"
                />
              </div>
            )}
            <h5 className="sidebar-title">
              <FiPackage className="me-2" />
              <span className={collapsed ? 'd-none' : ''}>Menu</span>
            </h5>
          </div>

          <nav className="sidebar-nav">
            <Link
              to="/"
              className={`sidebar-link ${isActive('/') ? 'active' : ''}`}
              title="Dashboard"
            >
              <FiHome className="sidebar-icon" />
              <span className={collapsed ? 'd-none' : ''}>Dashboard</span>
            </Link>

            {/* Menu Estoque */}
            <div className="sidebar-menu-group">
              <button
                className={`sidebar-link sidebar-dropdown-toggle ${openMenus.estoque ? 'open' : ''}`}
                onClick={() => toggleMenu('estoque')}
                title="Estoque"
              >
                <FiPackage className="sidebar-icon" />
                <span className={collapsed ? 'd-none' : ''}>Estoque</span>
                {!collapsed && (
                  <span className="dropdown-arrow">
                    {openMenus.estoque ? <FiChevronDown /> : <FiChevronRight />}
                  </span>
                )}
              </button>
              {!collapsed && (
                <div className={`sidebar-submenu ${openMenus.estoque ? 'open' : ''}`}>
                  <Link
                    to="/produtos"
                    className={`sidebar-submenu-link ${isActive('/produtos') ? 'active' : ''}`}
                  >
                    Produtos
                  </Link>
                  <Link
                    to="/categorias"
                    className={`sidebar-submenu-link ${isActive('/categorias') ? 'active' : ''}`}
                  >
                    Categorias
                  </Link>
                  <Link
                    to="/movimentacoes"
                    className={`sidebar-submenu-link ${isActive('/movimentacoes') ? 'active' : ''}`}
                  >
                    Movimentações
                  </Link>
                </div>
              )}
            </div>

            {/* Menu Financeiro */}
            <div className="sidebar-menu-group">
              <button
                className={`sidebar-link sidebar-dropdown-toggle ${openMenus.financeiro ? 'open' : ''}`}
                onClick={() => toggleMenu('financeiro')}
                title="Financeiro"
              >
                <FiDollarSign className="sidebar-icon" />
                <span className={collapsed ? 'd-none' : ''}>Financeiro</span>
                {!collapsed && (
                  <span className="dropdown-arrow">
                    {openMenus.financeiro ? <FiChevronDown /> : <FiChevronRight />}
                  </span>
                )}
              </button>
              {!collapsed && (
                <div className={`sidebar-submenu ${openMenus.financeiro ? 'open' : ''}`}>
                  <Link
                    to="/clientes"
                    className={`sidebar-submenu-link ${isActive('/clientes') ? 'active' : ''}`}
                  >
                    <FiUser className="me-2" size={14} />
                    Clientes
                  </Link>
                  <Link
                    to="/vendas"
                    className={`sidebar-submenu-link ${isActive('/vendas') ? 'active' : ''}`}
                  >
                    <FiDollarSign className="me-2" size={14} />
                    Vendas
                  </Link>
                  <Link
                    to="/compras"
                    className={`sidebar-submenu-link ${isActive('/compras') ? 'active' : ''}`}
                  >
                    <FiShoppingCart className="me-2" size={14} />
                    Compras
                  </Link>
                  <Link
                    to="/contas-pagar"
                    className={`sidebar-submenu-link ${isActive('/contas-pagar') ? 'active' : ''}`}
                  >
                    <FiFileText className="me-2" size={14} />
                    Contas a Pagar
                  </Link>
                  <Link
                    to="/contas-receber"
                    className={`sidebar-submenu-link ${isActive('/contas-receber') ? 'active' : ''}`}
                  >
                    <FiTrendingUp className="me-2" size={14} />
                    Contas a Receber
                  </Link>
                  <Link
                    to="/relatorios"
                    className={`sidebar-submenu-link ${isActive('/relatorios') ? 'active' : ''}`}
                  >
                    <FiBarChart2 className="me-2" size={14} />
                    Relatórios
                  </Link>
                </div>
              )}
            </div>
          </nav>

          {!collapsed && (
            <div className="sidebar-footer">
              <button className="sidebar-link logout-link" onClick={handleLogout}>
                <FiLogOut className="sidebar-icon" />
                <span>Sair</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Sidebar;

