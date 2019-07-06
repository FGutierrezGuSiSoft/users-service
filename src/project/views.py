from flask import Blueprint, request, jsonify
from project.models import Usuario
from project import db, bcrypt
import datetime
import jwt

blueprint = Blueprint('routes', __name__)

@blueprint.route('/')
def index():
    return '<h1>Hola</h1>'


@blueprint.route('/register', methods=['POST'])
def register():
    datos = request.get_json()

    name = datos.get('nombre')
    pswd = datos.get('password')

    usuario = Usuario(password=pswd, name=name)

    db.session.add(usuario)
    db.session.commit()

    return jsonify(user_to_dict(usuario)), 201


@blueprint.route('/users')
def users():
    if check_token() is False:
        return 'Forbidden', 403

    usuarios = Usuario.query.all()

    lista_usuarios = []

    for usuario in usuarios:
        lista_usuarios.append(user_to_dict(usuario))

    return jsonify(lista_usuarios), 200


@blueprint.route('/users/<id>', methods=['PUT'])
def update(id):
    if check_token() is False:
        return 'Forbidden', 403
    datos = request.get_json()

    nombre = datos.get('nombre')
    password = datos.get('password')

    usuario = Usuario.query.get_or_404(id)

    usuario.name = nombre
    usuario.password = usuario.generate_password(**datos)

    db.session.add(usuario)
    db.session.commit()

    return jsonify(user_to_dict(usuario)), 200


@blueprint.route('/users/<id>', methods=['DELETE'])
def delete(id):
    if check_token() is False:
        return 'Forbidden', 403
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return '', 204

@blueprint.route('/users/<id>', methods=['GET'])
def get(id):
    if check_token() is False:
        return 'Forbidden', 403
    usuario = Usuario.query.get_or_404(id)

    return jsonify(user_to_dict(usuario)), 200


@blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    nombre = data.get('nombre')
    password = data.get('password')

    usuario = Usuario.query.filter_by(name=nombre).first()

    if usuario is None:
        return 'Not found', 404

    if bcrypt.check_password_hash(usuario.password, password) is False:
        return 'Wrong Password', 400

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': usuario.id
    }

    token = jwt.encode(payload, '123456', algorithm='HS256')

    return token, 200

@blueprint.route('/user_by_token')
def user_by_token():
    user_id = get_token_data()
    if user_id is False:
        return 'Unauthorized', 401

    return get(user_id)

def get_token_data():
    if not check_token():
        return False

    token = request.headers.get('Authorization').split(' ')[1]
    secret = '123456'
    return jwt.decode(token, secret).get('sub')


def check_token():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return False

    partes = auth_header.split(' ')
    if len(partes) != 2:
        return False

    token = partes[1]

    try:
        jwt.decode(token, '123456')
        return True
    except:
        return False

def user_to_dict(usuario):
    return {
        'id': usuario.id,
        'nombre': usuario.name
    }
