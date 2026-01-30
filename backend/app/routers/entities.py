from typing import Any

from app.db import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter(prefix="/entities", tags=["entities"])


class EntityResponse(BaseModel):
    id: int
    name: str
    slug: str
    entity_type_id: int
    entity_type_name: str


class EntityDetailResponse(EntityResponse):
    values: dict[str, Any]


class UpdateEntityValuesRequest(BaseModel):
    values: dict[str, Any]


class CreateEntityRequest(BaseModel):
    entity_type_id: int
    name: str
    slug: str
    values: dict[str, Any] = {}


def fetch_entity_values(db: Session, entity_id: int, depth: int = 0, max_depth: int = 5) -> dict[str, Any]:
    """Fetch all values for an entity, recursively loading relations."""
    values: dict[str, Any] = {}

    # Text values
    text_result = db.execute(
        text("""
            SELECT a.slug, v.value
            FROM values_text v
            JOIN attributes a ON v.attribute_id = a.id
            WHERE v.entity_id = :entity_id
        """),
        {"entity_id": entity_id}
    )
    for row in text_result:
        values[row.slug] = row.value

    # Number values
    number_result = db.execute(
        text("""
            SELECT a.slug, v.value
            FROM values_number v
            JOIN attributes a ON v.attribute_id = a.id
            WHERE v.entity_id = :entity_id
        """),
        {"entity_id": entity_id}
    )
    for row in number_result:
        values[row.slug] = float(row.value) if row.value else None

    # Boolean values
    boolean_result = db.execute(
        text("""
            SELECT a.slug, v.value
            FROM values_boolean v
            JOIN attributes a ON v.attribute_id = a.id
            WHERE v.entity_id = :entity_id
        """),
        {"entity_id": entity_id}
    )
    for row in boolean_result:
        values[row.slug] = row.value

    # Datetime values
    datetime_result = db.execute(
        text("""
            SELECT a.slug, v.value
            FROM values_datetime v
            JOIN attributes a ON v.attribute_id = a.id
            WHERE v.entity_id = :entity_id
        """),
        {"entity_id": entity_id}
    )
    for row in datetime_result:
        values[row.slug] = row.value.isoformat() if row.value else None

    # JSON values
    json_result = db.execute(
        text("""
            SELECT a.slug, v.value
            FROM values_json v
            JOIN attributes a ON v.attribute_id = a.id
            WHERE v.entity_id = :entity_id
        """),
        {"entity_id": entity_id}
    )
    for row in json_result:
        values[row.slug] = row.value

    # Relation values (single) - recursively fetch related entities
    if depth < max_depth:
        relation_result = db.execute(
            text("""
                SELECT a.slug, v.related_entity_id, e.name, e.slug as entity_slug,
                       e.entity_type_id, et.name as entity_type_name
                FROM values_relation v
                JOIN attributes a ON v.attribute_id = a.id
                JOIN entities e ON v.related_entity_id = e.id
                JOIN entity_types et ON e.entity_type_id = et.id
                WHERE v.entity_id = :entity_id
            """),
            {"entity_id": entity_id}
        )
        for row in relation_result:
            # Recursively fetch the related entity's values
            related_values = fetch_entity_values(db, row.related_entity_id, depth + 1, max_depth)
            values[row.slug] = {
                "id": row.related_entity_id,
                "name": row.name,
                "slug": row.entity_slug,
                "entity_type_id": row.entity_type_id,
                "entity_type_name": row.entity_type_name,
                "values": related_values
            }

        # Multi-relation values (many-to-many) - returns array of related entities
        relation_multi_result = db.execute(
            text("""
                SELECT a.slug, v.related_entity_id, e.name, e.slug as entity_slug,
                       e.entity_type_id, et.name as entity_type_name
                FROM values_relation_multi v
                JOIN attributes a ON v.attribute_id = a.id
                JOIN entities e ON v.related_entity_id = e.id
                JOIN entity_types et ON e.entity_type_id = et.id
                WHERE v.entity_id = :entity_id
                ORDER BY a.slug, v.sort_order
            """),
            {"entity_id": entity_id}
        )
        for row in relation_multi_result:
            related_values = fetch_entity_values(db, row.related_entity_id, depth + 1, max_depth)
            related_entity = {
                "id": row.related_entity_id,
                "name": row.name,
                "slug": row.entity_slug,
                "entity_type_id": row.entity_type_id,
                "entity_type_name": row.entity_type_name,
                "values": related_values
            }
            # Append to array (multi-relation)
            if row.slug not in values:
                values[row.slug] = []
            values[row.slug].append(related_entity)

    return values


