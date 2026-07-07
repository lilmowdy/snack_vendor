from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, MenuItem

orders = Blueprint('orders', __name__)

@orders.route('/', methods=['POST'])
@jwt_required()
def place_order():
    data = request.get_json()
    customer_id = get_jwt_identity()

    total = 0
    for item in data['items']:
        menu_item = MenuItem.query.get(item['item_id'])
        if menu_item:
            total += menu_item.price * item['quantity']

    new_order = Order(
        customer_id=customer_id,
        vendor_id=data['vendor_id'],
        status='placed',
        total=total
    )
    db.session.add(new_order)
    db.session.flush()

    for item in data['items']:
        order_item = OrderItem(
            order_id=new_order.id,
            item_id=item['item_id'],
            quantity=item['quantity']
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'message': 'order placed', 'order_id': new_order.id, 'total': total}), 201

@orders.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'status': order.status,
        'total': order.total,
        'vendor_id': order.vendor_id
    }), 200

@orders.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_status(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'status updated', 'status': order.status}), 200

@orders.route('/vendor', methods=['GET'])
@jwt_required()
def vendor_orders():
    user_id = get_jwt_identity()
    from models import Vendor
    vendor = Vendor.query.filter_by(owner_id=user_id).first()
    if not vendor:
        return jsonify({'error': 'no vendor found for this account'}), 404
    all_orders = Order.query.filter_by(vendor_id=vendor.id).all()
    return jsonify([{
        'id': o.id,
        'status': o.status,
        'total': o.total
    } for o in all_orders]), 200

@orders.route('/mine', methods=['GET'])
@jwt_required()
def my_orders():
    customer_id = get_jwt_identity()
    my = Order.query.filter_by(customer_id=customer_id).order_by(Order.id.desc()).all()
    return jsonify([{
        'id': o.id,
        'status': o.status,
        'total': o.total,
        'vendor_id': o.vendor_id
    } for o in my]), 200
