from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.models import User, Libro, Categoria, Prestamo
from app.database import Database
from functools import wraps

# Crear blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
libros_bp = Blueprint('libros', __name__, url_prefix='/libros')
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')
categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

# ============= DECORADORES =============

def login_required(f):
    """Decorador para requerir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir rol ADMIN"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('user_rol') != 'ADMIN':
            return "Acceso denegado: Solo administradores", 403
        return f(*args, **kwargs)
    return decorated_function

# ============= AUTENTICACIÓN =============

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.authenticate(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_nombre'] = user['nombre']
            session['user_rol'] = user['rol']
            session.permanent = True
            return redirect(url_for('dashboard.dashboard'))
        else:
            return render_template('auth/login.html', error='Email o contraseña incorrectos'), 401
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Ruta de registro (solo usuarios normales)"""
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        
        if User.create(email, nombre, password, 'USUARIO'):
            return render_template('auth/registro.html', success=True)
        else:
            return render_template('auth/registro.html', error='Error al registrarse'), 400
    
    return render_template('auth/registro.html')

# ============= DASHBOARD =============

@dashboard_bp.route('/')
@login_required
def dashboard():
    """Panel principal"""
    libros = Libro.get_all()
    prestamos_usuario = Prestamo.get_by_usuario(session['user_id'])
    
    return render_template('dashboard/dashboard.html', 
                         user=session,
                         total_libros=len(libros) if libros else 0,
                         prestamos=prestamos_usuario)

# ============= LIBROS =============

@libros_bp.route('/')
@login_required
def lista_libros():
    """Lista de libros"""
    libros = Libro.get_all()
    return render_template('libros/lista.html', libros=libros)

