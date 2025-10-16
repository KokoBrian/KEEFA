import React, { useState, useEffect } from 'react';
import { createPartnership } from '../api/donations';
import Toast from './Alert';

interface FormData {
  orgName: string;
  contactName: string;
  contactEmail: string;
  partnershipType: string;
  partnershipMessage: string;
  phone: string;
  website: string;
  interests: string[];
}

const PartnershipInquiryForm: React.FC = () => {
  const [mounted, setMounted] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    orgName: '',
    contactName: '',
    contactEmail: '',
    partnershipType: '',
    partnershipMessage: '',
    phone: '',
    website: '',
    interests: [],
  });

  const [loading, setLoading] = useState(false);

  // Toast state
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState<'success' | 'error'>('success');

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleInterestChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value, checked } = e.target;
    setFormData((prev) => {
      const newInterests = checked
        ? [...prev.interests, value]
        : prev.interests.filter((interest) => interest !== value);
      return { ...prev, interests: newInterests };
    });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validate = (): Record<string, string> => {
    const errors: Record<string, string> = {};
    if (!formData.orgName.trim()) errors.orgName = 'Organization Name is required';
    if (!formData.contactName.trim()) errors.contactName = 'Contact Person is required';
    if (!formData.contactEmail.trim()) {
      errors.contactEmail = 'Contact Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.contactEmail)) {
      errors.contactEmail = 'Invalid email address';
    }
    if (!formData.partnershipType) errors.partnershipType = 'Partnership type is required';
    if (!formData.partnershipMessage.trim()) errors.partnershipMessage = 'Proposal is required';
    return errors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const errors = validate();
    if (Object.keys(errors).length > 0) {
      setToastType('error');
      setToastMessage('Please fill in all required fields correctly.');
      return;
    }

    setLoading(true);
    setToastMessage(''); // Clear existing toast

    try {
      const response = await createPartnership({
        organization_name: formData.orgName,
        organization_type: formData.partnershipType,
        contact_person: formData.contactName,
        email: formData.contactEmail,
        phone: formData.phone,
        website: formData.website || undefined,
        partnership_interests: formData.interests,
        proposal_details: formData.partnershipMessage || undefined,
      });

      if (response.status === 200 || response.status === 201) {
        setToastType('success');
        setToastMessage('Thank you! Your partnership inquiry was submitted successfully.');
        // Reset form fields
        setFormData({
          orgName: '',
          contactName: '',
          contactEmail: '',
          partnershipType: '',
          partnershipMessage: '',
          phone: '',
          website: '',
          interests: [],
        });
      } else {
        setToastType('error');
        setToastMessage('Submission failed. Please try again later.');
      }
    } catch (error: any) {
      console.error('Submission error:', error);

      setToastType('error');

      if (error.response?.data?.message) {
        setToastMessage(error.response.data.message);
      } else if (error.message) {
        setToastMessage(error.message);
      } else {
        setToastMessage('Submission failed. Please try again or contact support.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCloseToast = () => {
    setToastMessage('');
  };

  return (
    <>
      <div
        className={
          'bg-white rounded-2xl p-8 shadow-xl animate-on-scroll max-w-xl mx-auto ' +
          (mounted ? 'animate-fade-in' : '')
        }
      >
        <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Partnership Inquiry</h3>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* form fields here same as before */}
          {/* ... */}
          <div className="relative">
            <label htmlFor="orgName" className="block text-sm font-medium text-gray-700 mb-2">
              Organization Name *
            </label>
            <input
              type="text"
              id="orgName"
              name="orgName"
              value={formData.orgName}
              onChange={handleChange}
              required
              placeholder="Your organization's name"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="contactName" className="block text-sm font-medium text-gray-700 mb-2">
                Contact Person *
              </label>
              <input
                type="text"
                id="contactName"
                name="contactName"
                value={formData.contactName}
                onChange={handleChange}
                required
                placeholder="Full name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
              />
            </div>
            <div>
              <label htmlFor="contactEmail" className="block text-sm font-medium text-gray-700 mb-2">
                Contact Email *
              </label>
              <input
                type="email"
                id="contactEmail"
                name="contactEmail"
                value={formData.contactEmail}
                onChange={handleChange}
                required
                placeholder="Email address"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
              />
            </div>
          </div>

          <div>
            <label htmlFor="partnershipType" className="block text-sm font-medium text-gray-700 mb-2">
              Type of Partnership *
            </label>
            <select
              id="partnershipType"
              name="partnershipType"
              value={formData.partnershipType}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
            >
              <option value="">Select a partnership type</option>
              <option value="corporate">Corporate</option>
              <option value="educational">Educational Institution</option>
              <option value="ngo">Government / NGO</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label htmlFor="partnershipMessage" className="block text-sm font-medium text-gray-700 mb-2">
              Your Proposal *
            </label>
            <textarea
              id="partnershipMessage"
              name="partnershipMessage"
              value={formData.partnershipMessage}
              onChange={handleChange}
              rows={6}
              required
              placeholder="Describe your organization and how you envision partnering with us..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                Phone
              </label>
              <input
                type="text"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Optional phone number"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
              />
            </div>
            <div>
              <label htmlFor="website" className="block text-sm font-medium text-gray-700 mb-2">
                Website
              </label>
              <input
                type="url"
                id="website"
                name="website"
                value={formData.website}
                onChange={handleChange}
                placeholder="Optional website URL"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Areas of Interest</label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {['Volunteering', 'Donations', 'Partnerships', 'Other'].map((interest) => (
                <label key={interest} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    name="interests"
                    value={interest}
                    checked={formData.interests.includes(interest)}
                    onChange={handleInterestChange}
                    className="form-checkbox text-green-600"
                  />
                  <span>{interest}</span>
                </label>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Submitting...' : 'Submit Inquiry'}
          </button>
        </form>
      </div>

      {/* Toast notification */}
      {toastMessage && (
        <Toast message={toastMessage} type={toastType} onClose={handleCloseToast} />
      )}
    </>
  );
};

export default PartnershipInquiryForm;
