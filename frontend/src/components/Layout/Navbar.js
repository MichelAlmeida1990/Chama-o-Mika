import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Navbar as BootstrapNavbar, Nav, Container, Button } from 'react-bootstrap';
import { useAuth } from '../../contexts/AuthContext';
import { 
  FiPackage, 
  FiDollarSign, 
  FiBarChart2, 
  FiLogOut, 
  FiHome, 
  FiTag,
  FiRefreshCw,
  FiShoppingCart,
  FiFileText,
  FiTrendingUp
} from 'react-icons/fi';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

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

  return (
    <BootstrapNavbar expand="lg" className="custom-navbar" variant="dark">
      <Container fluid>
        <BootstrapNavbar.Brand as={Link} to="/" className="navbar-brand-custom">
          <FiPackage className="navbar-brand-icon" />
          <span>Chama o Mika</span>
        </BootstrapNavbar.Brand>
        
        <BootstrapNavbar.Toggle 
          aria-controls="basic-navbar-nav" 
          className="navbar-toggler-custom"
        >
          <span className="navbar-toggler-icon-custom"></span>
        </BootstrapNavbar.Toggle>
        
        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link 
              as={Link} 
              to="/" 
              className={`nav-link-custom ${isActive('/') ? 'active' : ''}`}
            >
              <FiHome className="nav-link-icon" />
              <span>Dashboard</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/produtos" 
              className={`nav-link-custom ${isActive('/produtos') ? 'active' : ''}`}
            >
              <FiPackage className="nav-link-icon" />
              <span>Produtos</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/categorias" 
              className={`nav-link-custom ${isActive('/categorias') ? 'active' : ''}`}
            >
              <FiTag className="nav-link-icon" />
              <span>Categorias</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/movimentacoes" 
              className={`nav-link-custom ${isActive('/movimentacoes') ? 'active' : ''}`}
            >
              <FiRefreshCw className="nav-link-icon" />
              <span>Movimentações</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/vendas" 
              className={`nav-link-custom ${isActive('/vendas') ? 'active' : ''}`}
            >
              <FiDollarSign className="nav-link-icon" />
              <span>Vendas</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/compras" 
              className={`nav-link-custom ${isActive('/compras') ? 'active' : ''}`}
            >
              <FiShoppingCart className="nav-link-icon" />
              <span>Compras</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/contas-pagar" 
              className={`nav-link-custom ${isActive('/contas-pagar') ? 'active' : ''}`}
              title="Contas a Pagar"
            >
              <FiFileText className="nav-link-icon" />
              <span className="d-none d-lg-inline">Contas a Pagar</span>
              <span className="d-lg-none">Pagar</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/contas-receber" 
              className={`nav-link-custom ${isActive('/contas-receber') ? 'active' : ''}`}
              title="Contas a Receber"
            >
              <FiTrendingUp className="nav-link-icon" />
              <span className="d-none d-lg-inline">Contas a Receber</span>
              <span className="d-lg-none">Receber</span>
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/relatorios" 
              className={`nav-link-custom ${isActive('/relatorios') ? 'active' : ''}`}
            >
              <FiBarChart2 className="nav-link-icon" />
              <span>Relatórios</span>
            </Nav.Link>
          </Nav>
          
          <div className="navbar-user-section">
            <div className="navbar-user-greeting">
              <span>Olá,</span>
              <span className="navbar-user-email">
                {user.email || user.username || 'Usuário'}
              </span>
            </div>
            <Button 
              variant="outline-light" 
              size="sm" 
              onClick={handleLogout}
              className="navbar-logout-btn"
            >
              <FiLogOut />
              <span>Sair</span>
            </Button>
          </div>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  );
};

export default Navbar;

