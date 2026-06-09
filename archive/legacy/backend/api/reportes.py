"""
Reportes de actividad (opcional, para admin)
"""

from api.auth import token_required
from flask import Blueprint, jsonify

bp_reportes = Blueprint("reportes", __name__)


@bp_reportes.route("/api/reportes", methods=["GET"])
@token_required
def get_reportes(current_user):
    if str(current_user.get("cr321_rol", "")).lower() != "administrador":
        return jsonify({"message": "No autorizado"}), 403
    # Aquí iría la lógica real de reportes
    return jsonify({"message": "Reportes de actividad (por implementar)"})
