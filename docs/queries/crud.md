# CRUD and transactions

Simple CRUD uses the python-arango collection API (`insert`, `get`, `update`, `delete`). Where AQL is the better fit, the queries below are used. Both styles are shown at the defense on purpose.

```python
# create
db.collection("symptoms").insert({"_key": "rough-idle", "name": {"en": "Rough idle"}})
# read
doc = db.collection("symptoms").get("rough-idle")
# update (merge)
db.collection("symptoms").update({"_key": "rough-idle", "name": {"sr": "Neravnomeran rad na leru"}})
# delete through the graph, so edges go too
db.graph("diagnostic_graph").vertex_collection("symptoms").delete("rough-idle")
```

## Q1: filtered, paginated code list

```aql
FOR d IN dtc_codes
  FILTER @category == null OR d.category == @category
  FILTER @min_severity == null OR d.severity >= @min_severity
  SORT d.severity DESC, d.code
  LIMIT @offset, @count
  RETURN { code: d.code, description: NOT_NULL(d.description[@lang], d.description.en), severity: d.severity }
```

Bind: `category`, `min_severity`, `offset`, `count`, `lang`. Index: `dtc_codes (category, severity)`.

## Q2: one code

```aql
FOR d IN dtc_codes
  FILTER d.code == @code
  LIMIT 1
  RETURN d
```

Index: unique on `dtc_codes.code`. Same result as `DOCUMENT("dtc_codes", @code)`, but used to show the difference between a primary key lookup and a persistent index lookup in `explain`.

## Q3: insert or update a symptom

```aql
UPSERT { _key: @key }
  INSERT MERGE(@doc, { _key: @key, created_at: @now, updated_at: @now })
  UPDATE MERGE(@doc, { updated_at: @now })
  IN symptoms
  RETURN { doc: NEW, created: OLD == null }
```

## Q4: create a service record (stream transaction)

A service record is a document plus several edges, and it changes the vehicle's mileage. It must be all or nothing.

Steps inside one transaction:

1. Read the vehicle and its latest record mileage. If the new `mileage_km` is lower, abort with `422`.
2. Read the mechanic's `works_at` edge to get the workshop.
3. Insert the `service_records` document.
4. Insert edges `serviced`, `performed_at`, `performed_by`, one `found_code` per code, one `replaced` per part.
5. Compute `parts_rsd` and `total_rsd`, update the record.
6. Update `vehicles.mileage_km`.

```python
txn = db.begin_transaction(
    read=["vehicles", "service_records", "works_at"],
    write=["service_records", "vehicles", "serviced", "performed_at",
           "performed_by", "found_code", "replaced"],
)
try:
    tdb = txn  # TransactionDatabase, same API as db
    rec = tdb.collection("service_records").insert(record, return_new=True)["new"]
    tdb.collection("serviced").insert({"_from": vehicle_id, "_to": rec["_id"]})
    # ... other edges ...
    tdb.collection("vehicles").update({"_key": vin, "mileage_km": record["mileage_km"]})
    txn.commit_transaction()
except Exception:
    txn.abort_transaction()
    raise
```

The test suite forces an error after step 4 and checks that no edge or record was left behind.

## Deleting with the 409 rule

Before deleting a DTC code or a component, the service checks for history:

```aql
RETURN LENGTH(
  FOR e IN @@edge
    FILTER e._to == @id
    LIMIT 1
    RETURN 1
) > 0
```

Bind: `@edge` = `found_code` or `replaced`. If it returns `true`, the API answers `409 Conflict`.
