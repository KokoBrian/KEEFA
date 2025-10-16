// paginated response

export interface Event {
  id: number;
  title: string;
  description: string;
  date: string;
  location: string;
  registrationUrl: string;
  colorScheme: "primary" | "success" | "secondary"; // assuming this is part of your API data
}           
        

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Organization---homepage data
export interface Organization {
  id: number;
  name: string;
  tagline: string;
  mission: string;
  vision: string;
  values: string;
  story: string;
  email: string;
  phone: string;
  address: string;
  facebook_url: string | null;
  twitter_url: string | null;
  instagram_url: string | null;
  linkedin_url: string | null;
  youtube_url: string | null;
  logo: string | null;
  hero_image: string | null;
  created_at: string;
  updated_at: string;
}
