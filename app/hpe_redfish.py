import redfish
import urllib3
import time
from config import Config
from flask import Blueprint, request, jsonify
from .models import db, Server  # Use shared db
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HPERedfishClient:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.redfish_obj = None

    def login(self):
        try:
            self.redfish_obj = redfish.redfish_client(
                base_url=f"https://{self.ip}",
                username=self.username,
                password=self.password,
                default_prefix='/redfish/v1',
                timeout=30,
                verify=Config.REDFISH_VERIFY_SSL
            )
            self.redfish_obj.login(auth="session")
            return True
        except Exception as e:
            print(f"[{self.ip}] Login failed: {e}")
            return False

    def logout(self):
        if self.redfish_obj:
            try:
                self.redfish_obj.logout()
            except Exception:
                pass

    def flash_firmware(self, firmware_url, progress_callback=None):
        update_uri = "/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate/"

        try:
            payload = {
                "ImageURI": firmware_url,
                "TransferProtocol": "HTTP"
            }
            response = self.redfish_obj.post(update_uri, body=payload)
            if response.status != 202:
                err_msg = f"Failed to start update: HTTP {response.status}"
                if progress_callback:
                    progress_callback(0, err_msg)
                return False

            task_monitor_url = response.dict.get('@odata.id') or response.dict.get('Location')

            if task_monitor_url:
                task_id = task_monitor_url.split('/')[-1]
                return self._monitor_task(task_id, progress_callback)
            else:
                for i in range(0, 101, 20):
                    if progress_callback:
                        progress_callback(i, 'Flashing in progress...')
                    time.sleep(2)
                if progress_callback:
                    progress_callback(100, 'Flashing complete')
                return True

        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Error: {e}")
            return False

    def _monitor_task(self, task_id, progress_callback):
        task_uri = f"/redfish/v1/TaskService/Tasks/{task_id}"
        try:
            while True:
                response = self.redfish_obj.get(task_uri)
                if response.status != 200:
                    if progress_callback:
                        progress_callback(0, "Failed to get task status")
                    return False
                task_obj = response.dict
                task_state = task_obj.get('TaskState', 'Unknown')
                percent_complete = task_obj.get('PercentComplete', 0)
                if progress_callback:
                    progress_callback(percent_complete, f"Task State: {task_state}")
                if task_state in ['Completed', 'Exception', 'Killed', 'Cancelled']:
                    return task_state == 'Completed'
                time.sleep(3)
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Error: {e}")
            return False
