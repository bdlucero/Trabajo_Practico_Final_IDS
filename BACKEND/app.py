from flask import Flask, Blueprint
from flask_cors import CORS
from busqueda import busqueda_bp
  

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  

    api_bp = Blueprint("api", __name__, url_prefix="/api")

    api_bp.register_blueprint(busqueda_bp)
    


    app.register_blueprint(api_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5050)