@libros_bp.route('/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_libro():
    """Crear nuevo libro (solo admin)"""
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        isbn = request.form.get('isbn')
        categoria_id = request.form.get('categoria_id')
        descripcion = request.form.get('descripcion')
        anio_publicacion = request.form.get('anio_publicacion')
        cantidad_total = request.form.get('cantidad_total')
        
        if Libro.create(titulo, autor, isbn, categoria_id, descripcion, anio_publicacion, cantidad_total):
            return redirect(url_for('libros.lista_libros'))
        else:
            return render_template('libros/formulario.html', 
                                 categorias=Categoria.get_all(),
                                 error='Error al crear libro'), 400
    
    categorias = Categoria.get_all()
    return render_template('libros/formulario.html', categorias=categorias)

@libros_bp.route('/<int:libro_id>')
@login_required
def detalle_libro(libro_id):
    """Detalle de un libro"""
    libro = Libro.get_by_id(libro_id)
    if not libro:
        return "Libro no encontrado", 404
    return render_template('libros/detalle.html', libro=libro)

@libros_bp.route('/<int:libro_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_libro(libro_id):
    """Editar un libro (solo admin)"""
    libro = Libro.get_by_id(libro_id)
    if not libro:
        return "Libro no encontrado", 404
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        isbn = request.form.get('isbn')
        categoria_id = request.form.get('categoria_id')
        descripcion = request.form.get('descripcion')
        anio_publicacion = request.form.get('anio_publicacion')
        cantidad_total = request.form.get('cantidad_total')
        
        if Libro.update(libro_id, titulo, autor, isbn, categoria_id, descripcion, anio_publicacion, cantidad_total):
            return redirect(url_for('libros.lista_libros'))
        else:
            return render_template('libros/formulario.html', 
                                 libro=libro,
                                 categorias=Categoria.get_all(),
                                 error='Error al actualizar libro'), 400
    
    categorias = Categoria.get_all()
    return render_template('libros/formulario.html', libro=libro, categorias=categorias)

@libros_bp.route('/<int:libro_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_libro(libro_id):
    """Eliminar un libro (solo admin)"""
    if Libro.delete(libro_id):
        return redirect(url_for('libros.lista_libros'))
    else:
        return "Error al eliminar", 500

# ============= CATEGORÍAS =============

@categorias_bp.route('/')
@admin_required
def lista_categorias():
    """Lista de categorías"""
    categorias = Categoria.get_all()
    return render_template('categorias/lista.html', categorias=categorias)

@categorias_bp.route('/nueva', methods=['GET', 'POST'])
@admin_required
def nueva_categoria():
    """Crear nueva categoría"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        if Categoria.create(nombre, descripcion):
            return redirect(url_for('categorias.lista_categorias'))
        else:
            return render_template('categorias/formulario.html', 
                                 error='Error al crear categoría'), 400
    
    return render_template('categorias/formulario.html')

# ============= USUARIOS (Solo Admin) =============

@usuarios_bp.route('/')
@admin_required
def lista_usuarios():
    """Lista de usuarios (solo admin)"""
    usuarios = User.get_all()
    return render_template('usuarios/lista.html', usuarios=usuarios)

@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_usuario():
    """Crear nuevo usuario (solo admin)"""
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        rol = request.form.get('rol', 'USUARIO')
        
        if User.create(email, nombre, password, rol):
            return redirect(url_for('usuarios.lista_usuarios'))
        else:
            return render_template('usuarios/formulario.html', 
                                 error='Error al crear usuario'), 400
    
    return render_template('usuarios/formulario.html')

@usuarios_bp.route('/<int:usuario_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_usuario(usuario_id):
    """Editar un usuario (solo admin)"""
    usuario = User.get_by_id(usuario_id)
    if not usuario:
        return "Usuario no encontrado", 404
    
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        rol = request.form.get('rol', 'USUARIO')
        
        if User.update(usuario_id, email, nombre, rol):
            return redirect(url_for('usuarios.lista_usuarios'))
        else:
            return render_template('usuarios/formulario.html', 
                                 usuario=usuario,
                                 error='Error al actualizar usuario'), 400
    
    return render_template('usuarios/formulario.html', usuario=usuario)

@usuarios_bp.route('/<int:usuario_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_usuario(usuario_id):
    """Eliminar un usuario (solo admin)"""
    if User.delete(usuario_id):
        return redirect(url_for('usuarios.lista_usuarios'))
    else:
        return "Error al eliminar", 500

# ============= CATEGORÍAS - Rutas adicionales =============

@categorias_bp.route('/<int:categoria_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_categoria(categoria_id):
    """Editar una categoría"""
    categoria = Categoria.get_by_id(categoria_id)
    if not categoria:
        return "Categoría no encontrada", 404
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        if Categoria.update(categoria_id, nombre, descripcion):
            return redirect(url_for('categorias.lista_categorias'))
        else:
            return render_template('categorias/formulario.html', 
                                 categoria=categoria,
                                 error='Error al actualizar categoría'), 400
    
    return render_template('categorias/formulario.html', categoria=categoria)

@categorias_bp.route('/<int:categoria_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_categoria(categoria_id):
    """Eliminar una categoría"""
    if Categoria.delete(categoria_id):
        return redirect(url_for('categorias.lista_categorias'))
    else:
        return "Error al eliminar", 500

# ============= PRÉSTAMOS =============

@libros_bp.route('/<int:libro_id>/solicitar_prestamo', methods=['POST'])
@login_required
def solicitar_prestamo(libro_id):
    """Solicitar préstamo de un libro"""
    libro = Libro.get_by_id(libro_id)
    if not libro:
        return "Libro no encontrado", 404
    
    if libro['cantidad_disponible'] <= 0:
        return render_template('libros/detalle.html', 
                             libro=libro,
                             error='No hay copias disponibles'), 400
    
    if Prestamo.create(session['user_id'], libro_id):
        # Actualizar cantidad disponible
        nueva_cantidad = libro['cantidad_disponible'] - 1
        query = "UPDATE libros SET cantidad_disponible = %s WHERE id = %s"
        Database.execute_update(query, (nueva_cantidad, libro_id))
        
        return redirect(url_for('dashboard.dashboard'))
    else:
        return "Error al solicitar préstamo", 500

@dashboard_bp.route('/prestamos')
@admin_required
def gestionar_prestamos():
    """Panel del admin para gestionar préstamos (ver qué libro tiene cada usuario)"""
    prestamos_activos = Prestamo.get_activos()
    return render_template('dashboard/prestamos.html', prestamos=prestamos_activos)

@dashboard_bp.route('/prestamos/<int:prestamo_id>/recepcionar', methods=['POST'])
@admin_required
def recepcionar_devolucion(prestamo_id):
    """Recepcionar la devolución de un libro"""
    prestamo = Prestamo.get_by_id(prestamo_id)
    if not prestamo:
        return "Préstamo no encontrado", 404
    
    if Prestamo.recepcionar_devolucion(prestamo_id):
        # Actualizar cantidad disponible del libro
        libro = Libro.get_by_id(prestamo['libro_id'])
        nueva_cantidad = libro['cantidad_disponible'] + 1
        query = "UPDATE libros SET cantidad_disponible = %s WHERE id = %s"
        Database.execute_update(query, (nueva_cantidad, prestamo['libro_id']))
        
        return redirect(url_for('dashboard.gestionar_prestamos'))
    else:
        return "Error al recepcionar la devolución", 500
