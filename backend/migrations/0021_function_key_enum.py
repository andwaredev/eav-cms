"""
Add function_key enum type and register it as an attribute type
"""

from yoyo import step

__depends__ = {"0020_text_component"}

steps = [
    step(
        "CREATE TYPE function_key AS ENUM ('TO_DOLLARS', 'JOIN', 'FORMAT', 'UUID')",
        "DROP TYPE function_key"
    ),
    step(
        "ALTER TYPE attribute_type ADD VALUE IF NOT EXISTS 'function_key'",
        ""  # Cannot remove enum values in PostgreSQL
    ),
]
