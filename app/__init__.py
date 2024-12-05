from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi aplikasi (misalnya secret key)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Import routes
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
