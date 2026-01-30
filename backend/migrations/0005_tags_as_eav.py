"""
Convert blog_post tags from JSON to multi-relation (many-to-many via EAV)
Adds support for multi-value relations
"""

from yoyo import step

__depends__ = {"0004_seed_relations"}

steps = [
    # Add 'relation_multi' to the attribute_type enum for many-to-many relations
    step(
        "ALTER TYPE attribute_type ADD VALUE 'relation_multi'",
    ),
]
