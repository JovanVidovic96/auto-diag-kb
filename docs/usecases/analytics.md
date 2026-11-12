# Use cases: analytics and Query Lab

## UC-30 View analytics

- **Actor:** Mechanic, Admin
- **Precondition:** service records exist.
- **Flow:**
    1. User opens Analytics.
    2. User picks a report and its filters (period, mileage band size, limit).
    3. System returns the rows and the UI draws a chart and a table.
- **Reports:**
    - top codes per model (Q13)
    - spending per year (Q14)
    - faults by mileage band (Q15)
    - most replaced components (Q16)
    - workshop comparison (Q17)
- **Exceptions:** no data for the filter: empty chart with a message.
- **Realized by:** `GET /analytics/{report}`

## UC-31 Inspect queries in Query Lab

- **Actor:** Admin
- **Precondition:** logged in as admin.
- **Flow:**
    1. Admin opens Query Lab and picks a query from Q1 to Q18.
    2. UI shows the AQL text and a form for its bind variables, filled with examples.
    3. Admin runs it and sees the result.
    4. Admin opens the plan: node types, used indexes, estimated cost.
    5. Admin runs it with profiling and sees execution time and scanned documents.
- **Exceptions:**
    - Invalid bind values: `422`.
    - Query Lab only runs catalogued queries. Free AQL is not accepted, so it cannot be used to change data.
- **Realized by:** `GET /queries`, `POST /queries/{id}/run`, `POST /queries/{id}/explain`, `POST /queries/{id}/profile`

This is the page used at the defense to show indexes and optimization live.
