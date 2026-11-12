# Work plan

Seven weeks, one milestone per week. Each week ends with something that runs.

| Week | Milestone | Done when |
| --- | --- | --- |
| 1 | Setup | repo, Docker Compose with ArangoDB, minimal FastAPI app, `schema.py` creates all collections, graphs, indexes, analyzers and the view |
| 2 | Knowledge base data | JSON for catalog and knowledge base, seed loader with validation |
| 3 | CRUD and auth | Pydantic models, repositories, catalog and knowledge base routers, JWT and roles, first tests |
| 4 | Diagnosis and services | Q5 to Q12, vehicles, service records with the transaction, service data transcribed from reports |
| 5 | Analytics and optimization | Q13 to Q18, explain and profile before and after for indexed queries |
| 6 | Streamlit UI | all pages, EN / SR switch, graph view, Query Lab |
| 7 | Finish | coverage, docs filled with real plans and timings, slides, rehearsing query explanations |

## Defense slides

1. Problem and idea
2. Why a multi-model database
3. Architecture
4. Document model
5. Graph model
6. CRUD and the service record transaction
7. Diagnosis by symptoms (Q6)
8. Traversals: diagnosis tree, component impact, shortest path (Q7, Q8, Q11)
9. Indexes: explain and profile before and after
10. Analytics (Q13 to Q17)
11. Testing
12. Live demo and lessons learned
