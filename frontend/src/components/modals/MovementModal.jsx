import React from 'react'
import Modal from '../Modal'
import MovementForm from '../MovementForm'

export default function MovementModal({ open, product, onClose, onSubmit }){
  if (!open) return null
  return (
    <Modal id="movement-modal" onClose={onClose}>
      <div className="modal-header">
        <h3 id="movement-modal-title">Registrar movimentação</h3>
        <button className="close-btn" onClick={onClose} aria-label="Fechar">×</button>
      </div>
      <MovementForm initialProduct={product} onSubmit={onSubmit} onCancel={onClose} />
    </Modal>
  )
}