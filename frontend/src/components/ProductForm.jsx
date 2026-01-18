import React, { useState, useEffect, useRef } from 'react'

export default function ProductForm({ initial, onSubmit, onCancel }){
  const [form, setForm] = useState({ name: '', description:'', price:0, quantity:0, min_quantity:0 })
  const [submitting, setSubmitting] = useState(false)
  const nameRef = useRef(null)

  useEffect(()=>{
    if (initial) setForm({ name: initial.name, description: initial.description || '', price: initial.price, quantity: initial.quantity, min_quantity: initial.min_quantity ?? 0 })
    else setForm({ name: '', description:'', price:0, quantity:0, min_quantity:0 })

    // focus the first input when the form mounts (useful inside a modal)
    setTimeout(()=>{ try{ nameRef.current && nameRef.current.focus(); nameRef.current && nameRef.current.select(); } catch(e){} }, 0)
  }, [initial])

  const change = (e)=>{
    if (e.target.type === 'number' && e.target.value !== '' && Number(e.target.value) < 0) return
    const value = e.target.type === 'number' ? (e.target.value === '' ? '' : Number(e.target.value)) : e.target.value
    setForm({...form, [e.target.name]: value })
  }

  const submit = async (e)=>{
    e.preventDefault()
    if (Number(form.price) < 0) return
    // normalize number fields
    const payload = {...form, price: Number(form.price || 0), quantity: Number(form.quantity || 0), min_quantity: Number(form.min_quantity || 0)}
    try{
      setSubmitting(true)
      await onSubmit(payload)
    }catch(err){
      console.error(err)
      alert('Erro ao salvar o produto')
    }finally{
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={submit} className="product-form" aria-label="formulário de produto">
      <label>Nome
        <input name="name" ref={nameRef} placeholder="Nome do produto" value={form.name} onChange={change} required aria-required="true" />
      </label>

      <label>Descrição (opcional)
        <input name="description" placeholder="Escrever descrição" value={form.description} onChange={change} />
      </label>

      <label>Preço
        <input type="number" step="0.01" min={0} name="price" value={form.price} onChange={change} required aria-required="true" />
      </label>

      <label>Quantidade
        <input type="number" min={0} name="quantity" value={form.quantity} onChange={change} required aria-required="true" />
      </label>

      <label>Quantidade mínima (alerta)
        <input disabled={submitting} type="number" name="min_quantity" value={form.min_quantity} onChange={change} min={0} aria-describedby="min-help" />
        <small id="min-help" className="muted">*Defina um valor para ser avisado quando houver estoque baixo. Se for 0, não haverá alerta.</small>
      </label>

      <div style={{display:'flex', gap:8}}>
        <button type="submit" disabled={submitting}>{submitting ? 'Salvando...' : 'Salvar'}</button>
        <button type="button" className="secondary" onClick={onCancel} disabled={submitting}>Cancelar</button>
      </div>
    </form>
  )
}
