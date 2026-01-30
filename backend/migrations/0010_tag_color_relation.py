"""
Update tag's color attribute to reference Color EAV
"""

from yoyo import step

__depends__ = {"0009_color_eav"}

steps = [
    # Create the specific colors used by tags (if they don't match existing ones)
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Sky Blue', 'sky-blue'),
            ((SELECT id FROM entity_types WHERE name = 'color'), 'Emerald', 'emerald')
        """,
        "DELETE FROM entities WHERE slug IN ('sky-blue', 'emerald') AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')"
    ),
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sky-blue' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             'Sky Blue'),
            ((SELECT id FROM entities WHERE slug = 'sky-blue' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#3B82F6'),
            ((SELECT id FROM entities WHERE slug = 'emerald' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             'Emerald'),
            ((SELECT id FROM entities WHERE slug = 'emerald' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             (SELECT id FROM attributes WHERE slug = 'hex' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')),
             '#10B981')
        """,
        "DELETE FROM values_text WHERE entity_id IN (SELECT id FROM entities WHERE slug IN ('sky-blue', 'emerald') AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color'))"
    ),
    # Update tag's color attribute to be a relation to color entity type
    step(
        """
        UPDATE attributes
        SET type = 'relation',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')
        WHERE slug = 'color'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')
        """,
        """
        UPDATE attributes
        SET type = 'text', related_entity_type_id = NULL
        WHERE slug = 'color'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')
        """
    ),
    # Remove old text values for tag colors
    step(
        """
        DELETE FROM values_text
        WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'color'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag'))
        """,
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'announcement' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             '#3b82f6'),
            ((SELECT id FROM entities WHERE slug = 'welcome' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             '#10b981')
        """
    ),
    # Create relations from tags to color entities
    step(
        """
        INSERT INTO values_relation (entity_id, attribute_id, related_entity_id) VALUES
            ((SELECT id FROM entities WHERE slug = 'announcement' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM entities WHERE slug = 'sky-blue' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color'))),
            ((SELECT id FROM entities WHERE slug = 'welcome' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM entities WHERE slug = 'emerald' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'color')))
        """,
        """
        DELETE FROM values_relation
        WHERE attribute_id = (SELECT id FROM attributes WHERE slug = 'color'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag'))
        """
    ),
]
