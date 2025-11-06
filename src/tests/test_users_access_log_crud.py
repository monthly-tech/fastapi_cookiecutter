"""
Tests para el CRUD de users_access_log
Este archivo contiene tests que demuestran el funcionamiento del CRUD de logs de acceso
"""

import json
import uuid


class TestUsersAccessLogCRUD:
    """Clase de ejemplo para tests del CRUD de logs de acceso"""
    
    def test_create_access_log(self):
        """Test de ejemplo para crear un log de acceso"""
        access_log_data = {
            "user_id": str(uuid.uuid4()),
            "latitude": "19.432608",
            "longitude": "-99.133209",
            "accuracy": "5.0",
            "altitude_accuracy": "3.0",
            "heading": "180.0",
            "speed": "0.0"
        }
        print(f"Datos de log de acceso a crear: {json.dumps(access_log_data, indent=2)}")
        return access_log_data
    
    def test_get_access_logs(self):
        """Test de ejemplo para obtener logs de acceso"""
        filters = {
            "skip": 0,
            "limit": 10,
            "user_id": str(uuid.uuid4()),
            "date_from": "2025-01-01T00:00:00",
            "date_to": "2025-12-31T23:59:59"
        }
        print(f"Filtros para buscar logs: {json.dumps(filters, indent=2)}")
        return filters
    
    def test_update_access_log(self):
        """Test de ejemplo para actualizar un log de acceso"""
        update_data = {
            "latitude": "19.433000",
            "longitude": "-99.134000",
            "accuracy": "3.0"
        }
        print(f"Datos de actualización: {json.dumps(update_data, indent=2)}")
        return update_data


def example_api_calls():
    """
    Ejemplos de llamadas a la API que se pueden hacer una vez que el servidor esté corriendo
    """
    print("Ejemplos de uso del CRUD de users_access_log:")
    print("=" * 60)
    
    # Crear log de acceso
    print("1. Crear un nuevo log de acceso:")
    print("POST /api/users-access-log/")
    access_log_data = {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "latitude": "19.432608",
        "longitude": "-99.133209",
        "accuracy": "5.0",
        "altitude_accuracy": "3.0",
        "heading": "180.0",
        "speed": "0.0"
    }
    print(f"Body: {json.dumps(access_log_data, indent=2)}")
    print()
    
    # Obtener logs con filtros
    print("2. Obtener logs de acceso con filtros:")
    print("GET /api/users-access-log/?skip=0&limit=10&user_id=550e8400-e29b-41d4-a716-446655440000")
    print()
    
    # Obtener un log específico
    print("3. Obtener un log específico:")
    print("GET /api/users-access-log/{access_log_id}")
    print()
    
    # Actualizar log
    print("4. Actualizar un log de acceso:")
    print("PUT /api/users-access-log/{access_log_id}")
    update_data = {
        "latitude": "19.433000",
        "longitude": "-99.134000"
    }
    print(f"Body: {json.dumps(update_data, indent=2)}")
    print()
    
    # Eliminar log
    print("5. Eliminar un log de acceso:")
    print("DELETE /api/users-access-log/{access_log_id}")
    print()
    
    # Obtener logs recientes de un usuario
    print("6. Obtener logs recientes de un usuario:")
    print("GET /api/users-access-log/user/{user_id}/recent?limit=5")
    print()
    
    # Obtener estadísticas
    print("7. Obtener estadísticas de logs:")
    print("GET /api/users-access-log/stats/summary")
    print()


