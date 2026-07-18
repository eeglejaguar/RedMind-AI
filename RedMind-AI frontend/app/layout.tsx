import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'RedMind-AI // VAPT Console',
  description: 'Aggressive automated vulnerability assessment console',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-void text-text-primary min-h-screen">
        {children}
      </body>
    </html>
  );
}
