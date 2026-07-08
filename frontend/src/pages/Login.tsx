import type { FormEvent } from 'react';
import { useState } from 'react';
import { Button } from '../components/Button';
import { Input } from '../components/Input';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-50 px-4">
      <section className="w-full max-w-sm rounded-md border border-slate-200 bg-white p-6">
        <div className="mb-6">
          <p className="text-sm font-medium text-blue-700">Staffy</p>
          <h1 className="mt-1 text-2xl font-semibold text-slate-900">Iniciar sesion</h1>
          <p className="mt-2 text-sm text-slate-500">Acceso para el equipo de recursos humanos.</p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Correo</span>
            <Input
              className="w-full"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="admin@staffy.com"
            />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Contrasena</span>
            <Input
              className="w-full"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="********"
            />
          </label>

          <Button className="w-full" type="submit">
            Ingresar
          </Button>
        </form>
      </section>
    </main>
  );
}
