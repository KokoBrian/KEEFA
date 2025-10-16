// api/about.ts
import http from './http';

export interface AboutData {
  organization: any | null;      // Define more specifically if you have structure
  team_members: any[];           // Ideally typed as TeamMember[], if imported
  partners: any[];               // Ideally typed as Partner[], if imported
}

export async function fetchAboutData(): Promise<AboutData> {
  const response = await http.get<AboutData>('about-data/');
  return response.data;
}
