import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { createEntity, deleteEntity, fetchEntities, fetchEntity, fetchEntityType, updateEntityValues } from '../api';
import type { Attribute, Entity, EntityDetail, EntityTypeDetail } from '../api';
import { useAdminMode } from '../context/AdminModeContext';

interface RelatedEntity {
  id: number;
  name: string;
  slug: string;
  entity_type_id: number;
  entity_type_name: string;
  values: Record<string, unknown>;
}

function isRelatedEntity(value: unknown): value is RelatedEntity {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    'values' in value &&
    'entity_type_name' in value
  );
}

function isRelatedEntityArray(value: unknown): value is RelatedEntity[] {
  return Array.isArray(value) && value.length > 0 && isRelatedEntity(value[0]);
}

// Check if a value looks like a hex color
function isHexColor(value: unknown): value is string {
  return typeof value === 'string' && /^#[0-9A-Fa-f]{6}$/.test(value);
}

// Get hex color from a color entity if it has one
function getColorHex(entity: RelatedEntity): string | null {
  if (entity.entity_type_name === 'color' && entity.values.hex) {
    return String(entity.values.hex);
  }
  // Check if this entity has a nested color relation
  if (entity.values.color && isRelatedEntity(entity.values.color)) {
    return getColorHex(entity.values.color);
  }
  return null;
}

// Color swatch component
function ColorSwatch({ hex, size = 'normal' }: { hex: string; size?: 'small' | 'normal' }) {
  const sizeClass = size === 'small' ? 'color-swatch-small' : 'color-swatch';
  return (
    <span
      className={sizeClass}
      style={{ backgroundColor: hex }}
      title={hex}
    />
  );
}

