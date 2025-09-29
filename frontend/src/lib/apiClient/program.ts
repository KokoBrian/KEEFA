import api from '../api'

//Paginated Response Type
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}


//program API call
export interface Program{
  id: number;
  name: string;
}

//GET /program/
export async function getPrograms(): Promise<PaginatedResponse<Program>> {
  const res = await api.get<PaginatedResponse<Program>>('programs/');
  return res.data;
}