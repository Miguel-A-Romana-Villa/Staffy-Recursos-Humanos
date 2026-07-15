import { NavLink } from 'react-router-dom';
import { BarChart3, CalendarCheck, FileText, Gift, LayoutDashboard, Users, WalletCards } from 'lucide-react';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/empleados', label: 'Empleados', icon: Users },
  { to: '/asistencia', label: 'Asistencia', icon: CalendarCheck },
  { to: '/bonos-descuentos', label: 'Bonos y descuentos', icon: Gift },
  { to: '/sueldos', label: 'Sueldos', icon: WalletCards },
  { to: '/boletas', label: 'Boletas', icon: FileText },
  { to: '/reportes', label: 'Reportes', icon: BarChart3 },
];

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 hidden w-64 bg-[#0d1426] p-4 text-white md:block">
      <div className="mb-7">
        <h1 className="text-xl font-bold">Staffy</h1>
        <p className="text-xs text-[#b2c2db]">Gestión RR.HH.</p>
      </div>
      <nav className="space-y-1">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium ${
                  isActive ? 'bg-[#17213b] text-white' : 'text-[#b2c2db] hover:bg-[#17213b] hover:text-white'
                }`
              }
            >
              <Icon size={18} strokeWidth={2} />
              {link.label}
            </NavLink>
          );
        })}
      </nav>
      <div className="absolute bottom-4 left-4 right-4 rounded-md bg-[#17213b] p-3">
        <p className="text-sm font-semibold">Usuario</p>
        <p className="text-xs text-[#b2c2db]">Encargado RR.HH.</p>
      </div>
    </aside>
  );
}
