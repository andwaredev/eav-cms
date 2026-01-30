"""
Update color's hex attribute to use hex type
"""

from yoyo import step

__depends__ = {"0016_hex_attribute_type"}

steps = [
    step(
        """
        UPDATE attributes
        SET type = 'hex'
        WHERE slug = 'hex'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')
        """,
        """
        UPDATE attributes
        SET type = 'text'
        WHERE slug = 'hex'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')
        """
    ),
]
