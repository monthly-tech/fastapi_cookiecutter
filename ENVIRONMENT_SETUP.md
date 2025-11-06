# Environment Configuration Guide

This guide explains how to set up environment variables for the Monthly Onboarding Microservice.

## Environment Files Structure

The project uses environment-specific configuration files located in the `envs/` directory:

```
envs/
├── .env.local    # Local development environment
├── .env.dev      # Development environment  
├── .env.stg      # Staging environment
├── .env.prd      # Production environment
└── .env.test     # Testing environment
```

## Setup Instructions

### 1. Main Environment File
Copy the example file and configure your local environment:
```bash
cp .env.example .env
```

### 2. Environment-Specific Files
The application automatically loads the appropriate environment file based on the `ENVIRONMENT` variable:

- `ENVIRONMENT=local` → loads `envs/.env.local`
- `ENVIRONMENT=development` → loads `envs/.env.dev`
- `ENVIRONMENT=staging` → loads `envs/.env.stg`
- `ENVIRONMENT=production` → loads `envs/.env.prd`
- `ENVIRONMENT=testing` → loads `envs/.env.test`

### 3. Required Configuration

#### Database
```bash
POSTGRESQL_URL=postgresql+psycopg2://user:password@host:port/database
```

#### Google Cloud Platform
```bash
GCP_PROJECT_ID=your-project-id
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GCP_MONTHLY_PROVIDERS_SECRET_ID=secret-manager-secret-id
GCP_BUCKET_NAME=your-storage-bucket
```

#### Firebase Authentication
```bash
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_SERVICE_ACCOUNT_JSON={"service_account_json"}
FIREBASE_AUTH_ENABLED=true
```

#### Email Configuration
```bash
MAIL_SERVER=smtp.fastmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-password
MAIL_STARTTLS=true
MAIL_FROM=your-email@domain.com
```

## Docker Compose Integration

The `docker-compose.yml` file is configured to automatically load environment variables from the `.env` file:

```yaml
services:
  app:
    env_file:
      - .env
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-local}
```

## Security Notes

- Never commit `.env` files with real credentials to version control
- Use `.env.example` as a template for required variables
- Environment files in `envs/` should contain actual values for their respective environments
- Store production secrets in secure secret management systems (Google Secret Manager, AWS Secrets Manager, etc.)

## Troubleshooting

1. **Environment not loading**: Check that `ENVIRONMENT` variable is set correctly
2. **Missing variables**: Ensure all required variables are defined in your environment file
3. **Database connection issues**: Verify database URL format and credentials
4. **GCP authentication**: Ensure service account JSON file exists and path is correct

## Development Workflow

1. Set `ENVIRONMENT=local` in your `.env` file
2. Configure `envs/.env.local` with your local development settings
3. Use Docker Compose for local development: `docker-compose up`
4. For testing: Set `ENVIRONMENT=testing` and run tests

## Production Deployment

1. Set `ENVIRONMENT=production`
2. Configure `envs/.env.prd` with production values
3. Ensure all secrets are properly secured
4. Use orchestration tools (Kubernetes, Docker Swarm) to manage environment variables securely
