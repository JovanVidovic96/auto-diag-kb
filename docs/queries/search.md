# Full-text search

## Q5: search the knowledge base

```aql
FOR doc IN kb_search
  SEARCH ANALYZER(
      doc.name.en IN TOKENS(@q, "text_en")
      OR doc.description.en IN TOKENS(@q, "text_en")
      OR doc.title.en IN TOKENS(@q, "text_en"),
    "text_en")
  OR ANALYZER(
      doc.name.sr IN TOKENS(@q, "text_sr")
      OR doc.description.sr IN TOKENS(@q, "text_sr")
      OR doc.title.sr IN TOKENS(@q, "text_sr"),
    "text_sr")
  OR NGRAM_MATCH(doc.name.sr, @q, 0.6, "ngram_sr")
  OR ANALYZER(doc.code == UPPER(@q), "identity")
  SORT BM25(doc) DESC
  LIMIT @limit
  RETURN {
    type: PARSE_IDENTIFIER(doc._id).collection,
    key: doc._key,
    label: NOT_NULL(doc.name[@lang], doc.title[@lang], doc.code),
    score: BM25(doc)
  }
```

Bind: `q`, `lang`, `limit`.

| Input | Finds |
| --- | --- |
| `misfire` | P0300 to P0304, symptom "Engine misfires" |
| `kocnica` | Serbian texts with "kočnica" (accents ignored) |
| `paljen` | "paljenje", "preskakanje paljenja", through n-grams |
| `p0420` | code P0420 (identity analyzer, upper-cased) |

The exact `SEARCH` expression may be tuned once real seed data exists; the analyzers and the view definition stay as in [Indexes and search](../database/indexes.md).
