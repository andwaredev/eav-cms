"""
Seed relation data - converts product specifications from JSON to relation
"""

from yoyo import step

__depends__ = {"0003_add_relation_type"}

steps = [
    # Create a "Specification" entity type for product specs
    step(
        """
        INSERT INTO entity_types (name, description) VALUES
            ('specification', 'Product specifications as structured data')
        """,
        "DELETE FROM entity_types WHERE name = 'specification'"
    ),
    # Add attributes for specifications
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'Weight', 'weight', 'text', false, 1),
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'Dimensions', 'dimensions', 'text', false, 2),
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'Color', 'color', 'text', false, 3)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')"
    ),
    # Update product's specifications attribute to be a relation instead of JSON
    step(
        """
        UPDATE attributes
        SET type = 'relation',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        WHERE slug = 'specifications'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')
        """,
        """
        UPDATE attributes
        SET type = 'json', related_entity_type_id = NULL
        WHERE slug = 'specifications'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')
        """
    ),
    # Remove old JSON value for sample product specifications
    step(
        """
        DELETE FROM values_json
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'specifications'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product'))
        """,
        """
        INSERT INTO values_json (entity_id, attribute_id, value)
        SELECT
            (SELECT id FROM entities WHERE slug = 'sample-product'),
            (SELECT id FROM attributes WHERE slug = 'specifications'
             AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
            '{"weight": "1.5kg", "dimensions": "10x10x5cm", "color": "black"}'
        """
    ),
    # Create a specification entity for the sample product
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'Sample Product Specs', 'sample-product-specs')
        """,
        "DELETE FROM entities WHERE slug = 'sample-product-specs'"
    ),
    # Add values to the specification entity
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'weight' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             '1.5kg'),
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'dimensions' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             '10x10x5cm'),
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             'black')
        """,
        "DELETE FROM values_text WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-specs')"
    ),
    # Create the relation from product to specification
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product'),
             (SELECT id FROM attributes WHERE slug = 'specifications'
              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'sample-product-specs'))
        """,
        "DELETE FROM values_relation WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')"
    ),
]
