import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { haySesion } from '../services/authSession';

export function ProtectedRoute() {
  const location = useLocation();

  if (!haySesion()) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <Outlet />;
}
