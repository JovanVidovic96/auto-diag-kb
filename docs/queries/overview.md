# Query catalog

Eighteen queries cover all seven course requirements. Each one is a file in `backend/app/queries/` and uses bind parameters (`@name` for values, `@@name` for collection names). The ID is the file prefix: Q7 is `q07_diagnosis_tree.aql`.

| ID | Question | Technique | Page |
| --- | --- | --- | --- |
| Q1 | Which codes match a category and severity, page by page? | `FILTER`, `SORT`, `LIMIT offset, count` | [CRUD](crud.md) |
| Q2 | What is code P0420? | unique index lookup | [CRUD](crud.md) |
| Q3 | Add or update a symptom | `UPSERT` | [CRUD](crud.md) |
| Q4 | Save a service record with its codes and parts | stream transaction | [CRUD](crud.md) |
| Q5 | Which symptoms or codes match "misfire" or "trza"? | ArangoSearch, `BM25` | [Search](search.md) |
| Q6 | Which codes best explain the selected symptoms? | `INBOUND` traversal + `COLLECT` ranking | [Traversals](traversal.md) |
| Q7 | Causes, parts and fixes for P0300 | nested `OUTBOUND` traversals | [Traversals](traversal.md) |
| Q8 | Which codes can a failing ignition coil produce? | `2..2 INBOUND` over two edge collections | [Traversals](traversal.md) |
| Q9 | Which problems are common for this car's engine? | multi-hop, vertex-centric index | [Traversals](traversal.md) |
| Q10 | Models and engines of a maker | `1..2 OUTBOUND`, `PRUNE` | [Traversals](traversal.md) |
| Q11 | How is a symptom connected to a solution? | `ANY SHORTEST_PATH` on a named graph | [Traversals](traversal.md) |
| Q12 | Full history of a vehicle | traversal over `service_graph` | [Traversals](traversal.md) |
| Q13 | Most frequent codes per model | `COLLECT ... WITH COUNT INTO` | [Aggregations](aggregation.md) |
| Q14 | Service spending per year | `COLLECT ... AGGREGATE` | [Aggregations](aggregation.md) |
| Q15 | Faults by mileage band | `FLOOR` bucketing | [Aggregations](aggregation.md) |
| Q16 | Most replaced components and money spent | aggregation over edge attributes | [Aggregations](aggregation.md) |
| Q17 | Workshop comparison | `COUNT_DISTINCT`, `AVERAGE` | [Aggregations](aggregation.md) |
| Q18 | Nearest workshops | geo index, `GEO_DISTANCE` | [Aggregations](aggregation.md) |

## Running a query from Python

```python
from app.db.queries import load_aql

query = load_aql("q07_diagnosis_tree")
cursor = db.aql.execute(query, bind_vars={"dtc_id": "dtc_codes/P0300", "lang": "sr"})
rows = list(cursor)
```

`load_aql` reads the file once and caches it.

## How each query is documented

- the question it answers, in one sentence
- the AQL
- bind variables
- a short sample result
- for indexed queries, the plan and timing before and after the index

Plans and timings are filled in once the seed data is complete, because they depend on the data size.
