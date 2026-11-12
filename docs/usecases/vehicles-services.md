# Use cases: vehicles and service records

## UC-20 Register a vehicle

- **Actor:** Owner (for himself), Admin (for any owner)
- **Precondition:** the model and engine exist in the catalog.
- **Flow:**
    1. User enters VIN, plate, year, mileage, color, and picks model and engine.
    2. System validates the VIN and checks that the engine is offered in that model (`has_engine`).
    3. System creates the vehicle and the edges `owns` (with `since` = today), `is_model`, `powered_by`.
- **Exceptions:**
    - VIN or plate already registered: `409`.
    - Engine not offered in the model: `422`.
- **Realized by:** `POST /vehicles`

## UC-21 View vehicle history

- **Actor:** Owner of the vehicle, Mechanic, Admin
- **Precondition:** the vehicle exists.
- **Flow:**
    1. User opens a vehicle.
    2. System shows its data, common problems of its engine and all service records, newest first, with codes, parts, cost, workshop and mechanic.
- **Exceptions:**
    - Owner opens a vehicle he does not currently own: `403`.
    - Unknown VIN: `404`.
- **Realized by:** `GET /vehicles/{vin}`, `GET /vehicles/{vin}/history` (Q12), `GET /vehicles/{vin}/known-issues` (Q9)

History belongs to the VIN. After a sale the new owner sees the full history, and the old owner no longer sees the vehicle.

## UC-22 Transfer a vehicle

- **Actor:** current Owner, Admin
- **Precondition:** the new owner has an active account.
- **Flow:**
    1. User opens the vehicle and chooses Transfer, then enters the new owner's username.
    2. System sets `until` = today on the current `owns` edge and creates a new `owns` edge for the new owner, in one transaction.
- **Exceptions:**
    - Username not found, not active or not an owner: `422`.
    - Transfer to the same user: `409`.
- **Realized by:** `POST /vehicles/{vin}/transfer`

## UC-23 Find a vehicle

- **Actor:** Mechanic, Admin
- **Precondition:** none.
- **Flow:**
    1. Mechanic types a VIN or a plate.
    2. System shows the vehicle with model, engine and current owner.
- **Exceptions:** not found: the UI offers to register it for the customer (admin only) or to ask the owner to register it.
- **Realized by:** `GET /vehicles?q=`

## UC-24 Create service record

- **Actor:** Mechanic
- **Precondition:** the mechanic is assigned to a workshop; the vehicle exists.
- **Flow:**
    1. Mechanic finds the vehicle (UC-23) and opens New service record.
    2. Mechanic enters date, mileage, labor cost, notes, codes read and parts replaced (component, part number, brand, quantity, price).
    3. System runs one transaction: checks mileage, creates the record and edges `serviced`, `performed_at` (workshop from `works_at`), `performed_by`, `found_code`, `replaced`, computes totals and updates the vehicle's mileage.
    4. UI shows the saved record in the vehicle history.
- **Exceptions:**
    - Mileage lower than the previous record: `422`, nothing saved.
    - Mechanic without a workshop: `409`.
    - Unknown code or component: `422`.
    - Any error during the transaction: everything is rolled back.
- **Realized by:** `POST /services` (Q4)

## UC-25 Edit or delete service record

- **Actor:** Mechanic (only records he created), Admin (all)
- **Precondition:** the record exists.
- **Flow:**
    1. User opens the record from the vehicle history.
    2. User edits fields, codes or parts, or deletes the record.
    3. System applies the change in one transaction and recomputes totals. If the record was the latest one, the vehicle's mileage is recomputed from the remaining records.
- **Exceptions:**
    - Mechanic edits someone else's record: `403`.
    - Changed mileage breaks the order of records: `422`.
- **Realized by:** `PUT /services/{key}`, `DELETE /services/{key}`
