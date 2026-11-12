"""Creates everything the application needs in ArangoDB.

Idempotent: it checks what exists and creates only what is missing,
so it is safe to run on every start.

Run by hand:  python -m app.db.schema
"""

import logging

from arango.database import StandardDatabase

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Collections
# ---------------------------------------------------------------------------

DOCUMENT_COLLECTIONS = [
    # catalog
    "manufacturers",
    "models",
    "engines",
    "components",
    # knowledge base
    "dtc_codes",
    "symptoms",
    "causes",
    "solutions",
    # service history
    "users",
    "vehicles",
    "service_records",
    "workshops",
]

# graph name -> list of (edge collection, [from collections], [to collections])
GRAPHS = {
    "diagnostic_graph": [
        ("has_model", ["manufacturers"], ["models"]),
        ("has_engine", ["models"], ["engines"]),
        ("has_component", ["engines"], ["components"]),
        ("known_issue", ["engines"], ["dtc_codes"]),
        ("exhibits", ["dtc_codes"], ["symptoms"]),
        ("caused_by", ["dtc_codes"], ["causes"]),
        ("affects", ["causes"], ["components"]),
        ("fixed_by", ["causes"], ["solutions"]),
    ],
    "service_graph": [
        ("owns", ["users"], ["vehicles"]),
        ("works_at", ["users"], ["workshops"]),
        ("is_model", ["vehicles"], ["models"]),
        ("powered_by", ["vehicles"], ["engines"]),
        ("serviced", ["vehicles"], ["service_records"]),
        ("performed_at", ["service_records"], ["workshops"]),
        ("performed_by", ["service_records"], ["users"]),
        ("found_code", ["service_records"], ["dtc_codes"]),
        ("replaced", ["service_records"], ["components"]),
    ],
}

EDGE_COLLECTIONS = [edge for defs in GRAPHS.values() for edge, _, _ in defs]

# ---------------------------------------------------------------------------
# Indexes (see docs/database/indexes.md)
# ---------------------------------------------------------------------------

# collection -> list of index definitions (ArangoDB REST format)
INDEXES = {
    "dtc_codes": [
        {"name": "idx_dtc_code", "type": "persistent", "fields": ["code"], "unique": True},
        {"name": "idx_dtc_category_severity", "type": "persistent", "fields": ["category", "severity"]},
    ],
    "vehicles": [
        {"name": "idx_vehicle_vin", "type": "persistent", "fields": ["vin"], "unique": True},
        {
            "name": "idx_vehicle_registration",
            "type": "persistent",
            "fields": ["registration"],
            "unique": True,
            "sparse": True,
        },
    ],
    "users": [
        {"name": "idx_user_username", "type": "persistent", "fields": ["username"], "unique": True},
        {"name": "idx_user_email", "type": "persistent", "fields": ["email"], "unique": True},
    ],
    "service_records": [
        {"name": "idx_service_date", "type": "persistent", "fields": ["date"]},
        {"name": "idx_service_mileage", "type": "persistent", "fields": ["mileage_km"]},
    ],
    # vertex-centric indexes: _from + an edge attribute
    "known_issue": [
        {"name": "vci_known_issue_frequency", "type": "persistent", "fields": ["_from", "frequency"]},
    ],
    "caused_by": [
        {"name": "vci_caused_by_probability", "type": "persistent", "fields": ["_from", "probability"]},
    ],
    "owns": [
        {"name": "vci_owns_until", "type": "persistent", "fields": ["_from", "until"]},
    ],
    "workshops": [
        # geoJson false: location is stored as [lat, lon]
        {"name": "geo_workshop_location", "type": "geo", "fields": ["location"], "geoJson": False},
    ],
}

# ---------------------------------------------------------------------------
# ArangoSearch
# ---------------------------------------------------------------------------

SEARCH_FEATURES = ["frequency", "norm", "position"]

