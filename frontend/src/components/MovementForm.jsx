import React, { useState, useEffect, useRef } from 'react'

export default function MovementForm({ initialProduct, onSubmit, onCancel }){
  const [type, setType] = useState('entrada')
  const [quantity, setQuantity] = useState(0)
  const [note, setNote] = useState('')
  const inputRef = useRef(null)

  useEffect(()=>{
    setQuantity(0)
    setNote('')
    setType('entrada')
    setTimeout(()=>{ try{ inputRef.current && inputRef.current.focus(); }catch(e){} }, 0)
  }, [initialProduct])

  const submit = (e)=>{
    e.preventDefault()
    const q = Number(quantity || 0)
    if (!q || q <= 0) return alert('Informe uma quantidade maior que 0')
    const payload = { product_id: initialProduct.id, type, quantity: q, note: note || undefined }
    onSubmit(payload)
  }

  return (
    <form onSubmit={submit} className="product-form" aria-label="formulário de movimentação">
      <div style={{marginBottom:8}}><strong>{initialProduct?.name}</strong></div>

      <label>Tipo
        <select name="type" value={type} onChange={(e)=>setType(e.target.value)}>
          <option value="entrada">Entrada</option>
          <option value="saida">Saída</option>
        </select>
      </label>

      <label>Quantidade
        <input ref={inputRef} type="number" name="quantity" value={quantity} onChange={(e)=>setQuantity(e.target.value)} min={1} />
      </label>

      <label>Observação (opcional)
        <input name="note" value={note} onChange={(e)=>setNote(e.target.value)} />
      </label>

      <div style={{display:'flex', gap:8}}>
        <button type="submit">Registrar</button>
        <button type="button" className="secondary" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}