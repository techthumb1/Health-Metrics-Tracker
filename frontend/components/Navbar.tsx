import Link from 'next/link';
import { useRouter } from 'next/router';

const Navbar = () => {
  const router = useRouter(); // To track the current route
  const isLoggedIn = false; // Replace with your authentication logic

  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* Brand Name */}
        <Link href="/" className="text-white text-lg font-bold">
          Health Metrics Tracker
        </Link>

        {/* Navigation Links */}
        <div className="space-x-4">
          <Link
            href="/dashboard"
            className={`${
              router.pathname === '/dashboard' ? 'text-white' : 'text-gray-300'
            } hover:text-white`}
          >
            Dashboard
          </Link>
          <Link
            href="/log-metrics"
            className={`${
              router.pathname === '/log-metrics' ? 'text-white' : 'text-gray-300'
            } hover:text-white`}
          >
            Log Metrics
          </Link>
          {isLoggedIn ? (
            <>
              <button
                onClick={() => {
                  // Add logout functionality here
                  console.log('Logging out...');
                }}
                className="text-gray-300 hover:text-white"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className={`${
                  router.pathname === '/login' ? 'text-white' : 'text-gray-300'
                } hover:text-white`}
              >
                Login
              </Link>
              <Link
                href="/register"
                className={`${
                  router.pathname === '/register' ? 'text-white' : 'text-gray-300'
                } hover:text-white`}
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
