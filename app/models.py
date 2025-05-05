from . import db
from datetime import datetime


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    telefono_cliente = db.Column(db.String(20), nullable=False)
    tipo_asunto = db.Column(db.String(50), nullable=False)
    abogado = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