@router.get("", response_model=list[EntityResponse])
def list_entities(
    entity_type_id: int | None = Query(None, description="Filter by entity type"),
    db: Session = Depends(get_db)
):
    """List all entities, optionally filtered by entity type."""
    if entity_type_id:
        result = db.execute(
            text("""
                SELECT e.id, e.name, e.slug, e.entity_type_id, et.name as entity_type_name
                FROM entities e
                JOIN entity_types et ON e.entity_type_id = et.id
                WHERE e.entity_type_id = :entity_type_id
                ORDER BY e.name
            """),
            {"entity_type_id": entity_type_id}
        )
    else:
        result = db.execute(
            text("""
                SELECT e.id, e.name, e.slug, e.entity_type_id, et.name as entity_type_name
                FROM entities e
                JOIN entity_types et ON e.entity_type_id = et.id
                ORDER BY et.name, e.name
            """)
        )

    return [dict(row._mapping) for row in result]


@router.post("", response_model=EntityDetailResponse, status_code=201)
def create_entity(
    request: CreateEntityRequest,
    db: Session = Depends(get_db)
):
    """Create a new entity with optional initial values."""
    # Verify entity type exists
    type_result = db.execute(
        text("SELECT id, name FROM entity_types WHERE id = :id"),
        {"id": request.entity_type_id}
    )
    entity_type = type_result.fetchone()
    if not entity_type:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    # Create the entity
    result = db.execute(
        text("""
            INSERT INTO entities (entity_type_id, name, slug)
            VALUES (:entity_type_id, :name, :slug)
            RETURNING id
        """),
        {
            "entity_type_id": request.entity_type_id,
            "name": request.name,
            "slug": request.slug,
        }
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=500, detail="Failed to create entity")
    entity_id = row[0]

    # Set initial values if provided
    if request.values:
        # Get attributes for this entity type
        attributes_result = db.execute(
            text("""
                SELECT id, slug, type::text as type
                FROM attributes
                WHERE entity_type_id = :entity_type_id
            """),
            {"entity_type_id": request.entity_type_id}
        )
        attributes = {row.slug: {"id": row.id, "type": row.type} for row in attributes_result}

        for slug, value in request.values.items():
            if slug not in attributes:
                continue  # Skip unknown attributes

            attr = attributes[slug]
            attr_id = attr["id"]
            attr_type = attr["type"]

            if attr_type in ("text", "textarea", "hex"):
                _upsert_value(db, "values_text", entity_id, attr_id, value)
            elif attr_type == "number":
                _upsert_value(db, "values_number", entity_id, attr_id, value)
            elif attr_type == "boolean":
                _upsert_value(db, "values_boolean", entity_id, attr_id, value)
            elif attr_type == "datetime":
                _upsert_value(db, "values_datetime", entity_id, attr_id, value)
            elif attr_type == "json":
                _upsert_json_value(db, entity_id, attr_id, value)
            elif attr_type == "relation":
                _upsert_relation(db, entity_id, attr_id, value)
            elif attr_type == "relation_multi":
                _upsert_relation_multi(db, entity_id, attr_id, value)

    db.commit()
    return get_entity(entity_id, depth=5, db=db)


