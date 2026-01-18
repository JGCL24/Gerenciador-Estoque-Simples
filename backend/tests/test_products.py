def test_create_and_get_product(client):
    # create product
    resp = client.post("/products", json={
        "name": "Teste Produto",
        "description": "Um produto de teste",
        "price": 9.99,
        "quantity": 10,
        "min_quantity": 1
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] is not None
    assert data["name"] == "Teste Produto"

    # get product by id
    pid = data["id"]
    resp2 = client.get(f"/products/{pid}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["id"] == pid
    assert data2["quantity"] == 10


def test_update_and_delete_product(client):
    # create product
    resp = client.post("/products", json={"name": "UpdateProd", "price": 1.0, "quantity": 5})
    assert resp.status_code == 201
    pid = resp.json()["id"]

    # update
    resp_up = client.put(f"/products/{pid}", json={"price": 2.5, "name": "Updated"})
    assert resp_up.status_code == 200
    up = resp_up.json()
    assert up["price"] == 2.5
    assert up["name"] == "Updated"

    # delete
    resp_del = client.delete(f"/products/{pid}")
    assert resp_del.status_code == 204

    # now get -> 404
    resp_get = client.get(f"/products/{pid}")
    assert resp_get.status_code == 404


def test_list_products(client):
    # ensure list endpoint works
    client.post("/products", json={"name": "P1"})
    client.post("/products", json={"name": "P2"})
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_product_not_found(client):
    resp = client.get("/products/9999")
    assert resp.status_code == 404
