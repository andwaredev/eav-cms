"""
Seed initial data for CMS
"""

from yoyo import step

__depends__ = {"0001_create_eav_tables"}

steps = [
    # Create entity types
    step(
        """
        INSERT INTO entity_types (name, description) VALUES
            ('page', 'Static pages like About, Contact, etc.'),
            ('blog_post', 'Blog articles and news'),
            ('product', 'E-commerce products')
        """,
        "DELETE FROM entity_types WHERE name IN ('page', 'blog_post', 'product')"
    ),
    # Create attributes for pages
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'page'), 'Title', 'title', 'text', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'page'), 'Content', 'content', 'textarea', true, 2),
            ((SELECT id FROM entity_types WHERE name = 'page'), 'Meta Description', 'meta_description', 'text', false, 3),
            ((SELECT id FROM entity_types WHERE name = 'page'), 'Published', 'published', 'boolean', false, 4)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'page')"
    ),
    # Create attributes for blog posts
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Title', 'title', 'text', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Excerpt', 'excerpt', 'textarea', false, 2),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Content', 'content', 'textarea', true, 3),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Author', 'author', 'text', false, 4),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Published Date', 'published_date', 'datetime', false, 5),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Tags', 'tags', 'json', false, 6),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Featured', 'featured', 'boolean', false, 7)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')"
    ),
    # Create attributes for products
    step(
        """
        INSERT INTO attributes (entity_type_id, name, slug, type, is_required, sort_order) VALUES
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Name', 'name', 'text', true, 1),
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Description', 'description', 'textarea', false, 2),
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Price', 'price', 'number', true, 3),
            ((SELECT id FROM entity_types WHERE name = 'product'), 'SKU', 'sku', 'text', false, 4),
            ((SELECT id FROM entity_types WHERE name = 'product'), 'In Stock', 'in_stock', 'boolean', false, 5),
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Specifications', 'specifications', 'json', false, 6)
        """,
        "DELETE FROM attributes WHERE entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')"
    ),
    # Create sample entities
    step(
        """
        INSERT INTO entities (entity_type_id, name, slug) VALUES
            ((SELECT id FROM entity_types WHERE name = 'page'), 'About Us', 'about-us'),
            ((SELECT id FROM entity_types WHERE name = 'page'), 'Contact', 'contact'),
            ((SELECT id FROM entity_types WHERE name = 'blog_post'), 'Welcome to Our Blog', 'welcome-to-our-blog'),
            ((SELECT id FROM entity_types WHERE name = 'product'), 'Sample Product', 'sample-product')
        """,
        "DELETE FROM entities"
    ),
    # Seed values for About Us page
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'about-us'), (SELECT id FROM attributes WHERE slug = 'title' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'page')), 'About Us'),
            ((SELECT id FROM entities WHERE slug = 'about-us'), (SELECT id FROM attributes WHERE slug = 'content' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'page')), 'Welcome to our company. We are dedicated to providing the best service possible.'),
            ((SELECT id FROM entities WHERE slug = 'about-us'), (SELECT id FROM attributes WHERE slug = 'meta_description' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'page')), 'Learn more about our company and mission.')
        """,
        "DELETE FROM values_text WHERE entity_id = (SELECT id FROM entities WHERE slug = 'about-us')"
    ),
    step(
        """
        INSERT INTO values_boolean (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'about-us'), (SELECT id FROM attributes WHERE slug = 'published' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'page')), true)
        """,
        "DELETE FROM values_boolean WHERE entity_id = (SELECT id FROM entities WHERE slug = 'about-us')"
    ),
    # Seed values for blog post
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'), (SELECT id FROM attributes WHERE slug = 'title' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')), 'Welcome to Our Blog'),
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'), (SELECT id FROM attributes WHERE slug = 'excerpt' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')), 'This is our first blog post. Exciting things are coming!'),
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'), (SELECT id FROM attributes WHERE slug = 'content' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')), 'We are thrilled to launch our new blog. Stay tuned for updates, tutorials, and news.'),
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'), (SELECT id FROM attributes WHERE slug = 'author' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')), 'Admin')
        """,
        "DELETE FROM values_text WHERE entity_id = (SELECT id FROM entities WHERE slug = 'welcome-to-our-blog')"
    ),
    step(
        """
        INSERT INTO values_json (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'), (SELECT id FROM attributes WHERE slug = 'tags' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')), '["announcement", "welcome"]')
        """,
        "DELETE FROM values_json WHERE entity_id = (SELECT id FROM entities WHERE slug = 'welcome-to-our-blog')"
    ),
    step(
        """
        INSERT INTO values_boolean (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'welcome-to-our-blog'), (SELECT id FROM attributes WHERE slug = 'featured' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'blog_post')), true)
        """,
        "DELETE FROM values_boolean WHERE entity_id = (SELECT id FROM entities WHERE slug = 'welcome-to-our-blog')"
    ),
    # Seed values for sample product
    step(
        """
        INSERT INTO values_text (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product'), (SELECT id FROM attributes WHERE slug = 'name' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')), 'Sample Product'),
            ((SELECT id FROM entities WHERE slug = 'sample-product'), (SELECT id FROM attributes WHERE slug = 'description' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')), 'This is a sample product to demonstrate the EAV system.'),
            ((SELECT id FROM entities WHERE slug = 'sample-product'), (SELECT id FROM attributes WHERE slug = 'sku' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')), 'SKU-001')
        """,
        "DELETE FROM values_text WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')"
    ),
    step(
        """
        INSERT INTO values_number (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product'), (SELECT id FROM attributes WHERE slug = 'price' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')), 29.99)
        """,
        "DELETE FROM values_number WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')"
    ),
    step(
        """
        INSERT INTO values_boolean (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product'), (SELECT id FROM attributes WHERE slug = 'in_stock' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')), true)
        """,
        "DELETE FROM values_boolean WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')"
    ),
    step(
        """
        INSERT INTO values_json (entity_id, attribute_id, value) VALUES
            ((SELECT id FROM entities WHERE slug = 'sample-product'), (SELECT id FROM attributes WHERE slug = 'specifications' AND entity_type_id = (SELECT id FROM entity_types WHERE name = 'product')), '{"weight": "1.5kg", "dimensions": "10x10x5cm", "color": "black"}')
        """,
        "DELETE FROM values_json WHERE entity_id = (SELECT id FROM entities WHERE slug = 'sample-product')"
    ),
]
