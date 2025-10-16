// src/api/donations.ts
import http from './http';

export interface PartnershipRequest {
  organization_name: string;
  organization_type: string;
  contact_person: string;
  email: string;
  phone: string;
  website?: string;
  partnership_interests: string[];
  proposal_details?: string;
}

export interface VolunteerRequest {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  location?: string;
  interests?: string[];
  skills_experience?: string;
  availability?: string;
}

export interface DonationData {
  donor_name: string;
  donor_email: string;
  donor_phone?: string;
  is_anonymous: boolean;
  is_alumni: boolean;
  alumni_donation_period?: 'monthly' | 'yearly' | 'custom';
  amount: number;
  currency: string;
  donation_type: 'one_time' | 'monthly' | 'annual';
  campaign?: string;
  designation: string;
  message?: string;
  payment_method: 'mpesa' | 'stripe';
}


// partnerships.ts
export async function createPartnership(data: PartnershipRequest) {
  try {
    const response = await http.post('donations/partnerships/', data);
    return response;
  } catch (error) {
    console.error('API Error in createPartnership:', error);
    throw error;
  }
}

// volunteers

export async function createVolunteer(data: VolunteerRequest) {
  try {
    const response = await http.post('donations/volunteers/', data);
    return response;
  } catch (error) {
    console.error('API Error in createVolunteer:', error);
    throw error;
  }
}


//donate
export const createDonation = async (data: DonationData) => {
  const response = await http.post('donations/create/', data);
  return response;
};

// Function to fetch donation statistics
export async function getDonationStats() {
  try {
    const response = await http.get('donations/stats/');
    return response.data;
  } catch (error) {
    console.error('Error fetching donation stats:', error);
    throw error;
  }
}