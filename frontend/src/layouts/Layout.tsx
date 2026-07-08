import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="md:pl-64">
        <Header />
        <section className="p-4 md:p-6">
          <Outlet />
        </section>
      </main>
    </div>
  );
}
