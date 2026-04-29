from . import product_api_blueprint
from .. import db
from ..models import Product
from flask import request, jsonify

@product_api_blueprint.route('/products', methods=['POST'])
def create_product():
    items = []
    for row in Product.query.all():
        items.append(row.to_json())
    
    response = jsonify({'results':items})
    return response

@product_api_blueprint.route('/api/product/create', methods=['POST'])
def post_create():
    name = request.form['name']
    slug = request.form['slug']
    price = request.form['price']
    image = request.form['image']

    item = Product()
    item.name = name
    item.slug = slug
    item.price = price
    item.image = image

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Product added', 'product': item.to_json()})
    return response

