// lib/apiClient/programs.ts
import api from '../api';

export interface Program {
  id: string;
  name: string;
  description?: string;
  // Add more fields as needed
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Fetch paginated list of programs
export const fetchPrograms = async (
  page: number = 1
): Promise<PaginatedResponse<Program>> => {
  const res = await api.get<PaginatedResponse<Program>>('/api/v1/programs/', {
    params: { page },
  });
  return res.data;
};
