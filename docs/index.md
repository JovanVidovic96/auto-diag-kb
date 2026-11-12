# Auto Diagnostic Knowledge Base

ADKB is a knowledge base of car faults built on ArangoDB. It links vehicles, OBD-II trouble codes, symptoms, causes, engine components, solutions and real service history in one graph. A user picks the symptoms they notice and gets the most likely trouble codes, their causes and the recommended fixes.

It is a solo project for the NoSQL Databases course at Singidunum University. The defense is an oral walkthrough of the AQL queries, supported by slides and a live demo.

## What the project demonstrates

| # | Course requirement | Where to look |
| --- | --- | --- |
| 1 | Document collections | [Collections](database/collections.md) |
| 2 | Edge collections and named graphs | [Graph model](database/graph-model.md) |
| 3 | CRUD operations | [CRUD and transactions](queries/crud.md) |
| 4 | AQL queries | [Query catalog](queries/overview.md) |
| 5 | Graph traversals | [Graph traversals](queries/traversal.md) |
| 6 | Indexing and query optimization | [Indexes and search](database/indexes.md) |
| 7 | Aggregation and analysis | [Aggregations](queries/aggregation.md) |

## Stack

| Part | Technology |
| --- | --- |
| Language | Python 3.12 |
| API | FastAPI, Pydantic v2 |
| Database | ArangoDB 3.11 Community, python-arango |
| UI | Streamlit, Plotly, pyvis |
| Auth | JWT (PyJWT), bcrypt |
| Tests | pytest |
| Runtime | Docker Compose |

## Scope

In scope: catalog of makers, models and engines; OBD-II codes with symptoms, causes, components and solutions; concrete vehicles and their service history; diagnosis by symptoms; analytics; user accounts with three roles; English and Serbian content.

Out of scope: reading codes from a real OBD-II device, password reset, email verification, rate limiting, payments, mobile app.
