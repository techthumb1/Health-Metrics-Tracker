import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto'; // Ensure chart.js is properly initialized

// Define a type for the metrics
interface Metric {
  dateLogged: string;
  heartRate: number;
  weight: number;
}

const Dashboard = () => {
  const [metrics, setMetrics] = useState<Metric[]>([]); // Use the defined Metric type
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null); // Add error handling

  useEffect(() => {
    axios
      .get('http://localhost:5001/api/log_metrics') // Verify backend API endpoint
      .then((response) => {
        setMetrics(response.data.metrics || []); // Safely handle undefined response
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError('Failed to fetch metrics. Please try again later.');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>;
  }

  if (metrics.length === 0) {
    return (
      <div className="text-center text-gray-500">
        No metrics available. Start by logging your health metrics.
      </div>
    );
  }

  const chartData = {
    labels: metrics.map((m) => new Date(m.dateLogged).toLocaleDateString()), // Format dates
    datasets: [
      {
        label: 'Heart Rate',
        data: metrics.map((m) => m.heartRate),
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4, // Smooth curves
      },
      {
        label: 'Weight',
        data: metrics.map((m) => m.weight),
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: 'black',
        },
      },
      title: {
        display: true,
        text: 'Health Metrics Over Time',
        color: 'black',
      },
    },
    scales: {
      x: {
        ticks: { color: 'black' },
        grid: { color: 'rgba(0, 0, 0, 0.1)' },
      },
      y: {
        ticks: { color: 'black' },
        grid: { color: 'rgba(0, 0, 0, 0.1)' },
      },
    },
  };

  return (
    <div className="container mx-auto mt-5">
      <h2 className="text-2xl font-bold text-center mb-5">Health Metrics Dashboard</h2>
      <div className="w-full md:w-3/4 mx-auto">
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

export default Dashboard;
