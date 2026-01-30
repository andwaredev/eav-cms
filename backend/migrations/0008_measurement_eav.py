"""
Convert individual dimensions to measurement entities with value + unit
"""

from yoyo import step

__depends__ = {"0007_dimensions_eav"}

steps = [
    # Create a "measurement" entity type (value + unit pair)
    step(
        """
        INSERT INTO entity_types (name, description) VALUES
            ('measurement', 'A numeric value with a unit (e.g., 10 cm, 5 kg)')
        """,
        "DELETE FROM entity_types WHERE name = 'measurement'"
    ),
    # Add attributes for measurement
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'measurement'), 'Value', 'value', 'number', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), 'Unit', 'unit', 'text', true, 2)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')"
    ),
    # Update dimensions entity type: width, height, depth become relations to measurement
    step(
        """
        UPDATE attributes
        SET type = 'relation',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')
        WHERE slug IN ('width', 'height', 'depth')
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')
        """,
        """
        UPDATE attributes
        SET type = 'number', related_entity_type_id = NULL
        WHERE slug IN ('width', 'height', 'depth')
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')
        """
    ),
    # Remove the unit attribute from dimensions (each measurement has its own unit now)
    step(
        """
        DELETE FROM values_text
        WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'unit'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions'))
        """,
        ""
    ),
    step(
        """
        DELETE FROM attributes
        WHERE slug = 'unit'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')
        """,
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order)
        VALUES ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Unit', 'unit', 'text', true, 4)
        """
    ),
    # Remove old number values for sample product dimensions
    step(
        """
        DELETE FROM values_number
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-dimensions')
        """,
        ""
    ),
    # Create measurement entities for width, height, depth
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'measurement'), 'Width: 10cm', 'sample-product-width'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), 'Height: 10cm', 'sample-product-height'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), 'Depth: 5cm', 'sample-product-depth')
        """,
        "DELETE FROM entities WHERE slug IN ('sample-product-width', 'sample-product-height', 'sample-product-depth')"
    ),
    # Add values to measurement entities
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-width'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             10),
            ((SELECT id FROM entities WHERE slug = 'sample-product-height'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             10),
            ((SELECT id FROM entities WHERE slug = 'sample-product-depth'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             5)
        """,
        "DELETE FROM values_number WHERE entity_id IN (SELECT id FROM entities WHERE slug IN ('sample-product-width', 'sample-product-height', 'sample-product-depth'))"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-width'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             'cm'),
            ((SELECT id FROM entities WHERE slug = 'sample-product-height'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             'cm'),
            ((SELECT id FROM entities WHERE slug = 'sample-product-depth'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')),
             'cm')
        """,
        "DELETE FROM values_text WHERE entity_id IN (SELECT id FROM entities WHERE slug IN ('sample-product-width', 'sample-product-height', 'sample-product-depth'))"
    ),
    # Create relations from dimensions to measurement entities
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'width' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'sample-product-width')),
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'height' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'sample-product-height')),
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'depth' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'sample-product-depth'))
        """,
        """
        DELETE FROM values_relation
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-dimensions')
          AND attribute_id IN (SELECT id FROM attributes WHERE slug IN ('width', 'height', 'depth')
                               AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions'))
        """
    ),
]
