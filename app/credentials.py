from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify
from .models import db, Server  # Use shared db
import os
import os

bp = Blueprint('credentials', __name__)

@bp.route('', methods=['POST'])
def set_credentials():
    data = request.json or {}

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Set the credentials as environment variables for the Flask process.
    # In production, consider more secure storage (e.g., vault or config service)
    os.environ['HPE_FW_USERNAME'] = username
    os.environ['HPE_FW_PASSWORD'] = password

    return jsonify({'message': 'Global credentials set successfully'})
