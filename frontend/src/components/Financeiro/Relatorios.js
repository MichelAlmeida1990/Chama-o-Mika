import React, { useState, useEffect, useCallback } from 'react';
import { Card, Form, Button, Row, Col, Table } from 'react-bootstrap';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import api from '../../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Relatorios = () => {
  // Inicializa com datas padrão (mês atual)
  const hoje = new Date();
  const primeiroDia = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
  const [dataInicio, setDataInicio] = useState(primeiroDia.toISOString().split('T')[0]);
  const [dataFim, setDataFim] = useState(hoje.toISOString().split('T')[0]);
  const [fluxoCaixa, setFluxoCaixa] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);

  const loadFluxoCaixa = useCallback(async () => {
    if (!dataInicio || !dataFim) return;
    
    setLoading(true);
    try {
      const response = await api.get(
        `/api/relatorios/fluxo_caixa/?data_inicio=${dataInicio}&data_fim=${dataFim}`
      );
      setFluxoCaixa(response.data);
      setHasLoaded(true);
    } catch (error) {
      console.error('Erro ao carregar fluxo de caixa:', error);
    } finally {
      setLoading(false);
    }
  }, [dataInicio, dataFim]);

  // Carrega apenas uma vez quando o componente monta
  useEffect(() => {
    if (!hasLoaded && dataInicio && dataFim) {
      loadFluxoCaixa();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const chartData = fluxoCaixa ? {
    labels: ['Receitas', 'Despesas', 'Saldo'],
    datasets: [
      {
        label: 'Valores (R$)',
        data: [
          fluxoCaixa.receitas.total,
          fluxoCaixa.despesas.total,
          fluxoCaixa.saldo,
        ],
        backgroundColor: [
          'rgba(0, 175, 238, 0.6)',
          'rgba(194, 175, 0, 0.6)',
          fluxoCaixa.saldo >= 0 ? 'rgba(204, 255, 0, 0.6)' : 'rgba(202, 0, 202, 0.6)',
        ],
        borderColor: [
          'rgba(0, 175, 238, 1)',
          'rgba(194, 175, 0, 1)',
          fluxoCaixa.saldo >= 0 ? 'rgba(204, 255, 0, 1)' : 'rgba(202, 0, 202, 1)',
        ],
        borderWidth: 1,
      },
    ],
  } : null;

  return (
    <div>
      <h2 className="mb-4">Relatórios Financeiros</h2>

      <Card className="mb-4">
        <Card.Header>Filtros</Card.Header>
        <Card.Body>
          <Row>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Data Início</Form.Label>
                <Form.Control
                  type="date"
                  value={dataInicio}
                  onChange={(e) => setDataInicio(e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Data Fim</Form.Label>
                <Form.Control
                  type="date"
                  value={dataFim}
                  onChange={(e) => setDataFim(e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4} className="d-flex align-items-end">
              <Button 
                variant="primary" 
                onClick={() => {
                  setHasLoaded(false);
                  loadFluxoCaixa();
                }}
                disabled={loading}
              >
                {loading ? 'Carregando...' : 'Atualizar'}
              </Button>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {loading && (
        <div className="d-flex justify-content-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Carregando...</span>
          </div>
        </div>
      )}

      {fluxoCaixa && (
        <>
          <Row className="mb-4">
            <Col md={6}>
              <Card>
                <Card.Header>Fluxo de Caixa</Card.Header>
                <Card.Body>
                  {chartData && <Bar data={chartData} />}
                </Card.Body>
              </Card>
            </Col>
            <Col md={6}>
              <Card>
                <Card.Header>Resumo Financeiro</Card.Header>
                <Card.Body>
                  <Table>
                    <tbody>
                      <tr>
                        <th>Receitas Totais</th>
                        <td className="text-success">
                          R$ {fluxoCaixa.receitas.total.toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                      <tr>
                        <td className="ps-4">Vendas</td>
                        <td>
                          R$ {fluxoCaixa.receitas.vendas.toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                      <tr>
                        <td className="ps-4">Contas Recebidas</td>
                        <td>
                          R$ {fluxoCaixa.receitas.contas_recebidas.toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                      <tr>
                        <th>Despesas Totais</th>
                        <td className="text-danger">
                          R$ {fluxoCaixa.despesas.total.toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                      <tr>
                        <td className="ps-4">Compras</td>
                        <td>
                          R$ {fluxoCaixa.despesas.compras.toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                      <tr>
                        <td className="ps-4">Contas Pagas</td>
                        <td>
                          R$ {fluxoCaixa.despesas.contas_pagas.toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                      <tr>
                        <th>Saldo</th>
                        <td className={fluxoCaixa.saldo >= 0 ? 'text-success' : 'text-danger'}>
                          <strong>
                            R$ {fluxoCaixa.saldo.toLocaleString('pt-BR', {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2,
                            })}
                          </strong>
                        </td>
                      </tr>
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
};

export default Relatorios;