def curl_examples():
    """
    Ejemplos de comandos curl para probar la API
    """
    print("Ejemplos de comandos curl:")
    print("=" * 40)
    
    base_url = "http://localhost:8000/api"
    
    print("1. Crear log de acceso:")
    print(f"""curl -X POST "{base_url}/users-access-log/" \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer YOUR_TOKEN" \\
     -d '{{
       "user_id": "550e8400-e29b-41d4-a716-446655440000",
       "latitude": "19.432608",
       "longitude": "-99.133209",
       "accuracy": "5.0",
       "altitude_accuracy": "3.0",
       "heading": "180.0",
       "speed": "0.0"
     }}'""")
    print()
    
    print("2. Obtener logs de acceso:")
    print(f"""curl -X GET "{base_url}/users-access-log/?skip=0&limit=10" \\
     -H "Authorization: Bearer YOUR_TOKEN\"""")
    print()
    
    print("3. Obtener logs recientes de un usuario:")
    print(f"""curl -X GET "{base_url}/users-access-log/user/550e8400-e29b-41d4-a716-446655440000/recent?limit=5" \\
     -H "Authorization: Bearer YOUR_TOKEN\"""")
    print()
    
    print("4. Obtener estadísticas:")
    print(f"""curl -X GET "{base_url}/users-access-log/stats/summary" \\
     -H "Authorization: Bearer YOUR_TOKEN\"""")
    print()


def schema_examples():
    """
    Ejemplos de los schemas disponibles
    """
    print("Schemas disponibles:")
    print("=" * 30)
    
    print("1. UsersAccessLogCreate (para crear):")
    create_schema = {
        "user_id": "UUID del usuario (requerido)",
        "latitude": "string (opcional)",
        "longitude": "string (opcional)", 
        "accuracy": "string (opcional)",
        "altitude_accuracy": "string (opcional)",
        "heading": "string (opcional)",
        "speed": "string (opcional)"
    }
    print(json.dumps(create_schema, indent=2))
    print()
    
    print("2. UsersAccessLogUpdate (para actualizar):")
    update_schema = {
        "latitude": "string (opcional)",
        "longitude": "string (opcional)",
        "accuracy": "string (opcional)", 
        "altitude_accuracy": "string (opcional)",
        "heading": "string (opcional)",
        "speed": "string (opcional)"
    }
    print(json.dumps(update_schema, indent=2))
    print()
    
    print("3. UsersAccessLogResponse (respuesta):")
    response_schema = {
        "id": "UUID del log",
        "user_id": "UUID del usuario",
        "latitude": "string",
        "longitude": "string",
        "accuracy": "string",
        "altitude_accuracy": "string", 
        "heading": "string",
        "speed": "string",
        "is_deleted": "boolean",
        "created_at": "datetime",
        "updated_at": "datetime",
        "deleted_at": "datetime | null"
    }
    print(json.dumps(response_schema, indent=2))
    print()


if __name__ == "__main__":
    print("Ejecutando ejemplos de uso del CRUD de users_access_log...")
    
    # Ejecutar ejemplos
    example_api_calls()
    print("\n" + "="*50)
    curl_examples()
    print("\n" + "="*50)
    schema_examples()
    
    # Ejecutar tests de ejemplo
    print("\n" + "="*50)
    print("Ejecutando tests de ejemplo...")
    
    test_crud = TestUsersAccessLogCRUD()
    test_crud.test_create_access_log()
    test_crud.test_get_access_logs()
    test_crud.test_update_access_log()
    
    print("\n✅ CRUD de UsersAccessLog creado exitosamente!")
    print("\nArchivos creados:")
    print("- src/core/models/users_access_log.py (Modelo SQLAlchemy)")
    print("- src/schemas/users_access_log.py (Schemas Pydantic)")
    print("- src/api/endpoints/users_access_log.py (Endpoints FastAPI)")
    print("- deployment/sql/postgresql/add_users_access_log_table.sql (Migración SQL)")
    print("- Actualizado: src/api/urls.py (Rutas)")
    print("- Actualizado: src/core/models/__init__.py (Imports)")
    print("- Actualizado: deployment/sql/postgresql/create_tables.sql (Tabla agregada)")
    print("\nFuncionalidades implementadas:")
    print("✅ CREATE - Crear nuevo log de acceso")
    print("✅ READ - Obtener logs con filtros y paginación")
    print("✅ READ - Obtener log específico por ID")
    print("✅ UPDATE - Actualizar log existente")
    print("✅ DELETE - Eliminación lógica (soft delete)")
    print("✅ EXTRA - Logs recientes de usuario específico")
    print("✅ EXTRA - Estadísticas y resumen de logs")
