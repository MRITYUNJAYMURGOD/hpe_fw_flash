from flask import Blueprint, request, jsonify
from .models import db, Server
from .hpe_redfish import HPERedfishClient
import os
from flask import Blueprint, request, jsonify
from .models import db, Server  # Use shared db
import os

bp = Blueprint('servers', __name__)

@bp.route('', methods=['GET'])
def list_servers():
    servers = Server.query.all()
    return jsonify([
        {
            'id': s.id,
            'ip': s.ip,
            'status': s.status,
            'progress': s.progress,
            'message': s.message
        }
        for s in servers
    ])

@bp.route('', methods=['POST'])
def add_server():
    data = request.json
    ip = data.get('ip')
    username = data.get('username') or os.getenv('HPE_FW_USERNAME')
    password = data.get('password') or os.getenv('HPE_FW_PASSWORD')

    if not ip:
        return jsonify({'error': 'IP address required'}), 400
    if not username or not password:
        return jsonify({'error': 'Credentials required'}), 400

    if Server.query.filter_by(ip=ip).first():
        return jsonify({'error': 'Server already exists'}), 400

    client = HPERedfishClient(ip, username, password)
    if not client.login():
        return jsonify({'error': 'Authentication failed with given credentials'}), 400
    client.logout()

    server = Server(ip=ip)
    db.session.add(server)
    db.session.commit()
    return jsonify({'message': f'Server {ip} added', 'id': server.id})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_server(id):
    server = Server.query.get_or_404(id)
    db.session.delete(server)
    db.session.commit()
    return jsonify({'message': 'Server deleted'})
