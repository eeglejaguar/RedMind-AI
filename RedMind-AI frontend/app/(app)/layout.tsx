import Sidebar from '@/components/Sidebar';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex bg-void text-text-primary min-h-screen">
      <Sidebar />
      <main className="flex-1 min-h-screen grid-bg">
        <div className="max-w-6xl mx-auto p-8">{children}</div>
      </main>
    </div>
  );
}