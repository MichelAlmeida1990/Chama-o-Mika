import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert, Badge, Row, Col } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus, FiEye } from 'react-icons/fi';

const Compras = () => {
  const [compras, setCompras] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDetalhes, setShowDetalhes] = useState(false);
  const [compraSelecionada, setCompraSelecionada] = useState(null);
  const [formData, setFormData] = useState({
    fornecedor: '',
    status: 'CONCLUIDA',
    data_vencimento: '',
    observacoes: '',
  });
  const [itens, setItens] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    loadCompras();
    loadProdutos();
  }, []);

  const loadCompras = async () => {
    try {
      const response = await api.get('/api/compras/');
      setCompras(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar compras:', error);
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

    if (itens.length === 0) {
      setError('Adicione pelo menos um item à compra');
      return;
    }

    try {
      const compraData = {
        ...formData,
        itens_data: itens.map(item => ({
          produto: item.produto,
          quantidade: item.quantidade,
          preco_unitario: item.preco_unitario,
        })),
      };

      await api.post('/api/compras/', compraData);
      setShowModal(false);
      resetForm();
      loadCompras();
    } catch (error) {
      setError(error.response?.data?.message || 'Erro ao salvar compra');
    }
  };

  const adicionarItem = () => {
    const produtoSelecionado = produtos.find(p => p.id === parseInt(document.getElementById('produto-select-compra').value));
    if (!produtoSelecionado) return;

    const quantidade = parseInt(document.getElementById('quantidade-input-compra').value) || 1;
    const preco = parseFloat(document.getElementById('preco-input-compra').value) || produtoSelecionado.preco_custo;

    setItens([
      ...itens,
      {
        produto: produtoSelecionado.id,
        produto_nome: produtoSelecionado.nome,
        quantidade,
        preco_unitario: preco,
        subtotal: quantidade * preco,
      },
    ]);
  };

  const removerItem = (index) => {
    setItens(itens.filter((_, i) => i !== index));
  };

  const calcularTotal = () => {
    return itens.reduce((sum, item) => sum + item.subtotal, 0);
  };

  const resetForm = () => {
    setFormData({
      fornecedor: '',
      status: 'CONCLUIDA',
      data_vencimento: '',
      observacoes: '',
    });
    setItens([]);
  };

  const verDetalhes = async (compra) => {
    try {
      const response = await api.get(`/api/compras/${compra.id}/`);
      setCompraSelecionada(response.data);
      setShowDetalhes(true);
    } catch (error) {
      console.error('Erro ao carregar detalhes da compra:', error);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      CONCLUIDA: 'success',
      PENDENTE: 'warning',
      CANCELADA: 'danger',
    };
    return badges[status] || 'secondary';
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Compras</h2>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Nova Compra
        </Button>
      </div>

      <Card>
        <Card.Body>
          <Table responsive>
            <thead>
              <tr>
                <th>Número</th>
                <th>Fornecedor</th>
                <th>Total</th>
                <th>Status</th>
                <th>Data</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {compras.map((compra) => (
                <tr key={compra.id}>
                  <td>{compra.numero}</td>
                  <td>{compra.fornecedor}</td>
                  <td>R$ {parseFloat(compra.total).toFixed(2)}</td>
                  <td>
                    <Badge bg={getStatusBadge(compra.status)}>{compra.status}</Badge>
                  </td>
                  <td>{new Date(compra.criado_em).toLocaleDateString('pt-BR')}</td>
                  <td>
                    <Button
                      variant="outline-info"
                      size="sm"
                      onClick={() => verDetalhes(compra)}
                    >
                      <FiEye />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => { setShowModal(false); resetForm(); }} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Nova Compra</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Fornecedor *</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.fornecedor}
                    onChange={(e) => setFormData({ ...formData, fornecedor: e.target.value })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Status</Form.Label>
                  <Form.Select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="CONCLUIDA">Concluída</option>
                    <option value="PENDENTE">Pendente</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Data Vencimento</Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.data_vencimento}
                    onChange={(e) => setFormData({ ...formData, data_vencimento: e.target.value })}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Card className="mb-3">
              <Card.Header>Itens da Compra</Card.Header>
              <Card.Body>
                <Row className="mb-3">
                  <Col md={4}>
                    <Form.Select id="produto-select-compra">
                      <option value="">Selecione um produto...</option>
                      {produtos.map((prod) => (
                        <option key={prod.id} value={prod.id}>
                          {prod.nome} - {prod.tamanho} - {prod.cor}
                        </option>
                      ))}
                    </Form.Select>
                  </Col>
                  <Col md={2}>
                    <Form.Control
                      id="quantidade-input-compra"
                      type="number"
                      min="1"
                      placeholder="Qtd"
                      defaultValue="1"
                    />
                  </Col>
                  <Col md={3}>
                    <Form.Control
                      id="preco-input-compra"
                      type="number"
                      step="0.01"
                      min="0.01"
                      placeholder="Preço unit."
                    />
                  </Col>
                  <Col md={3}>
                    <Button variant="success" onClick={adicionarItem}>
                      Adicionar
                    </Button>
                  </Col>
                </Row>

                <Table>
                  <thead>
                    <tr>
                      <th>Produto</th>
                      <th>Quantidade</th>
                      <th>Preço Unit.</th>
                      <th>Subtotal</th>
                      <th>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {itens.map((item, index) => (
                      <tr key={index}>
                        <td>{item.produto_nome}</td>
                        <td>{item.quantidade}</td>
                        <td>R$ {item.preco_unitario.toFixed(2)}</td>
                        <td>R$ {item.subtotal.toFixed(2)}</td>
                        <td>
                          <Button
                            variant="outline-danger"
                            size="sm"
                            onClick={() => removerItem(index)}
                          >
                            Remover
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr>
                      <th colSpan="3">Total:</th>
                      <th>R$ {calcularTotal().toFixed(2)}</th>
                      <th></th>
                    </tr>
                  </tfoot>
                </Table>
              </Card.Body>
            </Card>

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
              Salvar Compra
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      <Modal show={showDetalhes} onHide={() => setShowDetalhes(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Detalhes da Compra {compraSelecionada?.numero}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {compraSelecionada && (
            <div>
              <p><strong>Fornecedor:</strong> {compraSelecionada.fornecedor}</p>
              <p><strong>Status:</strong> {compraSelecionada.status}</p>
              <Table>
                <thead>
                  <tr>
                    <th>Produto</th>
                    <th>Quantidade</th>
                    <th>Preço Unit.</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {compraSelecionada.itens?.map((item, index) => (
                    <tr key={index}>
                      <td>{item.produto_nome}</td>
                      <td>{item.quantidade}</td>
                      <td>R$ {parseFloat(item.preco_unitario).toFixed(2)}</td>
                      <td>R$ {parseFloat(item.subtotal).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr>
                    <th colSpan="3">Total:</th>
                    <th>R$ {parseFloat(compraSelecionada.total).toFixed(2)}</th>
                  </tr>
                </tfoot>
              </Table>
            </div>
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

export default Compras;

