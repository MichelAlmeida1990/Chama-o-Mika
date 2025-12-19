import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert, Badge, InputGroup, Row, Col } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus, FiEdit, FiTrash2, FiEye, FiUser, FiMail, FiPhone } from 'react-icons/fi';

const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDetalhes, setShowDetalhes] = useState(false);
  const [editingCliente, setEditingCliente] = useState(null);
  const [clienteSelecionado, setClienteSelecionado] = useState(null);
  const [formData, setFormData] = useState({
    nome: '',
    cpf_cnpj: '',
    email: '',
    telefone: '',
    endereco: '',
    cidade: '',
    estado: '',
    cep: '',
    data_nascimento: '',
    observacoes: '',
    ativo: true,
  });
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadClientes();
  }, []);

  const loadClientes = async () => {
    try {
      const response = await api.get('/api/clientes/');
      setClientes(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      if (editingCliente) {
        await api.put(`/api/clientes/${editingCliente.id}/`, formData);
      } else {
        await api.post('/api/clientes/', formData);
      }
      setShowModal(false);
      resetForm();
      loadClientes();
    } catch (error) {
      setError(error.response?.data?.detail || 'Erro ao salvar cliente');
    }
  };

  const handleEdit = (cliente) => {
    setEditingCliente(cliente);
    setFormData({
      nome: cliente.nome || '',
      cpf_cnpj: cliente.cpf_cnpj || '',
      email: cliente.email || '',
      telefone: cliente.telefone || '',
      endereco: cliente.endereco || '',
      cidade: cliente.cidade || '',
      estado: cliente.estado || '',
      cep: cliente.cep || '',
      data_nascimento: cliente.data_nascimento || '',
      observacoes: cliente.observacoes || '',
      ativo: cliente.ativo !== undefined ? cliente.ativo : true,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este cliente?')) {
      try {
        await api.delete(`/api/clientes/${id}/`);
        loadClientes();
      } catch (error) {
        alert('Erro ao excluir cliente');
      }
    }
  };

  const handleViewDetails = async (cliente) => {
    try {
      const response = await api.get(`/api/clientes/${cliente.id}/historico_compras/`);
      setClienteSelecionado(response.data);
      setShowDetalhes(true);
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
      alert('Erro ao carregar histórico de compras');
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      cpf_cnpj: '',
      email: '',
      telefone: '',
      endereco: '',
      cidade: '',
      estado: '',
      cep: '',
      data_nascimento: '',
      observacoes: '',
      ativo: true,
    });
    setEditingCliente(null);
    setError('');
  };

  const filteredClientes = clientes.filter(cliente =>
    cliente.nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.cpf_cnpj?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="container-fluid">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0">Clientes</h2>
          <p className="text-muted">Gerencie seus clientes</p>
        </div>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Novo Cliente
        </Button>
      </div>

      <Card>
        <Card.Body>
          <InputGroup className="mb-3">
            <InputGroup.Text>
              <FiUser />
            </InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Buscar por nome, CPF/CNPJ ou email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </InputGroup>

          <Table hover responsive>
            <thead>
              <tr>
                <th>Nome</th>
                <th>CPF/CNPJ</th>
                <th>Email</th>
                <th>Telefone</th>
                <th>Total Compras</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {filteredClientes.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-4">
                    <p className="text-muted mb-0">Nenhum cliente encontrado</p>
                  </td>
                </tr>
              ) : (
                filteredClientes.map((cliente) => (
                  <tr key={cliente.id}>
                    <td>
                      <div className="d-flex align-items-center">
                        <FiUser className="me-2" />
                        {cliente.nome}
                      </div>
                    </td>
                    <td>{cliente.cpf_cnpj || '-'}</td>
                    <td>
                      {cliente.email ? (
                        <div className="d-flex align-items-center">
                          <FiMail className="me-2" size={14} />
                          {cliente.email}
                        </div>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td>
                      {cliente.telefone ? (
                        <div className="d-flex align-items-center">
                          <FiPhone className="me-2" size={14} />
                          {cliente.telefone}
                        </div>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td>
                      <strong>
                        R$ {parseFloat(cliente.total_compras || 0).toLocaleString('pt-BR', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </strong>
                      <br />
                      <small className="text-muted">
                        {cliente.quantidade_compras || 0} compra(s)
                      </small>
                    </td>
                    <td>
                      <Badge bg={cliente.ativo ? 'success' : 'secondary'}>
                        {cliente.ativo ? 'Ativo' : 'Inativo'}
                      </Badge>
                    </td>
                    <td>
                      <Button
                        variant="info"
                        size="sm"
                        className="me-2"
                        onClick={() => handleViewDetails(cliente)}
                        title="Ver detalhes"
                      >
                        <FiEye />
                      </Button>
                      <Button
                        variant="warning"
                        size="sm"
                        className="me-2"
                        onClick={() => handleEdit(cliente)}
                        title="Editar"
                      >
                        <FiEdit />
                      </Button>
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleDelete(cliente.id)}
                        title="Excluir"
                      >
                        <FiTrash2 />
                      </Button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Modal de Cadastro/Edição */}
      <Modal show={showModal} onHide={() => { setShowModal(false); resetForm(); }} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{editingCliente ? 'Editar Cliente' : 'Novo Cliente'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}

            <Row>
              <Col md={8}>
                <Form.Group className="mb-3">
                  <Form.Label>Nome *</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.nome}
                    onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>CPF/CNPJ</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.cpf_cnpj}
                    onChange={(e) => setFormData({ ...formData, cpf_cnpj: e.target.value })}
                    placeholder="000.000.000-00"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Telefone</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.telefone}
                    onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                    placeholder="(00) 00000-0000"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Endereço</Form.Label>
              <Form.Control
                type="text"
                value={formData.endereco}
                onChange={(e) => setFormData({ ...formData, endereco: e.target.value })}
                placeholder="Rua, número, complemento"
              />
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Cidade</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.cidade}
                    onChange={(e) => setFormData({ ...formData, cidade: e.target.value })}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Estado</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.estado}
                    onChange={(e) => setFormData({ ...formData, estado: e.target.value })}
                    placeholder="MG"
                    maxLength={2}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>CEP</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.cep}
                    onChange={(e) => setFormData({ ...formData, cep: e.target.value })}
                    placeholder="00000-000"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Data de Nascimento</Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.data_nascimento}
                    onChange={(e) => setFormData({ ...formData, data_nascimento: e.target.value })}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Check
                    type="checkbox"
                    label="Cliente Ativo"
                    checked={formData.ativo}
                    onChange={(e) => setFormData({ ...formData, ativo: e.target.checked })}
                  />
                </Form.Group>
              </Col>
            </Row>

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
              {editingCliente ? 'Atualizar' : 'Salvar'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Modal de Detalhes */}
      <Modal show={showDetalhes} onHide={() => setShowDetalhes(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            <FiUser className="me-2" />
            Detalhes do Cliente
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {clienteSelecionado && (
            <>
              <Card className="mb-3">
                <Card.Body>
                  <h5>{clienteSelecionado.cliente.nome}</h5>
                  <Row className="mt-3">
                    <Col md={6}>
                      <p className="mb-2">
                        <strong>CPF/CNPJ:</strong> {clienteSelecionado.cliente.cpf_cnpj || '-'}
                      </p>
                      <p className="mb-2">
                        <strong>Email:</strong> {clienteSelecionado.cliente.email || '-'}
                      </p>
                      <p className="mb-2">
                        <strong>Telefone:</strong> {clienteSelecionado.cliente.telefone || '-'}
                      </p>
                    </Col>
                    <Col md={6}>
                      <p className="mb-2">
                        <strong>Endereço:</strong> {clienteSelecionado.cliente.endereco || '-'}
                      </p>
                      <p className="mb-2">
                        <strong>Cidade/Estado:</strong>{' '}
                        {clienteSelecionado.cliente.cidade || '-'}
                        {clienteSelecionado.cliente.estado ? ` / ${clienteSelecionado.cliente.estado}` : ''}
                      </p>
                      <p className="mb-2">
                        <strong>CEP:</strong> {clienteSelecionado.cliente.cep || '-'}
                      </p>
                    </Col>
                  </Row>
                  <hr />
                  <Row>
                    <Col md={4}>
                      <div className="text-center">
                        <h4 className="text-primary">
                          R$ {parseFloat(clienteSelecionado.total_compras || 0).toLocaleString('pt-BR', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}
                        </h4>
                        <small className="text-muted">Total em Compras</small>
                      </div>
                    </Col>
                    <Col md={4}>
                      <div className="text-center">
                        <h4 className="text-success">
                          {clienteSelecionado.quantidade_compras || 0}
                        </h4>
                        <small className="text-muted">Quantidade de Compras</small>
                      </div>
                    </Col>
                    <Col md={4}>
                      <div className="text-center">
                        <h4 className="text-info">
                          {clienteSelecionado.vendas.length > 0
                            ? new Date(clienteSelecionado.vendas[0].criado_em).toLocaleDateString('pt-BR')
                            : '-'}
                        </h4>
                        <small className="text-muted">Última Compra</small>
                      </div>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>

              <h6 className="mb-3">Histórico de Compras</h6>
              {clienteSelecionado.vendas.length > 0 ? (
                <Table hover responsive>
                  <thead>
                    <tr>
                      <th>Número</th>
                      <th>Data</th>
                      <th>Total</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {clienteSelecionado.vendas.map((venda) => (
                      <tr key={venda.id}>
                        <td>{venda.numero}</td>
                        <td>{new Date(venda.criado_em).toLocaleDateString('pt-BR')}</td>
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
                      </tr>
                    ))}
                  </tbody>
                </Table>
              ) : (
                <Alert variant="info">Nenhuma compra registrada para este cliente.</Alert>
              )}
            </>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDetalhes(false)}>
            Fechar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Clientes;


