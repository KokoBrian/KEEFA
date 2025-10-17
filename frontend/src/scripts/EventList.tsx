import React, { useState, useEffect } from 'react';
import { fetchUpcomingEvents, type ApiEvent } from '../api/news';
import EventRegistrationForm from './EventRegistrationForm';

const EventList: React.FC = () => {
  const [events, setEvents] = useState<ApiEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedEvent, setSelectedEvent] = useState<ApiEvent | null>(null);
  const [successMessages, setSuccessMessages] = useState<Record<number, string>>({});

  useEffect(() => {
    const loadEvents = async () => {
      setLoading(true);
      setError(null);
      try {
        const { results, count } = await fetchUpcomingEvents(page);
        setEvents(results);
        setTotalPages(Math.ceil(count / 10));
      } catch {
        setError('Failed to load events. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    loadEvents();
  }, [page]);

  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= totalPages) setPage(newPage);
  };

  const handleRegistrationSuccess = (eventId: number, message: string) => {
    setSuccessMessages((prev) => ({ ...prev, [eventId]: message }));
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
              <span className="text-sm text-primary-600 font-semibold">{event.start_date}</span>
              <h3 className="text-xl font-bold text-gray-900 mb-2">{event.title}</h3>
              <p className="text-gray-600">{event.venue}</p>
              <p className="text-gray-600">{event.registration_fee}</p>
              {successMessages[event.id] && (
                <p className="text-green-500 mt-2">{successMessages[event.id]}</p>
              )}
            </div>
            <div className="mt-4 md:mt-0 md:ml-6">
              <button
                onClick={() => setSelectedEvent(event)}
                className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-2 rounded-full font-semibold transition-colors duration-200"
              >
                Register
              </button>
            </div>
          </div>
        </div>
      ))}

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

      {/* Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <EventRegistrationForm
            eventSlug={selectedEvent.slug}
            onClose={() => setSelectedEvent(null)}
            onSuccess={(message) => handleRegistrationSuccess(selectedEvent.id, message)}
          />
        </div>
      )}
    </div>
  );
};

export default EventList;
