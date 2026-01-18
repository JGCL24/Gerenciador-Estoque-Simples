def test_create_movement_entrada_increases_quantity(client):
    # create product
    resp = client.post("/products", json={"name": "ProdEntrada", "quantity": 5})
    pid = resp.json()["id"]

    # create entrada movement
    resp2 = client.post("/movements", json={"product_id": pid, "type": "entrada", "quantity": 3, "note": "recebimento"})
    assert resp2.status_code == 201
    m = resp2.json()
    assert m["product_id"] == pid
    assert m["quantity"] == 3

    # product quantity should be updated
    p = client.get(f"/products/{pid}").json()
    assert p["quantity"] == 8


def test_create_movement_saida_decreases_quantity(client):
    resp = client.post("/products", json={"name": "ProdSaida", "quantity": 10})
    pid = resp.json()["id"]

    resp2 = client.post("/movements", json={"product_id": pid, "type": "saida", "quantity": 4})
    assert resp2.status_code == 201
    assert client.get(f"/products/{pid}").json()["quantity"] == 6


def test_create_movement_cannot_remove_more_than_available(client):
    resp = client.post("/products", json={"name": "ProdLow", "quantity": 2})
    pid = resp.json()["id"]

    resp2 = client.post("/movements", json={"product_id": pid, "type": "saida", "quantity": 5})
    assert resp2.status_code == 400


def test_create_movement_invalid_type_or_product(client):
    # invalid type
    resp = client.post("/products", json={"name": "ProdX", "quantity": 2})
    pid = resp.json()["id"]
    resp2 = client.post("/movements", json={"product_id": pid, "type": "transfer", "quantity": 1})
    assert resp2.status_code == 400

    # invalid product id
    resp3 = client.post("/movements", json={"product_id": 9999, "type": "entrada", "quantity": 1})
    assert resp3.status_code == 404


def test_list_movements(client):
    resp = client.post("/products", json={"name": "MovList", "quantity": 1})
    pid = resp.json()["id"]
    client.post("/movements", json={"product_id": pid, "type": "entrada", "quantity": 1})
    client.post("/movements", json={"product_id": pid, "type": "saida", "quantity": 1})
    r = client.get("/movements")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2
