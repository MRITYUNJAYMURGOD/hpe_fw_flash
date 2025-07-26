from app import create_app
from flask import Blueprint, request, jsonify
import os
from app.models import db, Server
from app.models import db, Server


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
with app.app_context():
    print("\nAvailable routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    with app.app_context():
        print("\nAvailable routes:")
        for rule in app.url_map.iter_rules():
            print(rule)


