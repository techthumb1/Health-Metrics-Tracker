import { useState } from 'react';
import axios from 'axios';

const LogMetrics = () => {
  const [formData, setFormData] = useState({
    heartRate: '',
    weight: '',
    systolic: '',
    diastolic: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/metrics', formData); // Removed response variable
      alert('Metrics logged successfully!');
      setFormData({ heartRate: '', weight: '', systolic: '', diastolic: '' });
    } catch (error) {
      console.error('Error logging metrics:', error);
      alert('Failed to log metrics.');
    }
  };

  return (
    <div className="container mx-auto mt-5">
      <h2 className="text-2xl font-bold text-center mb-5">Log Your Health Metrics</h2>
      <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white p-6 shadow-md rounded">
        <div className="mb-4">
          <label className="block text-gray-700">Heart Rate (bpm):</label>
          <input
            type="number"
            name="heartRate"
            value={formData.heartRate}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Weight (kg):</label>
          <input
            type="number"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Systolic Pressure (mmHg):</label>
          <input
            type="number"
            name="systolic"
            value={formData.systolic}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Diastolic Pressure (mmHg):</label>
          <input
            type="number"
            name="diastolic"
            value={formData.diastolic}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
          Log Metrics
        </button>
      </form>
    </div>
  );
};

export default LogMetrics;
