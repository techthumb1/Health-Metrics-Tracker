// _app.tsx
import { AppProps } from 'next/app';
import '../styles/globals.css'; // or your tailwind imports
import Navbar from '../../components/Navbar';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Navbar />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
