from flask import Blueprint, request, jsonify
from models.participante_model import Participante
from views.participante_view import render_participante_list, render_participante_detail
from utils.decorators import jwt_required, roles_required

participante_bp = Blueprint("participante", __name__)

# Obtener todos los participantes
@participante_bp.route("/participantes", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_participantes():
    participantes = Participante.get_all()
    return jsonify(render_participante_list(participantes))

# Obtener un participante por ID
@participante_bp.route("/participantes/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_participante(id):
    participante = Participante.get_by_id(id)
    if participante:
        return jsonify(render_participante_detail(participante))
    return jsonify({"error": "Participante no encontrado"}), 404

# Crear un nuevo participante
@participante_bp.route("/participantes", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_participante():
    data = request.json
    nombre = data.get("nombre")
    apellidos = data.get("apellidos")
    email = data.get("email")
    telefono = data.get("telefono")
    codigo = data.get("codigo")
    tipo_id = data.get("tipo_id")
    iglesia_id = data.get("iglesia_id")
    user_id = data.get("user_id")

    if not all([nombre, apellidos, tipo_id, iglesia_id, user_id]):
        return jsonify({"error": "Faltan datos requeridos"}), 400

    participante = Participante(
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        telefono=telefono,
        codigo=codigo,
        tipo_id=tipo_id,
        iglesia_id=iglesia_id,
        user_id=user_id
    )
    participante.save()
    return jsonify(render_participante_detail(participante)), 201

# Actualizar un participante existente
@participante_bp.route("/participantes/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_participante(id):
    participante = Participante.get_by_id(id)
    if not participante:
        return jsonify({"error": "Participante no encontrado"}), 404

    data = request.json
    nombre = data.get("nombre")
    apellidos = data.get("apellidos")
    email = data.get("email")
    telefono = data.get("telefono")
    codigo = data.get("codigo")
    tipo_id = data.get("tipo_id")
    iglesia_id = data.get("iglesia_id")
    user_id = data.get("user_id")

    participante.update(
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        telefono=telefono,
        codigo=codigo,
        tipo_id=tipo_id,
        iglesia_id=iglesia_id,
        user_id=user_id
    )
    return jsonify(render_participante_detail(participante))

# Eliminar un participante
@participante_bp.route("/participantes/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_participante(id):
    participante = Participante.get_by_id(id)
    if not participante:
        return jsonify({"error": "Participante no encontrado"}), 404
    participante.delete()
    return "", 204
