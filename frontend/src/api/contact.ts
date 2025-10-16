import http from './http';
import type { PaginatedResponse } from './types';

// =============================
// TYPES
// =============================

export interface ContactInquiryPayload {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  organization?: string;
  subject?: string;
  general_inquiry?: string;
  message: string;
  subscribe_newsletter?: boolean;
}

export interface ContactInquiryResponse {
  id?: number;
  success?: boolean;
  detail?: string;
  [key: string]: any;
}

export interface OfficeLocation {
  id: number;
  name: string;
  address: string;
  city: string;
  county: string;
  postal_code: string;
  country: string;
  phone: string;
  email: string;
  latitude: string;
  longitude: string;
  office_hours: string;
  services_offered: string;
  is_main_office: boolean;
}

export interface ContactPerson {
  id: number;
  name: string;
  position: string;
  department: string;
  email: string;
  phone: string;
  extension?: string | null;
  office_hours?: string | null;
  languages_spoken?: string | null;
  photo?: string | null;
  bio?: string | null;
}

export interface SocialMediaAccount {
  id?: number;
  platform?: string;
  url?: string;
  icon?: string;
  [key: string]: any;
}

export interface ContactPageData {
  office_locations: OfficeLocation[];
  contact_persons: ContactPerson[];
  social_media: SocialMediaAccount[];
}

// =============================
// API FUNCTIONS
// =============================

/**
 * Submit a contact inquiry (POST)
 */
export async function submitContactInquiry(
  data: ContactInquiryPayload
): Promise<ContactInquiryResponse | null> {
  try {
    const response = await http.post<ContactInquiryResponse>('contact/inquiries/', data);
    return response.data;
  } catch (error: any) {
    console.error('submitContactInquiry error:', error?.response?.data || error.message || error);
    return null;
  }
}


/**
 * Get list of office locations (paginated)
 */
export async function fetchOfficeLocations(): Promise<PaginatedResponse<OfficeLocation> | null> {
  try {
    const response = await http.get<PaginatedResponse<OfficeLocation>>(
      'contact/offices/'
    );
    return response.data;
  } catch (error: any) {
    console.error('fetchOfficeLocations error:', error?.message || error);
    return null;
  }
}

/**
 * Get list of contact persons (paginated)
 */
export async function fetchContactPersons(): Promise<PaginatedResponse<ContactPerson> | null> {
  try {
    const response = await http.get<PaginatedResponse<ContactPerson>>(
      'contact/persons/'
    );
    return response.data;
  } catch (error: any) {
    console.error('fetchContactPersons error:', error?.message || error);
    return null;
  }
}

/**
 * Get list of social media accounts (paginated)
 */
export async function fetchSocialMedia(): Promise<PaginatedResponse<SocialMediaAccount> | null> {
  try {
    const response = await http.get<PaginatedResponse<SocialMediaAccount>>(
      'contact/social-media/'
    );
    return response.data;
  } catch (error: any) {
    console.error('fetchSocialMedia error:', error?.message || error);
    return null;
  }
}

/**
 * Get all data needed for the contact page
 */
export async function fetchContactPageData(): Promise<ContactPageData | null> {
  try {
    const response = await http.get<ContactPageData>(
      'contact/page-data/'
    );
    return response.data;
  } catch (error: any) {
    console.error('fetchContactPageData error:', error?.message || error);
    return null;
  }
}

/**
 * Get social media accounts for the footer
 */
export async function fetchFooterSocialMedia(): Promise<SocialMediaAccount[] | null> {
  try {
    const response = await http.get<SocialMediaAccount[]>(
      'contact/footer-social/'
    );
    return response.data;
  } catch (error: any) {
    console.error('fetchFooterSocialMedia error:', error?.message || error);
    return null;
  }
}
