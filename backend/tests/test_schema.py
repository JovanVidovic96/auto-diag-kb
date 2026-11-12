from app.db.schema import (
    ANALYZERS,
    DOCUMENT_COLLECTIONS,
    EDGE_COLLECTIONS,
    GRAPHS,
    INDEXES,
    SEARCH_VIEW,
    ensure_schema,
)


def test_counts_match_the_docs():
    assert len(DOCUMENT_COLLECTIONS) == 12
    assert len(EDGE_COLLECTIONS) == 17
    assert len(set(EDGE_COLLECTIONS)) == 17  # no edge collection in two graphs


def test_document_collections_exist(db):
    for name in DOCUMENT_COLLECTIONS:
        assert db.has_collection(name), name
        assert not db.collection(name).properties()["edge"]


def test_edge_collections_exist(db):
    for name in EDGE_COLLECTIONS:
        assert db.has_collection(name), name
        assert db.collection(name).properties()["edge"]


def test_graphs_have_all_edge_definitions(db):
    for graph_name, definitions in GRAPHS.items():
        assert db.has_graph(graph_name)
        graph = db.graph(graph_name)
        actual = {d["edge_collection"] for d in graph.edge_definitions()}
        assert actual == {edge for edge, _, _ in definitions}


def test_indexes_exist(db):
    for collection, indexes in INDEXES.items():
        names = {idx.get("name") for idx in db.collection(collection).indexes()}
        for definition in indexes:
            assert definition["name"] in names, f"{collection}.{definition['name']}"


def test_unique_index_rejects_duplicates(db):
    users = db.collection("users")
    users.insert({"username": "dup", "email": "a@test.rs"})
    try:
        users.insert({"username": "dup", "email": "b@test.rs"})
        raise AssertionError("duplicate username was accepted")
    except Exception as exc:  # DocumentInsertError, unique constraint violated
        assert "unique constraint" in str(exc)
    finally:
        users.truncate()


def test_analyzers_and_view_exist(db):
    names = {a["name"].split("::")[-1] for a in db.analyzers()}
    assert set(ANALYZERS) <= names
    assert SEARCH_VIEW in {v["name"] for v in db.views()}


def test_ensure_schema_is_idempotent(db):
    ensure_schema(db)  # second run must not fail or duplicate anything
    count = len([c for c in db.collections() if not c["system"]])
    assert count == 12 + 17
