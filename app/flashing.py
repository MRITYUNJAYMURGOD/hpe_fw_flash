from flask import Blueprint, request, jsonify
from .models import Server
from .tasks import flash_firmware_task
import os
from flask import Blueprint, request, jsonify
from .models import db, Server  # Use shared db
import os

bp = Blueprint('flashing', __name__)

@bp.route('/start', methods=['POST'])
def start_flash():
    # Fetch all servers from DB
    servers = Server.query.all()

    # Retrieve global credentials and firmware URL from environment
    username = os.getenv('HPE_FW_USERNAME')
    password = os.getenv('HPE_FW_PASSWORD')
    firmware_url = os.getenv('HPE_FW_FIRMWARE_URL')

    if not username or not password or not firmware_url:
        return jsonify({'error': 'Missing credentials or firmware URL'}), 400

    # Dispatch one Celery flashing task per server asynchronously
    task_ids = []
    for server in servers:
        task = flash_firmware_task.delay(server.id, username, password, firmware_url)
        task_ids.append({'server_id': server.id, 'task_id': task.id})

    return jsonify({
        'message': 'Firmware flashing started for all servers',
        'tasks': task_ids
    })

# Optional: Add a route to check flashing task status if you implement tracking
# @bp.route('/status/<task_id>', methods=['GET'])
# def get_flash_status(task_id):
#     # Implement logic to check Celery task status and return progress
#     pass
