"""
Add function component entity type with a key attribute of type function_key
"""

from yoyo import step

__depends__ = {"0021_function_key_enum"}

steps = [
    step(
        """
        INSERT INTO entity_types (name, description, category) VALUES
            ('function', 'A function component with a function_key value', 'component')
        """,
        "DELETE FROM entity_types WHERE name = 'function'"
    ),
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'function'), 'Key', 'key', 'function_key', true, 1)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'function')"
    ),
]
