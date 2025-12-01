from flask import Flask, Blueprint
from flask_cors import CORS
from blueprints.busqueda import busqueda_bp
from blueprints.home import home_bp
from blueprints.usuarios import usuarios_bp
from blueprints.publicaciones import publicaciones_bp
from blueprints.cursos import cursos_bp
from blueprints.resenas import resenas_bp

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  

    api_bp = Blueprint("api", __name__, url_prefix="/api")

    api_bp.register_blueprint(busqueda_bp)
    api_bp.register_blueprint(home_bp)
    api_bp.register_blueprint(usuarios_bp)
    api_bp.register_blueprint(publicaciones_bp)
    api_bp.register_blueprint(cursos_bp)
    api_bp.register_blueprint(resenas_bp)
    
    app.register_blueprint(api_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5050)
