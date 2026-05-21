from app.database import Database
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """Modelo de Usuario"""
    
    @staticmethod
    def authenticate(email, password):
        """Autentica un usuario por email y contraseña"""
        query = "SELECT id, email, nombre, rol FROM usuarios WHERE email = %s AND activo = 1"
        result = Database.execute_query(query, (email,))
        
        if result:
            user = result[0]
            query_password = "SELECT contrasena FROM usuarios WHERE id = %s"
            password_result = Database.execute_query(query_password, (user['id'],))
            
            if password_result and check_password_hash(password_result[0]['contrasena'], password):
                return user
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Obtiene un usuario por ID"""
        query = "SELECT id, email, nombre, rol FROM usuarios WHERE id = %s AND activo = 1"
        result = Database.execute_query(query, (user_id,))
        return result[0] if result else None
    
    @staticmethod
    def create(email, nombre, password, rol='USUARIO'):
        """Crea un nuevo usuario"""
        hashed_password = generate_password_hash(password)
        query = """
            INSERT INTO usuarios (email, nombre, contrasena, rol, activo) 
            VALUES (%s, %s, %s, %s, 1)
        """
        return Database.execute_update(query, (email, nombre, hashed_password, rol))
    
    @staticmethod
    def get_all():
        """Obtiene todos los usuarios activos"""
        query = "SELECT id, email, nombre, rol, activo FROM usuarios WHERE activo = 1"
        return Database.execute_query(query)
    
    @staticmethod
    def update(user_id, email, nombre, rol):
        """Actualiza un usuario"""
        query = "UPDATE usuarios SET email = %s, nombre = %s, rol = %s WHERE id = %s"
        return Database.execute_update(query, (email, nombre, rol, user_id))
    
    @staticmethod
    def delete(user_id):
        """Marca un usuario como inactivo"""
        query = "UPDATE usuarios SET activo = 0 WHERE id = %s"
        return Database.execute_update(query, (user_id,))


class Libro:
    """Modelo de Libro"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los libros"""
        query = """
            SELECT l.id, l.titulo, l.autor, l.isbn, l.categoria_id, 
                   l.descripcion, l.anio_publicacion, l.cantidad_total, 
                   l.cantidad_disponible, l.estado, c.nombre as categoria
            FROM libros l
            LEFT JOIN categorias c ON l.categoria_id = c.id
            WHERE l.activo = 1
            ORDER BY l.titulo
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(libro_id):
        """Obtiene un libro por ID"""
        query = """
            SELECT l.id, l.titulo, l.autor, l.isbn, l.categoria_id, 
                   l.descripcion, l.anio_publicacion, l.cantidad_total, 
                   l.cantidad_disponible, l.estado, c.nombre as categoria
            FROM libros l
            LEFT JOIN categorias c ON l.categoria_id = c.id
            WHERE l.id = %s AND l.activo = 1
        """
        result = Database.execute_query(query, (libro_id,))
        return result[0] if result else None
    
    @staticmethod
    def create(titulo, autor, isbn, categoria_id, descripcion, anio_publicacion, cantidad_total):
        """Crea un nuevo libro"""
        query = """
            INSERT INTO libros (titulo, autor, isbn, categoria_id, descripcion, 
                               anio_publicacion, cantidad_total, cantidad_disponible, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        return Database.execute_update(query, (titulo, autor, isbn, categoria_id, 
                                               descripcion, anio_publicacion, cantidad_total, cantidad_total))
    
    @staticmethod
    def update(libro_id, titulo, autor, isbn, categoria_id, descripcion, anio_publicacion, cantidad_total):
        """Actualiza un libro"""
        query = """
            UPDATE libros SET titulo = %s, autor = %s, isbn = %s, categoria_id = %s, 
                            descripcion = %s, anio_publicacion = %s, cantidad_total = %s
            WHERE id = %s
        """
        return Database.execute_update(query, (titulo, autor, isbn, categoria_id, 
                                               descripcion, anio_publicacion, cantidad_total, libro_id))
    
    @staticmethod
    def delete(libro_id):
        """Marca un libro como inactivo (soft delete)"""
        query = "UPDATE libros SET activo = 0 WHERE id = %s"
        return Database.execute_update(query, (libro_id,))


class Categoria:
    """Modelo de Categoría"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las categorías"""
        query = "SELECT id, nombre, descripcion FROM categorias WHERE activa = 1 ORDER BY nombre"
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(categoria_id):
        """Obtiene una categoría por ID"""
        query = "SELECT id, nombre, descripcion FROM categorias WHERE id = %s AND activa = 1"
        result = Database.execute_query(query, (categoria_id,))
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, descripcion):
        """Crea una nueva categoría"""
        query = "INSERT INTO categorias (nombre, descripcion, activa) VALUES (%s, %s, 1)"
        return Database.execute_update(query, (nombre, descripcion))
    
    @staticmethod
    def update(categoria_id, nombre, descripcion):
        """Actualiza una categoría"""
        query = "UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s"
        return Database.execute_update(query, (nombre, descripcion, categoria_id))
    
    @staticmethod
    def delete(categoria_id):
        """Marca una categoría como inactiva"""
        query = "UPDATE categorias SET activa = 0 WHERE id = %s"
        return Database.execute_update(query, (categoria_id,))


