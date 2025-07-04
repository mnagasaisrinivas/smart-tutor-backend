from flask import Flask, request, make_response
from .config import Config
from .extensions import db, migrate, jwt, cors
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, supports_credentials=True,
                   origins=["http://localhost:8080", "http://127.0.0.1:8080"],
                   methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], 
                   allow_headers=['Content-Type', 'Authorization'] )


    # Register Blueprints
    register_routes(app)

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8080")
            response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
            response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        return jsonify({
            "error": "Unprocessable Entity",
            "message": str(err)
        }), 422
    
    
    return app
