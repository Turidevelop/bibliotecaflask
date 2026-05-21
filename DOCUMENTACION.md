# [LIBROS] Biblioteca AJAX - Documentación Completa

## Descripción General

**Sistema de Gestión de Biblioteca** es una aplicación web educativa completa para la gestión de una biblioteca utilizando:
- **Backend:** Flask (Python 3.12.4)
- **Base de Datos:** MySQL 8.0
- **Frontend:** HTML5, CSS3, JavaScript
- **Deploy:** Docker + Docker Compose

### [*] Características Principales

- ✅ Autenticación de usuarios con contraseñas cifradas (scrypt)
- ✅ Sistema de roles (ADMIN y USUARIO) con control de acceso
- ✅ CRUD completo de libros, categorías y usuarios
- ✅ Gestión de préstamos y devoluciones
- ✅ Base de datos relacional con integridad referencial
- ✅ Interfaz web intuitiva y responsiva (mobile + desktop)
- ✅ Dashboard personalizado con estadísticas
- ✅ Sistema de auditoría
- ✅ Soft Delete (datos no se pierden, solo se ocultan)

---

## [->] Requisitos del Sistema

```
✅ Python 3.8+
✅ Docker Desktop (para MySQL)
✅ Puertos 5000 (Flask) y 3306 (MySQL) disponibles
```

---

## 🗂️ Estructura del Proyecto

```
BibliotecaFlask/
├── app/
│   ├── __init__.py              # Inicialización de la app
│   ├── config.py                # Configuración
│   ├── database.py              # Conexión a BD
│   ├── models.py                # Modelos (User, Libro, Categoria, Prestamo)
│   ├── routes.py                # Rutas y controladores
│   ├── templates/               # HTML
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── registro.html
│   │   ├── dashboard/
│   │   │   ├── dashboard.html
│   │   │   └── prestamos.html
│   │   ├── libros/
│   │   │   ├── lista.html
│   │   │   ├── detalle.html
│   │   │   └── formulario.html
│   │   ├── categorias/
│   │   │   ├── lista.html
│   │   │   └── formulario.html
│   │   └── usuarios/
│   │       ├── lista.html
│   │       └── formulario.html
│   └── static/
│       ├── css/
│       │   └── style.css        # Estilos globales
│       └── js/
│           └── main.js          # Scripts globales
├── sql/
│   └── database.sql             # Schema e datos iniciales
├── docker/                       # Archivos Docker
├── app.py                        # Punto de entrada
├── requirements.txt              # Dependencias Python
├── docker-compose.yml            # Orquestación Docker
├── .env                          # Variables de entorno
├── Python Backend.code-profile   # Perfil de desarrollo VS Code
├── README.md                     # Resumen ejecutivo
├── SETUP.md                      # Guía de instalación
├── TEST_REPORT.md                # Reporte de validación
└── DOCUMENTACION.md              # Esta documentación completa
```

---

## [->] Guía de Instalación

### [!] IMPORTANTE
**Flask SIEMPRE se ejecuta con `python app.py`. Docker es SOLO para la base de datos MySQL.**

### Paso 1: Crear Entorno Virtual