class Prestamo:
    """Modelo de Préstamo"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los préstamos"""
        query = """
            SELECT p.id, p.usuario_id, p.libro_id, p.fecha_prestamo, 
                   p.fecha_devolcion_esperada, p.fecha_devolucion_real, p.estado,
                   u.nombre as usuario_nombre, u.email as usuario_email, l.titulo as libro_titulo
            FROM prestamos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN libros l ON p.libro_id = l.id
            ORDER BY p.fecha_prestamo DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_activos():
        """Obtiene todos los préstamos activos (libros que tienen los usuarios)"""
        query = """
            SELECT p.id, p.usuario_id, p.libro_id, p.fecha_prestamo, 
                   p.fecha_devolcion_esperada, p.estado,
                   u.nombre as usuario_nombre, u.email as usuario_email, 
                   l.titulo as libro_titulo, l.autor as libro_autor
            FROM prestamos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN libros l ON p.libro_id = l.id
            WHERE p.estado = 'ACTIVO'
            ORDER BY u.nombre, p.fecha_prestamo DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_usuario(usuario_id):
        """Obtiene los préstamos de un usuario"""
        query = """
            SELECT p.id, p.usuario_id, p.libro_id, p.fecha_prestamo, 
                   p.fecha_devolcion_esperada, p.fecha_devolucion_real, p.estado,
                   l.titulo as libro_titulo, l.autor as libro_autor
            FROM prestamos p
            LEFT JOIN libros l ON p.libro_id = l.id
            WHERE p.usuario_id = %s
            ORDER BY p.fecha_prestamo DESC
        """
        return Database.execute_query(query, (usuario_id,))
    
    @staticmethod
    def get_by_id(prestamo_id):
        """Obtiene un préstamo por ID"""
        query = """
            SELECT p.id, p.usuario_id, p.libro_id, p.fecha_prestamo, 
                   p.fecha_devolcion_esperada, p.fecha_devolucion_real, p.estado,
                   u.nombre as usuario_nombre, l.titulo as libro_titulo
            FROM prestamos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN libros l ON p.libro_id = l.id
            WHERE p.id = %s
        """
        result = Database.execute_query(query, (prestamo_id,))
        return result[0] if result else None
    
    @staticmethod
    def create(usuario_id, libro_id, dias=14):
        """Crea un nuevo préstamo"""
        query = """
            INSERT INTO prestamos (usuario_id, libro_id, fecha_devolcion_esperada, estado)
            VALUES (%s, %s, DATE_ADD(CURDATE(), INTERVAL %s DAY), 'ACTIVO')
        """
        return Database.execute_update(query, (usuario_id, libro_id, dias))
    
    @staticmethod
    def recepcionar_devolucion(prestamo_id):
        """Registra la devolución de un libro"""
        query = """
            UPDATE prestamos SET fecha_devolucion_real = CURDATE(), estado = 'DEVUELTO'
            WHERE id = %s
        """
        return Database.execute_update(query, (prestamo_id,))

