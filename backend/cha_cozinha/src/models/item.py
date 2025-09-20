from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    escolhido = db.Column(db.Boolean, default=False, nullable=False)
    escolhido_por = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Item {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'escolhido': self.escolhido,
            'escolhido_por': self.escolhido_por
        }