```bash
cd "BibliotecaFlask"

# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Levantar MySQL con Docker

```bash
docker-compose up -d mysql
```

⏳ Espera ~10 segundos a que MySQL inicie completamente.

### Paso 4: Ejecutar Flask

```bash
python app.py
```

**Accede a:** http://localhost:5000

---

## 🔐 Credenciales de Prueba

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Admin | admin@ajax.com | admin123 |
| Usuario | juanga@ajax.com | usuario123 |
| Usuario | marilo@ajax.com | usuario123 |

> [+] En la página de login aparecen los botones para copiar rápidamente las credenciales.

---

## [DB] Base de Datos

### Tablas Principales

| Tabla | Descripción |
|-------|-------------|
| `roles` | Catálogo de roles (ADMIN, USUARIO) |
| `usuarios` | Gestión de usuarios registrados |
| `categorias` | Categorías de libros |
| `libros` | Catálogo de libros disponibles |
| `prestamos` | Registro de préstamos activos |
| `auditoria` | Log de auditoría (lista para uso) |

### Inicialización Automática

- **3 usuarios** (1 admin, 2 usuarios normales)
- **6 categorías** (Ficción, No Ficción, Ciencia, Historia, Tecnología, Infantil)
- **5 libros** de prueba con relaciones correctas
- **Relaciones FK** correctamente configuradas

---

## [USR] Roles y Permisos

### ADMIN
- ✅ Acceso a todas las funcionalidades
- ✅ CRUD completo de usuarios
- ✅ CRUD completo de libros y categorías
- ✅ Gestión de préstamos y devoluciones
- ✅ Acceso al dashboard administrativo
- ✅ Ver auditoría

### USUARIO
- ✅ Ver libros disponibles
- ✅ Ver detalles de libros
- ✅ Realizar préstamos
- ✅ Ver sus propios préstamos activos
- ✅ Dashboard personal
- [x] Sin acceso a gestión de usuarios
- [x] Sin acceso a gestión de categorías

---

## [USE] Casos de Uso

### 1. Registrarse como Nuevo Usuario
1. En la página de login, clic en "¿No tienes cuenta? Regístrate"
2. Llenar formulario (Email, Nombre, Contraseña)
3. La contraseña se encripta automáticamente
4. Se asigna rol USUARIO por defecto
5. Redirige a login para ingresar

### 2. Solicitar un Préstamo (Usuario)
1. Login como usuario (juanga@ajax.com / usuario123)
2. Ir a "Ver Libros"
3. Hacer clic en "Ver Detalle" de un libro
4. Clic en "[CLIPBOARD] Solicitar Préstamo"
5. El sistema descuenta la disponibilidad
6. Calcula fecha de devolución (14 días después)
7. El libro aparece en "Tus Préstamos Activos" en el dashboard

### 3. Recepcionar Devolución (Admin)
1. Login como admin (admin@ajax.com / admin123)
2. Dashboard → "Gestión de Préstamos Activos"
3. Ver tabla con todos los préstamos activos del sistema
4. Clic en "✅ Recepcionar" para cada devolución
5. El libro vuelve a estar disponible

### 4. Crear Nuevo Libro (Admin)
1. Login como admin
2. Dashboard → "Agregar Libro" o "Ver Libros" → "Crear"
3. Llenar formulario (Título, Autor, Categoría, Cantidad)
4. Clic en "Guardar"
5. El libro aparece en la lista

### 5. Editar Libro (Admin)
1. Login como admin
2. "Ver Libros"
3. Clic en el libro deseado
4. Clic en "✏️ Editar"
5. El formulario se precarga con los datos actuales
6. Modificar y guardar

### 6. Eliminar Libro (Admin - Soft Delete)
1. Login como admin
2. "Ver Libros"
3. Clic en el libro deseado
4. Clic en "🗑️ Eliminar"
5. El libro se marca como inactivo (no se elimina de BD)
6. Ya no aparece en las búsquedas, pero los datos persisten

### 7. Gestionar Usuarios (Admin)
1. Login como admin
2. "Gestionar Usuarios" en navbar
3. Ver lista de usuarios
4. Crear, editar o eliminar usuarios
5. Asignar roles (ADMIN/USUARIO)

### 8. Gestionar Categorías (Admin)
1. Login como admin
2. "Gestionar Categorías" en navbar
3. Crear, editar o eliminar categorías
4. Las categorías se relacionan automáticamente con libros

---

## [DOCKER] Comandos Docker Útiles

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs específicos de MySQL
docker-compose logs -f mysql

# Parar servicios
docker-compose stop

# Reiniciar servicios
docker-compose restart mysql

# Eliminar todo (sin perder datos - volúmenes persisten)
docker-compose down

# Eliminar todo (incluyendo datos)
docker-compose down -v

# Ejecutar comando en BD
docker-compose exec mysql mysql -u biblioteca_user -p biblioteca_db -e "SELECT * FROM usuarios;"

# Conectar a MySQL interactivamente
docker-compose exec mysql mysql -u biblioteca_user -p
# Contraseña: biblioteca_pass
```

---

## ⚙️ Configuración de Variables de Entorno (.env)

```env
# MySQL
MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=biblioteca_db
MYSQL_USER=biblioteca_user
MYSQL_PASSWORD=biblioteca_pass

# Flask
SECRET_KEY=change_in_production
FLASK_ENV=development
FLASK_DEBUG=True
```

> ⚠️ En producción, cambiar `SECRET_KEY` y `FLASK_DEBUG` a False.

---

## [ARCH] Arquitectura

```
Navegador
    ↓
Flask (app.py, puerto 5000)
    ↓
Blueprints (routes.py)
    ├── auth_bp (login, logout, registro)
    ├── dashboard_bp (panel principal)
    ├── libros_bp (CRUD + solicitar préstamo)
    ├── categorias_bp (CRUD)
    └── usuarios_bp (CRUD)
    ↓
Modelos (models.py)
    ├── User
    ├── Libro
    ├── Categoria
    └── Prestamo
    ↓
database.py (conexión MySQL)
    ↓
MySQL 8.0 (puerto 3306)
```

### Rutas Principales

```
GET  /auth/login                          # Página de login
POST /auth/login                          # Procesar login
GET  /auth/registro                       # Página de registro
POST /auth/registro                       # Procesar registro
GET  /auth/logout                         # Logout

GET  /dashboard/                          # Panel principal
GET  /dashboard/prestamos                 # Gestión de préstamos (Admin)

GET  /libros/                             # Listar libros
GET  /libros/<id>/                        # Detalle de libro
GET  /libros/crear/                       # Formulario crear (Admin)
POST /libros/crear/                       # Guardar nuevo libro (Admin)
GET  /libros/<id>/editar/                 # Formulario editar (Admin)
POST /libros/<id>/editar/                 # Guardar cambios (Admin)
POST /libros/<id>/eliminar/               # Eliminar libro (Admin)
POST /libros/<id>/solicitar_prestamo/     # Solicitar préstamo (Usuario)

GET  /categorias/                         # Listar categorías (Admin)
GET  /categorias/crear/                   # Formulario crear (Admin)
POST /categorias/crear/                   # Guardar nueva categoría (Admin)
GET  /categorias/<id>/editar/             # Formulario editar (Admin)
POST /categorias/<id>/editar/             # Guardar cambios (Admin)
POST /categorias/<id>/eliminar/           # Eliminar categoría (Admin)

GET  /usuarios/                           # Listar usuarios (Admin)
GET  /usuarios/crear/                     # Formulario crear (Admin)
POST /usuarios/crear/                     # Guardar nuevo usuario (Admin)
GET  /usuarios/<id>/editar/               # Formulario editar (Admin)
POST /usuarios/<id>/editar/               # Guardar cambios (Admin)
POST /usuarios/<id>/eliminar/             # Eliminar usuario (Admin)
```

