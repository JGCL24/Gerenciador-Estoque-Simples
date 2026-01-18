import React from 'react'

export default function Toolbar({ query, setQuery, onOpenAdd, onOpenSale }){
  return (
    <div className="toolbar">
      <input className="search" placeholder="Pesquisar produto..." value={query} onChange={(e)=>setQuery(e.target.value)} />
      <div style={{display:'flex', gap:10, alignItems:'center'}}>
        <button className="btn add-button" onClick={onOpenAdd} aria-controls="product-modal">Cadastrar Produto</button>
        <button className="btn sales-button" onClick={()=>onOpenSale(null)} aria-controls="sale-modal" title="Registrar venda">Registrar Venda</button>
        <div className="view-toggle" />
      </div>
    </div>
  )
}
