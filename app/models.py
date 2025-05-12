from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relación con Cita
    citas = db.relationship('Cita', backref='cliente', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Abogado(db.Model):
    __tablename__ = 'abogados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relación con Cita
    citas = db.relationship('Cita', backref='abogado', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    tipo_asunto = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    asunto = db.Column(db.String(300), nullable=False)  # Límite razonable
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con Abogado
    abogado_id = db.Column(db.Integer, db.ForeignKey(
        'abogados.id'), nullable=False)

    # Relación con Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey(
        'clientes.id'), nullable=False)


cliente = db.relationship('Cliente', backref='citas')
