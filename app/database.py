import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Clase para gestionar la conexión a la base de datos"""
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos"""
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', 'biblioteca_user'),
                password=os.getenv('DB_PASSWORD', 'biblioteca_pass'),
                database=os.getenv('DB_NAME', 'biblioteca_db'),
                charset='utf8mb4',
                use_unicode=True,
                collation='utf8mb4_unicode_ci'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        """Ejecuta una consulta SELECT"""
        connection = Database.get_connection()
        if connection is None:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            connection.close()
    
    @staticmethod
    def execute_update(query, params=None):
        """Ejecuta una consulta INSERT, UPDATE o DELETE"""
        connection = Database.get_connection()
        if connection is None:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            # Retorna last_id para INSERT, rowcount para UPDATE/DELETE
            result = cursor.lastrowid if cursor.lastrowid > 0 else cursor.rowcount
            cursor.close()
            return result
        except Error as e:
            print(f"Error en la actualización: {e}")
            connection.rollback()
            return None
        finally:
            connection.close()
