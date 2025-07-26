from .hpe_redfish import HPERedfishClient
from .models import db, Server
from flask import current_app
from celery_worker import celery  # ✅ Fixed import
from flask import Blueprint, request, jsonify
import os

@celery.task(bind=True)
def flash_firmware_task(self, server_id, username, password, firmware_url):
    """
    Celery task to asynchronously flash firmware on a single server.
    Updates the Server model's status and progress in the database.
    """
    with current_app.app_context():
        server = Server.query.get(server_id)
        if not server:
            return 'Server not found'

    client = HPERedfishClient(server.ip, username, password)

    def progress_callback(progress, message):
        with current_app.app_context():
            s = Server.query.get(server_id)
            if s:
                s.progress = progress
                s.status = message
                db.session.commit()

    if not client.login():
        with current_app.app_context():
            s = Server.query.get(server_id)
            s.status = "Login Failed"
            s.progress = 0
            db.session.commit()
        return 'Login Failed'

    with current_app.app_context():
        s = Server.query.get(server_id)
        s.status = "Flashing Firmware"
        db.session.commit()

    success = client.flash_firmware(firmware_url, progress_callback)
    client.logout()

    with current_app.app_context():
        s = Server.query.get(server_id)
        s.status = "Completed" if success else "Failed"
        s.progress = 100 if success else 0
        db.session.commit()

    return 'Completed' if success else 'Failed'
