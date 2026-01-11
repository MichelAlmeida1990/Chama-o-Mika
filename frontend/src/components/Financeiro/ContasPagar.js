import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert, Badge } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus, FiCheck } from 'react-icons/fi';

const ContasPagar = () => {
  const [contas, setContas] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingConta, setEditingConta] = useState(null);
  const [formData, setFormData] = useState({
    descricao: '',
    valor: 0,
    data_vencimento: '',
    observacoes: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    loadContas();
  }, []);

  const loadContas = async () => {
    try {
      const response = await api.get('/api/contas-pagar/');
      setContas(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar contas a pagar:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      if (editingConta) {
        await api.put(`/api/contas-pagar/${editingConta.id}/`, formData);
      } else {
        await api.post('/api/contas-pagar/', formData);
      }
      setShowModal(false);
      resetForm();
      loadContas();
    } catch (error) {
      setError(error.response?.data?.message || 'Erro ao salvar conta');
    }
  };

  const handleEdit = (conta) => {
    setEditingConta(conta);
    setFormData({
      descricao: conta.descricao,
      valor: conta.valor,
      data_vencimento: conta.data_vencimento,
      observacoes: conta.observacoes || '',
    });
    setShowModal(true);
  };

  const handlePagar = async (id) => {
    try {
      await api.post(`/api/contas-pagar/${id}/pagar/`);
      loadContas();
    } catch (error) {
      alert('Erro ao marcar conta como paga');
    }
  };

  const resetForm = () => {
    setEditingConta(null);
    setFormData({
      descricao: '',
      valor: 0,
      data_vencimento: '',
      observacoes: '',
    });
  };

  const getStatusBadge = (conta) => {
    if (conta.status === 'PAGA') return 'success';
    const hoje = new Date();
    const vencimento = new Date(conta.data_vencimento);
    if (vencimento < hoje) return 'danger';
    return 'warning';
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Contas a Pagar</h2>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Nova Conta
        </Button>
      </div>

      <Card>
        <Card.Body>
          <Table responsive>
            <thead>
              <tr>
                <th>Descrição</th>
                <th>Valor</th>
                <th>Vencimento</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {contas.map((conta) => (
                <tr key={conta.id}>
                  <td>{conta.descricao}</td>
                  <td>R$ {parseFloat(conta.valor).toFixed(2)}</td>
                  <td>{new Date(conta.data_vencimento).toLocaleDateString('pt-BR')}</td>
                  <td>
                    <Badge bg={getStatusBadge(conta)}>
                      {conta.status}
                    </Badge>
                  </td>
                  <td>
                    {conta.status !== 'PAGA' && (
                      <Button
                        variant="outline-success"
                        size="sm"
                        className="me-2"
                        onClick={() => handlePagar(conta.id)}
                      >
                        <FiCheck /> Pagar
                      </Button>
                    )}
                    <Button
                      variant="outline-primary"
                      size="sm"
                      onClick={() => handleEdit(conta)}
                    >
                      Editar
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => { setShowModal(false); resetForm(); }}>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingConta ? 'Editar Conta' : 'Nova Conta a Pagar'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form.Group className="mb-3">
              <Form.Label>Descrição *</Form.Label>
              <Form.Control
                type="text"
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Valor *</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                min="0.01"
                value={formData.valor}
                onChange={(e) => setFormData({ ...formData, valor: parseFloat(e.target.value) || 0 })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Data de Vencimento *</Form.Label>
              <Form.Control
                type="date"
                value={formData.data_vencimento}
                onChange={(e) => setFormData({ ...formData, data_vencimento: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Observações</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.observacoes}
                onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
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

export default ContasPagar;





