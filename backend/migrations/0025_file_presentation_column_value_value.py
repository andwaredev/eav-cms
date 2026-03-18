"""
Add value attribute to file_presentation_column_value (single relation to any content entity)
"""

from yoyo import step

__depends__ = {"0024_function_args"}

steps = [
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order)
        VALUES (
            (SELECT id FROM entity_types WHERE name = 'file_presentation_column_value'),
            'Value',
            'value',
            'relation',
            false,
            2
        )
        """,
        """
        DELETE FROM attributes
        WHERE slug = 'value'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'file_presentation_column_value')
        """
    ),
]
