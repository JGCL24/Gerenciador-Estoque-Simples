import React from 'react'
import Modal from '../Modal'
import ProductForm from '../ProductForm'

export default function ProductModal({ open, product, onClose, onCreate, onUpdate }){
  if (!open) return null
  return (
    <Modal id="product-modal" onClose={onClose}>
      <div className="modal-header">
        <h3 id="product-modal-title">{product ? 'Editar produto' : 'Cadastrar produto'}</h3>
        <button className="close-btn" onClick={onClose} aria-label="Fechar">×</button>
      </div>
      <ProductForm initial={product} onSubmit={product ? (data)=>onUpdate(product.id, data) : onCreate} onCancel={onClose} />
    </Modal>
  )
}