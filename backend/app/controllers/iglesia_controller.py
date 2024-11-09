from flask import Blueprint, request, jsonify
from models.iglesia_model import Iglesia
from views.iglesia_view import render_iglesia_list, render_iglesia_detail
from utils.decorators import jwt_required, roles_required

iglesia_bp = Blueprint("iglesia", __name__)

# Obtener todas las iglesias
@iglesia_bp.route("/iglesias", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_iglesias():
    iglesias = Iglesia.get_all()
    return jsonify(render_iglesia_list(iglesias))

# Obtener una iglesia por ID
@iglesia_bp.route("/iglesias/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_iglesia(id):
    iglesia = Iglesia.get_by_id(id)
    if iglesia:
        return jsonify(render_iglesia_detail(iglesia))
    return jsonify({"error": "Iglesia no encontrada"}), 404

# Crear una nueva iglesia
@iglesia_bp.route("/iglesias", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_iglesia():
    data = request.json
    nombre = data.get("nombre")
    area = data.get("area")
    ciudad = data.get("ciudad")
    direccion = data.get("direccion")

    if not nombre or not area or area not in ["urbano", "rural"]:
        return jsonify({"error": "Faltan datos requeridos o área inválida"}), 400

    iglesia = Iglesia(nombre=nombre, area=area, ciudad=ciudad, direccion=direccion)
    iglesia.save()
    return jsonify(render_iglesia_detail(iglesia)), 201

# Actualizar una iglesia existente
@iglesia_bp.route("/iglesias/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_iglesia(id):
    iglesia = Iglesia.get_by_id(id)
    if not iglesia:
        return jsonify({"error": "Iglesia no encontrada"}), 404

    data = request.json
    nombre = data.get("nombre")
    area = data.get("area")
    ciudad = data.get("ciudad")
    direccion = data.get("direccion")

    if area and area not in ["urbano", "rural"]:
        return jsonify({"error": "Área inválida"}), 400

    iglesia.update(nombre=nombre, area=area, ciudad=ciudad, direccion=direccion)
    return jsonify(render_iglesia_detail(iglesia))

# Eliminar una iglesia
@iglesia_bp.route("/iglesias/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_iglesia(id):
    iglesia = Iglesia.get_by_id(id)
    if not iglesia:
        return jsonify({"error": "Iglesia no encontrada"}), 404
    iglesia.delete()
    return "", 204
