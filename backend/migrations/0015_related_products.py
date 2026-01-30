"""
Add related_products multi-relation to product entity type
"""

from yoyo import step

__depends__ = {"0014_more_products"}

steps = [
    # Add related_products attribute to product entity type
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order, related_entity_type_id)
        VALUES (
            (SELECT id FROM entity_types WHERE name = 'product'),
            'Related Products',
            'related_products',
            'relation_multi',
            false,
            6,
            (SELECT id FROM entity_types WHERE name = 'product')
        )
        """,
        """
        DELETE FROM attributes
        WHERE slug = 'related_products'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')
        """
    ),
    # Sample Product -> related to Wireless Headphones, Mechanical Keyboard
    step(
        """
        INSERT INTO values_relation_multi (entity_id, attribute_id, related_entity_id, sort_order) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             0),
            ((SELECT id FROM entities WHERE slug = 'sample-product'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             1)
        """,
        """
        DELETE FROM values_relation_multi
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'related_products')
        """
    ),
    # Wireless Headphones -> related to USB-C Cable, Mechanical Keyboard
    step(
        """
        INSERT INTO values_relation_multi (entity_id, attribute_id, related_entity_id, sort_order) VALUES
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             0),
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             1)
        """,
        """
        DELETE FROM values_relation_multi
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'wireless-headphones')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'related_products')
        """
    ),
    # Mechanical Keyboard -> related to USB-C Cable, Wireless Headphones
    step(
        """
        INSERT INTO values_relation_multi (entity_id, attribute_id, related_entity_id, sort_order) VALUES
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             0),
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             1)
        """,
        """
        DELETE FROM values_relation_multi
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'mechanical-keyboard')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'related_products')
        """
    ),
    # USB-C Cable -> related to Wireless Headphones, Mechanical Keyboard
    step(
        """
        INSERT INTO values_relation_multi (entity_id, attribute_id, related_entity_id, sort_order) VALUES
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             0),
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'related_products' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             1)
        """,
        """
        DELETE FROM values_relation_multi
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'usb-c-charging-cable')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'related_products')
        """
    ),
]
