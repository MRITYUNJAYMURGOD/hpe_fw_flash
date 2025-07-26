"""import requests
from flask import Blueprint, request, jsonify
from .models import db, Server  # Use shared db
import os
BASE_URL = 'http://127.0.0.1:5000'

def test_add_server():
    r = requests.post(f'{BASE_URL}/api/servers', json={"ip": "10.0.0.101", "name": "Server1"})
    print("Add Server:", r.json())

def test_set_creds():
    r = requests.post(f'{BASE_URL}/api/credentials', json={"username": "admin", "password": "password"})
    print("Set Creds:", r.json())

def test_set_firmware():
    url = "https://example.com/firmware.fwpkg"
    r = requests.post(f'{BASE_URL}/api/firmware/url', json={"url": url})
    print("Set Firmware URL:", r.json())

def test_start_flash():
    r = requests.post(f'{BASE_URL}/api/flash/start')
    print("Start Flash:", r.json())

def test_list_servers():
    r = requests.get(f'{BASE_URL}/api/servers')
    print("List Servers:", r.json())

if __name__ == "__main__":
    test_add_server()
    test_set_creds()
    test_set_firmware()
    test_list_servers()
    test_start_flash()
"""