---

## [TECH] Stack Tecnológico

| Componente | Versión | Descripción |
|-----------|---------|------------|
| Python | 3.12.4 | Runtime principal |
| Flask | 3.0.0 | Framework web |
| MySQL | 8.0 | Base de datos relacional |
| Werkzeug | 3.0.1 | Utilitarios (hashing de contraseñas) |
| mysql-connector-python | 8.2.0 | Driver MySQL |
| python-dotenv | 1.0.0 | Gestión de variables de entorno |
| Docker | Latest | Contenerización |
| Docker Compose | Latest | Orquestación |
| HTML5 | - | Frontend |
| CSS3 | - | Estilos |
| JavaScript | ES6+ | Interactividad |

---

## [FIX] Solución de Problemas

### "Puerto 5000 ya en uso"

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### "No se puede conectar a MySQL"

```bash
# Verificar que el contenedor está corriendo
docker-compose ps

# Si no está, levantarlo
docker-compose up -d mysql

# Reiniciar si hay problemas
docker-compose restart mysql

# Ver logs para diagnóstico
docker-compose logs mysql
```

### "ModuleNotFoundError: Flask o mysql-connector"

```bash
# Verificar que el venv está activado
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # macOS/Linux

# Reinstalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep -i flask
```

### "Base de datos no existe o no se inicializa"

```bash
# Con Docker
docker-compose exec mysql mysql -u root -proot123 < sql/database.sql

# Localmente (si MySQL está instalado)
mysql -u root -proot123 < sql/database.sql

# Verificar tablas
docker-compose exec mysql mysql -u biblioteca_user -p biblioteca_db -e "SHOW TABLES;"
```

### "Cambios en el código no se reflejan"

```bash
# Reiniciar Flask (Ctrl+C y ejecutar nuevamente)
python app.py

# Limpiar archivos compilados de Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### "Error de contraseña en BD"

Verificar que las credenciales en `.env` coinciden con las del `docker-compose.yml`:
```yaml
MYSQL_USER: biblioteca_user
MYSQL_PASSWORD: biblioteca_pass
MYSQL_DATABASE: biblioteca_db
```

---

## 📦 Dependencias Python

```
Flask==2.3.2
mysql-connector-python==8.0.33
Werkzeug==2.3.6
python-dotenv==1.0.0
```

Instalar todas:
```bash
pip install -r requirements.txt
```

---

## [TOOLS] Herramientas de Desarrollo Utilizadas

### Python Backend.code-profile

Este proyecto utilizó el archivo **`Python Backend.code-profile`** que facilita enormemente el desarrollo:

**Beneficios proporcionados:**
- ✅ Configuración automática de extensiones recomendadas (Pylance, Python, etc.)
- ✅ Formateo automático de código (Black, autopep8)
- ✅ Linting integrado (Pylint, Flake8)
- ✅ Debugging configurado para Flask
- ✅ Autocompletado y type hints
- ✅ Ejecución rápida de scripts
- ✅ Gestión de entornos virtuales
- ✅ Configuración de pruebas

**Resultado:** Desarrollo más rápido, código más limpio y menos errores durante la implementación.

---

## ✅ Validación y Pruebas

Todos los requisitos han sido testeados y validados. Ver [TEST_REPORT.md](TEST_REPORT.md) para:
- ✅ Estado de cumplimiento de cada requisito
- ✅ Pruebas realizadas
- ✅ Métricas de calidad
- ✅ Casos de uso verificados
- ✅ Arquitectura implementada

---

## 🚀 Próximas Mejoras (Opcional)

- [ ] Exportación de datos a TXT/JSON/PDF
- [ ] Sistema de notificaciones por email
- [ ] API REST para consumo externo
- [ ] Búsqueda avanzada con filtros
- [ ] Despliegue en producción (AWS/Heroku)
- [ ] Autenticación social (Google, GitHub)
- [ ] Sistema de reservas de libros
- [ ] Reportes avanzados de préstamos

---

## [INFO] Información de Contacto

Para reportar errores, sugerencias o consultas sobre el proyecto, contacta al administrador del proyecto.

---

## 📚 Referencias

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/3/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/security/)

---

## [DOC] Otros Archivos de Documentación

- **TEST_REPORT.md** - Reporte completo de validación y pruebas

---


