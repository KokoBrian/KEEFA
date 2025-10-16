import React, { useState } from 'react';
import { createDonation, type DonationData } from '../api/donations';

const DonationForm: React.FC = () => {
  const [formData, setFormData] = useState<DonationData>({
    donor_name: '',
    donor_email: '',
    is_anonymous: false,
    is_alumni: false,
    amount: 0,
    currency: 'USD',
    donation_type: 'one_time',
    designation: 'general',
    payment_method: 'mpesa',
  });

  const [customAmount, setCustomAmount] = useState<number | null>(null);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const target = e.target;
    const { name, value, type } = target;

    setFormData((prev: DonationData) => ({
      ...prev,
      [name]: type === 'checkbox' && target instanceof HTMLInputElement
        ? target.checked
        : value,
    }));
  };

  const handleAmountClick = (amount: number) => {
    setCustomAmount(null);
    setFormData((prev: DonationData) => ({
      ...prev,
      amount,
    }));
  };

  const handleCustomAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const amount = parseFloat(e.target.value);
    setCustomAmount(amount);
    setFormData((prev: DonationData) => ({
      ...prev,
      amount: amount || 0,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Submitting donation data:', formData);

    try {
      const result = await createDonation(formData);
      alert('Donation submitted successfully!');
      console.log(result);
    } catch (error) {
      console.error('Submit error:', error);
      alert('Something went wrong during submission.');
    }
  };

   return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">Choose Your Donation</h3>

      {/* Donation Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Donation Type</label>
        <div className="grid grid-cols-2 gap-4">
          {['one_time', 'monthly'].map((type) => (
            <label
              key={type}
              className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-colors duration-200 ${
                formData.donation_type === type ? 'border-primary-500' : 'border-gray-200'
              }`}
            >
              <input
                type="radio"
                name="donation_type"
                value={type}
                checked={formData.donation_type === type}
                onChange={handleInputChange}
                className="sr-only"
              />
              <div className="w-4 h-4 border-2 rounded-full mr-3 flex items-center justify-center">
                {formData.donation_type === type && (
                  <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                )}
              </div>
              <span className="font-medium capitalize">{type.replace('_', ' ')}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Select Amount */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Select Amount</label>
        <div className="grid grid-cols-3 gap-3 mb-4">
          {[50, 150, 500].map((amount) => (
            <button
              key={amount}
              type="button"
              className={`amount-btn p-3 border-2 rounded-lg font-semibold transition-colors duration-200 ${
                formData.amount === amount ? 'border-primary-500' : 'border-gray-200'
              }`}
              onClick={() => handleAmountClick(amount)}
            >
              ${amount}
            </button>
          ))}
        </div>
        <div className="relative">
          <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
          <input
            type="number"
            id="customAmount"
            placeholder="Enter custom amount"
            className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg"
            min="1"
            value={customAmount ?? ''}
            onChange={handleCustomAmountChange}
          />
        </div>
      </div>

      {/* Designation */}
      <div>
        <label htmlFor="designation" className="block text-sm font-medium text-gray-700 mb-2">
          Designate Your Donation
        </label>
        <select
          id="designation"
          name="designation"
          value={formData.designation}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
        >
          <option value="general">General Fund - Where Most Needed</option>
          <option value="scholarships">Scholarship Program</option>
          <option value="workshops">Workshops & Mentorship</option>
          <option value="community">Community Projects</option>
          <option value="organic">Organic Farming Initiative</option>
          <option value="environment">Environmental Conservation</option>
        </select>
      </div>

      {/* Name & Email */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="donor_name" className="block text-sm font-medium text-gray-700 mb-2">
            Full Name
          </label>
          <input
            type="text"
            id="donor_name"
            name="donor_name"
            required
            value={formData.donor_name}
            onChange={handleInputChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg"
            placeholder="Enter your full name"
          />
        </div>
        <div>
          <label htmlFor="donor_email" className="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            type="email"
            id="donor_email"
            name="donor_email"
            required
            value={formData.donor_email}
            onChange={handleInputChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg"
            placeholder="Enter your email"
          />
        </div>
      </div>

      {/* Anonymous Checkbox */}
      <div className="flex items-center space-x-3">
        <input
          type="checkbox"
          id="is_anonymous"
          name="is_anonymous"
          checked={formData.is_anonymous}
          onChange={handleInputChange}
          className="w-4 h-4 text-primary-600 border-gray-300 rounded"
        />
        <label htmlFor="is_anonymous" className="text-sm text-gray-600">
          Make this donation anonymous
        </label>
      </div>

      {/* Alumni Checkbox */}
      <div className="flex items-center space-x-3">
        <input
          type="checkbox"
          id="is_alumni"
          name="is_alumni"
          checked={formData.is_alumni}
          onChange={handleInputChange}
          className="w-4 h-4 text-primary-600 border-gray-300 rounded"
        />
        <label htmlFor="is_alumni" className="text-sm text-gray-600">
          I am an alumni
        </label>
      </div>

      {/* Alumni Donation Period (only show if is_alumni) */}
      {formData.is_alumni && (
        <div>
          <label
            htmlFor="alumni_donation_period"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Alumni Donation Period
          </label>
          <select
            id="alumni_donation_period"
            name="alumni_donation_period"
            value={formData.alumni_donation_period ?? ''}
            onChange={handleInputChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg"
          >
            <option value="" disabled>
              Select period
            </option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
            <option value="custom">Custom</option>
          </select>
        </div>
      )}

      <button
        type="submit"
        className="w-full bg-primary-500 hover:bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 hover:scale-105 shadow-lg"
      >
        Proceed to Payment
      </button>
    </form>
  );
};

export default DonationForm;