import type { FormEvent } from 'react';
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { authApi } from '../services/authApi';
import { guardarSesion } from '../services/authSession';

export function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCargando(true);
    setError('');

    try {
      const response = await authApi.login({ email, password });
      guardarSesion(response.data);
      const destino =
        (location.state as { from?: string } | null)?.from ?? '/dashboard';
      navigate(destino, { replace: true });
    } catch {
      setError('Correo o contrasena incorrectos.');
    } finally {
      setCargando(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-50 px-4">
      <section className="w-full max-w-sm rounded-md border border-slate-200 bg-white p-6">
        <div className="mb-6">
          <p className="text-sm font-medium text-blue-700">Staffy</p>
          <h1 className="mt-1 text-2xl font-semibold text-slate-900">
            Iniciar sesion
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Acceso para el equipo de recursos humanos.
          </p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">
              Correo
            </span>
            <Input
              className="w-full"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="admin@staffy.com"
              autoComplete="email"
              required
            />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">
              Contrasena
            </span>
            <Input
              className="w-full"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="********"
              autoComplete="current-password"
              required
            />
          </label>

          {error && (
            <p className="text-sm text-red-700" role="alert">
              {error}
            </p>
          )}

          <Button
            className="w-full disabled:cursor-not-allowed disabled:bg-blue-300"
            disabled={cargando}
            type="submit"
          >
            {cargando ? 'Ingresando...' : 'Ingresar'}
          </Button>
        </form>
      </section>
    </main>
  );
}
