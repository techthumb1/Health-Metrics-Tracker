import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

// Define a type for the metrics
interface Metric {
  dateLogged: string;
  heartRate: number;
  weight: number;
}

const Dashboard = () => {
  const [metrics, setMetrics] = useState<Metric[]>([]); // Use the defined Metric type
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get('http://localhost:5000/api/metrics')
      .then((response) => {
        setMetrics(response.data.metrics); // Ensure API response aligns with the Metric type
        setLoading(false);
      })
      .catch((error) => console.error(error));
  }, []);

  if (loading) return <div className="text-center">Loading...</div>;

  const chartData = {
    labels: metrics.map((m) => new Date(m.dateLogged).toLocaleDateString()), // No 'any' here
    datasets: [
      {
        label: 'Heart Rate',
        data: metrics.map((m) => m.heartRate), // No 'any' here
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
      },
      {
        label: 'Weight',
        data: metrics.map((m) => m.weight), // No 'any' here
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: true,
      },
    ],
  };

  return (
    <div className="container mx-auto mt-5">
      <h2 className="text-2xl font-bold text-center mb-5">Health Metrics Dashboard</h2>
      <div className="w-full md:w-3/4 mx-auto">
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
