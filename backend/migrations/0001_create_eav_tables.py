"""
Create EAV (Entity-Attribute-Value) schema for CMS
"""

from yoyo import step

steps = [
    step(
        """
        CREATE TABLE entity_types (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        "DROP TABLE entity_types"
    ),
    step(
        """
        CREATE TABLE entities (
            id SERIAL PRIMARY KEY,
            entity_type_id INTEGER NOT NULL REFERENCES entity_types(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            slug VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_type_id, slug)
        )
        """,
        "DROP TABLE entities"
    ),
    step(
        """
        CREATE TYPE attribute_type AS ENUM ('text', 'textarea', 'number', 'boolean', 'date', 'datetime', 'json')
        """,
        "DROP TYPE attribute_type"
    ),
    step(
        """
        CREATE TABLE attributes (
            id SERIAL PRIMARY KEY,
            entity_type_id INTEGER NOT NULL REFERENCES entity_types(id) ON DELETE CASCADE,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(100) NOT NULL,
            type attribute_type NOT NULL DEFAULT 'text',
            is_required BOOLEAN DEFAULT FALSE,
            default_value TEXT,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_type_id, slug)
        )
        """,
        "DROP TABLE attributes"
    ),
    step(
        """
        CREATE TABLE values_text (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            value TEXT,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_text"
    ),
    step(
        """
        CREATE TABLE values_number (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            value NUMERIC,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_number"
    ),
    step(
        """
        CREATE TABLE values_boolean (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            value BOOLEAN,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_boolean"
    ),
    step(
        """
        CREATE TABLE values_datetime (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            value TIMESTAMP,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_datetime"
    ),
    step(
        """
        CREATE TABLE values_json (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            value JSONB,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_json"
    ),
    step(
        """
        CREATE INDEX idx_entities_type ON entities(entity_type_id);
        CREATE INDEX idx_attributes_type ON attributes(entity_type_id);
        CREATE INDEX idx_values_text_entity ON values_text(entity_id);
        CREATE INDEX idx_values_number_entity ON values_number(entity_id);
        CREATE INDEX idx_values_boolean_entity ON values_boolean(entity_id);
        CREATE INDEX idx_values_datetime_entity ON values_datetime(entity_id);
        CREATE INDEX idx_values_json_entity ON values_json(entity_id);
        """,
        """
        DROP INDEX idx_values_json_entity;
        DROP INDEX idx_values_datetime_entity;
        DROP INDEX idx_values_boolean_entity;
        DROP INDEX idx_values_number_entity;
        DROP INDEX idx_values_text_entity;
        DROP INDEX idx_attributes_type;
        DROP INDEX idx_entities_type;
        """
    ),
]
