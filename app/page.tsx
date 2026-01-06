import type { Metadata } from 'next';
import Dashboard from './components/dashboard';
import './globals.css';

export const metadata: Metadata = {
  title: 'Exam Result Processing System',
  description: 'Automated Exam Result Processing & Performance Analytics System',
  icons: {
    icon: '📊',
  },
};

export default function Home() {
  return (
    <main>
      <Dashboard />
    </main>
  );
}
