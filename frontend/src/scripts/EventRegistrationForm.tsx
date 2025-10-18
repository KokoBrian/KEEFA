import React, { useState } from 'react';
import { registerForEvent } from '../api/news';

interface Props {
  eventSlug: string;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

const EventRegistrationForm: React.FC<Props> = ({ eventSlug, onClose, onSuccess }) => {
    const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    organization: '',
    dietary_requirements: '',
    special_needs: '',
    comments: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

  try {
      const payload = { ...formData, event_slug: eventSlug };
      const result = await registerForEvent(payload);
      onSuccess(result.message);
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-semibold text-center mb-6">Event Registration</h1>

      {/* Display error or success message */}
      {error && <div className="text-red-500 text-center mb-4">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <input name="first_name" placeholder="First Name" required value={formData.first_name} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <input name="last_name" placeholder="Last Name" required value={formData.last_name} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <input type="email" name="email" placeholder="Email" required value={formData.email} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <input name="phone" placeholder="Phone" value={formData.phone} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <input name="organization" placeholder="Organization" value={formData.organization} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <input name="dietary_requirements" placeholder="Dietary Requirements" value={formData.dietary_requirements} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <input name="special_needs" placeholder="Special Needs" value={formData.special_needs} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <textarea name="comments" placeholder="Additional Comments" value={formData.comments} onChange={handleChange} className="w-full p-2 border rounded mb-3" />
        <div className="flex justify-end space-x-2">
          <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-200 rounded">
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className={`px-4 py-2 text-white rounded ${loading ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'}`}
          >
            {loading ? 'Registering...' : 'Register'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default EventRegistrationForm;