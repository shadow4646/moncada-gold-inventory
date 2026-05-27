import pytest
from app import create_app
from models import db as _db


@pytest.fixture
def app():
    application = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    application.config['TESTING'] = True
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_ok(client):
    r = client.get('/health')
    assert r.status_code == 200
    body = r.get_json()
    assert body['status'] == 'ok'
    assert body['db'] == 'connected'


def test_list_productos_empty(client):
    r = client.get('/productos')
    assert r.status_code == 200
    assert r.get_json() == []


def test_create_producto(client):
    payload = {
        'nombre': 'Anillo Eternidad',
        'categoria': 'anillos',
        'material': 'Oro laminado 18k',
        'precio': 85000,
        'stock': 10,
    }
    r = client.post('/productos', json=payload)
    assert r.status_code == 201
    data = r.get_json()
    assert data['nombre'] == 'Anillo Eternidad'
    assert data['precio'] == 85000.0
    assert data['id'] is not None


def test_list_productos_after_create(client):
    payload = {'nombre': 'Collar Luna', 'categoria': 'collares',
               'material': 'Plata 925', 'precio': 45000, 'stock': 5}
    client.post('/productos', json=payload)
    r = client.get('/productos')
    assert r.status_code == 200
    assert len(r.get_json()) == 1


def test_get_producto(client):
    payload = {'nombre': 'Pulsera Eslabón', 'categoria': 'pulseras',
               'material': 'Oro laminado 18k', 'precio': 65000, 'stock': 8}
    pid = client.post('/productos', json=payload).get_json()['id']

    r = client.get(f'/productos/{pid}')
    assert r.status_code == 200
    assert r.get_json()['nombre'] == 'Pulsera Eslabón'


def test_get_producto_not_found(client):
    r = client.get('/productos/9999')
    assert r.status_code == 404


def test_update_producto(client):
    payload = {'nombre': 'Aretes Perla Gota', 'categoria': 'aretes',
               'material': 'Plata 925', 'precio': 38000, 'stock': 20}
    pid = client.post('/productos', json=payload).get_json()['id']

    r = client.put(f'/productos/{pid}', json={'stock': 5, 'precio': 40000})
    assert r.status_code == 200
    data = r.get_json()
    assert data['stock'] == 5
    assert data['precio'] == 40000.0


def test_update_producto_not_found(client):
    r = client.put('/productos/9999', json={'stock': 1})
    assert r.status_code == 404


def test_delete_producto(client):
    payload = {'nombre': 'Cadena Figaro', 'categoria': 'cadenas',
               'material': 'Oro laminado 18k', 'precio': 95000, 'stock': 10}
    pid = client.post('/productos', json=payload).get_json()['id']

    r = client.delete(f'/productos/{pid}')
    assert r.status_code == 200
    assert r.get_json()['message'] == 'Producto eliminado'

    r = client.get(f'/productos/{pid}')
    assert r.status_code == 404


def test_delete_producto_not_found(client):
    r = client.delete('/productos/9999')
    assert r.status_code == 404
