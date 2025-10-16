import React, { useState, useEffect } from 'react';
import { getDonationStats } from '../api/donations'; // Import the API function

const DonationStats = () => {
  const [stats, setStats] = useState({
    total_donations: 0,
    total_amount: 0,
    active_campaigns: 0,
    active_volunteers: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch donation stats when the component mounts
    const fetchStats = async () => {
      try {
        const data = await getDonationStats();
        setStats(data); // Set the stats data into state
      } catch (err) {
        setError('Failed to load donation statistics'); // Handle any errors
      } finally {
        setLoading(false); // Set loading to false once data is fetched or if there's an error
      }
    };

    fetchStats();
  }, []); // Empty dependency array means this runs only once when the component mounts

  if (loading) {
    return <div>Loading donation statistics...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Donation Statistics</h2>
      <ul>
        <li><strong>Total Donations:</strong> {stats.total_donations}</li>
        <li><strong>Total Amount Donated:</strong> {stats.total_amount}</li>
        <li><strong>Active Campaigns:</strong> {stats.active_campaigns}</li>
        <li><strong>Active Volunteers:</strong> {stats.active_volunteers}</li>
      </ul>
    </div>
  );
};

export default DonationStats;
