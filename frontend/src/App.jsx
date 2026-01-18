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
  const [gridView, setGridView] = useState(true)
  // modal state
  const [modalOpen, setModalOpen] = useState(false)
  const [modalProduct, setModalProduct] = useState(null)

  // movements
  const [movements, setMovements] = useState([])
  const [movementOpen, setMovementOpen] = useState(false)
  const [movementProduct, setMovementProduct] = useState(null)

  // sales
  const [saleOpen, setSaleOpen] = useState(false)
  const [saleProduct, setSaleProduct] = useState(null)

  // quick add (add stock) modal
  const [quickAddOpen, setQuickAddOpen] = useState(false)
  const [quickAddProduct, setQuickAddProduct] = useState(null)

  // movement details modal
  const [movementDetailsOpen, setMovementDetailsOpen] = useState(false)
  const [selectedMovement, setSelectedMovement] = useState(null)

  const load = async ()=>{
    const data = await fetchProducts()
    setProducts(data)
  }

  useEffect(()=>{ load(); loadMovements() }, [])

  const loadMovements = async ()=>{
    try{
      const m = await fetchMovements()
      setMovements(m)
    }catch(err){ console.error(err) }
  }

  // sales modal
  const openSaleModal = (product)=>{
    setSaleProduct(product || null)
    setSaleOpen(true)
  }
  const closeSaleModal = ()=>{ setSaleOpen(false); setSaleProduct(null) }

  const onCreateSale = async (payload)=>{
    try{
      // payload: { items: [{product_id, quantity, unit_price, subtotal}], total }
      const { items, total } = payload

      // validate available stock for all items
      for(const it of items){
        const prod = products.find(p=>p.id === it.product_id)
        if (!prod) throw new Error(`Produto não encontrado: ${it.product_id}`)
        if (prod.quantity < it.quantity) throw new Error(`Estoque insuficiente para ${prod.name}: tem ${prod.quantity}, pediu ${it.quantity}`)
      }

      // create movements sequentially
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

  // quick add: add stock modal (entrada only)
  const openQuickAddModal = (product)=>{
    setQuickAddProduct(product)
    setQuickAddOpen(true)
  }
  const closeQuickAddModal = ()=>{ setQuickAddOpen(false); setQuickAddProduct(null) }

  const onCreateQuickAdd = async (payload)=>{
    try{
      // payload: { product_id, type: 'entrada', quantity, note }
      await createMovement(payload)
      await load()
      await loadMovements()
      closeQuickAddModal()
    }catch(err){
      console.error(err)
      alert(err?.message || 'Erro ao adicionar produto')
    }
  }

  // movement details modal
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

  // movements modal
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
  // only consider products with a positive configured minimum as candidates for alerts
  const lowStock = products.filter(p => (p.min_quantity ?? 0) > 0 && p.quantity < p.min_quantity)
  const missingMin = products.filter(p => (p.min_quantity ?? 0) <= 0)

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

          <ProductList filtered={filtered} gridView={gridView} setGridView={setGridView} onEdit={openEditModal} onDelete={onDelete} />

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
