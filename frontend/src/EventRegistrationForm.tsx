import React, { useState } from 'react';
import { registerForEvent } from './api/news';

const EventRegistrationForm: React.FC = () => {
  const [eventSlug, setEventSlug] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    const payload = {
      event_slug: eventSlug,
      user_email: userEmail,
    };

    try {
      const result = await registerForEvent(payload);
      setSuccessMessage(result.message);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-semibold text-center mb-6">Event Registration</h1>

      {/* Display error or success message */}
      {error && <div className="text-red-500 text-center mb-4">{error}</div>}
      {successMessage && <div className="text-green-500 text-center mb-4">{successMessage}</div>}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="eventSlug" className="block text-sm font-medium text-gray-700 mb-2">
            Event Slug
          </label>
          <input
            type="text"
            id="eventSlug"
            value={eventSlug}
            onChange={(e) => setEventSlug(e.target.value)}
            required
            placeholder="Enter the event slug"
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="userEmail" className="block text-sm font-medium text-gray-700 mb-2">
            Your Email
          </label>
          <input
            type="email"
            id="userEmail"
            value={userEmail}
            onChange={(e) => setUserEmail(e.target.value)}
            required
            placeholder="Enter your email"
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full p-3 mt-4 text-white font-semibold rounded-md focus:outline-none ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
};

export default EventRegistrationForm;
