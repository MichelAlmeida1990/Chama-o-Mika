import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert, Badge, Row, Col } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus, FiEye } from 'react-icons/fi';

const Vendas = () => {
  const [vendas, setVendas] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDetalhes, setShowDetalhes] = useState(false);
  const [vendaSelecionada, setVendaSelecionada] = useState(null);
  const [formData, setFormData] = useState({
    cliente: null,
    cliente_nome: '',
    desconto: 0,
    status: 'CONCLUIDA',
    observacoes: '',
  });
  const [itens, setItens] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    loadVendas();
    loadProdutos();
    loadClientes();
  }, []);

  const loadVendas = async () => {
    try {
      const response = await api.get('/api/vendas/');
      setVendas(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar vendas:', error);
    }
  };

  const loadProdutos = async () => {
    try {
      const response = await api.get('/api/produtos/?ativo=true');
      setProdutos(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    }
  };

  const loadClientes = async () => {
    try {
      const response = await api.get('/api/clientes/?ativo=true');
      setClientes(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (itens.length === 0) {
      setError('Adicione pelo menos um item à venda');
      return;
    }

    try {
      const vendaData = {
        ...formData,
        itens_data: itens.map(item => ({
          produto: item.produto,
          quantidade: item.quantidade,
          preco_unitario: item.preco_unitario,
        })),
      };

      await api.post('/api/vendas/', vendaData);
      setShowModal(false);
      resetForm();
      loadVendas();
    } catch (error) {
      setError(error.response?.data?.message || 'Erro ao salvar venda');
    }
  };

  const adicionarItem = () => {
    const produtoSelecionado = produtos.find(p => p.id === parseInt(document.getElementById('produto-select').value));
    if (!produtoSelecionado) return;

    const quantidade = parseInt(document.getElementById('quantidade-input').value) || 1;
    if (quantidade > produtoSelecionado.quantidade) {
      alert('Quantidade maior que o estoque disponível');
      return;
    }

    setItens([
      ...itens,
      {
        produto: produtoSelecionado.id,
        produto_nome: produtoSelecionado.nome,
        quantidade,
        preco_unitario: parseFloat(produtoSelecionado.preco_venda),
        subtotal: quantidade * parseFloat(produtoSelecionado.preco_venda),
      },
    ]);
  };

  const removerItem = (index) => {
    setItens(itens.filter((_, i) => i !== index));
  };

  const calcularTotal = () => {
    const subtotal = itens.reduce((sum, item) => sum + item.subtotal, 0);
    return subtotal - (parseFloat(formData.desconto) || 0);
  };

  const resetForm = () => {
    setFormData({
      cliente: null,
      cliente_nome: '',
      desconto: 0,
      status: 'CONCLUIDA',
      observacoes: '',
    });
    setItens([]);
  };

  const verDetalhes = async (venda) => {
    try {
      const response = await api.get(`/api/vendas/${venda.id}/`);
      setVendaSelecionada(response.data);
      setShowDetalhes(true);
    } catch (error) {
      console.error('Erro ao carregar detalhes da venda:', error);
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
        <h2>Vendas</h2>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Nova Venda
        </Button>
      </div>

      <Card>
        <Card.Body>
          <Table responsive>
            <thead>
              <tr>
                <th>Número</th>
                <th>Cliente</th>
                <th>Total</th>
                <th>Status</th>
                <th>Data</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {vendas.map((venda) => (
                <tr key={venda.id}>
                  <td>{venda.numero}</td>
                  <td>{venda.cliente_nome_display || venda.cliente_nome || venda.cliente || '-'}</td>
                  <td>R$ {parseFloat(venda.total).toFixed(2)}</td>
                  <td>
                    <Badge bg={getStatusBadge(venda.status)}>{venda.status}</Badge>
                  </td>
                  <td>{new Date(venda.criado_em).toLocaleDateString('pt-BR')}</td>
                  <td>
                    <Button
                      variant="outline-info"
                      size="sm"
                      onClick={() => verDetalhes(venda)}
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
          <Modal.Title>Nova Venda</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Cliente</Form.Label>
                  <Form.Select
                    value={formData.cliente || ''}
                    onChange={(e) => {
                      const clienteId = e.target.value ? parseInt(e.target.value) : null;
                      const clienteSelecionado = clientes.find(c => c.id === clienteId);
                      setFormData({
                        ...formData,
                        cliente: clienteId,
                        cliente_nome: clienteSelecionado ? clienteSelecionado.nome : '',
                      });
                    }}
                  >
                    <option value="">Selecione um cliente ou digite o nome</option>
                    {clientes.map((cliente) => (
                      <option key={cliente.id} value={cliente.id}>
                        {cliente.nome} {cliente.cpf_cnpj ? `(${cliente.cpf_cnpj})` : ''}
                      </option>
                    ))}
                  </Form.Select>
                  {!formData.cliente && (
                    <Form.Control
                      type="text"
                      className="mt-2"
                      placeholder="Ou digite o nome do cliente"
                      value={formData.cliente_nome}
                      onChange={(e) => setFormData({ ...formData, cliente_nome: e.target.value })}
                    />
                  )}
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Desconto (R$)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    min="0"
                    value={formData.desconto}
                    onChange={(e) => setFormData({ ...formData, desconto: parseFloat(e.target.value) || 0 })}
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
            </Row>

            <Card className="mb-3">
              <Card.Header>Itens da Venda</Card.Header>
              <Card.Body>
                <Row className="mb-3">
                  <Col md={6}>
                    <Form.Select id="produto-select">
                      <option value="">Selecione um produto...</option>
                      {produtos.map((prod) => (
                        <option key={prod.id} value={prod.id}>
                          {prod.nome} - {prod.tamanho} - {prod.cor} (Estoque: {prod.quantidade})
                        </option>
                      ))}
                    </Form.Select>
                  </Col>
                  <Col md={3}>
                    <Form.Control
                      id="quantidade-input"
                      type="number"
                      min="1"
                      placeholder="Quantidade"
                      defaultValue="1"
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
              Salvar Venda
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      <Modal show={showDetalhes} onHide={() => setShowDetalhes(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Detalhes da Venda {vendaSelecionada?.numero}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {vendaSelecionada && (
            <div>
              <p><strong>Cliente:</strong> {vendaSelecionada.cliente || '-'}</p>
              <p><strong>Status:</strong> {vendaSelecionada.status}</p>
              <p><strong>Desconto:</strong> R$ {parseFloat(vendaSelecionada.desconto || 0).toFixed(2)}</p>
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
                  {vendaSelecionada.itens?.map((item, index) => (
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
                    <th>R$ {parseFloat(vendaSelecionada.total).toFixed(2)}</th>
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

export default Vendas;

