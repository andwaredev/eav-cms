import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { createEntity, fetchEntityType, fetchEntities } from '../api';
import type { EntityTypeDetail, Entity } from '../api';
import { useAdminMode } from '../context/AdminModeContext';

export default function EntityTypeView() {
  const { typeId } = useParams<{ typeId: string }>();
  const navigate = useNavigate();
  const { isAdminMode } = useAdminMode();
  const [entityType, setEntityType] = useState<EntityTypeDetail | null>(null);
  const [entities, setEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Create form state
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newName, setNewName] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (!typeId) return;

    Promise.all([
      fetchEntityType(Number(typeId)),
      fetchEntities(Number(typeId)),
    ])
      .then(([type, ents]) => {
        setEntityType(type);
        setEntities(ents);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [typeId]);

  const handleCreate = async () => {
    if (!entityType || !newName.trim()) return;

    setCreating(true);
    try {
      const slug = newName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
      const created = await createEntity({
        entity_type_id: entityType.id,
        name: newName.trim(),
        slug,
        values: { name: newName.trim() },
      });
      
      // Navigate to the new entity
      navigate(`/entities/${created.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create');
      setCreating(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!entityType) return <div className="error">Entity type not found</div>;

  return (
    <div className="page">
      <nav className="breadcrumb">
        <Link to="/">Home</Link> / <span>{entityType.name}</span>
      </nav>

      <header className="page-header">
        <h2>{entityType.name}</h2>
        {entityType.description && <p>{entityType.description}</p>}
      </header>

      <section className="attributes-section">
        <h3>Attributes</h3>
        <table className="attributes-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Slug</th>
              <th>Type</th>
              <th>Required</th>
            </tr>
          </thead>
          <tbody>
            {entityType.attributes.map((attr) => (
              <tr key={attr.id}>
                <td>{attr.name}</td>
                <td><code>{attr.slug}</code></td>
                <td>
                  <span className="type-badge">{attr.type}</span>
                  {attr.related_entity_type && (
                    <Link 
                      to={`/types/${attr.related_entity_type.id}`}
                      className="relation-target"
                    >
                      → {attr.related_entity_type.name}
                    </Link>
                  )}
                </td>
                <td>{attr.is_required ? '✓' : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="entities-section">
        <div className="section-header">
          <h3>Entities ({entities.length})</h3>
          {isAdminMode && !showCreateForm && (
            <button
              className="btn btn-primary"
              onClick={() => setShowCreateForm(true)}
            >
              + New {entityType.name}
            </button>
          )}
        </div>
        
        {isAdminMode && showCreateForm && (
          <div className="create-entity-form">
            <input
              type="text"
              className="edit-input"
              placeholder={`New ${entityType.name} name...`}
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
              autoFocus
            />
            <button
              className="btn btn-primary"
              onClick={handleCreate}
              disabled={creating || !newName.trim()}
            >
              {creating ? 'Creating...' : 'Create'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setShowCreateForm(false);
                setNewName('');
              }}
            >
              Cancel
            </button>
          </div>
        )}

        {entities.length === 0 && !showCreateForm ? (
          <p className="empty">No entities of this type yet.</p>
        ) : (
          <div className="entity-list">
            {entities.map((entity) => (
              <Link
                key={entity.id}
                to={`/entities/${entity.id}`}
                className="entity-card"
              >
                <strong>{entity.name}</strong>
                <code>/{entity.slug}</code>
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
