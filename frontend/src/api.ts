const API_BASE = 'http://localhost:8000';

export const EntityTypeCategory = {
  Content: 'content',
  Component: 'component',
} as const;

export type EntityTypeCategory = typeof EntityTypeCategory[keyof typeof EntityTypeCategory];

export interface EntityType {
  id: number;
  name: string;
  description: string | null;
  category: EntityTypeCategory;
}

export interface RelatedEntityType {
  id: number;
  name: string;
}

export interface Attribute {
  id: number;
  name: string;
  slug: string;
  type: string;
  is_required: boolean;
  default_value: string | null;
  sort_order: number;
  related_entity_type: RelatedEntityType | null;
}

export interface EntityTypeDetail extends EntityType {
  attributes: Attribute[];
}

export interface Entity {
  id: number;
  name: string;
  slug: string;
  entity_type_id: number;
  entity_type_name: string;
}

export interface EntityDetail extends Entity {
  values: Record<string, unknown>;
}

export async function fetchEntityTypes(): Promise<EntityType[]> {
  const response = await fetch(`${API_BASE}/entity-types`);
  if (!response.ok) throw new Error('Failed to fetch entity types');
  return response.json();
}

export async function fetchEntityType(id: number): Promise<EntityTypeDetail> {
  const response = await fetch(`${API_BASE}/entity-types/${id}`);
  if (!response.ok) throw new Error('Failed to fetch entity type');
  return response.json();
}

export async function fetchEntities(entityTypeId?: number): Promise<Entity[]> {
  const url = entityTypeId 
    ? `${API_BASE}/entities?entity_type_id=${entityTypeId}`
    : `${API_BASE}/entities`;
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to fetch entities');
  return response.json();
}

export async function fetchEntity(id: number): Promise<EntityDetail> {
  const response = await fetch(`${API_BASE}/entities/${id}`);
  if (!response.ok) throw new Error('Failed to fetch entity');
  return response.json();
}

export async function updateEntityValues(
  id: number,
  values: Record<string, unknown>
): Promise<EntityDetail> {
  const response = await fetch(`${API_BASE}/entities/${id}/values`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
  if (!response.ok) throw new Error('Failed to update entity');
  return response.json();
}

export interface CreateEntityRequest {
  entity_type_id: number;
  name: string;
  slug: string;
  values?: Record<string, unknown>;
}

export async function createEntity(
  request: CreateEntityRequest
): Promise<EntityDetail> {
  const response = await fetch(`${API_BASE}/entities`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) throw new Error('Failed to create entity');
  return response.json();
}

export async function deleteEntity(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/entities/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete entity');
}
