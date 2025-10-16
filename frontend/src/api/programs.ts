import http from './http';
import type { PaginatedResponse } from './types';

export interface Programs {
  id: number;
  name: string;
  slug: string;
  program_type: string;
  short_description: string;
  full_description: string;
  image: string;
  icon: string;
  color: string;
  beneficiaries_count: string;
  success_rate: string | null;
  is_accepting_applications: string | null;
  application_deadline: string | null;
}

export async function getPrograms(): Promise<Programs[]> {
  const response = await http.get<PaginatedResponse<Programs>>('programs/');
  return response.data.results;
}
