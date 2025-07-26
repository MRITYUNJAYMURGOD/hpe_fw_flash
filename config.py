import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hpe_fw_pkg.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDFISH_VERIFY_SSL = False  # Set to True in production
