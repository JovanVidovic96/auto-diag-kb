# Aggregations

All reports are available at `GET /api/v1/analytics/{report}` and drawn in the Analytics page.

## Q13: most frequent codes per model

```aql
FOR rec IN service_records
  FOR veh IN 1..1 INBOUND rec serviced
    FOR m IN 1..1 OUTBOUND veh is_model
      FOR d IN 1..1 OUTBOUND rec found_code
        COLLECT model = CONCAT(m.name, " ", m.generation), code = d.code WITH COUNT INTO times
        SORT model, times DESC
        RETURN { model, code, times }
```

The UI keeps the top 3 codes per model.

## Q14: service spending per year

```aql
FOR s IN service_records
  FILTER s.date >= @from AND s.date < @to
  COLLECT year = DATE_YEAR(s.date)
  AGGREGATE services = COUNT(1),
            total = SUM(s.total_rsd),
            average = AVERAGE(s.total_rsd),
            highest = MAX(s.total_rsd)
  SORT year
  RETURN { year, services, total, average: ROUND(average), highest }
```

Index: `service_records (date)`.

## Q15: faults by mileage band

```aql
FOR s IN service_records
  FILTER s.mileage_km >= @min_km
  LET band = FLOOR(s.mileage_km / @band_km) * @band_km
  LET codes = LENGTH(FOR d IN 1..1 OUTBOUND s found_code RETURN 1)
  COLLECT from_km = band AGGREGATE visits = COUNT(1), faults = SUM(codes), cost = AVERAGE(s.total_rsd)
  SORT from_km
  RETURN { from_km, to_km: from_km + @band_km, visits, faults, avg_cost_rsd: ROUND(cost) }
```

Bind: `band_km` (default 50000), `min_km`. Index: `service_records (mileage_km)`.

## Q16: most replaced components

```aql
FOR r IN replaced
  LET c = DOCUMENT(r._to)
  COLLECT component = NOT_NULL(c.name[@lang], c.name.en)
  AGGREGATE times = SUM(r.qty), spent = SUM(r.qty * r.price_rsd)
  SORT times DESC
  LIMIT @limit
  RETURN { component, times, spent_rsd: spent }
```

Aggregation over attributes stored on edges, not on documents.

## Q17: workshop comparison

```aql
FOR w IN workshops
  LET recs = (FOR r IN 1..1 INBOUND w performed_at RETURN r)
  LET vehicles = (
    FOR r IN recs
      FOR v IN 1..1 INBOUND r serviced
        RETURN v._key
  )
  RETURN {
    workshop: w.name,
    services: LENGTH(recs),
    distinct_vehicles: COUNT_DISTINCT(vehicles),
    avg_cost_rsd: ROUND(AVERAGE(recs[*].total_rsd)),
    revenue_rsd: SUM(recs[*].total_rsd)
  }
```

## Q18: nearest workshops

```aql
FOR w IN workshops
  LET dist = DISTANCE(w.location[0], w.location[1], @lat, @lon)
  SORT dist
  LIMIT @limit
  RETURN { name: w.name, city: w.city, address: w.address, km: ROUND(dist / 100) / 10 }
```

Index: geo on `workshops.location`, created with `geo_json: false`, so `location` is stored as `[lat, lon]`. `SORT DISTANCE(...)` with `LIMIT` is the pattern the optimizer turns into a geo index scan; `explain` shows it as an `IndexNode` with the geo index.
