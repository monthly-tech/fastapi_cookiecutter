# Documentación de la API

Este proyecto FastAPI ahora incluye **tres** opciones diferentes para explorar la documentación de la API:

## 🔗 Rutas de Documentación Disponibles

### 1. **Swagger UI** (FastAPI predeterminado)
- **URL**: `/docs`
- **Descripción**: Interfaz interactiva clásica de Swagger para probar endpoints
- **Características**: 
  - Prueba de endpoints en tiempo real
  - Esquemas de datos detallados
  - Autenticación integrada

### 2. **ReDoc** (FastAPI predeterminado)
- **URL**: `/redoc`
- **Descripción**: Documentación estática y elegante generada automáticamente
- **Características**:
  - Diseño limpio y profesional
  - Navegación por categorías
  - Ideal para documentación de referencia

### 3. **Scalar** (Recién agregado) ✨
- **URL**: `/scalar`
- **Descripción**: Interfaz moderna y hermosa para documentación de APIs
- **Características**:
  - Diseño moderno y atractivo
  - Interfaz intuitiva y fácil de usar
  - Funcionalidad de prueba de endpoints
  - Experiencia de usuario mejorada

## 🚀 Cómo usar

1. **Inicia el servidor**:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

2. **Accede a cualquiera de las interfaces**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Scalar: http://localhost:8000/scalar

## 📦 Instalación de Scalar

Scalar FastAPI se agregó al proyecto usando:

```bash
poetry add scalar-fastapi
```

## ⚙️ Configuración

La configuración de Scalar se encuentra en `src/main.py`:

```python
from scalar_fastapi import get_scalar_api_reference

# Add Scalar API documentation at /scalar
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
```

## 🎨 Personalización

Puedes personalizar Scalar agregando más parámetros:

```python
return get_scalar_api_reference(
    openapi_url=app.openapi_url,
    title=app.title,
    dark_mode=True,  # Modo oscuro
    hide_search=False,  # Mostrar búsqueda
    persist_auth=True,  # Persistir autenticación
    # Y muchas más opciones...
)
```

---

**¡Disfruta explorando tu API con estas tres interfaces de documentación!** 🎉
