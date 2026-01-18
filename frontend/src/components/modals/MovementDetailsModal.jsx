import React from 'react'
import Modal from '../Modal'

export default function MovementDetailsModal({ open, movement, product, onClose }){
  if (!movement) return null

  return (
    <Modal open={open} onClose={onClose}>
      <div className="modal-header">
        <h2>Detalhes da Movimentação</h2>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      <div className="modal-body">
        <div className="detail-row">
          <span className="detail-label">Tipo:</span>
          <span className={`movement-type ${movement.type === 'entrada' ? 'in' : 'out'}`}>
            {movement.type === 'entrada' ? 'Entrada' : 'Saída'}
          </span>
        </div>
        
        <div className="detail-row">
          <span className="detail-label">Produto:</span>
          <span className="detail-value">{product?.name || '—'}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">Quantidade:</span>
          <span className="detail-value"><strong>{movement.quantity}</strong></span>
        </div>

        <div className="detail-row">
          <span className="detail-label">Data e Hora:</span>
          <span className="detail-value">{new Date(movement.timestamp).toLocaleString('pt-BR')}</span>
        </div>

        {movement.note && (
          <div className="detail-row">
            <span className="detail-label">Observação:</span>
            <span className="detail-value">{movement.note}</span>
          </div>
        )}
      </div>
      <div className="modal-footer">
        <button className="btn btn-secondary" onClick={onClose}>Fechar</button>
      </div>
    </Modal>
  )
}
