# Indexes and search

ArangoDB always has a primary index on `_key` and an edge index on `_from` and `_to`. The indexes below are added on top of those. Each one exists because a query in the catalog filters or sorts on its fields.

| Collection | Fields | Type | Used by |
| --- | --- | --- | --- |
| `dtc_codes` | `code` | persistent, unique | Q2 |
| `dtc_codes` | `category`, `severity` | persistent | Q1 |
| `vehicles` | `vin` | persistent, unique | vehicle lookup |
| `vehicles` | `registration` | persistent, unique, sparse | lookup by plate |
| `users` | `username` | persistent, unique | login |
| `users` | `email` | persistent, unique | registration |
| `service_records` | `date` | persistent | Q12, Q14 |
| `service_records` | `mileage_km` | persistent | Q15 |
| `known_issue` | `_from`, `frequency` | persistent (vertex-centric) | Q9 |
| `caused_by` | `_from`, `probability` | persistent (vertex-centric) | Q7 |
| `owns` | `_from`, `until` | persistent (vertex-centric) | ownership checks |
| `workshops` | `location` | geo | Q18 |

`registration` is sparse because it is optional; a unique sparse index allows many vehicles without a plate.

A vertex-centric index starts with `_from` (or `_to`) and adds an edge attribute. During a traversal ArangoDB can then read only the matching edges of one vertex instead of all of them and filtering afterwards.

## ArangoSearch view

The view `kb_search` indexes text fields of four collections:

| Collection | Fields |
| --- | --- |
| `symptoms` | `name.en`, `name.sr`, `description.en`, `description.sr` |
| `dtc_codes` | `code`, `description.en`, `description.sr` |
| `causes` | `title.en`, `title.sr` |
| `components` | `name.en`, `name.sr` |

| Analyzer | Type | Used for |
| --- | --- | --- |
| `text_en` | built in | English fields: tokenizing, stemming, case |
| `text_sr` | text, locale `sr`, `accent: false`, `case: lower`, no stemming | Serbian words: "kocnica" matches "kočnica" |
| `ngram_sr` | pipeline: norm (lower case, no accents), then ngram 3 to 5 | partial words: "paljen" matches "paljenje" |
| `identity` | built in | `code` |

Results are ranked with `BM25(doc)`. See [Full-text search](../queries/search.md).

## How optimization is shown

For each indexed query in the catalog the docs contain a before and after:

1. Explain the query with the optimizer rule `use-indexes` turned off (`optimizer_rules=["-use-indexes"]`), which behaves as if the index did not exist. The plan contains an `EnumerateCollectionNode`, meaning a full scan.
2. Explain it again normally. The plan contains an `IndexNode` with the index name.
3. Run both versions with `profile=True` and record execution time and `scannedFull` / `scannedIndex` from the stats.

```python
plan = db.aql.explain(query, bind_vars=bind)
nodes = [n["type"] for n in plan["nodes"]]
cursor = db.aql.execute(query, bind_vars=bind, profile=True)
stats = cursor.statistics()   # scanned_full, scanned_index, execution_time
```

Query Lab in the UI does the same thing live, which is the easiest way to show it at the defense.

## Other optimization habits

- Bind parameters everywhere: plans can be cached and there is no AQL injection.
- `LIMIT` as early as possible and only the needed fields in `RETURN`.
- Traversals use `PRUNE` and `OPTIONS { order: "bfs", uniqueVertices: "global" }` where it makes sense.
- Edge filters inside traversals are written so that vertex-centric indexes apply (`FILTER e.probability >= @min`).
