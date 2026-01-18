const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchProducts(){
  const res = await fetch(`${API_BASE}/products`)
  return res.json()
}

export async function createProduct(payload){
  const res = await fetch(`${API_BASE}/products`, {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function updateProduct(id, payload){
  const res = await fetch(`${API_BASE}/products/${id}`, {
    method: 'PUT', headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function deleteProduct(id){
  return fetch(`${API_BASE}/products/${id}`, { method: 'DELETE' })
}

export async function fetchMovements(){
  const res = await fetch(`${API_BASE}/movements`)
  return res.json()
}

export async function createMovement(payload){
  const res = await fetch(`${API_BASE}/movements`, {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || data.message || 'Failed to create movement')
  return data
}
