from flask import Blueprint, jsonify
from app.auth.decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    return jsonify({"message": "Dashboard acessado com"})