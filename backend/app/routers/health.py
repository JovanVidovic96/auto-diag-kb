from arango.database import StandardDatabase
from fastapi import APIRouter, Depends

from app.db.connection import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health(db: StandardDatabase = Depends(get_db)) -> dict:
    """Quick check that the API is up and the schema exists."""
    collections = [c for c in db.collections() if not c["system"]]
    return {
        "status": "ok",
        "arangodb": db.version(),
        "database": db.name,
        "document_collections": sum(1 for c in collections if c["type"] == "document"),
        "edge_collections": sum(1 for c in collections if c["type"] == "edge"),
        "graphs": sorted(g["name"] for g in db.graphs()),
        "views": sorted(v["name"] for v in db.views()),
    }
