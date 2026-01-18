import React from 'react'
import ProductCard from './ProductCard'

export default function ProductList({ filtered = [], gridView = true, setGridView = ()=>{}, onEdit = ()=>{}, onDelete = ()=>{} }){
  return (
    <>
      {gridView ? (
        <div className="product-card-grid">
          {filtered.map(p => <ProductCard key={p.id} product={p} onEdit={()=>onEdit(p)} onDelete={()=>onDelete(p.id)} />)}
        </div>
      ) : (
        <table className="table">
          <thead>
            <tr><th>Nome</th><th>Qtd</th><th>Preço</th><th>Ações</th></tr>
          </thead>
          <tbody>
            {filtered.map(p => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>{p.quantity}</td>
                <td>R$ {p.price.toFixed(2)}</td>
                <td className="actions">
                  <button onClick={()=>onEdit(p)}>Editar</button>
                  <button className="btn-danger" onClick={()=>onDelete(p.id)}>Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  )
}
