from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Vendor, MenuItem

vendors = Blueprint('vendors', __name__)

@vendors.route('/', methods=['GET'])
def get_vendors():
    all_vendors = Vendor.query.filter_by(is_open=True).all()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'location': v.location
    } for v in all_vendors]), 200

@vendors.route('/', methods=['POST'])
@jwt_required()
def create_vendor():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_vendor = Vendor(
        name=data['name'],
        location=data['location'],
        owner_id=user_id
    )
    db.session.add(new_vendor)
    db.session.commit()
    return jsonify({'message': 'vendor created', 'id': new_vendor.id}), 201

@vendors.route('/<int:vendor_id>/menu', methods=['GET'])
def get_menu(vendor_id):
    items = MenuItem.query.filter_by(vendor_id=vendor_id).all()
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'price': i.price
    } for i in items]), 200

@vendors.route('/<int:vendor_id>/menu', methods=['POST'])
@jwt_required()
def add_menu_item(vendor_id):
    data = request.get_json()
    item = MenuItem(
        vendor_id=vendor_id,
        name=data['name'],
        price=data['price']
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'item added', 'id': item.id}), 201

@vendors.route('/mine', methods=['GET'])
@jwt_required()
def get_my_vendor():
    user_id = get_jwt_identity()
    vendor = Vendor.query.filter_by(owner_id=user_id).first()
    if not vendor:
        return jsonify({'error': 'no vendor found'}), 404
    return jsonify({'id': vendor.id, 'name': vendor.name, 'location': vendor.location}), 200
