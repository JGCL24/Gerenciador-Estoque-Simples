import React from 'react'
import ProductModal from './modals/ProductModal'
import MovementModal from './modals/MovementModal'
import SaleModal from './modals/SaleModal'
import QuickAddModal from './modals/QuickAddModal'
import MovementDetailsModal from './modals/MovementDetailsModal'

export default function ModalsContainer({
  modalOpen, modalProduct, closeModal, onCreate, onUpdate,
  movementOpen, movementProduct, closeMovementModal, onCreateMovement,
  saleOpen, saleProduct, closeSaleModal, onCreateSale, products,
  quickAddOpen, quickAddProduct, closeQuickAddModal, onCreateQuickAdd,
  movementDetailsOpen, selectedMovement, closeMovementDetailsModal
}){
  // Encontra o produto relacionado à movimentação selecionada
  const movementDetailProduct = selectedMovement 
    ? products.find(p => p.id === selectedMovement.product_id)
    : null

  return (
    <>
      <ProductModal open={modalOpen} product={modalProduct} onClose={closeModal} onCreate={onCreate} onUpdate={onUpdate} />
      <MovementModal open={movementOpen} product={movementProduct} onClose={closeMovementModal} onSubmit={onCreateMovement} />
      <SaleModal open={saleOpen} products={products} initialProduct={saleProduct} onClose={closeSaleModal} onSubmit={onCreateSale} />
      <QuickAddModal open={quickAddOpen} product={quickAddProduct} onClose={closeQuickAddModal} onSubmit={onCreateQuickAdd} />
      <MovementDetailsModal 
        open={movementDetailsOpen} 
        movement={selectedMovement} 
        product={movementDetailProduct}
        onClose={closeMovementDetailsModal} 
      />
    </>
  )
}
