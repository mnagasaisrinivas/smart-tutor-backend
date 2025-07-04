from .auth import auth_bp
from .ask import ask_bp
from .notes import notes_bp
from .quiz import quiz_bp
from .practice import practice_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ask_bp, url_prefix="/api/ask")
    app.register_blueprint(notes_bp, url_prefix="/api/notes")
    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(practice_bp, url_prefix="/api/practice")
