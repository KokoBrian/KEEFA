import http from './http';
import type { ImpactStatistic } from './impact';
import type { Testimonial } from './testimonials';
import type {Organization } from './types';


export interface HomepageData {
  organization: Organization | null;
  impact_statistics: ImpactStatistic[];
  featured_testimonials: Testimonial[];
}

export async function fetchHomepageData(): Promise<HomepageData> {
  const response = await http.get<HomepageData>('homepage-data/');
  return response.data;
}
