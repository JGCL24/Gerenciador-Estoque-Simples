import React, { useState, useEffect, useRef } from 'react'

export default function SalesForm({ products, initialProduct, onSubmit, onCancel }){
  const [lines, setLines] = useState([{ product_id: initialProduct?.id ?? (products[0]?.id ?? null), quantity: 1 }])
  const ref = useRef(null)

  useEffect(()=>{
    setLines([{ product_id: initialProduct?.id ?? (products[0]?.id ?? null), quantity: 1 }])
    setTimeout(()=>{ try{ ref.current && ref.current.focus() }catch(e){} }, 0)
  }, [initialProduct, products])

  const updateLine = (idx, patch)=>{
    const next = lines.slice()
    next[idx] = { ...next[idx], ...patch }
    setLines(next)
  }

  const addLine = ()=> setLines([...lines, { product_id: products[0]?.id ?? null, quantity: 1 }])
  const removeLine = (idx)=> setLines(lines.filter((_,i)=>i!==idx))

  const computeLineTotal = (line)=>{
    const p = products.find(x=>String(x.id) === String(line.product_id))
    return (Number(p?.price || 0) * Number(line.quantity || 0))
  }

  const grandTotal = lines.reduce((s,l)=> s + computeLineTotal(l), 0)

  const submit = (e)=>{
    e.preventDefault()
    // validate
    for(const l of lines){
      if (!l.product_id) return alert('Selecione um produto em todas as linhas')
      const q = Number(l.quantity || 0)
      if (!q || q <= 0) return alert('Informe uma quantidade maior que 0 em todas as linhas')
    }

    // prepare items
    const items = lines.map(l => {
      const prod = products.find(x => String(x.id) === String(l.product_id))
      return { product_id: Number(l.product_id), quantity: Number(l.quantity), unit_price: Number(prod?.price ?? 0), subtotal: computeLineTotal(l) }
    })

    onSubmit({ items, total: grandTotal })
  }

  return (
    <form onSubmit={submit} className="product-form" aria-label="formulário de venda">
      {lines.map((line,idx)=> (
        <div key={idx} style={{display:'flex', gap:8, alignItems:'flex-end', marginBottom:8}}>
          <div style={{flex:1}}>
            <label>Produto
              <select ref={idx===0?ref:null} value={line.product_id ?? ''} onChange={(e)=>updateLine(idx, { product_id: e.target.value })}>
                {products.map(p => <option key={p.id} value={p.id}>{p.name} • Qtd: {p.quantity}</option>)}
              </select>
            </label>
          </div>

          <div style={{width:120}}>
            <label>Quantidade
              <input type="number" name="quantity" value={line.quantity} onChange={(e)=>updateLine(idx, { quantity: e.target.value })} min={1} />
            </label>
          </div>

          <div style={{width:140}}>
            <label>Subtotal
              <div style={{padding:8, fontWeight:700}}>R$ {computeLineTotal(line).toFixed(2)}</div>
            </label>
          </div>

          <div style={{width:38}}>
            {lines.length > 1 && <button type="button" className="secondary" onClick={()=>removeLine(idx)} aria-label="Remover linha">✕</button>}
          </div>
        </div>
      ))}

      <div style={{display:'flex', gap:8, marginBottom:10}}>
        <button type="button" className="secondary" onClick={addLine}>Adicionar item</button>
      </div>

      <div style={{marginTop:6, marginBottom:12}}>Total da venda: <strong>R$ {grandTotal.toFixed(2)}</strong></div>

      <div style={{display:'flex', gap:8}}>
        <button type="submit">Registrar venda</button>
        <button type="button" className="secondary" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}