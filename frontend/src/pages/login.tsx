import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

const Login = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({ email: '', password: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/login', formData);
      localStorage.setItem('token', response.data.token);
      alert('Login successful!');
      router.push('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      alert('Invalid credentials');
    }
  };

  return (
    <div className="container mx-auto mt-5">
      <h2 className="text-2xl font-bold text-center mb-5">Login</h2>
      <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white p-6 shadow-md rounded">
        <div className="mb-4">
          <label className="block text-gray-700">Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <button type="submit" className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
