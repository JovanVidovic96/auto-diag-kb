# API overview

The backend is a JSON REST API under `/api/v1`. FastAPI generates the OpenAPI description, so the interactive docs at `http://localhost:8000/docs` are always up to date. This section lists the endpoints and the rules they share.

## Authentication

Send the token from `POST /auth/login` in every request:

```text
Authorization: Bearer <token>
```

Roles and ownership are checked on every request, see [Authentication](../architecture/auth.md).

## Common parameters

| Parameter | Where | Meaning |
| --- | --- | --- |
| `lang` | query | `en` or `sr`, default `en`. Texts fall back to English. |
| `page`, `size` | query | pagination, `size` at most 100, default 20 |

Paginated responses look like:

```json
{ "items": [ ... ], "page": 1, "size": 20, "total": 40 }
```

## Errors

FastAPI's default error body is used:

```json
{ "detail": "VIN already registered" }
```

| Status | When |
| --- | --- |
| 400 | malformed request |
| 401 | missing, invalid or expired token; inactive user; wrong login |
| 403 | role not allowed or not the owner |
| 404 | item not found |
| 409 | duplicate key, item still referenced, rule conflict (mechanic without workshop) |
| 422 | validation error (Pydantic) or a business rule on the input (mileage, probability sum) |

## CORS

Streamlit calls the API from the server side, so CORS is not needed for it. `CORS_ORIGINS` is configured anyway so that Swagger and a possible browser client work.
