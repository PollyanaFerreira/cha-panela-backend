#!/usr/bin/env python3
"""
Ferramenta administrativa para gerenciar itens do chá de cozinha
Use este script para desmarcar itens escolhidos quando necessário
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.item import Item, db

def listar_itens_escolhidos():
    """Lista todos os itens que foram escolhidos"""
    with app.app_context():
        items = Item.query.filter_by(escolhido=True).all()
        if not items:
            print("Nenhum item foi escolhido ainda.")
            return
        
        print("\n=== ITENS ESCOLHIDOS ===")
        for item in items:
            print(f"ID: {item.id} | {item.nome} | Categoria: {item.categoria} | Escolhido por: {item.escolhido_por}")

def desmarcar_item(item_id):
    """Desmarca um item específico"""
    with app.app_context():
        item = Item.query.get(item_id)
        if not item:
            print(f"Item com ID {item_id} não encontrado.")
            return False
        
        if not item.escolhido:
            print(f"Item '{item.nome}' já está disponível.")
            return False
        
        print(f"Desmarcando item: {item.nome} (escolhido por: {item.escolhido_por})")
        item.escolhido = False
        item.escolhido_por = None
        db.session.commit()
        print("Item desmarcado com sucesso!")
        return True

def desmarcar_todos():
    """Desmarca todos os itens (CUIDADO!)"""
    with app.app_context():
        items = Item.query.filter_by(escolhido=True).all()
        if not items:
            print("Nenhum item escolhido para desmarcar.")
            return
        
        confirmacao = input(f"Tem certeza que deseja desmarcar TODOS os {len(items)} itens? (digite 'SIM' para confirmar): ")
        if confirmacao != 'SIM':
            print("Operação cancelada.")
            return
        
        for item in items:
            item.escolhido = False
            item.escolhido_por = None
        
        db.session.commit()
        print(f"Todos os {len(items)} itens foram desmarcados!")

def menu_principal():
    """Menu principal da ferramenta administrativa"""
    while True:
        print("\n" + "="*50)
        print("FERRAMENTA ADMINISTRATIVA - CHÁ DE COZINHA")
        print("Marina & Henrique")
        print("="*50)
        print("1. Listar itens escolhidos")
        print("2. Desmarcar item específico")
        print("3. Desmarcar TODOS os itens")
        print("0. Sair")
        print("-"*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            listar_itens_escolhidos()
        
        elif opcao == "2":
            listar_itens_escolhidos()
            if Item.query.filter_by(escolhido=True).count() > 0:
                try:
                    item_id = int(input("\nDigite o ID do item para desmarcar: "))
                    desmarcar_item(item_id)
                except ValueError:
                    print("ID inválido. Digite apenas números.")
        
        elif opcao == "3":
            desmarcar_todos()
        
        elif opcao == "0":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    print("Iniciando ferramenta administrativa...")
    menu_principal()

