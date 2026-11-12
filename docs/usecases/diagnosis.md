# Use cases: diagnosis and lookup

## UC-10 Diagnose by symptoms

- **Actor:** any logged-in user
- **Precondition:** at least one symptom exists.
- **Flow:**
    1. User opens Diagnose and picks one or more symptoms from the list.
    2. Optionally the user picks a vehicle (owners see only their own, mechanics search by VIN or plate).
    3. System returns codes ranked by how many picked symptoms they explain, then by total weight. With a vehicle, only known issues of its engine are kept.
    4. User opens a code and sees its causes with probability, affected parts and solutions with cost and time (UC-11).
- **Exceptions:**
    - No symptom picked: the button is disabled; the API returns `422`.
    - No code matches: empty result with a hint to pick fewer symptoms or remove the vehicle filter.
    - Owner picks a vehicle he does not own: `403`.
- **Realized by:** `POST /diagnose` (Q6), then `GET /dtc/{code}/diagnosis` (Q7)

## UC-11 Look up a code

- **Actor:** any logged-in user
- **Precondition:** none.
- **Flow:**
    1. User types a code, for example `P0420`.
    2. System shows description, severity, category and system.
    3. System shows the diagnosis tree: causes, components, solutions.
    4. User can open the graph view of the code and its neighbors.
- **Exceptions:** unknown code: `404`, UI suggests full-text search.
- **Realized by:** `GET /dtc/{code}` (Q2), `GET /dtc/{code}/diagnosis` (Q7)

## UC-12 Search knowledge base

- **Actor:** any logged-in user
- **Precondition:** none.
- **Flow:**
    1. User types free text in English or Serbian, for example "trza na leru".
    2. System returns matching symptoms, codes, causes and components ranked by relevance.
    3. User opens a result.
- **Exceptions:** query shorter than 2 characters: `422`.
- **Realized by:** `GET /search` (Q5)

## UC-13 Browse catalog

- **Actor:** any logged-in user
- **Precondition:** none.
- **Flow:**
    1. User picks a maker and sees its models and engines.
    2. User opens an engine and sees its components and known issues by frequency.
    3. User can ask for the path between two items, for example a symptom and a solution.
- **Exceptions:** no path found: the UI says so.
- **Realized by:** `GET /manufacturers/{key}/models` (Q10), `GET /engines/{key}`, `GET /components/{key}/impact` (Q8), `GET /paths` (Q11)

## UC-14 Find nearest workshop

- **Actor:** any logged-in user
- **Precondition:** workshops have coordinates.
- **Flow:**
    1. User enters a location or picks a city.
    2. System lists workshops sorted by distance.
- **Exceptions:** invalid coordinates: `422`.
- **Realized by:** `GET /workshops?lat=&lon=` (Q18)
