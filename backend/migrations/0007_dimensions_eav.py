"""
Convert dimensions from text to structured EAV entity
"""

from yoyo import step

__depends__ = {"0006_tags_seed"}

steps = [
    # Create a "dimensions" entity type
    step(
        """
        INSERT INTO entity_types (name, description) VALUES
            ('dimensions', 'Physical dimensions with width, height, depth')
        """,
        "DELETE FROM entity_types WHERE name = 'dimensions'"
    ),
    # Add attributes for dimensions
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Width', 'width', 'number', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Height', 'height', 'number', true, 2),
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Depth', 'depth', 'number', true, 3),
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Unit', 'unit', 'text', true, 4)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')"
    ),
    # Update specification's dimensions attribute to be a relation
    step(
        """
        UPDATE attributes
        SET type = 'relation',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')
        WHERE slug = 'dimensions'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        """,
        """
        UPDATE attributes
        SET type = 'text', related_entity_type_id = NULL
        WHERE slug = 'dimensions'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        """
    ),
    # Remove old text value for sample product specs dimensions
    step(
        """
        DELETE FROM values_text
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-specs')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'dimensions'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification'))
        """,
        """
        INSERT INTO values_text (entity_id, attribute_id, value)
        SELECT
            (SELECT id FROM entities WHERE slug = 'sample-product-specs'),
            (SELECT id FROM attributes WHERE slug = 'dimensions'
             AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
            '10x10x5cm'
        """
    ),
    # Create a dimensions entity for the sample product specs
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Sample Product Dimensions', 'sample-product-dimensions')
        """,
        "DELETE FROM entities WHERE slug = 'sample-product-dimensions'"
    ),
    # Add values to the dimensions entity (10x10x5cm = width:10, height:10, depth:5, unit:cm)
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'width' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             10),
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'height' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             10),
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'depth' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             5)
        """,
        "DELETE FROM values_number WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-dimensions')"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             'cm')
        """,
        "DELETE FROM values_text WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-dimensions')"
    ),
    # Create the relation from specification to dimensions
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'dimensions'
              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'sample-product-dimensions'))
        """,
        """
        DELETE FROM values_relation
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-specs')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'dimensions'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification'))
        """
    ),
]
