import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Badge, Alert, Table } from 'react-bootstrap';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import api from '../../services/api';
import { FiPackage, FiDollarSign, FiTrendingUp, FiAlertCircle, FiShoppingBag, FiActivity, FiArrowUp, FiArrowDown } from 'react-icons/fi';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalProdutos: 0,
    estoqueBaixo: 0,
    vendasHoje: 0,
    receitasMes: 0,
    totalVendas: 0,
    totalCompras: 0,
    produtosAtivos: 0,
  });
  const [vendasSemana, setVendasSemana] = useState({ labels: [], data: [] });
  const [produtosEstoqueBaixo, setProdutosEstoqueBaixo] = useState([]);
  const [vendasRecentes, setVendasRecentes] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [produtosPorCategoria, setProdutosPorCategoria] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      // Total de produtos
      const produtosRes = await api.get('/api/produtos/');
      const produtos = Array.isArray(produtosRes.data) ? produtosRes.data : produtosRes.data.results || [];
      const totalProdutos = produtosRes.data.count || produtos.length;
      const produtosAtivos = produtos.filter(p => p.ativo).length;

      // Produtos com estoque baixo
      const estoqueBaixoRes = await api.get('/api/produtos/estoque_baixo/');
      const estoqueBaixo = estoqueBaixoRes.data.length || 0;
      setProdutosEstoqueBaixo(estoqueBaixoRes.data.slice(0, 5) || []);

      // Categorias
      const categoriasRes = await api.get('/api/categorias/');
      const categoriasData = Array.isArray(categoriasRes.data) ? categoriasRes.data : categoriasRes.data.results || [];
      setCategorias(categoriasData);

      // Contar produtos por categoria
      const contagem = {};
      produtos.forEach(produto => {
        const catId = produto.categoria;
        if (catId) {
          contagem[catId] = (contagem[catId] || 0) + 1;
        }
      });
      setProdutosPorCategoria(contagem);

      // Vendas de hoje
      const hoje = new Date().toISOString().split('T')[0];
      const vendasRes = await api.get(`/api/vendas/relatorio/?data_inicio=${hoje}&data_fim=${hoje}`);
      const vendasHoje = vendasRes.data.quantidade_vendas || 0;

      // Vendas da semana (últimos 7 dias)
      const hojeObj = new Date();
      const diasSemana = [];
      const vendasPorDia = [];
      
      for (let i = 6; i >= 0; i--) {
        const data = new Date(hojeObj);
        data.setDate(hojeObj.getDate() - i);
        const dataStr = data.toISOString().split('T')[0];
        const diaNome = data.toLocaleDateString('pt-BR', { weekday: 'short' });
        diasSemana.push(diaNome);
        
        try {
          const vendasDiaRes = await api.get(`/api/vendas/relatorio/?data_inicio=${dataStr}&data_fim=${dataStr}`);
          vendasPorDia.push(parseFloat(vendasDiaRes.data.total_vendas || 0));
        } catch {
          vendasPorDia.push(0);
        }
      }
      
      setVendasSemana({ labels: diasSemana, data: vendasPorDia });

      // Vendas recentes
      const vendasRecentesRes = await api.get('/api/vendas/?ordering=-criado_em');
      const vendasRecentesData = Array.isArray(vendasRecentesRes.data) ? vendasRecentesRes.data : vendasRecentesRes.data.results || [];
      setVendasRecentes(vendasRecentesData.slice(0, 5));

      // Receitas do mês
      const primeiroDiaMes = new Date(new Date().getFullYear(), new Date().getMonth(), 1)
        .toISOString().split('T')[0];
      const ultimoDiaMes = new Date().toISOString().split('T')[0];
      const relatorioRes = await api.get(
        `/api/relatorios/fluxo_caixa/?data_inicio=${primeiroDiaMes}&data_fim=${ultimoDiaMes}`
      );
      const receitasMes = relatorioRes.data.receitas?.total || 0;
      const totalVendas = relatorioRes.data.receitas?.vendas || 0;
      const totalCompras = relatorioRes.data.despesas?.compras || 0;

      setStats({
        totalProdutos,
        estoqueBaixo,
        vendasHoje,
        receitasMes,
        totalVendas,
        totalCompras,
        produtosAtivos,
      });
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  // Gráfico de vendas da semana
  const vendasSemanaChart = {
    labels: vendasSemana.labels || [],
    datasets: [
      {
        label: 'Vendas (R$)',
        data: vendasSemana.data || [],
        borderColor: 'rgba(0, 175, 238, 1)',
        backgroundColor: 'rgba(0, 175, 238, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  // Gráfico de receitas vs despesas
  const receitasDespesasChart = {
    labels: ['Receitas', 'Despesas'],
    datasets: [
      {
        label: 'Valores (R$)',
        data: [stats.totalVendas, stats.totalCompras],
        backgroundColor: [
          'rgba(67, 233, 123, 0.8)',
          'rgba(245, 87, 108, 0.8)',
        ],
        borderColor: [
          'rgba(67, 233, 123, 1)',
          'rgba(245, 87, 108, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Gráfico de produtos por categoria
  const produtosPorCategoriaChart = {
    labels: categorias.slice(0, 5).map(cat => cat.nome),
    datasets: [
      {
        label: 'Produtos',
        data: categorias.slice(0, 5).map(cat => produtosPorCategoria[cat.id] || 0),
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(79, 172, 254, 0.8)',
          'rgba(0, 242, 254, 0.8)',
          'rgba(67, 233, 123, 0.8)',
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(118, 75, 162, 1)',
          'rgba(79, 172, 254, 1)',
          'rgba(0, 242, 254, 1)',
          'rgba(67, 233, 123, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '60vh' }}>
        <div className="spinner-border text-primary" role="status" style={{ width: '3rem', height: '3rem' }}>
          <span className="visually-hidden">Carregando...</span>
        </div>
      </div>
    );
  }

  const lucroBruto = stats.totalVendas - stats.totalCompras;
  const margemLucro = stats.totalVendas > 0 ? ((lucroBruto / stats.totalVendas) * 100).toFixed(1) : 0;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header mb-4">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-subtitle">Visão geral do seu negócio</p>
      </div>

      {stats.estoqueBaixo > 0 && (
        <Alert variant="warning" className="mb-4 alert-custom">
          <FiAlertCircle className="me-2" size={20} />
          <strong>Atenção!</strong> Você tem {stats.estoqueBaixo} produto(s) com estoque baixo.
        </Alert>
      )}

      {/* Cards de Estatísticas */}
      <Row className="g-4 mb-4">
        <Col md={3} sm={6}>
          <Card className="stat-card stat-card-primary h-100">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-primary">
                  <FiPackage size={24} />
                </div>
              </div>
              <h6 className="stat-label text-uppercase">Total de Produtos</h6>
              <h2 className="stat-value mb-0">{stats.totalProdutos}</h2>
              <small className="stat-description text-muted">
                {stats.produtosAtivos} ativos
              </small>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3} sm={6}>
          <Card className={`stat-card stat-card-warning h-100 ${stats.estoqueBaixo > 0 ? 'stat-card-alert' : ''}`}>
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-warning">
                  <FiAlertCircle size={24} />
                </div>
                {stats.estoqueBaixo > 0 && (
                  <Badge bg="danger" className="stat-badge">Atenção</Badge>
                )}
              </div>
              <h6 className="stat-label text-uppercase">Estoque Baixo</h6>
              <h2 className="stat-value mb-0">{stats.estoqueBaixo}</h2>
              <small className="stat-description text-muted">Requer atenção</small>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3} sm={6}>
          <Card className="stat-card stat-card-success h-100">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-success">
                  <FiShoppingBag size={24} />
                </div>
              </div>
              <h6 className="stat-label text-uppercase">Vendas Hoje</h6>
              <h2 className="stat-value mb-0">{stats.vendasHoje}</h2>
              <small className="stat-description text-muted">Vendas realizadas hoje</small>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3} sm={6}>
          <Card className="stat-card stat-card-info h-100">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-info">
                  <FiTrendingUp size={24} />
                </div>
              </div>
              <h6 className="stat-label text-uppercase">Receitas do Mês</h6>
              <h2 className="stat-value mb-0">
                R$ {stats.receitasMes.toLocaleString('pt-BR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </h2>
              <small className="stat-description text-muted">Receita total do mês</small>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Cards Adicionais */}
      <Row className="g-4 mb-4">
        <Col md={4} sm={6}>
          <Card className="stat-card stat-card-secondary h-100">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-secondary">
                  <FiDollarSign size={24} />
                </div>
              </div>
              <h6 className="stat-label text-uppercase">Total Vendas (Mês)</h6>
              <h2 className="stat-value mb-0">
                R$ {stats.totalVendas.toLocaleString('pt-BR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </h2>
              <small className="stat-description text-muted">Vendas do mês atual</small>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4} sm={6}>
          <Card className="stat-card stat-card-danger h-100">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-danger">
                  <FiActivity size={24} />
                </div>
              </div>
              <h6 className="stat-label text-uppercase">Total Compras (Mês)</h6>
              <h2 className="stat-value mb-0">
                R$ {stats.totalCompras.toLocaleString('pt-BR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </h2>
              <small className="stat-description text-muted">Compras do mês atual</small>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4} sm={6}>
          <Card className="stat-card stat-card-profit h-100">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon-wrapper stat-icon-profit">
                  {lucroBruto >= 0 ? <FiArrowUp size={24} /> : <FiArrowDown size={24} />}
                </div>
              </div>
              <h6 className="stat-label text-uppercase">Lucro Bruto</h6>
              <h2 className={`stat-value mb-0 ${lucroBruto >= 0 ? 'text-success' : 'text-danger'}`}>
                R$ {lucroBruto.toLocaleString('pt-BR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </h2>
              <small className="stat-description text-muted">
                Margem: {margemLucro}%
              </small>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Gráficos */}
      <Row className="g-4 mb-4">
        <Col md={8}>
          <Card className="chart-card">
            <Card.Header className="chart-card-header">
              <h5 className="mb-0">
                <FiTrendingUp className="me-2" />
                Vendas dos Últimos 7 Dias
              </h5>
            </Card.Header>
            <Card.Body>
              <div style={{ height: '300px' }}>
                <Line data={vendasSemanaChart} options={chartOptions} />
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="chart-card">
            <Card.Header className="chart-card-header">
              <h5 className="mb-0">
                <FiDollarSign className="me-2" />
                Receitas vs Despesas
              </h5>
            </Card.Header>
            <Card.Body>
              <div style={{ height: '300px' }}>
                <Bar data={receitasDespesasChart} options={chartOptions} />
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="g-4 mb-4">
        <Col md={6}>
          <Card className="chart-card">
            <Card.Header className="chart-card-header">
              <h5 className="mb-0">
                <FiPackage className="me-2" />
                Produtos por Categoria
              </h5>
            </Card.Header>
            <Card.Body>
              <div style={{ height: '300px' }}>
                {categorias.length > 0 ? (
                  <Doughnut data={produtosPorCategoriaChart} options={chartOptions} />
                ) : (
                  <div className="d-flex justify-content-center align-items-center h-100">
                    <p className="text-muted">Nenhuma categoria cadastrada</p>
                  </div>
                )}
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="chart-card">
            <Card.Header className="chart-card-header">
              <h5 className="mb-0">
                <FiAlertCircle className="me-2" />
                Produtos com Estoque Baixo
              </h5>
            </Card.Header>
            <Card.Body>
              {produtosEstoqueBaixo.length > 0 ? (
                <Table hover responsive>
                  <thead>
                    <tr>
                      <th>Produto</th>
                      <th>Tamanho</th>
                      <th>Estoque</th>
                      <th>Mínimo</th>
                    </tr>
                  </thead>
                  <tbody>
                    {produtosEstoqueBaixo.map((produto) => (
                      <tr key={produto.id}>
                        <td>{produto.nome}</td>
                        <td>{produto.tamanho}</td>
                        <td>
                          <Badge bg="danger">{produto.quantidade}</Badge>
                        </td>
                        <td>{produto.quantidade_minima}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              ) : (
                <div className="text-center py-4">
                  <p className="text-muted mb-0">Nenhum produto com estoque baixo</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Vendas Recentes */}
      <Row className="g-4">
        <Col md={12}>
          <Card className="chart-card">
            <Card.Header className="chart-card-header">
              <h5 className="mb-0">
                <FiShoppingBag className="me-2" />
                Vendas Recentes
              </h5>
            </Card.Header>
            <Card.Body>
              {vendasRecentes.length > 0 ? (
                <Table hover responsive>
                  <thead>
                    <tr>
                      <th>Número</th>
                      <th>Cliente</th>
                      <th>Total</th>
                      <th>Status</th>
                      <th>Data</th>
                    </tr>
                  </thead>
                  <tbody>
                    {vendasRecentes.map((venda) => (
                      <tr key={venda.id}>
                        <td>{venda.numero}</td>
                        <td>{venda.cliente || '-'}</td>
                        <td>
                          <strong>
                            R$ {parseFloat(venda.total).toLocaleString('pt-BR', {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2,
                            })}
                          </strong>
                        </td>
                        <td>
                          <Badge bg={venda.status === 'CONCLUIDA' ? 'success' : 'warning'}>
                            {venda.status}
                          </Badge>
                        </td>
                        <td>{new Date(venda.criado_em).toLocaleDateString('pt-BR')}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              ) : (
                <div className="text-center py-4">
                  <p className="text-muted mb-0">Nenhuma venda registrada</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