@router.get("/{entity_id}", response_model=EntityDetailResponse)
def get_entity(
    entity_id: int,
    depth: int = Query(5, description="Max depth for recursive relation loading"),
    db: Session = Depends(get_db)
):
    """Get an entity with all its attribute values, including nested relations."""
    result = db.execute(
        text("""
            SELECT e.id, e.name, e.slug, e.entity_type_id, et.name as entity_type_name
            FROM entities e
            JOIN entity_types et ON e.entity_type_id = et.id
            WHERE e.id = :id
        """),
        {"id": entity_id}
    )
    entity = result.fetchone()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    values = fetch_entity_values(db, entity_id, depth=0, max_depth=depth)

    return {
        **dict(entity._mapping),
        "values": values
    }


@router.get("/by-slug/{entity_type_name}/{slug}", response_model=EntityDetailResponse)
def get_entity_by_slug(
    entity_type_name: str,
    slug: str,
    depth: int = Query(5, description="Max depth for recursive relation loading"),
    db: Session = Depends(get_db)
):
    """Get an entity by its type and slug."""
    result = db.execute(
        text("""
            SELECT e.id
            FROM entities e
            JOIN entity_types et ON e.entity_type_id = et.id
            WHERE et.name = :entity_type_name AND e.slug = :slug
        """),
        {"entity_type_name": entity_type_name, "slug": slug}
    )
    entity = result.fetchone()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return get_entity(entity.id, depth, db)


@router.patch("/{entity_id}/values", response_model=EntityDetailResponse)
def update_entity_values(
    entity_id: int,
    request: UpdateEntityValuesRequest,
    db: Session = Depends(get_db)
):
    """Update values for an entity. Only updates provided attributes."""
    # Verify entity exists
    entity_result = db.execute(
        text("SELECT id, entity_type_id FROM entities WHERE id = :id"),
        {"id": entity_id}
    )
    entity = entity_result.fetchone()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    # Get attributes for this entity type
    attributes_result = db.execute(
        text("""
            SELECT id, slug, type::text as type
            FROM attributes
            WHERE entity_type_id = :entity_type_id
        """),
        {"entity_type_id": entity.entity_type_id}
    )
    attributes = {row.slug: {"id": row.id, "type": row.type} for row in attributes_result}

    # Update each provided value
    for slug, value in request.values.items():
        if slug not in attributes:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown attribute: {slug}"
            )

        attr = attributes[slug]
        attr_id = attr["id"]
        attr_type = attr["type"]

        # Determine table and update/insert value
        if attr_type in ("text", "textarea", "hex"):
            _upsert_value(db, "values_text", entity_id, attr_id, value)
        elif attr_type == "number":
            _upsert_value(db, "values_number", entity_id, attr_id, value)
        elif attr_type == "boolean":
            _upsert_value(db, "values_boolean", entity_id, attr_id, value)
        elif attr_type == "datetime":
            _upsert_value(db, "values_datetime", entity_id, attr_id, value)
        elif attr_type == "json":
            _upsert_json_value(db, entity_id, attr_id, value)
        elif attr_type == "relation":
            _upsert_relation(db, entity_id, attr_id, value)
        elif attr_type == "relation_multi":
            _upsert_relation_multi(db, entity_id, attr_id, value)

    db.commit()
    return get_entity(entity_id, depth=5, db=db)


@router.delete("/{entity_id}", status_code=204)
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    """Delete an entity and all its values."""
    # Check if entity exists
    entity_result = db.execute(
        text("SELECT id FROM entities WHERE id = :id"),
        {"id": entity_id}
    )
    if not entity_result.fetchone():
        raise HTTPException(status_code=404, detail="Entity not found")

    # Delete all values (cascade through value tables)
    db.execute(text("DELETE FROM values_text WHERE entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_number WHERE entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_boolean WHERE entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_datetime WHERE entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_json WHERE entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_relation WHERE entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_relation_multi WHERE entity_id = :id"), {"id": entity_id})

    # Also delete relations pointing TO this entity
    db.execute(text("DELETE FROM values_relation WHERE related_entity_id = :id"), {"id": entity_id})
    db.execute(text("DELETE FROM values_relation_multi WHERE related_entity_id = :id"), {"id": entity_id})

    # Delete the entity itself
    db.execute(text("DELETE FROM entities WHERE id = :id"), {"id": entity_id})

    db.commit()
    return None


