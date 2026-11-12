# Testing

Tests use pytest and run against a real ArangoDB database named `autodiag_test`. A session fixture creates it with `schema.py` and a small fixture data set, and drops it at the end. Nothing is mocked at the database level, because the AQL itself is what needs testing.

```bash
docker compose run --rm backend pytest --cov=app --cov-report=term-missing
```

Target: at least 80% line coverage for `repositories/` and `services/`.

## Levels

| Level | What | How |
| --- | --- | --- |
| Unit | Pydantic rules: DTC format, severity, probability, VIN, mileage | parametrized tests with equivalence classes and boundary values |
| Repository | each catalogued query returns the expected rows on fixture data | fixtures in `tests/fixtures/` |
| API | status codes, 401 without token, 403 wrong role or not owner, 409, 422, CRUD round trip | `TestClient`, database dependency overridden to `autodiag_test` |
| Index usage | key queries use their index | assert the `explain()` plan contains an `IndexNode` with the expected index name |
| Transaction | a failed service record leaves nothing behind | force an error after the edges are inserted, compare counts before and after |

## Boundary value examples

| Field | Invalid | Valid | Valid | Invalid |
| --- | --- | --- | --- | --- |
| severity | 0 | 1 | 5 | 6 |
| probability | -0.01 | 0 | 1 | 1.01 |
| VIN length | 16 | 17 | 17 | 18 |
| password length | 7 | 8 | | |

## Fixture data

A small, hand-made graph that is easy to reason about:

- 2 makers, 2 models, 2 engines, 4 components
- 3 codes (P0300, P0420, P0401), 4 symptoms, 4 causes, 4 solutions
- 1 workshop, 3 users (owner, mechanic, admin), 2 vehicles, 3 service records

Expected results in tests are written by hand from this data, so a wrong query cannot "agree with itself".

## Test layout

```text
backend/tests/
├── conftest.py            # test db, fixture data, TestClient, tokens per role
├── fixtures/              # small JSON data set
├── unit/test_models.py
├── repositories/test_q01_q05.py ... test_q13_q18.py
├── api/test_auth.py, test_vehicles.py, test_services.py, ...
└── test_indexes.py
```
