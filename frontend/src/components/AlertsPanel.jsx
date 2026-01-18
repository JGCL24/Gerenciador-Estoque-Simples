import React from 'react'

export default function AlertsPanel({ lowStock = [], onQuickAdd }){
  if (!lowStock || lowStock.length === 0) return null
  return (
    <div className="alerts-panel">
      <div className="alerts-title">Produtos abaixo do estoque mínimo ({lowStock.length})</div>
      <div className="alerts-list" style={{marginTop:8}}>
        {lowStock.map(p => (
          <div key={p.id} className="alerts-item">
            <div className="alerts-left">
              <div className="alerts-name">{p.name}</div>
              <div className="alerts-meta">Qtd: <strong>{p.quantity}</strong> • Mín: <strong>{p.min_quantity ?? 0}</strong></div>
            </div>
            <div className="alerts-actions">
              <button className="edit-small" onClick={()=>onQuickAdd(p)}>Adicionar Produto</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
