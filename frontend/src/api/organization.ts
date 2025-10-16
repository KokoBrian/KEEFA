import http from './http';
import type { PaginatedResponse, Organization } from './types';

export async function getOrganization(): Promise<Organization> {
  const response = await http.get<Organization>('organization/');
  return response.data;
}