"""
Convert color from text to EAV entity with name and hex code
"""

from yoyo import step

__depends__ = {"0008_measurement_eav"}

steps = [
    # Create a "color" entity type
    step(
        """
        INSERT INTO entity_types (name, description) VALUES
            ('color', 'A color with name and hex code')
        """,
        "DELETE FROM entity_types WHERE name = 'color'"
    ),
    # Add attributes for color
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Name', 'name', 'text', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Hex', 'hex', 'text', true, 2)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')"
    ),
    # Create seed color entities
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Black', 'black'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'White', 'white'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Red', 'red'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Green', 'green'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Blue', 'blue'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Yellow', 'yellow'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Orange', 'orange'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Purple', 'purple'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Gray', 'gray'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Navy', 'navy')
        """,
        "DELETE FROM entities WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')"
    ),
    # Add values to color entities
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value)
        SELECT e.id,
               (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
               e.name
        FROM entities e
        WHERE e.entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')
        """,
        "DELETE FROM values_text WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color'))"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'black' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#000000'),
            ((SELECT id FROM entities WHERE slug = 'white' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#FFFFFF'),
            ((SELECT id FROM entities WHERE slug = 'red' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#EF4444'),
            ((SELECT id FROM entities WHERE slug = 'green' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#22C55E'),
            ((SELECT id FROM entities WHERE slug = 'blue' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#3B82F6'),
            ((SELECT id FROM entities WHERE slug = 'yellow' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#EAB308'),
            ((SELECT id FROM entities WHERE slug = 'orange' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#F97316'),
            ((SELECT id FROM entities WHERE slug = 'purple' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#A855F7'),
            ((SELECT id FROM entities WHERE slug = 'gray' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#6B7280'),
            ((SELECT id FROM entities WHERE slug = 'navy' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#1E3A5F')
        """,
        "DELETE FROM values_text WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color'))"
    ),
    # Update specification's color attribute to be a relation
    step(
        """
        UPDATE attributes
        SET type = 'relation',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')
        WHERE slug = 'color'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        """,
        """
        UPDATE attributes
        SET type = 'text', related_entity_type_id = NULL
        WHERE slug = 'color'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')
        """
    ),
    # Remove old text value for sample product specs color
    step(
        """
        DELETE FROM values_text
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-specs')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'color'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification'))
        """,
        """
        INSERT INTO values_text (entity_id, attribute_id, value)
        SELECT
            (SELECT id FROM entities WHERE slug = 'sample-product-specs'),
            (SELECT id FROM attributes WHERE slug = 'color'
             AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
            'black'
        """
    ),
    # Create relation from specification to black color
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product-specs'),
             (SELECT id FROM attributes WHERE slug = 'color'
              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'black' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')))
        """,
        """
        DELETE FROM values_relation
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product-specs')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'color'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification'))
        """
    ),
]
