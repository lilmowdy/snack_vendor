from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()


    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error':'email already exists'}), 400

    hashed_password = generate_password_hash(data['password'])


    new_user = User(
            name = data['name'],
            email = data['email'],
            password = hashed_password,
            role = data['role']
        )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'user created successfully'}), 201
@auth.route('/login',methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error':'invalid credentials'}), 401
    
    token = create_access_token(identity=str(user.id))

    return jsonify({
        'token':token,
        'role':user.role,
        'name':user.name
        }), 200
