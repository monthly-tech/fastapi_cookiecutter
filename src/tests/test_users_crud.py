"""
Tests para el CRUD de usuarios
Este archivo contiene tests que demuestran el funcionamiento del CRUD de usuarios
"""

import json

# Estos tests están diseñados para demostrar el uso del CRUD
# En un entorno real, se necesitaría configurar una base de datos de test

class TestUsersCRUD:
    """
    Tests de ejemplo para el CRUD de usuarios
    Nota: Estos tests requieren configuración adicional de base de datos de pruebas
    """

    def test_create_user_example(self):
        """Ejemplo de datos para crear un usuario"""
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "first_name": "Test",
            "second_name": "Middle",
            "surname": "User",
            "second_surname": "LastName",
            "phone": "+1234567890",
            "second_phone": "+0987654321",
            "role": "Owner",
            "other_role": "Custom Role Description",
            "is_active": True,
            "external_id": 12345
        }

        # En un test real, esto haría una llamada HTTP POST
        print("Ejemplo de datos para crear usuario:")
        print(json.dumps(user_data, indent=2))

        assert user_data["username"] == "test_user"
        assert user_data["is_active"]
        assert user_data["external_id"] == 12345
        assert user_data["email"] == "test@example.com"

    def test_user_search_example(self):
        """Ejemplo de búsqueda de usuarios"""
        search_params = {
            "q": "test",
            "skip": 0,
            "limit": 10
        }

        print("Ejemplo de parámetros de búsqueda:")
        print(json.dumps(search_params, indent=2))

        assert len(search_params["q"]) >= 2

    def test_user_update_example(self):
        """Ejemplo de actualización de usuario"""
        update_data = {
            "role": "user",
            "is_active": False,
            "first_name": "Test Updated"
        }

        print("Ejemplo de datos para actualizar usuario:")
        print(json.dumps(update_data, indent=2))

        assert "role" in update_data

    def test_user_filters_example(self):
        """Ejemplo de filtros para listar usuarios"""
        filter_params = {
            "skip": 0,
            "limit": 50,
            "is_active": True,
            "role": "admin"
        }

        print("Ejemplo de filtros para listar usuarios:")
        print(json.dumps(filter_params, indent=2))

        assert filter_params["limit"] <= 1000
        assert filter_params["skip"] >= 0


def example_api_calls():
    """
    Ejemplos de llamadas a la API que se pueden hacer una vez que el servidor esté corriendo
    """

    examples = {
        "create_user": {
            "method": "POST",
            "url": "/users/",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "role": "user",
                "is_active": True,
                "external_id": 12345
            }
        },

        "get_all_users": {
            "method": "GET",
            "url": "/users/?skip=0&limit=10&is_active=true",
            "headers": {}
        },

        "get_user_by_id": {
            "method": "GET",
            "url": "/users/{user_id}",
            "headers": {}
        },

        "get_user_by_external_id": {
            "method": "GET",
            "url": "/users/external/12345",
            "headers": {}
        },

        "update_user": {
            "method": "PUT",
            "url": "/users/{user_id}",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "role": "admin",
                "is_active": True
            }
        },

        "toggle_user_status": {
            "method": "PATCH",
            "url": "/users/{user_id}/toggle-active",
            "headers": {}
        },

        "search_users": {
            "method": "GET",
            "url": "/users/search/?q=john",
            "headers": {}
        },

        "delete_user": {
            "method": "DELETE",
            "url": "/users/{user_id}",
            "headers": {}
        }
    }

    print("=== Ejemplos de llamadas a la API ===")
    for operation, details in examples.items():
        print(f"\n{operation.upper().replace('_', ' ')}:")
        print(f"  Método: {details['method']}")
        print(f"  URL: {details['url']}")
        if details.get('body'):
            print(f"  Body: {json.dumps(details['body'], indent=4)}")


def curl_examples():
    """
    Ejemplos de comandos curl para probar la API
    """

    curl_commands = [
        {
            "description": "Crear un nuevo usuario",
            "command": """curl -X POST "http://localhost:8000/users/" \\
     -H "Content-Type: application/json" \\
     -d '{
       "username": "jane_smith",
       "first_name": "Jane",
       "last_name": "Smith",
       "role": "user",
       "is_active": true,
       "external_id": 54321
     }'"""
        },

        {
            "description": "Obtener todos los usuarios con filtros",
            "command": 'curl "http://localhost:8000/users/?skip=0&limit=10&is_active=true&role=admin"'
        },

        {
            "description": "Buscar usuarios por nombre",
            "command": 'curl "http://localhost:8000/users/search/?q=jane"'
        },

        {
            "description": "Obtener usuario por ID externo",
            "command": 'curl "http://localhost:8000/users/external/54321"'
        },

        {
            "description": "Actualizar un usuario",
            "command": """curl -X PUT "http://localhost:8000/users/{user_id}" \\
     -H "Content-Type: application/json" \\
     -d '{
       "role": "admin",
       "first_name": "Jane Updated"
     }'"""
        },

        {
            "description": "Alternar estado activo del usuario",
            "command": 'curl -X PATCH "http://localhost:8000/users/{user_id}/toggle-active"'
        },

        {
            "description": "Eliminar un usuario",
            "command": 'curl -X DELETE "http://localhost:8000/users/{user_id}"'
        }
    ]

    print("=== Ejemplos de comandos curl ===")
    for example in curl_commands:
        print(f"\n{example['description']}:")
        print(example['command'])


if __name__ == "__main__":
    print("Ejecutando ejemplos de uso del CRUD de usuarios...")

    # Ejecutar ejemplos
    example_api_calls()
    print("\n" + "="*50)
    curl_examples()

    # Ejecutar tests de ejemplo
    print("\n" + "="*50)
    print("Ejecutando tests de ejemplo...")

    test_crud = TestUsersCRUD()
    test_crud.test_create_user_example()
    test_crud.test_user_search_example()
    test_crud.test_user_update_example()
    test_crud.test_user_filters_example()

    print("\n✅ Todos los ejemplos ejecutados correctamente!")
    print("\nPara probar la API real:")
    print("1. Asegúrate de que el servidor esté corriendo")
    print("2. Usa los comandos curl mostrados arriba")
    print("3. O visita http://localhost:8000/docs para la documentación interactiva")