// Editor for multi-relations (e.g., tags)
function MultiRelationEditor({
  value,
  onChange,
}: {
  value: RelatedEntity[];
  onChange: (newValue: RelatedEntity[]) => void;
}) {
  const [availableEntities, setAvailableEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newName, setNewName] = useState('');
  const [creating, setCreating] = useState(false);

  // Get the entity type ID and name from the first related entity
  const entityTypeId = value.length > 0 ? value[0].entity_type_id : null;
  const entityTypeName = value.length > 0 ? value[0].entity_type_name : null;

  const loadEntities = () => {
    if (!entityTypeId) {
      setLoading(false);
      return;
    }
    fetchEntities(entityTypeId)
      .then(setAvailableEntities)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadEntities();
  }, [entityTypeId]);

  const handleRemove = (idToRemove: number) => {
    onChange(value.filter((e) => e.id !== idToRemove));
  };

  const handleAdd = (entityId: number) => {
    const entityToAdd = availableEntities.find((e) => e.id === entityId);
    if (entityToAdd && !value.some((e) => e.id === entityId)) {
      // Create a minimal RelatedEntity from the Entity
      const newRelated: RelatedEntity = {
        id: entityToAdd.id,
        name: entityToAdd.name,
        slug: entityToAdd.slug,
        entity_type_id: entityToAdd.entity_type_id,
        entity_type_name: entityToAdd.entity_type_name,
        values: { name: entityToAdd.name },
      };
      onChange([...value, newRelated]);
    }
  };

  const handleCreate = async () => {
    if (!entityTypeId || !newName.trim()) return;

    setCreating(true);
    try {
      // Generate a slug from the name
      const slug = newName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');

      const created = await createEntity({
        entity_type_id: entityTypeId,
        name: newName.trim(),
        slug,
        values: { name: newName.trim() },
      });

      // Add the new entity to the selection
      const newRelated: RelatedEntity = {
        id: created.id,
        name: created.name,
        slug: created.slug,
        entity_type_id: created.entity_type_id,
        entity_type_name: created.entity_type_name,
        values: created.values,
      };
      onChange([...value, newRelated]);

      // Reset form and refresh available entities
      setNewName('');
      setShowCreateForm(false);
      loadEntities();
    } catch (err) {
      console.error('Failed to create entity:', err);
    } finally {
      setCreating(false);
    }
  };

  // Filter out already-selected entities
  const unselectedEntities = availableEntities.filter(
    (e) => !value.some((v) => v.id === e.id)
  );

  return (
    <div className="multi-relation-editor">
      <div className="selected-tags">
        {value.map((entity) => {
          const colorHex = getColorHex(entity);
          return (
            <span
              key={entity.id}
              className="editable-tag"
              style={colorHex ? { backgroundColor: colorHex } : undefined}
            >
              {entity.values.name ? String(entity.values.name) : entity.name}
              <button
                type="button"
                className="tag-remove"
                onClick={() => handleRemove(entity.id)}
                title="Remove"
              >
                ×
              </button>
            </span>
          );
        })}
      </div>
      <div className="relation-actions">
        {!loading && unselectedEntities.length > 0 && (
          <select
            className="edit-select"
            value=""
            onChange={(e) => handleAdd(Number(e.target.value))}
          >
            <option value="" disabled>
              + Add existing...
            </option>
            {unselectedEntities.map((entity) => (
              <option key={entity.id} value={entity.id}>
                {entity.name}
              </option>
            ))}
          </select>
        )}
        {entityTypeId && !showCreateForm && (
          <button
            type="button"
            className="btn btn-secondary btn-small"
            onClick={() => setShowCreateForm(true)}
          >
            + New {entityTypeName}
          </button>
        )}
      </div>
      {showCreateForm && (
        <div className="create-form">
          <input
            type="text"
            className="edit-input"
            placeholder={`New ${entityTypeName} name...`}
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
            autoFocus
          />
          <button
            type="button"
            className="btn btn-primary btn-small"
            onClick={handleCreate}
            disabled={creating || !newName.trim()}
          >
            {creating ? 'Creating...' : 'Create'}
          </button>
          <button
            type="button"
            className="btn btn-secondary btn-small"
            onClick={() => {
              setShowCreateForm(false);
              setNewName('');
            }}
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}

// Editor for single relations (e.g., color, weight)
function SingleRelationEditor({
  value,
  onChange,
}: {
  value: RelatedEntity;
  onChange: (newValue: RelatedEntity) => void;
}) {
  const [availableEntities, setAvailableEntities] = useState<EntityDetail[]>([]);
  const [loading, setLoading] = useState(true);

  const entityTypeId = value.entity_type_id;
  const entityTypeName = value.entity_type_name;

  useEffect(() => {
    // Fetch entities with their values
    fetchEntities(entityTypeId)
      .then(async (entities) => {
        // For color entities, we need the full details with hex values
        if (entityTypeName === 'color') {
          const detailed = await Promise.all(
            entities.map((e) => fetchEntity(e.id))
          );
          setAvailableEntities(detailed);
        } else {
          // For non-color entities, basic info is enough
          setAvailableEntities(entities.map(e => ({ ...e, values: {} })) as EntityDetail[]);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [entityTypeId, entityTypeName]);

  const handleChange = (entityId: number) => {
    const selected = availableEntities.find((e) => e.id === entityId);
    if (selected) {
      // Create a RelatedEntity from the EntityDetail
      const newRelated: RelatedEntity = {
        id: selected.id,
        name: selected.name,
        slug: selected.slug,
        entity_type_id: selected.entity_type_id,
        entity_type_name: selected.entity_type_name,
        values: selected.values,
      };
      onChange(newRelated);
    }
  };

  // Special display for color entities - show color swatch
  const isColorType = entityTypeName === 'color';

  if (loading) {
    return <span>Loading...</span>;
  }

  // Color selector UI for color types (dropdown with swatch preview)
  if (isColorType) {
    const currentHex = value.values.hex ? String(value.values.hex) : '#888888';
    return (
      <div className="single-relation-editor color-editor">
        <ColorSwatch hex={currentHex} />
        <select
          className="edit-select"
          value={value.id}
          onChange={(e) => handleChange(Number(e.target.value))}
        >
          {availableEntities.map((entity) => {
            const hex = entity.values?.hex ? String(entity.values.hex) : null;
            return (
              <option key={entity.id} value={entity.id}>
                {entity.name} {hex ? `(${hex})` : ''}
              </option>
            );
          })}
        </select>
      </div>
    );
  }

  return (
    <div className="single-relation-editor">
      <select
        className="edit-select"
        value={value.id}
        onChange={(e) => handleChange(Number(e.target.value))}
      >
        {availableEntities.map((entity) => (
          <option key={entity.id} value={entity.id}>
            {entity.name}
          </option>
        ))}
      </select>
    </div>
  );
}

// Editor for empty relations - when no value exists yet
function EmptyRelationEditor({
  relatedEntityTypeId,
  relatedEntityTypeName,
  isMulti,
  onChange,
}: {
  relatedEntityTypeId: number;
  relatedEntityTypeName: string;
  isMulti: boolean;
  onChange: (newValue: unknown) => void;
}) {
  const [availableEntities, setAvailableEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newName, setNewName] = useState('');
  const [creating, setCreating] = useState(false);
  const [selectedEntities, setSelectedEntities] = useState<RelatedEntity[]>([]);

  useEffect(() => {
    fetchEntities(relatedEntityTypeId)
      .then(setAvailableEntities)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [relatedEntityTypeId]);

  const handleAdd = (entityId: number) => {
    const entityToAdd = availableEntities.find((e) => e.id === entityId);
    if (entityToAdd) {
      const newRelated: RelatedEntity = {
        id: entityToAdd.id,
        name: entityToAdd.name,
        slug: entityToAdd.slug,
        entity_type_id: entityToAdd.entity_type_id,
        entity_type_name: entityToAdd.entity_type_name,
        values: { name: entityToAdd.name },
      };
      
      if (isMulti) {
        const updated = [...selectedEntities, newRelated];
        setSelectedEntities(updated);
        onChange(updated);
      } else {
        onChange(newRelated);
      }
    }
  };

  const handleRemove = (idToRemove: number) => {
    const updated = selectedEntities.filter((e) => e.id !== idToRemove);
    setSelectedEntities(updated);
    onChange(updated.length > 0 ? updated : null);
  };

  const handleCreate = async () => {
    if (!newName.trim()) return;

    setCreating(true);
    try {
      const slug = newName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
      const created = await createEntity({
        entity_type_id: relatedEntityTypeId,
        name: newName.trim(),
        slug,
        values: { name: newName.trim() },
      });

      const newRelated: RelatedEntity = {
        id: created.id,
        name: created.name,
        slug: created.slug,
        entity_type_id: created.entity_type_id,
        entity_type_name: created.entity_type_name,
        values: created.values,
      };

      if (isMulti) {
        const updated = [...selectedEntities, newRelated];
        setSelectedEntities(updated);
        onChange(updated);
      } else {
        onChange(newRelated);
      }

      setNewName('');
      setShowCreateForm(false);
      // Refresh available entities
      const entities = await fetchEntities(relatedEntityTypeId);
      setAvailableEntities(entities);
    } catch (err) {
      console.error('Failed to create:', err);
    } finally {
      setCreating(false);
    }
  };

  const unselectedEntities = availableEntities.filter(
    (e) => !selectedEntities.some((s) => s.id === e.id)
  );

  if (loading) {
    return <span className="empty-value">Loading...</span>;
  }

  // Special UI for color type (single relation) - just dropdown, no color picker
  const isColorType = relatedEntityTypeName === 'color';
  if (isColorType && !isMulti) {
    return (
      <div className="single-relation-editor color-editor">
        <select
          className="edit-select"
          value=""
          onChange={(e) => handleAdd(Number(e.target.value))}
        >
          <option value="" disabled>
            Select color...
          </option>
          {availableEntities.map((entity) => {
            const hex = entity.values?.hex ? String(entity.values.hex) : null;
            return (
              <option key={entity.id} value={entity.id}>
                {entity.name} {hex ? `(${hex})` : ''}
              </option>
            );
          })}
        </select>
      </div>
    );
  }

  return (
    <div className="multi-relation-editor">
      {isMulti && selectedEntities.length > 0 && (
        <div className="selected-tags">
          {selectedEntities.map((entity) => (
            <span key={entity.id} className="editable-tag">
              {entity.values.name ? String(entity.values.name) : entity.name}
              <button
                type="button"
                className="tag-remove"
                onClick={() => handleRemove(entity.id)}
                title="Remove"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}
      <div className="relation-actions">
        {unselectedEntities.length > 0 && (
          <select
            className="edit-select"
            value=""
            onChange={(e) => handleAdd(Number(e.target.value))}
          >
            <option value="" disabled>
              {isMulti ? '+ Add' : 'Select'} {relatedEntityTypeName}...
            </option>
            {unselectedEntities.map((entity) => (
              <option key={entity.id} value={entity.id}>
                {entity.name}
              </option>
            ))}
          </select>
        )}
        {!showCreateForm && (
          <button
            type="button"
            className="btn btn-secondary btn-small"
            onClick={() => setShowCreateForm(true)}
          >
            + New {relatedEntityTypeName}
          </button>
        )}
      </div>
      {showCreateForm && (
        <div className="create-form">
          <input
            type="text"
            className="edit-input"
            placeholder={`New ${relatedEntityTypeName} name...`}
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
            autoFocus
          />
          <button
            type="button"
            className="btn btn-primary btn-small"
            onClick={handleCreate}
            disabled={creating || !newName.trim()}
          >
            {creating ? 'Creating...' : 'Create'}
          </button>
          <button
            type="button"
            className="btn btn-secondary btn-small"
            onClick={() => {
              setShowCreateForm(false);
              setNewName('');
            }}
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}

// Editor that knows the attribute type - handles both empty and existing values
function AttributeEditor({
  attribute,
  value,
  onChange,
}: {
  attribute: Attribute | null;
  value: unknown;
  onChange: (newValue: unknown) => void;
}) {
  const hasValue = value !== undefined && value !== null;

  // No attribute info available
  if (!attribute) {
    if (hasValue) {
      return <ValueEditor value={value} onChange={onChange} />;
    }
    return <span className="empty-value">—</span>;
  }

  // For complex types (objects/arrays like relations), delegate to ValueEditor
  if (hasValue && typeof value === 'object') {
    return <ValueEditor value={value} onChange={onChange} />;
  }

  // Handle each type with consistent inputs (no component switching)
  switch (attribute.type) {
    case 'text':
    case 'textarea':
      return (
        <input
          type="text"
          className="edit-input"
          placeholder={`Enter ${attribute.name.toLowerCase()}...`}
          value={hasValue ? String(value) : ''}
          onChange={(e) => onChange(e.target.value)}
        />
      );
    case 'number':
      return (
        <input
          type="number"
          className="edit-input"
          placeholder="0"
          value={hasValue ? Number(value) : ''}
          onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
        />
      );
    case 'boolean':
      return (
        <label className="edit-checkbox">
          <input
            type="checkbox"
            checked={hasValue ? Boolean(value) : false}
            onChange={(e) => onChange(e.target.checked)}
          />
          {(hasValue ? Boolean(value) : false) ? 'Yes' : 'No'}
        </label>
      );
    case 'hex':
      return (
        <div className="edit-color">
          <input
            type="color"
            value={hasValue ? String(value) : '#000000'}
            onChange={(e) => onChange(e.target.value)}
          />
          <input
            type="text"
            className="edit-input edit-input-short"
            value={hasValue ? String(value) : ''}
            placeholder="#000000"
            onChange={(e) => onChange(e.target.value)}
            pattern="#[0-9A-Fa-f]{6}"
          />
        </div>
      );
    case 'datetime':
      return (
        <input
          type="datetime-local"
          className="edit-input"
          value={hasValue ? String(value).slice(0, 16) : ''}
          onChange={(e) => onChange(e.target.value ? new Date(e.target.value).toISOString() : null)}
        />
      );
    case 'relation':
      // Single relation - show dropdown to select
      if (attribute.related_entity_type) {
        return (
          <EmptyRelationEditor
            relatedEntityTypeId={attribute.related_entity_type.id}
            relatedEntityTypeName={attribute.related_entity_type.name}
            isMulti={false}
            onChange={onChange}
          />
        );
      }
      return <span className="empty-value">No relation type configured</span>;
    case 'relation_multi':
      // Multi relation - show dropdown to add
      if (attribute.related_entity_type) {
        return (
          <EmptyRelationEditor
            relatedEntityTypeId={attribute.related_entity_type.id}
            relatedEntityTypeName={attribute.related_entity_type.name}
            isMulti={true}
            onChange={onChange}
          />
        );
      }
      return <span className="empty-value">No relation type configured</span>;
    default:
      return (
        <input
          type="text"
          className="edit-input"
          placeholder={`Enter value...`}
          value={hasValue ? String(value) : ''}
          onChange={(e) => onChange(e.target.value)}
        />
      );
  }
}

// Editor for simple values (text, number, boolean)
function ValueEditor({
  value,
  onChange,
}: {
  value: unknown;
  onChange: (newValue: unknown) => void;
}) {
  // Boolean - checkbox
  if (typeof value === 'boolean') {
    return (
      <label className="edit-checkbox">
        <input
          type="checkbox"
          checked={value}
          onChange={(e) => onChange(e.target.checked)}
        />
        {value ? 'Yes' : 'No'}
      </label>
    );
  }

  // Number
  if (typeof value === 'number') {
    return (
      <input
        type="number"
        className="edit-input"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    );
  }

  // Hex color - special input
  if (isHexColor(value)) {
    return (
      <div className="edit-color">
        <input
          type="color"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
        <input
          type="text"
          className="edit-input edit-input-short"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          pattern="#[0-9A-Fa-f]{6}"
        />
      </div>
    );
  }

  // Multi-relation (array of related entities)
  if (isRelatedEntityArray(value)) {
    return <MultiRelationEditor value={value} onChange={onChange} />;
  }

  // Single relation (e.g., color, weight)
  if (isRelatedEntity(value)) {
    return <SingleRelationEditor value={value} onChange={onChange} />;
  }

  // Default: text input
  return (
    <input
      type="text"
      className="edit-input"
      value={String(value ?? '')}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

function ValueDisplay({ value }: { value: unknown }) {
  if (typeof value === 'boolean') {
    return (
      <span className={value ? 'bool-true' : 'bool-false'}>
        {value ? '✓ Yes' : '✗ No'}
      </span>
    );
  }

  // Hex color string - show swatch with code
  if (isHexColor(value)) {
    return (
      <span className="color-value">
        <ColorSwatch hex={value} />
        <code>{value}</code>
      </span>
    );
  }

  // Multi-relation (array of related entities)
  if (isRelatedEntityArray(value)) {
    return (
      <div className="related-entity-list">
        {value.map((entity) => {
          const colorHex = getColorHex(entity);
          return (
            <Link
              key={entity.id}
              to={`/entities/${entity.id}`}
              className="related-tag"
              style={colorHex ? { backgroundColor: colorHex } : undefined}
            >
              {entity.values.name ? String(entity.values.name) : entity.name}
            </Link>
          );
        })}
      </div>
    );
  }

  // Single relation - check if it's a color entity
  if (isRelatedEntity(value)) {
    // Special display for color entities
    if (value.entity_type_name === 'color' && value.values.hex) {
      const hex = String(value.values.hex);
      return (
        <span className="color-value">
          <ColorSwatch hex={hex} />
          <Link to={`/entities/${value.id}`} className="color-link">
            {value.values.name ? String(value.values.name) : value.name}
          </Link>
          <code>{hex}</code>
        </span>
      );
    }

    return (
      <div className="related-entity">
        <div className="related-header">
          <Link to={`/entities/${value.id}`} className="related-link">
            {value.name}
          </Link>
          <span className="type-badge">{value.entity_type_name}</span>
        </div>
        <table className="nested-values-table">
          <tbody>
            {Object.entries(value.values).map(([key, val]) => (
              <tr key={key}>
                <td>{key}</td>
                <td><ValueDisplay value={val} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (typeof value === 'object' && value !== null) {
    return <pre>{JSON.stringify(value, null, 2)}</pre>;
  }

  return <>{String(value)}</>;
}

export default function EntityView() {
  const { entityId } = useParams<{ entityId: string }>();
  const { isAdminMode } = useAdminMode();
  const navigate = useNavigate();
  const [entity, setEntity] = useState<EntityDetail | null>(null);
  const [entityType, setEntityType] = useState<EntityTypeDetail | null>(null);
  const [editedValues, setEditedValues] = useState<Record<string, unknown>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!entityId) return;

    setLoading(true);
    fetchEntity(Number(entityId))
      .then(async (data) => {
        setEntity(data);
        setEditedValues({});
        // Fetch entity type to get all attributes
        const type = await fetchEntityType(data.entity_type_id);
        setEntityType(type);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [entityId]);

  const handleValueChange = (key: string, newValue: unknown) => {
    setEditedValues((prev) => ({ ...prev, [key]: newValue }));
  };

  const handleSave = async () => {
    if (!entity || Object.keys(editedValues).length === 0) return;

    setSaving(true);
    try {
      const updated = await updateEntityValues(entity.id, editedValues);
      setEntity(updated);
      setEditedValues({});
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditedValues({});
  };

  const handleDelete = async () => {
    if (!entity) return;
    
    const confirmed = window.confirm(
      `Are you sure you want to delete "${entity.name}"? This action cannot be undone.`
    );
    if (!confirmed) return;

    setDeleting(true);
    try {
      await deleteEntity(entity.id);
      // Navigate back to the entity type list
      navigate(`/types/${entity.entity_type_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete');
      setDeleting(false);
    }
  };

  const hasChanges = Object.keys(editedValues).length > 0;

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!entity) return <div className="error">Entity not found</div>;

  // Merge original values with edited values for display
  const displayValues = { ...entity.values, ...editedValues };

  // Get all attribute slugs - in admin mode, show all attributes even if no value
  const getAttributeRows = () => {
    if (isAdminMode && entityType) {
      // Show all attributes from the entity type
      return entityType.attributes.map((attr) => ({
        slug: attr.slug,
        name: attr.name,
        type: attr.type,
        value: displayValues[attr.slug],
        hasValue: attr.slug in displayValues,
        attribute: attr,
      }));
    } else {
      // Show only attributes with values
      return Object.entries(displayValues).map(([slug, value]) => ({
        slug,
        name: slug,
        type: null,
        value,
        hasValue: true,
        attribute: null,
      }));
    }
  };

  const attributeRows = getAttributeRows();

  return (
    <div className="page">
      <nav className="breadcrumb">
        <Link to="/">Home</Link> /{' '}
        <Link to={`/types/${entity.entity_type_id}`}>{entity.entity_type_name}</Link> /{' '}
        <span>{entity.name}</span>
      </nav>

      <header className="page-header">
        <div className="page-header-content">
          <div>
            <h2>{entity.name}</h2>
            <p className="meta">
              <span className="type-badge">{entity.entity_type_name}</span>
              <code>/{entity.slug}</code>
            </p>
          </div>
          {isAdminMode && (
            <button
              className="btn btn-danger"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? 'Deleting...' : 'Delete'}
            </button>
          )}
        </div>
      </header>

      <section className="values-section">
        <div className="section-header">
          <h3>Values</h3>
          {isAdminMode && hasChanges && (
            <div className="edit-actions">
              <button className="btn btn-secondary" onClick={handleCancel} disabled={saving}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          )}
        </div>
        <table className="values-table">
          <thead>
            <tr>
              <th>Attribute</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {attributeRows.map((row) => {
              const isEdited = row.slug in editedValues;
              return (
                <tr key={row.slug} className={isEdited ? 'row-edited' : ''}>
                  <td>
                    <strong>{row.name}</strong>
                    {row.type && <span className="attr-type-hint">{row.type}</span>}
                  </td>
                  <td>
                    {isAdminMode ? (
                      <AttributeEditor
                        attribute={row.attribute}
                        value={row.value}
                        onChange={(newValue) => handleValueChange(row.slug, newValue)}
                      />
                    ) : (
                      row.hasValue ? <ValueDisplay value={row.value} /> : <span className="empty-value">—</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>
    </div>
  );
}
