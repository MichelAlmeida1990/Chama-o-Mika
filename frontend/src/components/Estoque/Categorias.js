import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Alert } from 'react-bootstrap';
import api from '../../services/api';
import { FiPlus, FiEdit, FiTrash2 } from 'react-icons/fi';

const Categorias = () => {
  const [categorias, setCategorias] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingCategoria, setEditingCategoria] = useState(null);
  const [formData, setFormData] = useState({ nome: '', descricao: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    loadCategorias();
  }, []);

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

    console.log('Enviando categoria:', formData);
    console.log('Editando:', editingCategoria);

    try {
      let response;
      if (editingCategoria) {
        response = await api.put(`/api/categorias/${editingCategoria.id}/`, formData);
        console.log('Resposta PUT:', response.status, response.data);
      } else {
        response = await api.post('/api/categorias/', formData);
        console.log('Resposta POST:', response.status, response.data);
      }
      setShowModal(false);
      resetForm();
      loadCategorias();
    } catch (error) {
      console.error('Erro completo:', error);
      console.error('Response:', error.response);
      console.error('Data:', error.response?.data);
      setError(error.response?.data?.detail || error.response?.data?.message || 'Erro ao salvar categoria');
    }
  };

  const handleEdit = (categoria) => {
    setEditingCategoria(categoria);
    setFormData({
      nome: categoria.nome,
      descricao: categoria.descricao || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta categoria?')) {
      try {
        await api.delete(`/api/categorias/${id}/`);
        loadCategorias();
      } catch (error) {
        alert('Erro ao excluir categoria');
      }
    }
  };

  const resetForm = () => {
    setEditingCategoria(null);
    setFormData({ nome: '', descricao: '' });
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Categorias</h2>
        <Button variant="primary" onClick={() => { resetForm(); setShowModal(true); }}>
          <FiPlus className="me-2" />
          Nova Categoria
        </Button>
      </div>

      <Card>
        <Card.Body>
          <Table responsive>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Descrição</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {categorias.map((categoria) => (
                <tr key={categoria.id}>
                  <td>{categoria.nome}</td>
                  <td>{categoria.descricao || '-'}</td>
                  <td>
                    <Button
                      variant="outline-primary"
                      size="sm"
                      className="me-2"
                      onClick={() => handleEdit(categoria)}
                    >
                      <FiEdit />
                    </Button>
                    <Button
                      variant="outline-danger"
                      size="sm"
                      onClick={() => handleDelete(categoria.id)}
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
            {editingCategoria ? 'Editar Categoria' : 'Nova Categoria'}
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
              <Form.Label>Descrição</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
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

export default Categorias;





