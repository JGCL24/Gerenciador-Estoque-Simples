import React from 'react'

export default function ProductCard({ product, onEdit, onDelete }){
  const low = product.quantity < (product.min_quantity ?? 0)
  return (
    <div className="product-card">
      <h3>{product.name} {low && <span style={{color:'#b45309', marginLeft:8, fontSize:12}}> Estoque baixo</span>}</h3>
      <div className="meta">Quantidade: {product.quantity} • Mínimo: {product.min_quantity ?? 0} • Preço: R$ {product.price.toFixed(2)}</div>
      <div style={{display:'flex', gap:8}}>
        <button onClick={onEdit}>Editar</button>
        <button className="btn-danger" onClick={onDelete}>Excluir</button>
      </div>
    </div>
  )
}
