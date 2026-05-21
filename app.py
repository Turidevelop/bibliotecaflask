from flask import Flask, session, redirect, url_for
from dotenv import load_dotenv
import os
from datetime import timedelta

# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask con rutas correctas
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'app', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'app', 'static'))

# Configuración
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key_biblioteca')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Importar blueprints (rutas)
from app.routes import auth_bp, dashboard_bp, libros_bp, usuarios_bp, categorias_bp

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(libros_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(categorias_bp)

@app.route('/')
def index():
    """Redirecciona al dashboard o login según sesión"""
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return "Página no encontrada", 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    return "Error interno del servidor", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
