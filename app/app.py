import os
from flask import Flask, jsonify, request
from models import db, Producto


def create_app(config=None):
    app = Flask(__name__)

    db_uri = (
        config.get('SQLALCHEMY_DATABASE_URI')
        if config
        else os.getenv(
            'DATABASE_URL',
            'postgresql://moncada:moncada123@db:5432/moncada_gold',
        )
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/health')
    def health():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'ok', 'db': 'connected'}), 200
        except Exception as exc:
            return jsonify({'status': 'error', 'db': str(exc)}), 500

    @app.route('/productos', methods=['GET'])
    def list_productos():
        productos = db.session.execute(
            db.select(Producto).order_by(Producto.id)
        ).scalars().all()
        return jsonify([p.to_dict() for p in productos]), 200

    @app.route('/productos/<int:producto_id>', methods=['GET'])
    def get_producto(producto_id):
        producto = db.get_or_404(Producto, producto_id)
        return jsonify(producto.to_dict()), 200

    @app.route('/productos', methods=['POST'])
    def create_producto():
        data = request.get_json()
        producto = Producto(
            nombre=data['nombre'],
            categoria=data['categoria'],
            material=data['material'],
            precio=data['precio'],
            stock=data.get('stock', 0),
        )
        db.session.add(producto)
        db.session.commit()
        return jsonify(producto.to_dict()), 201

    @app.route('/productos/<int:producto_id>', methods=['PUT'])
    def update_producto(producto_id):
        producto = db.get_or_404(Producto, producto_id)
        data = request.get_json()
        for field in ('nombre', 'categoria', 'material', 'precio', 'stock'):
            if field in data:
                setattr(producto, field, data[field])
        db.session.commit()
        return jsonify(producto.to_dict()), 200

    @app.route('/productos/<int:producto_id>', methods=['DELETE'])
    def delete_producto(producto_id):
        producto = db.get_or_404(Producto, producto_id)
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': 'Producto eliminado'}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
