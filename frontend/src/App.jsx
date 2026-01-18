import React, { useEffect, useState } from 'react'
import { fetchProducts, createProduct, updateProduct, deleteProduct, fetchMovements, createMovement } from './api'

import Toolbar from './components/Toolbar'
import AlertsPanel from './components/AlertsPanel'
import Summary from './components/Summary'
import ProductList from './components/ProductList'
import MovementsCard from './components/MovementsCard'
import ModalsContainer from './components/ModalsContainer'

export default function App(){
  const [products, setProducts] = useState([])
  const [query, setQuery] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [modalProduct, setModalProduct] = useState(null)

  const [movements, setMovements] = useState([])
  const [movementOpen, setMovementOpen] = useState(false)
  const [movementProduct, setMovementProduct] = useState(null)

  const [saleOpen, setSaleOpen] = useState(false)
  const [saleProduct, setSaleProduct] = useState(null)

  const [quickAddOpen, setQuickAddOpen] = useState(false)
  const [quickAddProduct, setQuickAddProduct] = useState(null)

  const [movementDetailsOpen, setMovementDetailsOpen] = useState(false)
  const [selectedMovement, setSelectedMovement] = useState(null)

  const load = async ()=>{
    const data = await fetchProducts()
    setProducts(data)
  }

  useEffect(()=>{
    const cached = loadMovementsCache()
    if (cached.length) setMovements(cached)
    load(); loadMovements()
  }, [])

  const loadMovements = async ()=>{
    try{
      const m = await fetchMovements()
      const cached = loadMovementsCache()
      const merged = mergeMovements(m, cached)
      setMovements(merged)
      saveMovementsCache(merged)
    }catch(err){ console.error(err) }
  }

  const loadMovementsCache = ()=>{
    try{
      const raw = localStorage.getItem('movements_cache')
      const parsed = raw ? JSON.parse(raw) : []
      return Array.isArray(parsed) ? parsed : []
    }catch(e){
      return []
    }
  }

  const saveMovementsCache = (data)=>{
    try{
      localStorage.setItem('movements_cache', JSON.stringify(data))
    }catch(e){}
  }

  const mergeMovements = (primary = [], secondary = [])=>{
    const map = new Map()
    for (const item of [...primary, ...secondary]){
      if (item && item.id != null) map.set(String(item.id), item)
    }
    return Array.from(map.values()).sort((a,b)=> new Date(b.timestamp) - new Date(a.timestamp))
  }

  const openSaleModal = (product)=>{
    setSaleProduct(product || null)
    setSaleOpen(true)
  }
  const closeSaleModal = ()=>{ setSaleOpen(false); setSaleProduct(null) }

  const onCreateSale = async (payload)=>{
    try{
      const { items, total } = payload
      for(const it of items){
        const prod = products.find(p=>p.id === it.product_id)
        if (!prod) throw new Error(`Produto não encontrado: ${it.product_id}`)
        if (prod.quantity < it.quantity) throw new Error(`Estoque insuficiente para ${prod.name}: tem ${prod.quantity}, pediu ${it.quantity}`)
      }

      for(const it of items){
        const note = `Venda: ${it.quantity} x R$ ${it.unit_price.toFixed(2)} = R$ ${it.subtotal.toFixed(2)} — Total: R$ ${total.toFixed(2)}`
        await createMovement({ product_id: it.product_id, type: 'saida', quantity: it.quantity, note })
      }

      await load()
      await loadMovements()
      closeSaleModal()
    }catch(err){
      console.error(err)
      alert(err?.message || 'Erro ao registrar venda')
    }
  }

  const openQuickAddModal = (product)=>{
    setQuickAddProduct(product)
    setQuickAddOpen(true)
  }
  const closeQuickAddModal = ()=>{ setQuickAddOpen(false); setQuickAddProduct(null) }

  const onCreateQuickAdd = async (payload)=>{
    try{
      await createMovement(payload)
      await load()
      await loadMovements()
      closeQuickAddModal()
    }catch(err){
      console.error(err)
      alert(err?.message || 'Erro ao adicionar produto')
    }
  }

  const openMovementDetailsModal = (movement)=>{
    setSelectedMovement(movement)
    setMovementDetailsOpen(true)
  }
  const closeMovementDetailsModal = ()=>{
    setMovementDetailsOpen(false)
    setSelectedMovement(null)
  }

  const openAddModal = ()=>{
    setModalProduct(null)
    setModalOpen(true)
  }

  const openEditModal = (product)=>{
    setModalProduct(product)
    setModalOpen(true)
  }

  const closeModal = ()=>{
    setModalOpen(false)
    setModalProduct(null)
  }

  const openMovementModal = (product)=>{
    setMovementProduct(product)
    setMovementOpen(true)
  }

  const closeMovementModal = ()=>{
    setMovementOpen(false)
    setMovementProduct(null)
  }

  const onCreateMovement = async (payload)=>{
    try{
      await createMovement(payload)
      await load()
      await loadMovements()
      closeMovementModal()
    }catch(err){
      console.error(err)
      alert(err?.message || 'Erro ao registrar movimentação')
    }
  }

  const onCreate = async (payload)=>{
    try{
      await createProduct(payload)
      load()
      loadMovements()
      closeModal()
    }catch(err){
      console.error(err)
      alert('Erro ao criar o produto')
    }
  }

  const onUpdate = async (id, payload)=>{
    try{
      await updateProduct(id, payload)
      load()
      closeModal()
    }catch(err){
      console.error(err)
      alert('Erro ao atualizar o produto')
    }
  }

  const onDelete = async (id)=>{
    if (!confirm('Deseja excluir esse produto?')) return
    await deleteProduct(id)
    load()
    loadMovements()
  }

  const filtered = products.filter(p => {
    const q = query.trim().toLowerCase()
    if (!q) return true
    const name = p.name ? p.name.toLowerCase() : ''
    const desc = p.description ? p.description.toLowerCase() : ''
    return name.includes(q) || desc.includes(q) || String(p.price).includes(q) || String(p.quantity).includes(q)
  })

  const totalItems = products.reduce((s,p)=>s+p.quantity,0)
  const totalValue = products.reduce((s,p)=>s + (p.quantity * p.price),0)
  const lowStock = products.filter(p => (p.min_quantity ?? 0) > 0 && p.quantity < p.min_quantity)

  return (
    <div className="container">
      <div className="header">
        <div>
          <div className="title">Gerenciador de Estoque</div>
        </div>
        <Toolbar query={query} setQuery={setQuery} onOpenAdd={openAddModal} onOpenSale={openSaleModal} />
      </div>

      <AlertsPanel lowStock={lowStock} onQuickAdd={openQuickAddModal} />

      <div className="layout">
        <div className="card main-card">
          <Summary products={products} totalItems={totalItems} totalValue={totalValue} />

          <ProductList filtered={filtered} onEdit={openEditModal} onDelete={onDelete} />

        </div>

        <MovementsCard movements={movements} products={products} onMovementClick={openMovementDetailsModal} />
      </div>

      <ModalsContainer
        modalOpen={modalOpen} modalProduct={modalProduct} closeModal={closeModal} onCreate={onCreate} onUpdate={onUpdate}
        movementOpen={movementOpen} movementProduct={movementProduct} closeMovementModal={closeMovementModal} onCreateMovement={onCreateMovement}
        saleOpen={saleOpen} saleProduct={saleProduct} closeSaleModal={closeSaleModal} onCreateSale={onCreateSale} products={products}
        quickAddOpen={quickAddOpen} quickAddProduct={quickAddProduct} closeQuickAddModal={closeQuickAddModal} onCreateQuickAdd={onCreateQuickAdd}
        movementDetailsOpen={movementDetailsOpen} selectedMovement={selectedMovement} closeMovementDetailsModal={closeMovementDetailsModal}
      />
    </div>
  )
}
