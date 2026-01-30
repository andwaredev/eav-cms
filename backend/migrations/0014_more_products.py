"""
Seed additional sample products
"""

from yoyo import step

__depends__ = {"0013_weight_measurement"}

steps = [
    # === Product 2: Wireless Headphones ===
    # Create measurements for headphones
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '250 g', 'headphones-weight'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '18 cm', 'headphones-width'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '20 cm', 'headphones-height'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '8 cm', 'headphones-depth')
        """,
        """
        DELETE FROM entities WHERE slug IN ('headphones-weight', 'headphones-width', 'headphones-height', 'headphones-depth')
        """
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'headphones-weight'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 250),
            ((SELECT id FROM entities WHERE slug = 'headphones-width'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 18),
            ((SELECT id FROM entities WHERE slug = 'headphones-height'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 20),
            ((SELECT id FROM entities WHERE slug = 'headphones-depth'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 8)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'headphones-weight'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'g'),
            ((SELECT id FROM entities WHERE slug = 'headphones-width'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm'),
            ((SELECT id FROM entities WHERE slug = 'headphones-height'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm'),
            ((SELECT id FROM entities WHERE slug = 'headphones-depth'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm')
        """,
        "SELECT 1"
    ),
    # Create dimensions for headphones
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Headphones Dimensions', 'headphones-dimensions')
        """,
        "DELETE FROM entities WHERE slug = 'headphones-dimensions'"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'headphones-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'width' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'headphones-width')),
            ((SELECT id FROM entities WHERE slug = 'headphones-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'height' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'headphones-height')),
            ((SELECT id FROM entities WHERE slug = 'headphones-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'depth' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'headphones-depth'))
        """,
        "SELECT 1"
    ),
    # Create specification for headphones
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'Headphones Specs', 'headphones-specs')
        """,
        "DELETE FROM entities WHERE slug = 'headphones-specs'"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'headphones-specs'),
             (SELECT id FROM attributes WHERE slug = 'dimensions' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'headphones-dimensions')),
            ((SELECT id FROM entities WHERE slug = 'headphones-specs'),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'white')),
            ((SELECT id FROM entities WHERE slug = 'headphones-specs'),
             (SELECT id FROM attributes WHERE slug = 'weight' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'headphones-weight'))
        """,
        "SELECT 1"
    ),
    # Create the headphones product
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Wireless Headphones', 'wireless-headphones')
        """,
        "DELETE FROM entities WHERE slug = 'wireless-headphones'"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             'Wireless Headphones'),
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'description' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             'Premium wireless headphones with active noise cancellation and 30-hour battery life.')
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'price' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             299.99)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_boolean (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'in_stock' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             true)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'wireless-headphones'),
             (SELECT id FROM attributes WHERE slug = 'specifications' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'headphones-specs'))
        """,
        "SELECT 1"
    ),

    # === Product 3: USB-C Cable ===
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '50 g', 'cable-weight'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '200 cm', 'cable-length')
        """,
        "DELETE FROM entities WHERE slug IN ('cable-weight', 'cable-length')"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'cable-weight'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 50),
            ((SELECT id FROM entities WHERE slug = 'cable-length'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 200)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'cable-weight'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'g'),
            ((SELECT id FROM entities WHERE slug = 'cable-length'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm')
        """,
        "SELECT 1"
    ),
    # Create specification for cable (no dimensions, just weight and color)
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'USB-C Cable Specs', 'usb-c-cable-specs')
        """,
        "DELETE FROM entities WHERE slug = 'usb-c-cable-specs'"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'usb-c-cable-specs'),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'gray')),
            ((SELECT id FROM entities WHERE slug = 'usb-c-cable-specs'),
             (SELECT id FROM attributes WHERE slug = 'weight' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'cable-weight'))
        """,
        "SELECT 1"
    ),
    # Create the cable product
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'product'), 'USB-C Charging Cable', 'usb-c-charging-cable')
        """,
        "DELETE FROM entities WHERE slug = 'usb-c-charging-cable'"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             'USB-C Charging Cable'),
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'description' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             'Durable braided USB-C to USB-C cable, 2 meters long with 100W power delivery support.')
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'price' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             24.99)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_boolean (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'in_stock' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             true)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'usb-c-charging-cable'),
             (SELECT id FROM attributes WHERE slug = 'specifications' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'usb-c-cable-specs'))
        """,
        "SELECT 1"
    ),

    # === Product 4: Mechanical Keyboard ===
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '900 g', 'keyboard-weight'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '44 cm', 'keyboard-width'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '14 cm', 'keyboard-height'),
            ((SELECT id FROM entity_types WHERE name = 'measurement'), '4 cm', 'keyboard-depth')
        """,
        "DELETE FROM entities WHERE slug IN ('keyboard-weight', 'keyboard-width', 'keyboard-height', 'keyboard-depth')"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'keyboard-weight'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 900),
            ((SELECT id FROM entities WHERE slug = 'keyboard-width'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 44),
            ((SELECT id FROM entities WHERE slug = 'keyboard-height'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 14),
            ((SELECT id FROM entities WHERE slug = 'keyboard-depth'),
             (SELECT id FROM attributes WHERE slug = 'value' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 4)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'keyboard-weight'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'g'),
            ((SELECT id FROM entities WHERE slug = 'keyboard-width'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm'),
            ((SELECT id FROM entities WHERE slug = 'keyboard-height'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm'),
            ((SELECT id FROM entities WHERE slug = 'keyboard-depth'),
             (SELECT id FROM attributes WHERE slug = 'unit' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'measurement')), 'cm')
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'dimensions'), 'Keyboard Dimensions', 'keyboard-dimensions')
        """,
        "DELETE FROM entities WHERE slug = 'keyboard-dimensions'"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'keyboard-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'width' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'keyboard-width')),
            ((SELECT id FROM entities WHERE slug = 'keyboard-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'height' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'keyboard-height')),
            ((SELECT id FROM entities WHERE slug = 'keyboard-dimensions'),
             (SELECT id FROM attributes WHERE slug = 'depth' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'dimensions')),
             (SELECT id FROM entities WHERE slug = 'keyboard-depth'))
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'specification'), 'Keyboard Specs', 'keyboard-specs')
        """,
        "DELETE FROM entities WHERE slug = 'keyboard-specs'"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'keyboard-specs'),
             (SELECT id FROM attributes WHERE slug = 'dimensions' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'keyboard-dimensions')),
            ((SELECT id FROM entities WHERE slug = 'keyboard-specs'),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'black')),
            ((SELECT id FROM entities WHERE slug = 'keyboard-specs'),
             (SELECT id FROM attributes WHERE slug = 'weight' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'specification')),
             (SELECT id FROM entities WHERE slug = 'keyboard-weight'))
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Mechanical Keyboard', 'mechanical-keyboard')
        """,
        "DELETE FROM entities WHERE slug = 'mechanical-keyboard'"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             'Mechanical Keyboard'),
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'description' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             'Full-size mechanical keyboard with Cherry MX Blue switches, RGB backlighting, and detachable USB-C cable.')
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'price' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             149.99)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_boolean (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'in_stock' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             false)
        """,
        "SELECT 1"
    ),
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'mechanical-keyboard'),
             (SELECT id FROM attributes WHERE slug = 'specifications' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')),
             (SELECT id FROM entities WHERE slug = 'keyboard-specs'))
        """,
        "SELECT 1"
    ),
]
