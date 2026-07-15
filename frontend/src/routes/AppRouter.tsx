import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Layout } from '../layouts/Layout';
import { Asistencia } from '../pages/Asistencia';
import { BonosDescuentos } from '../pages/BonosDescuentos';
import { Boletas } from '../pages/Boletas';
import { Dashboard } from '../pages/Dashboard';
import { Empleados } from '../pages/Empleados';
import { Login } from '../pages/Login';
import { NotFound } from '../pages/NotFound';
import { Reportes } from '../pages/Reportes';
import { Sueldos } from '../pages/Sueldos';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/empleados" element={<Empleados />} />
          <Route path="/asistencia" element={<Asistencia />} />
          <Route path="/bonos-descuentos" element={<BonosDescuentos />} />
          <Route path="/sueldos" element={<Sueldos />} />
          <Route path="/boletas" element={<Boletas />} />
          <Route path="/reportes" element={<Reportes />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
