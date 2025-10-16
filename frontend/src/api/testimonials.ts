import http from './http';
import type { PaginatedResponse } from './types';

export interface Testimonial {
  id: number;
  name: string;
  position: string;
  content: string;
  photo: string;
  program_type: 'scholarship' | 'community' | 'workshop';
  rating: number;
  is_featured: boolean;
}

// Fetch all testimonials (paginated)
export async function fetchTestimonials(): Promise<PaginatedResponse<Testimonial>> {
  const response = await http.get<PaginatedResponse<Testimonial>>('testimonials/');
  return response.data;
}

// Fetch only featured testimonials
export async function fetchFeaturedTestimonials(): Promise<Testimonial[]> {
  const response = await http.get<Testimonial[]>('testimonials/featured/');
  return response.data;
}
