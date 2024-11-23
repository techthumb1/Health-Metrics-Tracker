import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/">
          <a className="text-white text-lg font-bold">Health Metrics Tracker</a>
        </Link>
        <div className="space-x-4">
          <Link href="/dashboard">
            <a className="text-gray-300 hover:text-white">Dashboard</a>
          </Link>
          <Link href="/log-metrics">
            <a className="text-gray-300 hover:text-white">Log Metrics</a>
          </Link>
          <Link href="/login">
            <a className="text-gray-300 hover:text-white">Login</a>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
