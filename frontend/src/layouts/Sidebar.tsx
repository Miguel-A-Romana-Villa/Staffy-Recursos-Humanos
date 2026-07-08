import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/empleados', label: 'Empleados' },
  { to: '/asistencia', label: 'Asistencia' },
  { to: '/boletas', label: 'Boletas' },
  { to: '/reportes', label: 'Reportes' },
];

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white p-4 md:block">
      <h1 className="mb-6 text-xl font-semibold">Staffy</h1>
      <nav className="space-y-1">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `block rounded-md px-3 py-2 text-sm ${
                isActive ? 'bg-blue-50 text-blue-700' : 'text-slate-700'
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
