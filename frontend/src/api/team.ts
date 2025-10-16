// api/team.ts
import http from './http';
import type { PaginatedResponse } from './types';  // <--- Use import type here

export interface TeamMember {
  [key: string]: any;
}

export async function fetchTeamMembers(): Promise<PaginatedResponse<TeamMember>> {
  const response = await http.get<PaginatedResponse<TeamMember>>('team-members/');
  return response.data;
}
