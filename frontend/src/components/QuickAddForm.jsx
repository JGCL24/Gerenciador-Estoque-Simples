import React, { useState, useEffect, useRef } from 'react'

export default function QuickAddForm({ initialProduct, onSubmit, onCancel }){
  const [quantity, setQuantity] = useState(1)
  const [note, setNote] = useState('')
  const ref = useRef(null)

  useEffect(()=>{
    setQuantity(1)
    setNote('')
    setTimeout(()=>{ try{ ref.current && ref.current.focus() }catch(e){} }, 0)
  }, [initialProduct])

  const submit = (e)=>{
    e.preventDefault()
    const q = Number(quantity || 0)
    if (!q || q <= 0) return alert('Informe uma quantidade maior que 0')
    const payload = { product_id: initialProduct.id, type: 'entrada', quantity: q, note: note || undefined }
    onSubmit(payload)
  }

  return (
    <form onSubmit={submit} className="product-form" aria-label="adicionar estoque">
      <div style={{marginBottom:8}}><strong>{initialProduct?.name}</strong></div>

      <label>Quantidade adicionada
        <input ref={ref} type="number" name="quantity" value={quantity} onChange={(e)=>setQuantity(e.target.value)} min={1} />
      </label>

      <label>Observação (opcional)
        <input name="note" value={note} onChange={(e)=>setNote(e.target.value)} />
      </label>

      <div style={{display:'flex', gap:8}}>
        <button type="submit">Adicionar</button>
        <button type="button" className="secondary" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}