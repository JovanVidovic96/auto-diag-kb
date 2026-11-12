# Endpoints

All paths are under `/api/v1`. "Any" means any logged-in active user.

## Auth

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| POST | `/auth/register` | public | create an owner account | UC-01 |
| POST | `/auth/login` | public | get a token (form fields `username`, `password`) | UC-02 |
| GET | `/auth/me` | any | current user | UC-02 |

## Users and workshops

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| GET | `/users` | admin | list users, filter by role and status | UC-05 |
| PATCH | `/users/{key}` | admin | change role, `is_active`, full name | UC-05 |
| PUT | `/users/{key}/workshop` | admin | set the mechanic's workshop (`works_at`) | UC-05 |
| GET | `/workshops` | any | list, or sorted by distance with `lat` and `lon` (Q18) | UC-14 |
| POST, PUT | `/workshops`, `/workshops/{key}` | admin | create, edit | UC-05 |

## Catalog

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| GET | `/manufacturers` | any | list makers | UC-13 |
| GET | `/manufacturers/{key}/models` | any | models and engines (Q10) | UC-13 |
| GET | `/engines/{key}` | any | engine, components, known issues | UC-13 |
| GET | `/components/{key}/impact` | any | codes the part can cause (Q8) | UC-13 |
| POST, PUT, DELETE | `/manufacturers`, `/models`, `/engines`, `/components` and `/{key}` | admin | catalog CRUD | UC-07 |

## Knowledge base

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| GET | `/dtc` | any | filtered, paginated list (Q1) | UC-11 |
| GET | `/dtc/{code}` | any | one code (Q2) | UC-11 |
| GET | `/dtc/{code}/diagnosis` | any | causes, components, solutions (Q7) | UC-11 |
| GET | `/symptoms` | any | symptom list for the picker | UC-10 |
| POST, PUT, DELETE | `/dtc`, `/symptoms`, `/causes`, `/solutions` and `/{key}` | admin | knowledge base CRUD (Q3 for symptoms) | UC-06 |
| POST | `/links/{edge_collection}` | admin | create an edge with attributes | UC-08 |
| DELETE | `/links/{edge_collection}/{key}` | admin | remove an edge | UC-08 |

## Diagnosis and search

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| POST | `/diagnose` | any | rank codes for symptoms (Q6) | UC-10 |
| GET | `/search?q=` | any | full-text search (Q5) | UC-12 |
| GET | `/paths?from=&to=` | any | shortest path (Q11) | UC-13 |

`POST /diagnose` body:

```json
{ "symptom_keys": ["rough-idle", "check-engine-light"], "vin": null, "limit": 10 }
```

## Vehicles and services

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| GET | `/vehicles` | owner: own; mechanic, admin: all, `q` searches VIN and plate | list | UC-23 |
| POST | `/vehicles` | owner, admin | register | UC-20 |
| GET | `/vehicles/{vin}` | owner of it, mechanic, admin | details | UC-21 |
| GET | `/vehicles/{vin}/history` | owner of it, mechanic, admin | service history (Q12) | UC-21 |
| GET | `/vehicles/{vin}/known-issues` | owner of it, mechanic, admin | common codes for its engine (Q9) | UC-21 |
| POST | `/vehicles/{vin}/transfer` | owner of it, admin | change owner | UC-22 |
| POST | `/services` | mechanic | create record in one transaction (Q4) | UC-24 |
| PUT, DELETE | `/services/{key}` | mechanic (own), admin | edit, delete | UC-25 |

`POST /services` body:

```json
{
  "vin": "WVWZZZAUZFW000001",
  "date": "2025-03-14",
  "mileage_km": 148200,
  "labor_rsd": 6000,
  "notes": "Misfire under load",
  "codes": [{ "code": "P0302", "note": "cylinder 2" }],
  "parts": [{ "component": "ignition-coil", "part_number": "06H905110G", "brand": "Bosch", "qty": 1, "price_rsd": 7800 }]
}
```

## Analytics and Query Lab

| Method | Path | Role | Purpose | UC |
| --- | --- | --- | --- | --- |
| GET | `/analytics/top-codes-per-model` | mechanic, admin | Q13 | UC-30 |
| GET | `/analytics/spending-per-year` | mechanic, admin | Q14 | UC-30 |
| GET | `/analytics/faults-by-mileage` | mechanic, admin | Q15 | UC-30 |
| GET | `/analytics/top-replaced-parts` | mechanic, admin | Q16 | UC-30 |
| GET | `/analytics/workshops` | mechanic, admin | Q17 | UC-30 |
| GET | `/queries` | admin | list catalogued queries with AQL text | UC-31 |
| POST | `/queries/{id}/run` | admin | run with bind variables | UC-31 |
| POST | `/queries/{id}/explain` | admin | execution plan | UC-31 |
| POST | `/queries/{id}/profile` | admin | run with profiling stats | UC-31 |
