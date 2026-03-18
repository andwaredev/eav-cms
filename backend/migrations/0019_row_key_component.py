"""
Add row_key component entity type with a value attribute
"""

from yoyo import step

__depends__ = {"0018_file_presentation_column_value"}

steps = [
    step(
        """
        INSERT INTO entity_types (name, description, category) VALUES
            ('row_key', 'A row key component with a text value', 'component')
        """,
        "DELETE FROM entity_types WHERE name = 'row_key'"
    ),
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'row_key'), 'Value', 'value', 'text', true, 1)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'row_key')"
    ),
]
