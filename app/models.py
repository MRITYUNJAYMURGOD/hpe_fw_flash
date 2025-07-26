from .extensions import db

class Server(db.Model):
    __tablename__ = 'servers'
    id       = db.Column(db.Integer, primary_key=True)
    ip       = db.Column(db.String(64), unique=True, nullable=False)
    name     = db.Column(db.String(128))
    status   = db.Column(db.String(64),  default='Ready')
    progress = db.Column(db.Integer,     default=0)
    message  = db.Column(db.String(256), default='')
