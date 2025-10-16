import http from './http';
import type { PaginatedResponse } from './types';

export interface Partner {
  // Define properties as you learn them
  [key: string]: any;
}

export async function fetchPartners(): Promise<PaginatedResponse<Partner>> {
  const response = await http.get<PaginatedResponse<Partner>>('partners/');
  return response.data;
}
