from flask import Blueprint, request, jsonify
from models.detacontrol_model import Detacontrol
from views.detacontrol_view import render_detacontrol_list, render_detacontrol_detail
from utils.decorators import jwt_required, roles_required

detacontrol_bp = Blueprint("detacontrol", __name__)

# Obtener todos los detalles de control
@detacontrol_bp.route("/detacontroles", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_detacontroles():
    detacontroles = Detacontrol.get_all()
    return jsonify(render_detacontrol_list(detacontroles))

# Obtener un detalle de control por ID
@detacontrol_bp.route("/detacontroles/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_detacontrol(id):
    detacontrol = Detacontrol.get_by_id(id)
    if detacontrol:
        return jsonify(render_detacontrol_detail(detacontrol))
    return jsonify({"error": "Detalle de control no encontrado"}), 404

# Crear un nuevo detalle de control
@detacontrol_bp.route("/detacontroles", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_detacontrol():
    data = request.json
    estado = data.get("estado")
    control_id = data.get("control_id")
    participante_id = data.get("participante_id")

    if estado is None or control_id is None or participante_id is None:
        return jsonify({"error": "El estado, control_id y participante_id son requeridos"}), 400

    detacontrol = Detacontrol(estado=estado, control_id=control_id, participante_id=participante_id)
    detacontrol.save()
    return jsonify(render_detacontrol_detail(detacontrol)), 201

# Actualizar un detalle de control existente
@detacontrol_bp.route("/detacontroles/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_detacontrol(id):
    detacontrol = Detacontrol.get_by_id(id)
    if not detacontrol:
        return jsonify({"error": "Detalle de control no encontrado"}), 404

    data = request.json
    estado = data.get("estado")
    control_id = data.get("control_id")
    participante_id = data.get("participante_id")

    detacontrol.update(estado=estado, control_id=control_id, participante_id=participante_id)
    return jsonify(render_detacontrol_detail(detacontrol))

# Eliminar un detalle de control
@detacontrol_bp.route("/detacontroles/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_detacontrol(id):
    detacontrol = Detacontrol.get_by_id(id)
    if not detacontrol:
        return jsonify({"error": "Detalle de control no encontrado"}), 404
    detacontrol.delete()
    return "", 204
