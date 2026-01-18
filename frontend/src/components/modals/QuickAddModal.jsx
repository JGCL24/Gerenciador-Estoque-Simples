import React from 'react'
import Modal from '../Modal'
import QuickAddForm from '../QuickAddForm'

export default function QuickAddModal({ open, product, onClose, onSubmit }){
  if (!open) return null
  return (
    <Modal id="quick-add-modal" onClose={onClose}>
      <div className="modal-header">
        <h3 id="quick-add-modal-title">Adicionar Produto</h3>
        <button className="close-btn" onClick={onClose}>Fechar</button>
      </div>
      <QuickAddForm initialProduct={product} onSubmit={onSubmit} onCancel={onClose} />
    </Modal>
  )
}