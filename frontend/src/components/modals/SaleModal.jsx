import React from 'react'
import Modal from '../Modal'
import SalesForm from '../SalesForm'

export default function SaleModal({ open, products, initialProduct, onClose, onSubmit }){
  if (!open) return null
  return (
    <Modal id="sale-modal" onClose={onClose}>
      <div className="modal-header">
        <h3 id="sale-modal-title">Registrar Venda</h3>
        <button className="close-btn" onClick={onClose} aria-label="Fechar">×</button>
      </div>
      <SalesForm products={products} initialProduct={initialProduct} onSubmit={onSubmit} onCancel={onClose} />
    </Modal>
  )
}