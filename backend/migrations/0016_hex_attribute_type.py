"""
Add hex to attribute_type enum
"""

from yoyo import step

__depends__ = {"0015_related_products"}

steps = [
    # Add 'hex' to the attribute_type enum
    step(
        "ALTER TYPE attribute_type ADD VALUE IF NOT EXISTS 'hex'",
        ""  # Cannot remove enum values in PostgreSQL
    ),
]
