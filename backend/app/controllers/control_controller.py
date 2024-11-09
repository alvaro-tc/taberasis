from flask import Blueprint, request, jsonify
from models.control_model import Control
from views.control_view import render_control_list, render_control_detail
from utils.decorators import jwt_required, roles_required

control_bp = Blueprint("control", __name__)

# Obtener todos los controles
@control_bp.route("/controles", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_controles():
    controles = Control.get_all()
    return jsonify(render_control_list(controles))

# Obtener un control por ID
@control_bp.route("/controles/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_control(id):
    control = Control.get_by_id(id)
    if control:
        return jsonify(render_control_detail(control))
    return jsonify({"error": "Control no encontrado"}), 404

# Crear un nuevo control
@control_bp.route("/controles", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_control():
    data = request.json
    descripcion = data.get("descripcion")
    estado = data.get("estado")
    tipoc_id = data.get("tipoc_id")

    if estado is None or tipoc_id is None:
        return jsonify({"error": "El estado y el ID de tipo de control son requeridos"}), 400

    control = Control(descripcion=descripcion, estado=estado, tipoc_id=tipoc_id)
    control.save()
    return jsonify(render_control_detail(control)), 201

# Actualizar un control existente
@control_bp.route("/controles/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_control(id):
    control = Control.get_by_id(id)
    if not control:
        return jsonify({"error": "Control no encontrado"}), 404

    data = request.json
    descripcion = data.get("descripcion")
    estado = data.get("estado")
    tipoc_id = data.get("tipoc_id")

    control.update(descripcion=descripcion, estado=estado, tipoc_id=tipoc_id)
    return jsonify(render_control_detail(control))

# Eliminar un control
@control_bp.route("/controles/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_control(id):
    control = Control.get_by_id(id)
    if not control:
        return jsonify({"error": "Control no encontrado"}), 404
    control.delete()
    return "", 204
