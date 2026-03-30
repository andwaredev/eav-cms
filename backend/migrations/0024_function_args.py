"""
Add args attribute to function component (ordered list of any component instance)
"""

from yoyo import step

__depends__ = {"0023_values_function_key_table"}

steps = [
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order)
        VALUES (
            (SELECT id FROM entity_types WHERE name = 'function'),
            'Args',
            'args',
            'relation_multi',
            false,
            2
        )
        """,
        """
        DELETE FROM attributes
        WHERE slug = 'args'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'function')
        """
    ),
]
