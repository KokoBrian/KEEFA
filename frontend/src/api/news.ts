// api/news.ts
import http from './http';
import type { PaginatedResponse } from './types';

export interface NewsCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  color: string; // e.g., "primary"
}


export interface NewsArticle {
  // fill in with actual properties when known
  [key: string]: any;
}

// Define the Event type
export interface ApiEvent  {
  id: number;
  title: string;
  slug: string;
  event_type: string;
  start_date: string; // You can parse it to a Date object if needed
  end_date: string;
  venue: string;
  featured_image: string;
  requires_registration: boolean;
  registration_fee: string;
  status: string;
  is_featured: boolean;
  is_past: boolean;
  is_today: boolean;
}


/**
 * Fetch all active news categories (paginated)
 */
export async function fetchNewsCategories(): Promise<PaginatedResponse<NewsCategory>> {
  const response = await http.get<PaginatedResponse<NewsCategory>>('news/categories/');
  return response.data;
}

/**
 * Fetch all published news articles (paginated)
 */
export async function fetchNewsArticles(): Promise<PaginatedResponse<NewsArticle>> {
  const response = await http.get<PaginatedResponse<NewsArticle>>('news/articles/');
  return response.data;
}

/**
 * Fetch featured news articles (paginated)
 */
export async function fetchFeaturedNews(): Promise<PaginatedResponse<NewsArticle>> {
  const response = await http.get<PaginatedResponse<NewsArticle>>('news/articles/featured/');
  return response.data;
}


export interface NewsletterSubscribePayload {
  email: string;
  first_name: string;
  last_name: string;
  interests: string[];  // interest categories
  frequency: string;    // e.g., 'Weekly'
}

export interface NewsletterSubscribeResponse {
  // Depending on response, maybe:
  success: boolean;
  message?: string; 
  [key: string]: any;
}

/**
 * Subscribe to newsletter
 */
export async function subscribeNewsletter(
  data: NewsletterSubscribePayload
): Promise<NewsletterSubscribeResponse> {
  const response = await http.post<NewsletterSubscribeResponse>('news/newsletter/subscribe/', data);
  return response.data;
}


/**
 * Fetch upcoming events (paginated)
 */
export async function fetchUpcomingEvents(page: number = 1): Promise<PaginatedResponse<Event>> {
  try {
    const response = await http.get<PaginatedResponse<Event>>('news/events/upcoming/', {
      params: { page },  // Pass `page` as query parameter
    });
    return response.data;  // Return the entire paginated response
  } catch (error) {
    throw new Error("Failed to fetch events");
  }
}


// Define the interface for the event registration payload
interface EventRegistrationPayload {
  event_slug: string;
  user_email: string;
  [key: string]: any; // Add any additional fields you need
}

// Function to register for an event
export const registerForEvent = async (payload: EventRegistrationPayload) => {
  try {
    const response = await axios.post(BASE_URL, payload);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      // If the server responded with an error
      throw new Error(error.response.data.error || 'Something went wrong!');
    }
    // If there was a network error
    throw new Error('Network error occurred');
  }
};