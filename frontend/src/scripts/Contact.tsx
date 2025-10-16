import React, { useState, useEffect } from 'react';
import { submitContactInquiry } from '../api/contact'; 
import Toast from './Alert'; 

interface ContactFormData {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  organization?: string;
  subject: string; // Changed to required field
  general_inquiry?: string;
  message: string;
  subscribe_newsletter?: boolean;
}

const ContactForm: React.FC = () => {
  const [mounted, setMounted] = useState(false);
  const [formData, setFormData] = useState<ContactFormData>({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    organization: '',
    subject: '', // Empty string is now not allowed
    general_inquiry: '',
    message: '',
    subscribe_newsletter: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  
  // Toast state management
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState<'success' | 'error'>('success');

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setFormData((prev) => ({ ...prev, [name]: checked }));
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
    if (!formData.message.trim()) errs.message = 'Message is required';
    if (!formData.subject.trim()) errs.subject = 'Subject is required'; // Added subject validation
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
    setErrors({}); // Clear previous errors
    setToastMessage(''); // Clear previous toast message

    // Log form data to inspect the subject field
    console.log('Form Data:', formData);

    try {
      const response = await submitContactInquiry(formData);
      if (response?.success) {
        setToastType('success');
        setToastMessage("Your inquiry has been successfully submitted. We'll get back to you as soon as possible!");
        setFormData({
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          organization: '',
          subject: '', // Reset subject to an empty string
          general_inquiry: '',
          message: '',
          subscribe_newsletter: false,
        });
      } else {
        setToastType('error');
        setToastMessage('Message submission failed. Please try again.');
      }
    } catch (error: any) {
      console.error('Contact form submission error:', error);
      setToastType('error');
      setToastMessage('Something went wrong. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleCloseToast = () => {
    setToastMessage(''); // Clear toast message when closed
  };

  return (
    <div className="bg-gray-50 rounded-2xl p-8">
      <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Contact Us</h3>

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
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${errors.first_name ? 'border-red-600' : 'border-gray-300'}`}
              placeholder="Mary"
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
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${errors.last_name ? 'border-red-600' : 'border-gray-300'}`}
              placeholder="Mackay"
            />
            {errors.last_name && <p className="text-red-600 text-sm mt-1">{errors.last_name}</p>}
          </div>
        </div>

        {/* Email */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-2">Email *</label>
          <input
            id="email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${errors.email ? 'border-red-600' : 'border-gray-300'}`}
            placeholder="email@example.com"
          />
          {errors.email && <p className="text-red-600 text-sm mt-1">{errors.email}</p>}
        </div>

        {/* Subject */}
        <div>
          <label htmlFor="subject" className="block text-sm font-medium mb-2">Subject *</label>
          <select
  id="subject"
  name="subject"
  value={formData.subject}
  onChange={handleChange}
  required
  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${errors.subject ? 'border-red-600' : 'border-gray-300'}`}
>
  <option value="">Select a subject</option>
  <option value="general">General Inquiry</option>
  <option value="volunteer">Volunteer Opportunities</option>
  <option value="partnership">Partnership Proposal</option>
  <option value="donation">Donation Information</option>
  <option value="scholarship">Scholarship Application</option>
  <option value="media">Media Inquiry</option>
  <option value="complaint">Complaint</option>
  <option value="other">Other</option>
</select>

          {errors.subject && <p className="text-red-600 text-sm mt-1">{errors.subject}</p>}
        </div>

        {/* Message */}
        <div>
          <label htmlFor="message" className="block text-sm font-medium mb-2">Message *</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows={4}
            required
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-secondary-500 ${errors.message ? 'border-red-600' : 'border-gray-300'}`}
            placeholder="Your message..."
          ></textarea>
          {errors.message && <p className="text-red-600 text-sm mt-1">{errors.message}</p>}
        </div>

        {/* Subscribe to Newsletter */}
        <div>
          <label className="flex items-center text-sm">
            <input
              type="checkbox"
              name="subscribe_newsletter"
              checked={formData.subscribe_newsletter || false}
              onChange={handleCheckboxChange}
              className="mr-2 text-secondary-600"
            />
            Subscribe to newsletter
          </label>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full bg-secondary-500 hover:bg-secondary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 hover:scale-105 shadow-lg ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading ? 'Submitting...' : 'Send Message'}
        </button>
      </form>

      {/* Toast Notification */}
      {toastMessage && (
        <Toast message={toastMessage} type={toastType} onClose={handleCloseToast} />
      )}
    </div>
  );
};

export default ContactForm;
