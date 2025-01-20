import React, { useState } from 'react';

interface MetricsFormData {
  heartRate: string;
  weight: string;
  systolic: string;
  diastolic: string;
}

const LogMetrics = () => {
  const [formData, setFormData] = useState<MetricsFormData>({
    heartRate: '',
    weight: '',
    systolic: '',
    diastolic: '',
  });
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    // Only allow numbers and decimal points
    if (!/^\d*\.?\d*$/.test(value) && value !== '') return;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  const validateForm = (): boolean => {
    if (!formData.heartRate || !formData.weight || !formData.systolic || !formData.diastolic) {
      setError('All fields are required');
      return false;
    }
    
    const hr = parseFloat(formData.heartRate);
    const w = parseFloat(formData.weight);
    const sys = parseFloat(formData.systolic);
    const dia = parseFloat(formData.diastolic);

    if (hr < 30 || hr > 220) {
      setError('Heart rate should be between 30 and 220 bpm');
      return false;
    }
    if (w < 20 || w > 300) {
      setError('Weight should be between 20 and 300 kg');
      return false;
    }
    if (sys < 70 || sys > 250) {
      setError('Systolic pressure should be between 70 and 250 mmHg');
      return false;
    }
    if (dia < 40 || dia > 150) {
      setError('Diastolic pressure should be between 40 and 150 mmHg');
      return false;
    }
    if (dia >= sys) {
      setError('Systolic pressure must be greater than diastolic pressure');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5001/log_metrics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setFormData({
        heartRate: '',
        weight: '',
        systolic: '',
        diastolic: '',
      });
      alert('Metrics logged successfully!');
    } catch (error) {
      console.error('Error logging metrics:', error);
      setError('Failed to log metrics. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-center mb-6">Log Your Health Metrics</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-600">
            {error}
          </div>
        )}
        
        <div>
          <label className="block text-sm font-medium mb-1">
            Heart Rate (bpm):
            <input
              type="text"
              name="heartRate"
              value={formData.heartRate}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="60-100"
            />
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Weight (kg):
            <input
              type="text"
              name="weight"
              value={formData.weight}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="Enter weight"
            />
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Systolic Pressure (mmHg):
            <input
              type="text"
              name="systolic"
              value={formData.systolic}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="90-120"
            />
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Diastolic Pressure (mmHg):
            <input
              type="text"
              name="diastolic"
              value={formData.diastolic}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="60-80"
            />
          </label>
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-blue-300"
        >
          {loading ? 'Logging...' : 'Log Metrics'}
        </button>
      </form>
    </div>
  );
};

export default LogMetrics;