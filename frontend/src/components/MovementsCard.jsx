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
            (()=>{
              const isDeleted = m.type === 'excluido'
              const typeLabel = isDeleted ? 'Excluído' : (m.type === 'entrada' ? 'Entrada' : 'Saída')
              const typeClass = isDeleted ? 'deleted' : (m.type === 'entrada' ? 'in' : 'out')
              const productName = (isDeleted ? m.note : null) || products.find(p=>p.id === m.product_id)?.name || '—'
              const clickable = !isDeleted && onMovementClick
              return (
            <div 
              key={m.id} 
              className={`movement-item ${clickable ? 'clickable' : ''}`}
              onClick={() => clickable && onMovementClick(m)}
              style={{ cursor: clickable ? 'pointer' : 'default' }}
            >
              <div className="movement-left">
                <div className={`movement-type ${typeClass}`}>{typeLabel}</div>
                <div className="movement-meta">{productName} • Qtd: <strong>{m.quantity}</strong></div>
              </div>
              <div className="movement-right">{new Date(m.timestamp).toLocaleString()}</div>
            </div>
              )
            })()
          ))}
        </div>
      )}
    </div>
  )
}
