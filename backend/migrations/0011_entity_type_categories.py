"""
Add category field to entity_types for grouping in UI
"""

from yoyo import step

__depends__ = {"0010_tag_color_relation"}

steps = [
    # Add category column
    step(
        "ALTER TABLE entity_types ADD COLUMN category VARCHAR(50) DEFAULT 'content'",
        "ALTER TABLE entity_types DROP COLUMN category"
    ),
    # Set content types (top-level)
    step(
        """
        UPDATE entity_types 
        SET category = 'content' 
        WHERE name IN ('blog_post', 'page', 'product')
        """,
        "SELECT 1"
    ),
    # Set component types (internal/reusable)
    step(
        """
        UPDATE entity_types 
        SET category = 'component' 
        WHERE name IN ('specification', 'tag', 'color', 'dimensions', 'measurement')
        """,
        "SELECT 1"
    ),
]
