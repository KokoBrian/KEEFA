import React, { useState, useEffect } from 'react';
import { createVolunteer } from '@/api/donations';
import Toast from './Alert'; 

interface VolunteerFormData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  location: string;
  interests: string[];
  skills_experience: string;
  availability: string;
}

const VolunteerForm: React.FC = () => {
  const [mounted, setMounted] = useState(false);
  const [formData, setFormData] = useState<VolunteerFormData>({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    location: '',
    interests: [],
    skills_experience: '',
    availability: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  // Remove inline errorMessage and successMessage state
  const [loading, setLoading] = useState(false);

  // Toast state
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState<'success' | 'error'>('success');

  useEffect(() => {
    setMounted(true);
  }, []);

  const interestOptions = [
    { label: 'Student Mentorship', value: 'mentorship' },
    { label: 'Workshop Facilitation', value: 'workshops' },
    { label: 'Community Projects', value: 'community' },
    { label: 'Administrative Support', value: 'admin' },
    { label: 'Documentation & Media', value: 'media' },
    { label: 'Fundraising & Outreach', value: 'fundraising' },
  ];

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (value: string) => {
    setFormData((prev) => {
      const current = prev.interests || [];
      const updated = current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value];
      return { ...prev, interests: updated };
    });
  };

  const validate = (): Record<string, string> => {
    const errs: Record<string, string> = {};
    if (!formData.first_name.trim()) errs.first_name = 'First name is required';
    if (!formData.last_name.trim()) errs.last_name = 'Last name is required';
    if (!formData.email.trim()) {
      errs.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errs.email = 'Invalid email format';
    }
    if ((formData.interests || []).length === 0)
      errs.interests = 'Select at least one interest area';
    return errs;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setToastType('error');
      setToastMessage('Please correct the errors in the form.');
      return;
    }

    setLoading(true);
    setErrors({});
    setToastMessage('');

    try {
      const response = await createVolunteer(formData);
      if (response.status === 200 || response.status === 201) {
        setToastType('success');
        setToastMessage('Thank you! Your volunteer application was submitted successfully.');
        setFormData({
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          location: '',
          interests: [],
          skills_experience: '',
          availability: '',
        });
      } else {
        setToastType('error');
        setToastMessage('Submission failed. Please try again.');
      }
    } catch (error: any) {
      console.error('Volunteer submission error:', error);
      if (error?.response?.data) {
        const apiErrors = error.response.data;
        const formattedErrors: Record<string, string> = {};

        for (const key in apiErrors) {
          if (Array.isArray(apiErrors[key])) {
            formattedErrors[key] = apiErrors[key][0];
          }
        }

        setErrors(formattedErrors);
        setToastType('error');
        setToastMessage('Please correct the errors and try again.');
      } else {
        setToastType('error');
        setToastMessage('Something went wrong. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCloseToast = () => {
    setToastMessage('');
  };

  return (
    <div className="bg-gray-50 rounded-2xl p-8">
      <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Volunteer Application</h3>

      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-6">
        {/* First & Last Name */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="first_name" className="block text-sm font-medium mb-2">First Name *</label>
            <input
              id="first_name"
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${
                errors.first_name ? 'border-red-600' : 'border-gray-300'
              }`}
              placeholder="Jane"
            />
            {errors.first_name && <p className="text-red-600 text-sm mt-1">{errors.first_name}</p>}
          </div>
          <div>
            <label htmlFor="last_name" className="block text-sm font-medium mb-2">Last Name *</label>
            <input
              id="last_name"
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${
                errors.last_name ? 'border-red-600' : 'border-gray-300'
              }`}
              placeholder="Doe"
            />
            {errors.last_name && <p className="text-red-600 text-sm mt-1">{errors.last_name}</p>}
          </div>
        </div>

        {/* Email & Phone */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-2">Email Address *</label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${
                errors.email ? 'border-red-600' : 'border-gray-300'
              }`}
              placeholder="email@example.com"
            />
            {errors.email && <p className="text-red-600 text-sm mt-1">{errors.email}</p>}
          </div>
          <div>
            <label htmlFor="phone" className="block text-sm font-medium mb-2">Phone Number</label>
            <input
              id="phone"
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500"
              placeholder="+123456789"
            />
          </div>
        </div>

        {/* Location */}
        <div>
          <label htmlFor="location" className="block text-sm font-medium mb-2">Location</label>
          <input
            id="location"
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500"
            placeholder="City, County"
          />
        </div>

        {/* Interests */}
        <div>
          <label className="block text-sm font-medium mb-2">Areas of Interest *</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {interestOptions.map(({ label, value }) => (
              <label key={value} className="flex items-center text-sm">
                <input
                  type="checkbox"
                  value={value}
                  checked={formData.interests.includes(value)}
                  onChange={() => handleCheckboxChange(value)}
                  className="mr-2 text-secondary-600"
                />
                {label}
              </label>
            ))}
          </div>
          {errors.interests && <p className="text-red-600 text-sm mt-1">{errors.interests}</p>}
        </div>

        {/* Skills & Experience */}
        <div>
          <label htmlFor="skills_experience" className="block text-sm font-medium mb-2">Skills & Experience</label>
          <textarea
            id="skills_experience"
            name="skills_experience"
            value={formData.skills_experience}
            onChange={handleChange}
            rows={4}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500"
            placeholder="Tell us about your relevant skills, experience, and what you'd like to contribute..."
          ></textarea>
        </div>

        {/* Availability */}
        <div>
          <label htmlFor="availability" className="block text-sm font-medium mb-2">Availability</label>
          <select
            id="availability"
            name="availability"
            value={formData.availability}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500"
          >
            <option value="">Select your availability</option>
            <option value="weekdays">Weekdays</option>
            <option value="weekends">Weekends</option>
            <option value="evenings">Evenings</option>
            <option value="flexible">Flexible</option>
            <option value="events">Events only</option>
          </select>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full bg-secondary-500 hover:bg-secondary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 hover:scale-105 shadow-lg ${
            loading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Submitting...' : 'Submit Volunteer Application'}
        </button>
      </form>

      {/* Toast Notification */}
      {toastMessage && (
        <Toast
          message={toastMessage}
          type={toastType}
          onClose={handleCloseToast}
        />
      )}
    </div>
  );
};

export default VolunteerForm;
