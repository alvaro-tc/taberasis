from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from models.user_model import User
from models.token_block_list import TokenBlocklist
from schemas.user_schema import UserSchema
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    roles = data.get("roles", ["user"])
    
    if not username or not password:
        return jsonify({"error": "Se requieren nombre de usuario y contraseña"}), 400

    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El usuario ya existe"}), 409
    
    
    new_user = User(username=username, roles=roles, password=password)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")


    user = User.find_by_username(username)

    if user and user.check_password(password):
        roles = user.get_roles()  # Asegúrate de que esto devuelva una lista.
        
        # Usa una lista de roles como parte de la identidad
        identity = json.dumps({"username": user.username, "roles": roles})
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        logger.info("Usuario autenticado: %s con roles: %s", username, roles)

        return (
            jsonify(
                {
                    "message": "Ha accedido correctamente",
                    "tokens": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    logger.warning("Credenciales inválidas para el usuario: %s", username)
    return jsonify({"error": "Credenciales inválidas"}), 400


@user_bp.route("/whoami", methods=["GET"])
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "username": current_user.username,
                "roles": json.loads(current_user.roles),
                "email": current_user.email,
            },
        }
    )
    
    
@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})

@user_bp.route('/logout', methods=["GET"])
@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify({"message": f"{token_type} token removido exitosamente"}) , 200



@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    claims = get_jwt()

    if claims.get("admin") == True:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=3, type=int)
        
        users = User.query.paginate(page=page, per_page=per_page)
        result = UserSchema().dump(users, many=True)
        
        return (
            jsonify(
                {
                    "users": result,
                }
            ),
            200,
        )

    return jsonify({"message": "No tienes autorizacion para acceder a estp"}), 401

