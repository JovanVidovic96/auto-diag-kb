# Database overview

ArangoDB is a multi-model database: documents and graphs live in the same engine and are queried with one language, AQL. That fits this domain. A trouble code is a document with its own fields, but what makes it useful are its connections to symptoms, causes, parts and fixes.

| Item | Count |
| --- | --- |
| Database | `autodiag` (tests use `autodiag_test`) |
| Document collections | 12 |
| Edge collections | 17 |
| Named graphs | 2: `diagnostic_graph`, `service_graph` |
| ArangoSearch view | 1: `kb_search` |
| Custom analyzers | 2: `norm_sr`, `ngram_sr` |

## Conventions

- `_key` is a readable slug for knowledge base and catalog data (`P0300`, `vw-golf-7`, `ignition-coil`). Seed files reference each other by these keys. Users and service records get generated keys.
- A vehicle's `_key` is its VIN.
- Text shown to users is a language object `{"en": "...", "sr": "..."}`. `en` is required.
- Every document has `created_at` and `updated_at` as ISO 8601 strings in UTC. The repository layer sets them; clients cannot.
- Money is stored in RSD in fields ending in `_rsd`. There is no currency conversion.
- Codes read and parts replaced in a service are edges, not arrays inside the service document, so they can be traversed and aggregated.

## Delete rules

| What is deleted | Rule |
| --- | --- |
| DTC code or component referenced by a service record (`found_code`, `replaced`) | Refused with `409 Conflict` |
| Other knowledge base vertices (symptom, cause, solution, unreferenced code or component) | Deleted through the graph API, which also removes their edges |
| User | Soft delete: `is_active: false`. Edges stay, history stays |
| Vehicle sold | The `owns` edge gets `until`; a new `owns` edge is created for the new owner |
| Service record | Hard delete by admin or the mechanic who created it, together with its edges, in one transaction |

## Schema creation

`app/db/schema.py` is idempotent. It checks what exists and creates only what is missing: collections, graphs (with their edge definitions), indexes, analyzers and the view. The backend runs it on every start.

```python
if not db.has_graph("diagnostic_graph"):
    db.create_graph("diagnostic_graph", edge_definitions=[
        {"edge_collection": "caused_by",
         "from_vertex_collections": ["dtc_codes"],
         "to_vertex_collections": ["causes"]},
        # ...
    ])
```
