import subprocess
import time
import urllib.request
import urllib.parse
import json

SERVER_PORT = 8001
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"


def start_server():
    return subprocess.Popen([
        "python", "-m", "uvicorn", "app.main:app", "--port", str(SERVER_PORT)
    ])


def stop_server(proc):
    proc.terminate()
    proc.wait()


def http_request(method, path, data=None, headers=None):
    headers = headers or {}
    if isinstance(data, dict):
        if headers.get("Content-Type") == "application/x-www-form-urlencoded":
            data_bytes = urllib.parse.urlencode(data).encode()
        else:
            data_bytes = json.dumps(data).encode()
            headers.setdefault("Content-Type", "application/json")
    elif data is not None:
        data_bytes = data
    else:
        data_bytes = None
    req = urllib.request.Request(BASE_URL + path, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def setup_module(module):
    global proc
    proc = start_server()
    time.sleep(1)


def teardown_module(module):
    stop_server(proc)


def get_token():
    http_request("POST", "/users/register", {"username": "test", "password": "secret"})
    code, data = http_request(
        "POST",
        "/users/token",
        {"username": "test", "password": "secret"},
    )
    assert code == 200
    return data["access_token"]


def test_product_crud():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # create category for products
    code, cat = http_request("POST", "/categories/", {"name": "Tools"}, headers=headers)
    assert code == 200
    category_id = cat["id"]
    product = {
        "name": "Widget",
        "description": "A useful widget",
        "price": 9.99,
        "in_stock": True,
        "category_id": category_id,
    }
    code, data = http_request("POST", "/products/", product, headers=headers)
    assert code == 200
    product_id = data["id"]

    code, _ = http_request("GET", f"/products/{product_id}", headers=headers)
    assert code == 200

    code, list_data = http_request("GET", "/products/", headers=headers)
    assert code == 200
    assert len(list_data) >= 1

    update = dict(product)
    update["price"] = 12.5
    code, data = http_request("PUT", f"/products/{product_id}", update, headers=headers)
    assert code == 200
    assert data["price"] == 12.5

    code, _ = http_request("DELETE", f"/products/{product_id}", headers=headers)
    assert code == 200

    code, _ = http_request("GET", f"/products/{product_id}", headers=headers)
    assert code == 404


def test_category_and_client_crud():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Categories
    code, data = http_request("POST", "/categories/", {"name": "Gadgets"}, headers=headers)
    assert code == 200
    cat_id = data["id"]

    code, data = http_request("GET", f"/categories/{cat_id}", headers=headers)
    assert code == 200
    assert data["name"] == "Gadgets"

    code, data = http_request("PUT", f"/categories/{cat_id}", {"name": "Widgets"}, headers=headers)
    assert code == 200
    assert data["name"] == "Widgets"

    # Clients
    client = {"name": "Alice", "tel": "123", "email": "a@example.com", "address": "Street"}
    code, data = http_request("POST", "/clients/", client, headers=headers)
    assert code == 200
    client_id = data["id"]

    code, data = http_request("GET", f"/clients/{client_id}", headers=headers)
    assert code == 200
    assert data["name"] == "Alice"

    client_update = dict(client)
    client_update["name"] = "Alice B"
    code, data = http_request("PUT", f"/clients/{client_id}", client_update, headers=headers)
    assert code == 200
    assert data["name"] == "Alice B"

    code, _ = http_request("DELETE", f"/clients/{client_id}", headers=headers)
    assert code == 200

    code, _ = http_request("DELETE", f"/categories/{cat_id}", headers=headers)
    assert code == 200
