from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from scalar_fastapi import get_scalar_api_reference

from api.urls import api_router
from core.settings import settings
from middleware.catcher import CatcherExceptionsMiddleware

# Define security schemes
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1}/openapi.json",
    description="""
    Template Microservice with FastAPI and Google Cloud integration.

    ## Authentication

    This API supports two types of authentication:

    ### 1. API Key Authentication
    - **Header name**: `X-API-KEY`
    - **Value**: Your API key (set in LOCAL_API_KEY environment variable)

    ### 2. Bearer Token Authentication (Firebase)
    - **Header name**: `Authorization`
    - **Value**: `Bearer {firebase_token}`
    - **Used for**: User validation endpoints

    ### How to test in Swagger UI:
    1. Click the "Authorize" button (🔒) at the top right
    2. For API Key: Enter your API key in the "X-API-KEY" field
    3. For Bearer Token: Enter your Firebase token in the "HTTPBearer" field
    4. Click "Authorize"
    5. Now you can test the protected endpoints

    ### Examples:
    - API Key: `X-API-KEY: your-api-key-here`
    - Bearer Token: `Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...`

    ### Exceptions:
    - Google Cloud Cron jobs (X-Appengine-Cron: true)
    - Google Cloud Tasks (User-Agent starts with "Google-Cloud-Tasks")
    """,
    version="0.1.0",
    middleware=[
        Middleware(CatcherExceptionsMiddleware),
    ],
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Set all CORS enabled origins
# Initialize routes
app.include_router(api_router, prefix=settings.API_V1)


# Add Scalar API documentation at /scalar
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
