"""
Create tag entity type and convert blog_post tags to multi-relation
"""

from yoyo import step

__depends__ = {"0005_tags_as_eav"}

steps = [
    # Create values_relation_multi table (no unique constraint - allows multiple values)
    step(
        """
        CREATE TABLE values_relation_multi (
            id SERIAL PRIMARY KEY,
            entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            attribute_id INTEGER NOT NULL REFERENCES attributes(id) ON DELETE CASCADE,
            related_entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
            sort_order INTEGER DEFAULT 0,
            UNIQUE(entity_id, attribute_id, related_entity_id)
        )
        """,
        "DROP TABLE values_relation_multi"
    ),
    step(
        "CREATE INDEX idx_values_relation_multi_entity ON values_relation_multi(entity_id)",
        "DROP INDEX idx_values_relation_multi_entity"
    ),
    # Create a "tag" entity type
    step(
        """
        INSERT INTO entity_types (name, description) VALUES
            ('tag', 'Tags for categorizing content')
        """,
        "DELETE FROM entity_types WHERE name = 'tag'"
    ),
    # Add attributes for tags
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'tag'), 'Name', 'name', 'text', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'tag'), 'Color', 'color', 'text', false, 2)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')"
    ),
    # Update blog_post's tags attribute to be a relation_multi instead of JSON
    step(
        """
        UPDATE attributes
        SET type = 'relation_multi',
            related_entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')
        WHERE slug = 'tags'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')
        """,
        """
        UPDATE attributes
        SET type = 'json', related_entity_type_id = NULL
        WHERE slug = 'tags'
          AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')
        """
    ),
    # Remove old JSON value for blog post tags
    step(
        """
        DELETE FROM values_json
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'welcome-to-our-blog')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'tags'
                              AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post'))
        """,
        """
        INSERT INTO values_json (entity_id, attribute_id, value)
        SELECT
            (SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'),
            (SELECT id FROM attributes WHERE slug = 'tags'
             AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')),
            '["announcement", "welcome"]'
        """
    ),
    # Create tag entities
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'tag'), 'Announcement', 'announcement'),
            ((SELECT id FROM entity_types WHERE name = 'tag'), 'Welcome', 'welcome')
        """,
        "DELETE FROM entities WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')"
    ),
    # Add values to tag entities
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'announcement' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             'Announcement'),
            ((SELECT id FROM entities WHERE slug = 'announcement' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             '#3b82f6'),
            ((SELECT id FROM entities WHERE slug = 'welcome' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             'Welcome'),
            ((SELECT id FROM entities WHERE slug = 'welcome' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             (SELECT id FROM attributes WHERE slug = 'color' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             '#10b981')
        """,
        """
        DELETE FROM values_text WHERE entity_id IN (
            SELECT id FROM entities WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')
        )
        """
    ),
    # Create relations from blog post to both tags
    step(
        """
        INSERT INTO values_relation_multi (entity_id, attribute_id, related_entity_id, sort_order) VALUES
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'),
             (SELECT id FROM attributes WHERE slug = 'tags' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')),
             (SELECT id FROM entities WHERE slug = 'announcement' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             1),
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'),
             (SELECT id FROM attributes WHERE slug = 'tags' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')),
             (SELECT id FROM entities WHERE slug = 'welcome' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'tag')),
             2)
        """,
        """
        DELETE FROM values_relation_multi
        WHERE entity_id = (SELECT id FROM entities WHERE slug = 'welcome-to-our-blog')
          AND attribute_id = (SELECT id FROM attributes WHERE slug = 'tags' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post'))
        """
    ),
]
