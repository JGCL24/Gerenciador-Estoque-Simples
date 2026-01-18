import React, { useEffect } from 'react'

export default function Modal({ children, onClose, id }){
  useEffect(()=>{
    function onKey(e){ if(e.key === 'Escape') onClose && onClose() }
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', onKey)
    return ()=>{ window.removeEventListener('keydown', onKey); document.body.style.overflow = prev }
  }, [onClose])

  return (
    <div className="modal-overlay" onClick={(e)=>{ if(e.target === e.currentTarget) onClose && onClose() }}>
      <div id={id} className="modal" role="dialog" aria-modal="true" aria-labelledby={id ? `${id}-title` : undefined}>
        {children}
      </div>
    </div>
  )
}