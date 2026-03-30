"""
Add text component entity type with a value attribute
"""

from yoyo import step

__depends__ = {"0019_row_key_component"}

steps = [
    step(
        """
        INSERT INTO entity_types (name, description, category) VALUES
            ('text', 'A text component with a text value', 'component')
        """,
        "DELETE FROM entity_types WHERE name = 'text'"
    ),
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'text'), 'Value', 'value', 'text', true, 1)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'text')"
    ),
]
