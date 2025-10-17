import React from "react";
import { fetchUpcomingEvents, type ApiEvent } from '../api/news';

type EventProps = {
  id: number;
  title: string;
  slug: string;
  event_type: string;
  start_date: string;  // Can be parsed to Date if necessary
  end_date: string;
  venue: string;
  featured_image: string;
  requires_registration: boolean;
  registration_fee: string;
  status: string;
  is_featured: boolean;
  is_past: boolean;
  is_today: boolean;
  
  // Add the missing properties here:
  date: string;         
  location: string;     
  description: string;  
  registrationUrl: string; 
  colorScheme?: string;  
};

const Event: React.FC<EventProps> = ({
  id,
  title,
  date,
  location,
  description,
  registrationUrl,
  colorScheme,
}) => {
  // Helper to map color scheme to Tailwind classes
  const bgColor = `${colorScheme}-50`;
  const borderColor = `${colorScheme}-500`;
  const textColor = `${colorScheme}-600`;
  const hoverColor = `${colorScheme}-600`;

  return (
    <div className={`bg-${bgColor} rounded-xl p-6 border-l-4 border-${borderColor} animate-on-scroll`}>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <svg
              className={`w-5 h-5 text-${borderColor} mr-2`}
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                clipRule="evenodd"
              />
            </svg>
            <span className={`text-sm text-${textColor} font-semibold`}>
              {new Date(date).toLocaleString()} • {location}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
          <p className="text-gray-600">{description}</p>
        </div>
        <div className="mt-4 md:mt-0 md:ml-6">
          <a
            href={registrationUrl}
            className={`bg-${borderColor} hover:bg-${hoverColor} text-white px-6 py-2 rounded-full font-semibold transition-colors duration-200`}
          >
            Register
          </a>
        </div>
      </div>
    </div>
  );
};

export default Event;
