# Asset Marketplace Backend

Production-oriented FastAPI + MongoDB backend targeting Python 3.14.7.

## Architecture

- Routers: HTTP/API layer only
- Services: business logic
- Repositories: MongoDB access
- Models: persistence/serialization helpers
- Schemas: request/response validation
- Core: configuration, security, database and logging
- JWT access tokens are short-lived (15 minutes by default)
- Refresh tokens are random opaque tokens, stored hashed and rotated on refresh
- Passwords are bcrypt hashed
- Admin access is role-based
- `.env` is local configuration only; production secrets should be injected by a secret manager/environment
- MongoDB indexes are created at startup
- `/health` is liveness; `/ready` checks MongoDB readiness
- Request IDs are returned for troubleshooting

## Local setup

```bash
python3.14 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

OpenAPI: http://localhost:8000/docs

## Production configuration

Do not commit `.env`. In AWS, inject secrets such as `MONGODB_URL`, `JWT_SECRET`, and `ADMIN_PASSWORD` from AWS Secrets Manager or another secret manager. Non-secret configuration can be injected as environment variables.

## Docker

```bash
cp .env.example .env
# edit .env
# for local Docker MongoDB, set MONGODB_URL=mongodb://root:change-me@mongodb:27017/asset_marketplace?authSource=admin
docker compose up --build
```

For production, prefer MongoDB Atlas or a managed MongoDB service rather than the MongoDB container in this compose file.
