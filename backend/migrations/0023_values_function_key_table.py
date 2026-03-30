"""
Create values_function_key table to store function_key enum values
"""

from yoyo import step

__depends__ = {"0022_function_component"}

steps = [
    step(
        """
        CREATE TABLE values_function_key (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            value function_key NOT NULL,
            UNIQUE(entity_id, attribute_id)
        )
        """,
        "DROP TABLE values_function_key"
    ),
    step(
        "CREATE INDEX idx_values_function_key_entity ON values_function_key(entity_id)",
        "DROP INDEX idx_values_function_key_entity"
    ),
]
