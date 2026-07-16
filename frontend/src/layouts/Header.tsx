import { useNavigate } from 'react-router-dom';
import { limpiarSesion, obtenerUsuario } from '../services/authSession';

export function Header() {
  const navigate = useNavigate();
  const usuario = obtenerUsuario();
  const iniciales =
    usuario?.nombres
      .split(' ')
      .slice(0, 2)
      .map((nombre) => nombre[0])
      .join('')
      .toUpperCase() || 'RH';

  function cerrarSesion() {
    limpiarSesion();
    navigate('/login', { replace: true });
  }

  return (
    <header className="border-b border-slate-200 bg-white px-4 py-3 md:px-6">
      <div className="flex items-center justify-between gap-4">
        <p className="text-sm font-medium text-slate-500">
          Sistema de Gestion de Recursos Humanos
        </p>
        <div className="flex items-center gap-3">
          <div className="hidden text-right sm:block">
            <p className="text-sm font-medium text-slate-700">
              {usuario?.nombres}
            </p>
            <p className="text-xs text-slate-500">{usuario?.rol}</p>
          </div>
          <div className="grid h-9 w-9 place-items-center rounded-full bg-blue-600 text-sm font-bold text-white">
            {iniciales}
          </div>
          <button
            className="text-sm font-medium text-slate-500 hover:text-slate-800"
            type="button"
            onClick={cerrarSesion}
          >
            Salir
          </button>
        </div>
      </div>
    </header>
  );
}
