-- ================================================
-- BASE DE DATOS BIBLIOTECA
-- ================================================

-- Crear base de datos
DROP DATABASE IF EXISTS biblioteca_db;
CREATE DATABASE biblioteca_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE biblioteca_db;

-- ================================================
-- TABLA: ROLES (catalogo)
-- ================================================
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    permisos_crud ENUM('LEER', 'LEER_CREAR', 'CRUD_COMPLETO') DEFAULT 'LEER',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: USUARIOS
-- ================================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('ADMIN', 'USUARIO') DEFAULT 'USUARIO',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: CATEGORÍAS
-- ================================================
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: LIBROS (Tabla Principal)
-- ================================================
CREATE TABLE libros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    categoria_id INT NOT NULL,
    descripcion TEXT,
    anio_publicacion INT,
    cantidad_total INT DEFAULT 0,
    cantidad_disponible INT DEFAULT 0,
    estado ENUM('DISPONIBLE', 'AGOTADO', 'DESCATALOGADO') DEFAULT 'DISPONIBLE',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT,
    INDEX idx_titulo (titulo),
    INDEX idx_autor (autor),
    INDEX idx_categoria (categoria_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: PRÉSTAMOS (Tabla Intermedia)
-- ================================================
CREATE TABLE prestamos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    libro_id INT NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolcion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE,
    estado ENUM('ACTIVO', 'DEVUELTO', 'RETRASADO') DEFAULT 'ACTIVO',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE RESTRICT,
    INDEX idx_usuario (usuario_id),
    INDEX idx_libro (libro_id),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: AUDITORÍA (Opcional - Mejora)
-- ================================================
CREATE TABLE auditoria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50) NOT NULL,
    registro_id INT,
    descripcion TEXT,
    fecha_accion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha (fecha_accion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- INSERTAR DATOS DE PRUEBA
-- ================================================

-- Roles
INSERT INTO roles (nombre, descripcion, permisos_crud) VALUES
('ADMIN', 'Administrador del sistema', 'CRUD_COMPLETO'),
('USUARIO', 'Usuario normal de la biblioteca', 'LEER_CREAR');

-- Usuarios
INSERT INTO usuarios (email, nombre, contrasena, rol) VALUES
('admin@ajax.com', 'Administrador', 'scrypt:32768:8:1$IC66oNYhzZu10gET$2cf5e8a9248efc7dd0c73a3bcd82d8d2dfa540ad8b70f3e383e2eb324030ceec0bb11c6fb1d88382048721498975f1f71b7096f6392edca88174c1fa6884ba89', 'ADMIN'),
('juanga@ajax.com', 'Juan Garcia', 'scrypt:32768:8:1$xixHAgAhk9vxFFZW$7ee1016852f4cef7aefb7989747e96c95d86f5c8214e11b7961a62f36b4c24edd41a2ca85e64bd05d5dede04b5d05607cf8aa449c9201f8193bdbf63a3be7f6f', 'USUARIO'),
('marilo@ajax.com', 'Maria Lopez', 'scrypt:32768:8:1$xixHAgAhk9vxFFZW$7ee1016852f4cef7aefb7989747e96c95d86f5c8214e11b7961a62f36b4c24edd41a2ca85e64bd05d5dede04b5d05607cf8aa449c9201f8193bdbf63a3be7f6f', 'USUARIO');

-- Categorias
INSERT INTO categorias (nombre, descripcion) VALUES
('Ficcion', 'Novelas, cuentos y obras literarias de ficcion'),
('No Ficcion', 'Ensayos, biografias y obras documentales'),
('Ciencia', 'Libros sobre ciencia, fisica, quimica y biologia'),
('Historia', 'Libros historicos y analisis de eventos historicos'),
('Tecnologia', 'Programacion, informatica y tecnologia'),
('Infantil', 'Libros para niños y adolescentes');

-- Libros
INSERT INTO libros (titulo, autor, isbn, categoria_id, descripcion, anio_publicacion, cantidad_total, cantidad_disponible) VALUES
('Cien años de soledad', 'Gabriel Garcia Marquez', '9780062073556', 1, 'Una novela maestra de la literatura latinoamericana', 1967, 3, 2),
('El quijote', 'Miguel de Cervantes', '9788424142024', 1, 'La novela mas famosa de la literatura española', 1605, 2, 1),
('Breve historia del tiempo', 'Stephen Hawking', '9780553380163', 3, 'Una exploracion del universo y sus misterios', 1988, 2, 2),
('Python para principiantes', 'Mark Lutz', '9781491913895', 5, 'Guia completa para aprender Python', 2013, 4, 3),
('Sapiens', 'Yuval Noah Harari', '9788499927627', 4, 'Una breve historia de la humanidad', 2014, 2, 1);

-- Préstamos de prueba
INSERT INTO prestamos (usuario_id, libro_id, fecha_devolcion_esperada, estado) VALUES
(2, 1, DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'ACTIVO'),
(3, 4, DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'ACTIVO');

-- ================================================
-- ÍNDICES Y OPTIMIZACIÓN
-- ================================================
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);
CREATE INDEX idx_libros_disponibles ON libros(cantidad_disponible, estado);
CREATE INDEX idx_prestamos_activos ON prestamos(estado, usuario_id);

-- ================================================
-- FIN DEL SCRIPT
-- ================================================
COMMIT;
