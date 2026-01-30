"""
Add relation attribute type enum value
"""

from yoyo import step

__depends__ = {"0002_seed_data"}

steps = [
    # Add 'relation' to the attribute_type enum
    step(
        "ALTER TYPE attribute_type ADD VALUE 'relation'",
        # Can't easily remove enum values in PostgreSQL
    ),
    # Add related_entity_type_id to attributes table
    step(
        """
        ALTER TABLE attributes
        ADD COLUMN related_entity_type_id INTEGER REFERENCES entity_types(id) ON DELETE SET NULL
        """,
        "ALTER TABLE attributes DROP COLUMN related_entity_type_id"
    ),
    # Create values_relation table for entity references
    step(
        """
        CREATE TABLE values_relation (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            related_entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_relation"
    ),
    step(
        "CREATE INDEX idx_values_relation_entity ON values_relation(entity_id)",
        "DROP INDEX idx_values_relation_entity"
    ),
    step(
        "CREATE INDEX idx_values_relation_related ON values_relation(related_entity_id)",
        "DROP INDEX idx_values_relation_related"
    ),
]
