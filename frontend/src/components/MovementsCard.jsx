import React from 'react'

export default function MovementsCard({ movements = [], products = [], onMovementClick }){
  return (
    <div className="card movements-card">
      <div className="muted" style={{marginBottom:8}}> <strong> Movimentações recentes </strong></div>
      {movements.length === 0 ? (
        <div className="muted">Nenhuma movimentação registrada</div>
      ) : (
        <div className="movements-list">
          {movements.slice(0,10).map(m => (
            <div 
              key={m.id} 
              className="movement-item clickable" 
              onClick={() => onMovementClick && onMovementClick(m)}
              style={{ cursor: 'pointer' }}
            >
              <div className="movement-left">
                <div className={`movement-type ${m.type === 'entrada' ? 'in' : 'out'}`}>{m.type === 'entrada' ? 'Entrada' : 'Saída'}</div>
                <div className="movement-meta">{products.find(p=>p.id === m.product_id)?.name || '—'} • Qtd: <strong>{m.quantity}</strong></div>
              </div>
              <div className="movement-right">{new Date(m.timestamp).toLocaleString()}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
