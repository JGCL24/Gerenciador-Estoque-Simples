import React from 'react'

export default function Summary({ products = [], totalItems = 0, totalValue = 0 }){
  return (
    <div className="summary">
      <div className="item"><div className="muted">Produtos</div><strong>{products.length}</strong></div>
      <div className="item"><div className="muted">Total itens</div><strong>{totalItems}</strong></div>
      <div className="item"><div className="muted">Valor em estoque</div><strong>R$ {Number(totalValue).toFixed(2)}</strong></div>
    </div>
  )
}
