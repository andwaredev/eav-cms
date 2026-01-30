from app.db import get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter(prefix="/entity-types", tags=["entity-types"])


class RelatedEntityType(BaseModel):
    id: int
    name: str


class AttributeResponse(BaseModel):
    id: int
    name: str
    slug: str
    type: str
    is_required: bool
    default_value: str | None
    sort_order: int
    related_entity_type: RelatedEntityType | None = None


class EntityTypeResponse(BaseModel):
    id: int
    name: str
    description: str | None
    category: str


class EntityTypeDetailResponse(EntityTypeResponse):
    attributes: list[AttributeResponse]


@router.get("", response_model=list[EntityTypeResponse])
def list_entity_types(db: Session = Depends(get_db)):
    """List all entity types."""
    result = db.execute(
        text("SELECT id, name, description, category FROM entity_types ORDER BY category, name")
    )
    return [dict(row._mapping) for row in result]


@router.get("/{entity_type_id}", response_model=EntityTypeDetailResponse)
def get_entity_type(entity_type_id: int, db: Session = Depends(get_db)):
    """Get an entity type with its attributes."""
    result = db.execute(
        text("SELECT id, name, description, category FROM entity_types WHERE id = :id"),
        {"id": entity_type_id}
    )
    entity_type = result.fetchone()

    if not entity_type:
        raise HTTPException(status_code=404, detail="Entity type not found")

    attributes_result = db.execute(
        text("""
            SELECT a.id, a.name, a.slug, a.type::text, a.is_required,
                   a.default_value, a.sort_order, a.related_entity_type_id,
                   ret.name as related_entity_type_name
            FROM attributes a
            LEFT JOIN entity_types ret ON a.related_entity_type_id = ret.id
            WHERE a.entity_type_id = :entity_type_id
            ORDER BY a.sort_order
        """),
        {"entity_type_id": entity_type_id}
    )

    attributes = []
    for row in attributes_result:
        attr = {
            "id": row.id,
            "name": row.name,
            "slug": row.slug,
            "type": row.type,
            "is_required": row.is_required,
            "default_value": row.default_value,
            "sort_order": row.sort_order,
            "related_entity_type": None
        }
        if row.related_entity_type_id:
            attr["related_entity_type"] = {
                "id": row.related_entity_type_id,
                "name": row.related_entity_type_name
            }
        attributes.append(attr)

    return {
        **dict(entity_type._mapping),
        "attributes": attributes
    }
