import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert, Badge } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus } from 'react-icons/fi';

const Movimentacoes = () => {
  const [movimentacoes, setMovimentacoes] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    produto: '',
    tipo: 'ENTRADA',
    quantidade: 1,
    observacao: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    loadMovimentacoes();
    loadProdutos();
  }, []);

  const loadMovimentacoes = async () => {
    try {
      const response = await api.get('/api/movimentacoes/');
      setMovimentacoes(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar movimentações:', error);
    }
  };

  const loadProdutos = async () => {
    try {
      const response = await api.get('/api/produtos/');
      setProdutos(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await api.post('/api/movimentacoes/', formData);
      setShowModal(false);
      resetForm();
      loadMovimentacoes();
      loadProdutos(); // Recarrega para atualizar quantidades
    } catch (error) {
      setError(error.response?.data?.message || 'Erro ao registrar movimentação');
    }
  };

  const resetForm = () => {
    setFormData({
      produto: '',
      tipo: 'ENTRADA',
      quantidade: 1,
      observacao: '',
    });
  };

  const getTipoBadge = (tipo) => {
    const badges = {
      ENTRADA: 'success',
      SAIDA: 'danger',
      AJUSTE: 'warning',
    };
    return badges[tipo] || 'secondary';
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Movimentações de Estoque</h2>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Nova Movimentação
        </Button>
      </div>

      <Card>
        <Card.Body>
          <Table responsive>
            <thead>
              <tr>
                <th>Data</th>
                <th>Produto</th>
                <th>Tipo</th>
                <th>Quantidade</th>
                <th>Usuário</th>
                <th>Observação</th>
              </tr>
            </thead>
            <tbody>
              {movimentacoes.map((mov) => (
                <tr key={mov.id}>
                  <td>{new Date(mov.criado_em).toLocaleString('pt-BR')}</td>
                  <td>{mov.produto_nome}</td>
                  <td>
                    <Badge bg={getTipoBadge(mov.tipo)}>{mov.tipo}</Badge>
                  </td>
                  <td>{mov.quantidade}</td>
                  <td>{mov.usuario_nome}</td>
                  <td>{mov.observacao || '-'}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => { setShowModal(false); resetForm(); }}>
        <Modal.Header closeButton>
          <Modal.Title>Nova Movimentação</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form.Group className="mb-3">
              <Form.Label>Produto *</Form.Label>
              <Form.Select
                value={formData.produto}
                onChange={(e) => setFormData({ ...formData, produto: e.target.value })}
                required
              >
                <option value="">Selecione...</option>
                {produtos.map((prod) => (
                  <option key={prod.id} value={prod.id}>
                    {prod.nome} - {prod.tamanho} - {prod.cor} (Estoque: {prod.quantidade})
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Tipo *</Form.Label>
              <Form.Select
                value={formData.tipo}
                onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
                required
              >
                <option value="ENTRADA">Entrada</option>
                <option value="SAIDA">Saída</option>
                <option value="AJUSTE">Ajuste</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Quantidade *</Form.Label>
              <Form.Control
                type="number"
                min="1"
                value={formData.quantidade}
                onChange={(e) => setFormData({ ...formData, quantidade: parseInt(e.target.value) || 1 })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Observação</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.observacao}
                onChange={(e) => setFormData({ ...formData, observacao: e.target.value })}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => { setShowModal(false); resetForm(); }}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit">
              Salvar
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
};

export default Movimentacoes;





