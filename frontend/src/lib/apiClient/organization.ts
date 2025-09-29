// lib/apiClient/organization.ts
import api from '../api';

export interface Organization {
  name: string;
  tagline: string;
  mission: string | null;
  vision: string | null;
  values: string | null;
  story: string | null;
  email: string;
  phone: string;
  address: string;
  facebook_url: string;
  twitter_url: string;
  instagram_url: string;
  linkedin_url: string;
  youtube_url: string;
  logo: string | null;
  hero_image: string | null;
}

export const fetchOrganization = async (): Promise<Organization> => {
  const res = await api.get<Organization>('/api/v1/organization/');
  return res.data;
};