ANALYZERS = {
    # Serbian words: lower case, accents removed ("kocnica" finds "kočnica"), no stemming.
    "text_sr": {
        "type": "text",
        "properties": {"locale": "sr", "case": "lower", "accent": False, "stemming": False, "stopwords": []},
    },
    # Partial words: normalize, then split into 3 to 5 character n-grams.
    "ngram_sr": {
        "type": "pipeline",
        "properties": {
            "pipeline": [
                {"type": "norm", "properties": {"locale": "sr", "case": "lower", "accent": False}},
                {
                    "type": "ngram",
                    "properties": {"min": 3, "max": 5, "preserveOriginal": True, "streamType": "utf8"},
                },
            ]
        },
    },
}

SEARCH_VIEW = "kb_search"


def _lang_field() -> dict:
    """Link definition for a language object {"en": ..., "sr": ...}."""
    return {
        "fields": {
            "en": {"analyzers": ["text_en"]},
            "sr": {"analyzers": ["text_sr", "ngram_sr"]},
        }
    }


SEARCH_LINKS = {
    "symptoms": {"fields": {"name": _lang_field(), "description": _lang_field()}},
    "dtc_codes": {"fields": {"code": {"analyzers": ["identity"]}, "description": _lang_field()}},
    "causes": {"fields": {"title": _lang_field()}},
    "components": {"fields": {"name": _lang_field()}},
}

# ---------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------


def _ensure_collections(db: StandardDatabase) -> None:
    for name in DOCUMENT_COLLECTIONS:
        if not db.has_collection(name):
            db.create_collection(name)
            log.info("Created collection %s", name)
    for name in EDGE_COLLECTIONS:
        if not db.has_collection(name):
            db.create_collection(name, edge=True)
            log.info("Created edge collection %s", name)


def _ensure_graphs(db: StandardDatabase) -> None:
    for graph_name, definitions in GRAPHS.items():
        graph = db.graph(graph_name) if db.has_graph(graph_name) else db.create_graph(graph_name)
        for edge, from_cols, to_cols in definitions:
            if not graph.has_edge_definition(edge):
                graph.create_edge_definition(
                    edge_collection=edge,
                    from_vertex_collections=from_cols,
                    to_vertex_collections=to_cols,
                )
                log.info("Graph %s: added edge definition %s", graph_name, edge)


def _ensure_indexes(db: StandardDatabase) -> None:
    for collection, indexes in INDEXES.items():
        col = db.collection(collection)
        existing = {idx.get("name") for idx in col.indexes()}
        for definition in indexes:
            if definition["name"] not in existing:
                col.add_index(definition)
                log.info("Created index %s on %s", definition["name"], collection)


def _ensure_analyzers(db: StandardDatabase) -> None:
    # Names come back with the database prefix, e.g. "autodiag::text_sr".
    existing = {a["name"].split("::")[-1] for a in db.analyzers()}
    for name, spec in ANALYZERS.items():
        if name not in existing:
            db.create_analyzer(name, spec["type"], spec["properties"], SEARCH_FEATURES)
            log.info("Created analyzer %s", name)


def _ensure_view(db: StandardDatabase) -> None:
    properties = {"links": SEARCH_LINKS}
    existing = {v["name"] for v in db.views()}
    if SEARCH_VIEW in existing:
        # Replace links so changes in SEARCH_LINKS are applied on restart.
        db.replace_arangosearch_view(SEARCH_VIEW, properties)
    else:
        db.create_arangosearch_view(SEARCH_VIEW, properties)
        log.info("Created view %s", SEARCH_VIEW)


def ensure_schema(db: StandardDatabase) -> None:
    """Order matters: collections before graphs and indexes,
    analyzers before the view that uses them."""
    _ensure_collections(db)
    _ensure_graphs(db)
    _ensure_indexes(db)
    _ensure_analyzers(db)
    _ensure_view(db)
    log.info("Schema of database %s is up to date", db.name)


if __name__ == "__main__":
    from app.config import get_settings
    from app.db.connection import ensure_database, wait_for_server

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    wait_for_server()
    ensure_schema(ensure_database(get_settings().arango_db))
