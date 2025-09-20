import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.item import Item, db

# Lista de itens 
itens_lista = [
    # Cozinha
    ("Abridor de garrafa, lata e saca-rolhas", "Cozinha"),
    ("Airfryer", "Cozinha"),
    ("Assadeiras de vidro, cerâmica ou alumínio", "Cozinha"),
    ("Avental de cozinha", "Cozinha"),
    ("Batedeira", "Cozinha"),
    ("Boleira de vidro ou bambu", "Cozinha"),
    ("Cafeteira", "Cozinha"),
    ("Colher de sobremesa", "Cozinha"),
    ("Colheres de pau e espátulas de silicone", "Cozinha"),
    ("Chaleira", "Cozinha"),
    ("Descascador de legumes", "Cozinha"),
    ("Escorredor de louça", "Cozinha"),
    ("Escorredor de macarrão", "Cozinha"),
    ("Espátula de bolo", "Cozinha"),
    ("Espremedor de alho e limão", "Cozinha"),
    ("Espremedor de limão", "Cozinha"),
    ("Fervedor de água", "Cozinha"),
    ("Formas de bolo e pudim", "Cozinha"),
    ("Forminhas de gelo", "Cozinha"),
    ("Frigideira antiaderente", "Cozinha"),
    ("Jarra de suco", "Cozinha"),
    ("Jogo de copos", "Cozinha"),
    ("Jogo de facas", "Cozinha"),
    ("Jogo de pratos ou jogo de jantar", "Cozinha"),
    ("Jogo de sobremesa", "Cozinha"),
    ("Jogo de talheres", "Cozinha"),
    ("Jogo de xícaras", "Cozinha"),
    ("Liquidificador", "Cozinha"),
    ("Lixeira para cozinha", "Cozinha"),
    ("Luvas térmicas", "Cozinha"),
    ("Medidores (colheres e copos)", "Cozinha"),
    ("Mixer", "Cozinha"),
    ("Panela de arroz", "Cozinha"),
    ("Panos de prato", "Cozinha"),
    ("Peneiras", "Cozinha"),
    ("Petisqueira", "Cozinha"),
    ("Porta papel toalha", "Cozinha"),
    ("Porta-detergente", "Cozinha"),
    ("Ramequim", "Cozinha"),
    ("Ralador", "Cozinha"),
    ("Rolo de massa", "Cozinha"),
    ("Saleiro e pimenteiro", "Cozinha"),
    ("Sanduicheira", "Cozinha"),
    ("Taças de vinho ou cerveja", "Cozinha"),
    ("Tábua de corte", "Cozinha"),
    ("Tapete para cozinha", "Cozinha"),
    ("Tesoura de cozinha", "Cozinha"),
    ("Torradeira", "Cozinha"),
    ("Travessas para servir", "Cozinha"),
    ("Toalha de mesa (4 lugares)", "Cozinha"),
    ("Pipoqueira", "Cozinha"),
    
    # Lavanderia/Área de Serviço
    ("Balde", "Lavanderia/Área de Serviço"),
    ("Ferro de passar roupa", "Lavanderia/Área de Serviço"),
    ("Tábua de passar roupa", "Lavanderia/Área de Serviço"),
    ("Mop spray", "Lavanderia/Área de Serviço"),
    ("Pano de chão", "Lavanderia/Área de Serviço"),
    ("Prendedor", "Lavanderia/Área de Serviço"),
    ("Varal de chão", "Lavanderia/Área de Serviço"),
    
    # Banheiro
    ("Lixeira para banheiro", "Banheiro"),
    ("Tapete para banheiro", "Banheiro"),
    ("Toalha de banho", "Banheiro"),
    ("Toalha de rosto", "Banheiro"),
    
    # Quarto
    ("Edredon", "Quarto"),
    ("Jogo de lençol (Queen)", "Quarto"),
    ("Tapete para quarto", "Quarto"),
    ("Cabides", "Quarto"),
    
    # Sala
    ("Almofada", "Sala"),
    ("Tapete para sala", "Sala")
]

def populate_database():
    with app.app_context():
        # NÃO apagar itens existentes! Apenas adicionar novos.
        novos_itens = 0
        for nome, categoria in itens_lista:
            # Verificar se o item já existe
            if not Item.query.filter_by(nome=nome).first():
                item = Item(nome=nome, categoria=categoria)
                db.session.add(item)
                novos_itens += 1
        
        db.session.commit()
        print(f"{novos_itens} novos itens adicionados! Itens já existentes foram preservados.")

if __name__ == '__main__':
    populate_database()
