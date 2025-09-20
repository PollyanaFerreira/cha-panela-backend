#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.models.user import db
from src.models.item import Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Verificar quantos itens estão escolhidos
    escolhidos = Item.query.filter_by(escolhido=True).all()
    print(f"Itens escolhidos no banco: {len(escolhidos)}")
    
    for item in escolhidos:
        print(f"ID: {item.id}, Nome: {item.nome}, Escolhido por: {item.escolhido_por}")
    
    # Verificar se há algum problema com transações pendentes
    try:
        db.session.commit()
        print("Commit realizado com sucesso")
    except Exception as e:
        print(f"Erro no commit: {e}")
        db.session.rollback()
    
    # Testar uma operação de escrita
    try:
        test_item = Item.query.filter_by(escolhido=False).first()
        if test_item:
            print(f"Testando marcar item {test_item.id} como escolhido...")
            test_item.escolhido = True
            test_item.escolhido_por = "Teste Script"
            db.session.commit()
            
            # Verificar se foi salvo
            updated_item = Item.query.get(test_item.id)
            if updated_item.escolhido:
                print("✅ Teste de escrita bem-sucedido!")
                # Reverter o teste
                updated_item.escolhido = False
                updated_item.escolhido_por = None
                db.session.commit()
                print("✅ Teste revertido com sucesso!")
            else:
                print("❌ Teste de escrita falhou!")
        else:
            print("Nenhum item disponível para teste")
    except Exception as e:
        print(f"❌ Erro no teste de escrita: {e}")
        db.session.rollback()