def _upsert_value(db: Session, table: str, entity_id: int, attr_id: int, value: Any):
    """Insert or update a simple value."""
    # Try update first
    result = db.execute(
        text(f"""
            UPDATE {table}
            SET value = :value
            WHERE entity_id = :entity_id AND attribute_id = :attr_id
        """),
        {"value": value, "entity_id": entity_id, "attr_id": attr_id}
    )
    if result.rowcount == 0:  # type: ignore[union-attr]
        # Insert if no row was updated
        db.execute(
            text(f"""
                INSERT INTO {table} (entity_id, attribute_id, value)
                VALUES (:entity_id, :attr_id, :value)
            """),
            {"value": value, "entity_id": entity_id, "attr_id": attr_id}
        )


def _upsert_json_value(db: Session, entity_id: int, attr_id: int, value: Any):
    """Insert or update a JSON value."""
    import json
    json_str = json.dumps(value) if value is not None else None

    result = db.execute(
        text("""
            UPDATE values_json
            SET value = :value::jsonb
            WHERE entity_id = :entity_id AND attribute_id = :attr_id
        """),
        {"value": json_str, "entity_id": entity_id, "attr_id": attr_id}
    )
    if result.rowcount == 0:  # type: ignore[union-attr]
        db.execute(
            text("""
                INSERT INTO values_json (entity_id, attribute_id, value)
                VALUES (:entity_id, :attr_id, :value::jsonb)
            """),
            {"value": json_str, "entity_id": entity_id, "attr_id": attr_id}
        )


def _upsert_relation(db: Session, entity_id: int, attr_id: int, value: Any):
    """Insert or update a single relation value. Value should be the related entity ID."""
    related_id = value if isinstance(value, int) else (value.get("id") if isinstance(value, dict) else None)
    if related_id is None:
        # Delete the relation if value is None
        db.execute(
            text("""
                DELETE FROM values_relation
                WHERE entity_id = :entity_id AND attribute_id = :attr_id
            """),
            {"entity_id": entity_id, "attr_id": attr_id}
        )
        return

    result = db.execute(
        text("""
            UPDATE values_relation
            SET related_entity_id = :related_id
            WHERE entity_id = :entity_id AND attribute_id = :attr_id
        """),
        {"related_id": related_id, "entity_id": entity_id, "attr_id": attr_id}
    )
    if result.rowcount == 0:  # type: ignore[union-attr]
        db.execute(
            text("""
                INSERT INTO values_relation (entity_id, attribute_id, related_entity_id)
                VALUES (:entity_id, :attr_id, :related_id)
            """),
            {"related_id": related_id, "entity_id": entity_id, "attr_id": attr_id}
        )


def _upsert_relation_multi(db: Session, entity_id: int, attr_id: int, value: Any):
    """Replace all multi-relation values. Value should be a list of entity IDs or objects with 'id'."""
    # Delete existing relations
    db.execute(
        text("""
            DELETE FROM values_relation_multi
            WHERE entity_id = :entity_id AND attribute_id = :attr_id
        """),
        {"entity_id": entity_id, "attr_id": attr_id}
    )

    if not value:
        return

    # Insert new relations
    for sort_order, item in enumerate(value):
        related_id = item if isinstance(item, int) else (item.get("id") if isinstance(item, dict) else None)
        if related_id is not None:
            db.execute(
                text("""
                    INSERT INTO values_relation_multi (entity_id, attribute_id, related_entity_id, sort_order)
                    VALUES (:entity_id, :attr_id, :related_id, :sort_order)
                """),
                {"entity_id": entity_id, "attr_id": attr_id, "related_id": related_id, "sort_order": sort_order}
            )
