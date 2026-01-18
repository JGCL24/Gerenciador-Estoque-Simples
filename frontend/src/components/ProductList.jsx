import React from 'react'
import ProductCard from './ProductCard'

export default function ProductList({ filtered = [], onEdit = ()=>{}, onDelete = ()=>{} }){
  return (
    <div className="product-card-grid">
      {filtered.map(p => <ProductCard key={p.id} product={p} onEdit={()=>onEdit(p)} onDelete={()=>onDelete(p.id)} />)}
    </div>
  )
}
