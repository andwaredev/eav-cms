"""
Convert weight from text to measurement relation
"""

from yoyo import step

__depends__ = {"0012_category_enum"}

steps = [
    # Create a measurement entity for the existing weight (1.5 kg)
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '1.5 kg', 'weight-1-5-kg')
        """,
        "DELETE FROM entities WHERE slug = 'weight-1-5-kg' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'weight-1-5-kg'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             1.5)
        """,
        "DELETE FROM values_number WHERE entity_id = (SELECT id FROM entities WHERE slug = 'weight-1-5-kg')"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'weight-1-5-kg'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             'kg')
        """,
        "DELETE FROM values_text WHERE entity_id = (SELECT id FROM entities WHERE slug = 'weight-1-5-kg')"
    ),
    # Delete old text value for weight
    step(
        """
        DELETE FROM values_text
        WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'weight'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification'))
        """,
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'weight' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             '1.5kg')
        """
    ),
    # Update weight attribute to relation type
    step(
        """
        UPDATE attributes
        SET type = 'relation',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')
        WHERE slug = 'weight'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        """,
        """
        UPDATE attributes
        SET type = 'text', related_entity_type_id = NULL
        WHERE slug = 'weight'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        """
    ),
    # Create relation from specification to weight measurement
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'weight' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'weight-1-5-kg'))
        """,
        """
        DELETE FROM values_relation
        WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'weight'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification'))
        """
    ),
]
