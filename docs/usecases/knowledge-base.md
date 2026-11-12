# Use cases: knowledge base and catalog

## UC-06 Manage knowledge base

- **Actor:** Admin
- **Precondition:** logged in as admin.
- **Flow:**
    1. Admin opens Knowledge base admin and picks a type: code, symptom, cause or solution.
    2. Admin creates a new item or edits an existing one, with English and optionally Serbian text.
    3. System validates and saves it, setting `updated_at`.
- **Exceptions:**
    - Invalid code format or missing English text: `422`.
    - Key already exists on create: `409`.
    - Deleting a code that appears in a service record: `409`. Other items are deleted together with their edges.
- **Realized by:** `POST/PUT/DELETE /dtc`, `/symptoms`, `/causes`, `/solutions`; Q3 for symptoms

## UC-07 Manage catalog

- **Actor:** Admin
- **Precondition:** logged in as admin.
- **Flow:**
    1. Admin opens the catalog part of Knowledge base admin.
    2. Admin creates or edits a maker, model, engine or component.
    3. When creating a model, admin picks the maker; system creates the `has_model` edge in the same request.
- **Exceptions:**
    - Deleting a component used in a service record: `409`.
    - Deleting a model or engine linked to a vehicle: `409`.
- **Realized by:** `POST/PUT/DELETE /manufacturers`, `/models`, `/engines`, `/components`

## UC-08 Link knowledge base items

- **Actor:** Admin
- **Precondition:** both items exist.
- **Flow:**
    1. Admin opens an item, for example code P0420, and chooses Add link.
    2. Admin picks the edge type (`exhibits`, `caused_by`, `affects`, `fixed_by`, `known_issue`, `has_engine`, `has_component`), the target and the edge attributes (weight, probability, priority, frequency, years).
    3. System checks the rules and saves the edge.
- **Exceptions:**
    - Target not allowed for that edge type (named graph definition): `422`.
    - `caused_by` probabilities of the code would go over 1: `422` with the current sum.
    - Same link already exists: `409`.
- **Realized by:** `POST /links/{edge_collection}`, `DELETE /links/{edge_collection}/{key}`
