# MD Asset Marketplace App

A full-stack asset marketplace built with **Python 3.14.7 + FastAPI + MongoDB + React + TypeScript**.

## What was upgraded

### Backend
- Layered architecture: routers → services → repositories → MongoDB
- Environment-driven configuration with `.env` for local development
- No application secrets hardcoded in source code
- Short-lived JWT access tokens (15 minutes by default)
- Opaque refresh tokens stored as SHA-256 hashes in MongoDB
- Refresh-token rotation to reduce replay risk
- Refresh token delivered through an `HttpOnly` cookie
- Bcrypt password hashing
- Role-based admin authorization
- Atomic asset purchase so two users cannot buy the same asset concurrently
- MongoDB indexes
- Duplicate-email protection at both application and database level
- Pydantic request validation
- Request IDs for troubleshooting
- Structured application logging
- Liveness and MongoDB readiness endpoints
- CORS configuration
- Dockerfile and local Docker Compose
- Production deployment guidance

### Frontend
- React + TypeScript + Vite
- Access token kept in memory rather than localStorage
- HttpOnly refresh cookie is not accessible to JavaScript
- Automatic access-token refresh on a 401 response
- Dashboard, My Assets and Admin views
- Admin asset creation and registered-user listing
- API error handling

## API

### Public
- `POST /api/users/register`
- `POST /api/users/login`
- `POST /api/users/refresh`
- `POST /api/users/logout`
- `GET /api/dashboard/assets`
- `GET /health`
- `GET /ready`

### Authenticated user
- `GET /api/users/me`
- `POST /api/dashboard/assets/{asset_id}/buy`
- `GET /api/dashboard/my-assets`

### Admin only
- `POST /api/admin/assets`
- `GET /api/admin/assets`
- `GET /api/admin/users`

## Local setup

### 1. Backend

```bash
cd backend
python3.14 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and use a random JWT secret of at least 32 characters.

Start MongoDB locally, then:

```bash
uvicorn app.main:app --reload
```

Swagger: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## Production configuration

Do not commit `.env`.

For AWS, inject secrets using **AWS Secrets Manager** (or another secret manager) and expose them to the application as environment variables. The application code does not need to change.

Recommended secret values:

- `MONGODB_URL`
- `JWT_SECRET`
- `ADMIN_PASSWORD`

Recommended non-secret configuration:

- `DATABASE_NAME`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `CORS_ORIGINS`
- `APP_ENV`
- `LOG_LEVEL`
- `COOKIE_SECURE=true`
- `COOKIE_SAMESITE=lax` for same-site deployments

If the SPA and API are genuinely cross-site and the browser requires a cross-site cookie, use `COOKIE_SAMESITE=none` together with HTTPS and `COOKIE_SECURE=true`, and add an explicit CSRF protection strategy.

## MongoDB

For production, use MongoDB Atlas or another managed MongoDB service rather than the MongoDB container from `docker-compose.yml`.

The backend creates indexes for:

- unique user email
- asset ownership/purchase lookup
- asset creation lookup
- asset creator lookup
- refresh-token hash
- refresh-session expiration (TTL)

## Docker local environment

```bash
cd backend
cp .env.example .env
```

For the compose MongoDB service, set:

```env
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxxxx.mongodb.net/asset_marketplace?appName=Cluster0
```

Then:

```bash
docker compose up --build
```

## Security notes

- Never store plaintext passwords in MongoDB.
- Never commit real `.env` files.
- Never use the example JWT secret in production.
- Rotate production secrets periodically.
- Use HTTPS in production.
- Keep access tokens short-lived.
- Refresh tokens are rotated and stored only as hashes.
- The frontend does not persist the access token in localStorage.
- The API enforces ownership server-side; hiding UI elements is not considered authorization.
- Admin endpoints require both a valid access token and `role=admin` in the current MongoDB user record.

## Architecture

```text
React + TypeScript
        |
        | HTTPS / JSON
        v
FastAPI routers
        |
        v
Services / business logic
        |
        v
Repositories
        |
        v
MongoDB

Auth:
React memory access token
        +
HttpOnly refresh cookie
        |
        v
Refresh-token session collection
```

## Important production note

The bootstrap admin credentials are used only to create the initial admin record. The password is immediately bcrypt-hashed before it is stored. In a real deployment, inject the bootstrap password from a secret manager and rotate/replace the bootstrap process as part of your deployment procedure.
