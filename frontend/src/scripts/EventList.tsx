import React, { useState, useEffect } from "react";
import Event from "./Event";
import { type ApiEvent } from "../api/news";
import { fetchUpcomingEvents, } from "../api/news";

const EventList: React.FC = () => {
  const [events, setEvents] = useState<ApiEvent[]>([]);  // Use ApiEvent type here
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);

  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true);
      setError(null);

      try {
        // Fetch events with the current page
        const { results, count, next, previous } = await fetchUpcomingEvents(page);

        // Update the events and pagination information
        setEvents(results);  // This works because `results` should be of type `ApiEvent[]`
        setTotalPages(Math.ceil(count / 10));  // Assume 10 events per page for pagination
      } catch (err) {
        setError("Failed to load events. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [page]);

  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= totalPages) {
      setPage(newPage);  // Change page
    }
  };

  return (
    <div className="space-y-6">
      {loading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      {!loading && !error && events.length === 0 && <div>No upcoming events</div>}

      {events.map((event) => (
        <div key={event.id} className="bg-primary-50 rounded-xl p-6 border-l-4 border-primary-500">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="flex-1">
              <div className="flex items-center mb-2">
                <svg className="w-5 h-5 text-primary-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                </svg>
                <span className="text-sm text-primary-600 font-semibold">{event.start_date}</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">{event.title}</h3>
              <p className="text-gray-600">{event.venue}</p>
              <p className="text-gray-600">{event.registration_fee}</p>
            </div>
            <div className="mt-4 md:mt-0 md:ml-6">
              <a href={event.registrationUrl} className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-2 rounded-full font-semibold transition-colors duration-200">
                Register
              </a>
            </div>
          </div>
        </div>
      ))}

      {/* Pagination controls */}
      <div className="flex justify-between mt-6">
        <button
          className="px-4 py-2 bg-gray-200 rounded-md"
          disabled={page === 1}
          onClick={() => handlePageChange(page - 1)}
        >
          Previous
        </button>
        <span className="self-center">Page {page} of {totalPages}</span>
        <button
          className="px-4 py-2 bg-gray-200 rounded-md"
          disabled={page === totalPages}
          onClick={() => handlePageChange(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default EventList;
