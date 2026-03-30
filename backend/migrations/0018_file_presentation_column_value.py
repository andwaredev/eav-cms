"""
Add file_presentation_column_value entity type with a name attribute
"""

from yoyo import step

__depends__ = {"0017_update_hex_attribute"}

steps = [
    step(
        """
        INSERT INTO entity_types (name, description, category) VALUES
            ('file_presentation_column_value', 'File presentation column values', 'content')
        """,
        "DELETE FROM entity_types WHERE name = 'file_presentation_column_value'"
    ),
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'file_presentation_column_value'), 'Name', 'name', 'text', true, 1)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'file_presentation_column_value')"
    ),
]
