
from flask import Blueprint, request, jsonify
from models.cargo_model import Cargo
from views.cargo_view import render_cargo_list, render_cargo_detail
from utils.decorators import jwt_required, roles_required

cargo_bp = Blueprint("cargo", __name__)

# Obtener todos los cargos
@cargo_bp.route("/cargos", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_cargos():
    cargos = Cargo.get_all()
    return jsonify(render_cargo_list(cargos))

# Obtener un cargo por ID
@cargo_bp.route("/cargos/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_cargo(id):
    cargo = Cargo.get_by_id(id)
    if cargo:
        return jsonify(render_cargo_detail(cargo))
    return jsonify({"error": "Cargo no encontrado"}), 404

# Crear un nuevo cargo
@cargo_bp.route("/cargos", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_cargo():
    data = request.json
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "La descripción es requerida"}), 400

    cargo = Cargo(descripcion=descripcion)
    cargo.save()
    return jsonify(render_cargo_detail(cargo)), 201

# Actualizar un cargo existente
@cargo_bp.route("/cargos/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_cargo(id):
    cargo = Cargo.get_by_id(id)
    if not cargo:
        return jsonify({"error": "Cargo no encontrado"}), 404

    data = request.json
    descripcion = data.get("descripcion")

    if descripcion:
        cargo.update(descripcion=descripcion)
    return jsonify(render_cargo_detail(cargo))

# Eliminar un cargo
@cargo_bp.route("/cargos/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_cargo(id):
    cargo = Cargo.get_by_id(id)
    if not cargo:
        return jsonify({"error": "Cargo no encontrado"}), 404
    cargo.delete()
    return "", 204
