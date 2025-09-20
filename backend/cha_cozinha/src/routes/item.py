from flask import Blueprint, jsonify, request
from src.models.item import Item, db

item_bp = Blueprint('item', __name__)

@item_bp.route('/items', methods=['GET'])
def get_items():
    """Retorna todos os itens da lista de presentes"""
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@item_bp.route('/items/<int:item_id>/escolher', methods=['POST'])
def escolher_item(item_id):
    """Marca um item como escolhido"""
    data = request.get_json()
    nome_pessoa = data.get('nome_pessoa', 'Anônimo')
    
    item = Item.query.get_or_404(item_id)
    
    if item.escolhido:
        return jsonify({'error': 'Item já foi escolhido'}), 400
    
    item.escolhido = True
    item.escolhido_por = nome_pessoa
    db.session.commit()
    
    return jsonify(item.to_dict())

@item_bp.route('/items/<int:item_id>/desmarcar', methods=['POST'])
def desmarcar_item(item_id):
    """Desmarca um item (para fins de administração)"""
    item = Item.query.get_or_404(item_id)
    
    item.escolhido = False
    item.escolhido_por = None
    db.session.commit()
    
    return jsonify(item.to_dict())

@item_bp.route('/items/reset-all', methods=['POST'])
def reset_all_items():
    """Reseta todos os itens escolhidos (para fins de administração)"""
    try:
        # Atualizar todos os itens para não escolhidos
        Item.query.update({Item.escolhido: False, Item.escolhido_por: None})
        db.session.commit()
        
        total_items = Item.query.count()
        return jsonify({
            'message': 'Todos os itens foram resetados com sucesso',
            'total_items': total_items,
            'escolhidos': 0,
            'disponiveis': total_items
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao resetar itens: {str(e)}'}), 500

@item_bp.route('/items/meus-presentes', methods=['POST'])
def meus_presentes():
    """Retorna os itens escolhidos por uma pessoa específica"""
    data = request.get_json()
    nome_pessoa = data.get('nome_pessoa', '')
    
    if not nome_pessoa:
        return jsonify({'error': 'Nome da pessoa é obrigatório'}), 400
    
    items = Item.query.filter_by(escolhido_por=nome_pessoa, escolhido=True).all()
    return jsonify([item.to_dict() for item in items])

