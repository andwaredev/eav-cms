"""
Convert category column to an enum type
"""

from yoyo import step

__depends__ = {"0011_entity_type_categories"}

steps = [
    # Create the enum type
    step(
        "CREATE TYPE entity_type_category AS ENUM ('content', 'component')",
        "DROP TYPE entity_type_category"
    ),
    # Drop existing default before type conversion
    step(
        "ALTER TABLE entity_types ALTER COLUMN category DROP DEFAULT",
        "ALTER TABLE entity_types ALTER COLUMN category SET DEFAULT 'content'"
    ),
    # Convert the column to use the enum
    step(
        """
        ALTER TABLE entity_types
        ALTER COLUMN category TYPE entity_type_category
        USING category::entity_type_category
        """,
        """
        ALTER TABLE entity_types
        ALTER COLUMN category TYPE VARCHAR(50)
        USING category::text
        """
    ),
    # Set default value with enum type
    step(
        "ALTER TABLE entity_types ALTER COLUMN category SET DEFAULT 'content'",
        "ALTER TABLE entity_types ALTER COLUMN category DROP DEFAULT"
    ),
]
