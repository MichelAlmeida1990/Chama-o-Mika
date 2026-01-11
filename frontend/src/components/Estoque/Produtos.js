import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert, Badge, InputGroup, Row, Col } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus, FiEdit, FiTrash2, FiAlertCircle } from 'react-icons/fi';

const Produtos = () => {
  const [produtos, setProdutos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingProduto, setEditingProduto] = useState(null);
  const [formData, setFormData] = useState({
    nome: '',
    categoria: '',
    modelo: '',
    tamanho: 'M',
    cor: '',
    quantidade: 0,
    quantidade_minima: 5,
    preco_custo: 0,
    preco_venda: 0,
    descricao: '',
    imagem: null,
    ativo: true,
  });
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [imagePreview, setImagePreview] = useState(null);

  useEffect(() => {
    loadProdutos();
    loadCategorias();
  }, []);

  const loadProdutos = async () => {
    try {
      let allProdutos = [];
      let nextUrl = '/api/produtos/';
      
      // Buscar todas as páginas de produtos
      while (nextUrl) {
        const response = await api.get(nextUrl);
        const data = response.data;
        
        if (Array.isArray(data)) {
          // Se for array direto, não há paginação
          allProdutos = data;
          break;
        } else {
          // Se tiver paginação, adicionar resultados e buscar próxima página
          allProdutos = allProdutos.concat(data.results || []);
          nextUrl = data.next ? data.next.replace(/^https?:\/\/[^\/]+/, '') : null;
        }
      }
      
      setProdutos(allProdutos);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    }
  };

  const loadCategorias = async () => {
    try {
      const response = await api.get('/api/categorias/');
      setCategorias(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar categorias:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const formDataToSend = new FormData();
      
      // Adicionar campos ao FormData
      Object.keys(formData).forEach(key => {
        if (key === 'imagem' && formData[key]) {
          formDataToSend.append('imagem', formData[key]);
        } else if (key !== 'imagem') {
          formDataToSend.append(key, formData[key]);
        }
      });

      if (editingProduto) {
        await api.put(`/api/produtos/${editingProduto.id}/`, formDataToSend, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      } else {
        await api.post('/api/produtos/', formDataToSend, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      }
      setShowModal(false);
      resetForm();
      loadProdutos();
    } catch (error) {
      setError(error.response?.data?.message || 'Erro ao salvar produto');
    }
  };

  const handleEdit = (produto) => {
    setEditingProduto(produto);
    setFormData({
      nome: produto.nome,
      categoria: produto.categoria,
      modelo: produto.modelo || '',
      tamanho: produto.tamanho,
      cor: produto.cor,
      quantidade: produto.quantidade,
      quantidade_minima: produto.quantidade_minima,
      preco_custo: produto.preco_custo,
      preco_venda: produto.preco_venda,
      descricao: produto.descricao || '',
      imagem: null,
      ativo: produto.ativo,
    });
    setImagePreview(produto.imagem || null);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este produto?')) {
      try {
        await api.delete(`/api/produtos/${id}/`);
        loadProdutos();
      } catch (error) {
        alert('Erro ao excluir produto');
      }
    }
  };

  const resetForm = () => {
    setEditingProduto(null);
    setFormData({
      nome: '',
      categoria: '',
      modelo: '',
      tamanho: 'M',
      cor: '',
      quantidade: 0,
      quantidade_minima: 5,
      preco_custo: 0,
      preco_venda: 0,
      descricao: '',
      imagem: null,
      ativo: true,
    });
    setImagePreview(null);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData({ ...formData, imagem: file });
      
      // Criar preview da imagem
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const filteredProdutos = produtos.filter((produto) =>
    produto.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    produto.cor.toLowerCase().includes(searchTerm.toLowerCase()) ||
    produto.modelo?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Produtos</h2>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Novo Produto
        </Button>
      </div>

      <Card>
        <Card.Body>
          <InputGroup className="mb-3">
            <Form.Control
              type="text"
              placeholder="Buscar produtos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </InputGroup>

          <Table responsive>
            <thead>
              <tr>
                <th>Imagem</th>
                <th>Nome</th>
                <th>Categoria</th>
                <th>Tamanho</th>
                <th>Cor</th>
                <th>Quantidade</th>
                <th>Preço Venda</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {filteredProdutos.map((produto) => (
                <tr key={produto.id}>
                  <td>
                    {produto.imagem ? (
                      <img 
                        src={produto.imagem} 
                        alt={produto.nome}
                        style={{ 
                          width: '50px', 
                          height: '50px', 
                          objectFit: 'cover',
                          borderRadius: '4px'
                        }}
                      />
                    ) : (
                      <div 
                        style={{ 
                          width: '50px', 
                          height: '50px', 
                          backgroundColor: '#f0f0f0',
                          borderRadius: '4px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: '#999',
                          fontSize: '12px'
                        }}
                      >
                        Sem img
                      </div>
                    )}
                  </td>
                  <td>{produto.nome}</td>
                  <td>{produto.categoria_nome || 'N/A'}</td>
                  <td>{produto.tamanho}</td>
                  <td>{produto.cor}</td>
                  <td>
                    {produto.quantidade}
                    {produto.estoque_baixo && (
                      <Badge bg="warning" className="ms-2">
                        <FiAlertCircle /> Baixo
                      </Badge>
                    )}
                  </td>
                  <td>R$ {parseFloat(produto.preco_venda).toFixed(2)}</td>
                  <td>
                    <Badge bg={produto.ativo ? 'success' : 'secondary'}>
                      {produto.ativo ? 'Ativo' : 'Inativo'}
                    </Badge>
                  </td>
                  <td>
                    <Button
                      variant="outline-primary"
                      size="sm"
                      className="me-2"
                      onClick={() => handleEdit(produto)}
                    >
                      <FiEdit />
                    </Button>
                    <Button
                      variant="outline-danger"
                      size="sm"
                      onClick={() => handleDelete(produto.id)}
                    >
                      <FiTrash2 />
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
            {editingProduto ? 'Editar Produto' : 'Novo Produto'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form.Group className="mb-3">
              <Form.Label>Nome *</Form.Label>
              <Form.Control
                type="text"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Categoria *</Form.Label>
              <Form.Select
                value={formData.categoria}
                onChange={(e) => {
                  const novaCategoria = e.target.value;
                  const categoriaSelecionada = categorias.find(cat => cat.id === parseInt(novaCategoria));
                  const isTenis = categoriaSelecionada?.nome?.toLowerCase().includes('tenis') || 
                                 categoriaSelecionada?.nome?.toLowerCase().includes('tênis');
                  
                  // Resetar tamanho quando mudar categoria
                  const novoTamanho = isTenis ? '38' : 'M';
                  setFormData({ ...formData, categoria: novaCategoria, tamanho: novoTamanho });
                }}
                required
              >
                <option value="">Selecione...</option>
                {categorias.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.nome}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Modelo</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.modelo}
                    onChange={(e) => setFormData({ ...formData, modelo: e.target.value })}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Tamanho *</Form.Label>
                  <Form.Select
                    value={formData.tamanho}
                    onChange={(e) => setFormData({ ...formData, tamanho: e.target.value })}
                    required
                  >
                    {(() => {
                      const categoriaSelecionada = categorias.find(cat => cat.id === parseInt(formData.categoria));
                      const isTenis = categoriaSelecionada?.nome?.toLowerCase().includes('tenis') || 
                                     categoriaSelecionada?.nome?.toLowerCase().includes('tênis');
                      
                      if (isTenis) {
                        // Tamanhos numéricos para tênis (34 a 45)
                        return Array.from({ length: 12 }, (_, i) => {
                          const numero = 34 + i;
                          return <option key={numero} value={numero.toString()}>{numero}</option>;
                        });
                      } else {
                        // Tamanhos de roupa (PP, P, M, G, etc.)
                        return (
                          <>
                            <option value="PP">PP</option>
                            <option value="P">P</option>
                            <option value="M">M</option>
                            <option value="G">G</option>
                            <option value="GG">GG</option>
                            <option value="XG">XG</option>
                            <option value="XXG">XXG</option>
                          </>
                        );
                      }
                    })()}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Cor *</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.cor}
                    onChange={(e) => setFormData({ ...formData, cor: e.target.value })}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Quantidade *</Form.Label>
                  <Form.Control
                    type="number"
                    min="0"
                    value={formData.quantidade}
                    onChange={(e) => setFormData({ ...formData, quantidade: parseInt(e.target.value) || 0 })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Qtd. Mínima *</Form.Label>
                  <Form.Control
                    type="number"
                    min="0"
                    value={formData.quantidade_minima}
                    onChange={(e) => setFormData({ ...formData, quantidade_minima: parseInt(e.target.value) || 0 })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Ativo</Form.Label>
                  <Form.Check
                    type="switch"
                    checked={formData.ativo}
                    onChange={(e) => setFormData({ ...formData, ativo: e.target.checked })}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Preço de Custo *</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={formData.preco_custo}
                    onChange={(e) => setFormData({ ...formData, preco_custo: parseFloat(e.target.value) || 0 })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Preço de Venda *</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={formData.preco_venda}
                    onChange={(e) => setFormData({ ...formData, preco_venda: parseFloat(e.target.value) || 0 })}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Form.Group className="mb-3">
              <Form.Label>Descrição</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Imagem do Produto</Form.Label>
              <Form.Control
                type="file"
                accept="image/*"
                onChange={handleImageChange}
              />
              {imagePreview && (
                <div className="mt-3">
                  <p className="mb-2">Preview:</p>
                  <img 
                    src={imagePreview} 
                    alt="Preview"
                    style={{ 
                      maxWidth: '200px', 
                      maxHeight: '200px',
                      objectFit: 'cover',
                      borderRadius: '4px',
                      border: '1px solid #ddd'
                    }}
                  />
                </div>
              )}
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

export default Produtos;

