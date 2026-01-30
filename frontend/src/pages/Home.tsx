import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { EntityTypeCategory, fetchEntityTypes } from '../api';
import type { EntityType } from '../api';

function formatCategory(category: string): string {
  return category.charAt(0).toUpperCase() + category.slice(1);
}

export default function Home() {
  const [entityTypes, setEntityTypes] = useState<EntityType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchEntityTypes()
      .then(setEntityTypes)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  // Group entity types by category
  const grouped = entityTypes.reduce((acc, type) => {
    const cat = type.category;
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(type);
    return acc;
  }, {} as Record<EntityTypeCategory, EntityType[]>);

  // Order categories: content first, then component
  const categoryOrder: EntityTypeCategory[] = [
    EntityTypeCategory.Content,
    EntityTypeCategory.Component,
  ];
  const sortedCategories = categoryOrder.filter((c) => grouped[c]);

  return (
    <div className="page">
      <h2>Entity Types</h2>
      {sortedCategories.map((category) => (
        <section key={category} className="category-section">
          <h3>{formatCategory(category)}</h3>
          <div className="card-grid">
            {grouped[category].map((type) => (
              <Link key={type.id} to={`/types/${type.id}`} className="card">
                <h4>{type.name}</h4>
                {type.description && <p>{type.description}</p>}
              </Link>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
