import http from './http';
import type { PaginatedResponse } from './types';  

export interface ImpactStatistic {
  id: number;
  title: string;
  value: string;
  description: string;
  icon: string;
  color: string;
  order: number;
}

export async function fetchImpactStatistics(): Promise<PaginatedResponse<ImpactStatistic>> {
  const response = await http.get<PaginatedResponse<ImpactStatistic>>('impact-statistics/');
  return response.data;
}
