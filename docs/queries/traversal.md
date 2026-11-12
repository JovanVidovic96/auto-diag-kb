# Graph traversals

Traversal syntax used throughout:

```aql
FOR vertex, edge, path IN min..max OUTBOUND|INBOUND|ANY start edge_collection1, edge_collection2
```

Or with a named graph: `... IN 1..3 ANY start GRAPH "diagnostic_graph"`.

## Q6: rank codes by selected symptoms

The main diagnosis query. Symptoms point to codes through `exhibits`, so we go `INBOUND` from each selected symptom and count how many selected symptoms each code explains. If a VIN is given, only codes that are known issues of that car's engine are kept.

```aql
LET engine_codes = @vin == null ? null : (
  FOR eng IN 1..1 OUTBOUND CONCAT("vehicles/", @vin) powered_by
    FOR dtc IN 1..1 OUTBOUND eng known_issue
      RETURN dtc._id
)
FOR s IN symptoms
  FILTER s._key IN @symptom_keys
  FOR dtc, e IN 1..1 INBOUND s exhibits
    FILTER engine_codes == null OR dtc._id IN engine_codes
    COLLECT dtc_id = dtc._id AGGREGATE matched = SUM(1), score = SUM(e.weight)
    SORT matched DESC, score DESC
    LIMIT @limit
    LET d = DOCUMENT(dtc_id)
    RETURN {
      code: d.code,
      description: NOT_NULL(d.description[@lang], d.description.en),
      severity: d.severity,
      matched,
      selected: LENGTH(@symptom_keys),
      score: ROUND(score * 100) / 100
    }
```

Bind: `symptom_keys` (list), `vin` (or null), `lang`, `limit`.

## Q7: diagnosis tree for one code

```aql
FOR cause, c IN 1..1 OUTBOUND @dtc_id caused_by
  SORT c.probability DESC
  RETURN {
    cause: NOT_NULL(cause.title[@lang], cause.title.en),
    probability: c.probability,
    components: (
      FOR comp IN 1..1 OUTBOUND cause affects
        RETURN NOT_NULL(comp.name[@lang], comp.name.en)
    ),
    solutions: (
      FOR sol, f IN 1..1 OUTBOUND cause fixed_by
        SORT f.priority
        RETURN { title: NOT_NULL(sol.title[@lang], sol.title.en), cost_rsd: sol.cost_rsd, time_h: sol.time_h }
    )
  }
```

Index: vertex-centric on `caused_by (_from, probability)`.

Sample result:

```json
[
  { "cause": "Worn spark plugs", "probability": 0.35,
    "components": ["Spark plug"],
    "solutions": [{ "title": "Replace spark plugs", "cost_rsd": {"min": 4000, "max": 9000}, "time_h": 0.5 }] },
  { "cause": "Faulty ignition coil", "probability": 0.25, "components": ["Ignition coil"], "solutions": [ ... ] }
]
```

## Q8: codes a failing component can produce

Two hops backwards: component ← cause ← code.

```aql
FOR v, e, p IN 2..2 INBOUND @component_id affects, caused_by
  RETURN DISTINCT {
    code: v.code,
    via_cause: NOT_NULL(p.vertices[1].title[@lang], p.vertices[1].title.en)
  }
```

## Q9: common problems for a concrete vehicle

```aql
FOR eng IN 1..1 OUTBOUND CONCAT("vehicles/", @vin) powered_by
  FOR dtc, k IN 1..1 OUTBOUND eng known_issue
    FILTER k.frequency IN @frequencies
    SORT k.frequency == "common" ? 0 : 1, dtc.severity DESC
    RETURN { code: dtc.code, frequency: k.frequency, note: k.note, severity: dtc.severity }
```

Index: vertex-centric on `known_issue (_from, frequency)`.

## Q10: models and engines of a maker

```aql
FOR v, e, p IN 1..2 OUTBOUND CONCAT("manufacturers/", @maker) has_model, has_engine
  PRUNE IS_SAME_COLLECTION("engines", v)
  OPTIONS { order: "bfs" }
  RETURN {
    level: LENGTH(p.edges),
    type: PARSE_IDENTIFIER(v._id).collection,
    name: v.name || v.code,
    parent: p.vertices[-2]._key
  }
```

`PRUNE` stops the walk at engines, so the traversal never reads `has_component` even if a later change adds it to the list.

## Q11: shortest path between two vertices

```aql
FOR v, e IN ANY SHORTEST_PATH @from TO @to GRAPH "diagnostic_graph"
  RETURN {
    id: v._id,
    label: NOT_NULL(v.name[@lang], v.title[@lang], v.code, v.name),
    via: PARSE_IDENTIFIER(e._id).collection
  }
```

Example: from `symptoms/rough-idle` to `solutions/replace-ignition-coil` gives symptom, code P0300, cause "Faulty ignition coil", solution.

## Q12: full history of a vehicle

```aql
FOR rec IN 1..1 OUTBOUND CONCAT("vehicles/", @vin) serviced
  SORT rec.date DESC
  RETURN {
    date: rec.date,
    mileage_km: rec.mileage_km,
    total_rsd: rec.total_rsd,
    workshop: FIRST(FOR w IN 1..1 OUTBOUND rec performed_at RETURN w.name),
    mechanic: FIRST(FOR u IN 1..1 OUTBOUND rec performed_by RETURN u.full_name),
    codes: (FOR d IN 1..1 OUTBOUND rec found_code RETURN d.code),
    parts: (
      FOR c, r IN 1..1 OUTBOUND rec replaced
        RETURN { part: NOT_NULL(c.name[@lang], c.name.en), brand: r.brand, qty: r.qty, price_rsd: r.price_rsd }
    )
  }
```

For an owner, the router first runs the ownership check from [Authentication](../architecture/auth.md#ownership-checks). History is tied to the VIN, so it stays with the car after a sale.
