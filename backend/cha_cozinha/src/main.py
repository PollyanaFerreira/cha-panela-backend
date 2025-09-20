import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.models.item import Item
from src.routes.user import user_bp
from src.routes.item import item_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(item_bp, url_prefix='/api')

db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

db.init_app(app)
with app.app_context():
    db.create_all()
    
    # Verificar quantos itens estão escolhidos ao iniciar
    try:
        escolhidos = Item.query.filter_by(escolhido=True).count()
        print(f"Itens escolhidos ao iniciar: {escolhidos}")
    except Exception as e:
        print(f"Erro ao verificar itens: {e}")

@app.route('/repopulate', methods=['POST'])
def repopulate_db():
    try:
        from populate_db import populate_database
        populate_database()
        return jsonify({"message": "Banco recriado com sucesso com os novos itens!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
