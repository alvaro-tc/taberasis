from flask import Blueprint, request, jsonify
from models.tipocontrol_model import Tipocontrol
from views.tipocontrol_view import render_tipocontrol_list, render_tipocontrol_detail
from utils.decorators import jwt_required, roles_required

tipocontrol_bp = Blueprint("tipocontrol", __name__)

# Obtener todos los tipos de control
@tipocontrol_bp.route("/tipocontroles", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_tipocontroles():
    tipocontroles = Tipocontrol.get_all()
    return jsonify(render_tipocontrol_list(tipocontroles))

# Obtener un tipo de control por ID
@tipocontrol_bp.route("/tipocontroles/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_tipocontrol(id):
    tipocontrol = Tipocontrol.get_by_id(id)
    if tipocontrol:
        return jsonify(render_tipocontrol_detail(tipocontrol))
    return jsonify({"error": "Tipo de control no encontrado"}), 404

# Crear un nuevo tipo de control
@tipocontrol_bp.route("/tipocontroles", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_tipocontrol():
    data = request.json
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "La descripción es requerida"}), 400

    tipocontrol = Tipocontrol(descripcion=descripcion)
    tipocontrol.save()
    return jsonify(render_tipocontrol_detail(tipocontrol)), 201

# Actualizar un tipo de control existente
@tipocontrol_bp.route("/tipocontroles/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_tipocontrol(id):
    tipocontrol = Tipocontrol.get_by_id(id)
    if not tipocontrol:
        return jsonify({"error": "Tipo de control no encontrado"}), 404

    data = request.json
    descripcion = data.get("descripcion")

    tipocontrol.update(descripcion=descripcion)
    return jsonify(render_tipocontrol_detail(tipocontrol))

# Eliminar un tipo de control
@tipocontrol_bp.route("/tipocontroles/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_tipocontrol(id):
    tipocontrol = Tipocontrol.get_by_id(id)
    if not tipocontrol:
        return jsonify({"error": "Tipo de control no encontrado"}), 404
    tipocontrol.delete()
    return "", 204
