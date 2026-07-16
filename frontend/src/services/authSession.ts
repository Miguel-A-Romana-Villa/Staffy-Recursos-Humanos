import type { LoginResponse, UsuarioSesion } from '../types/auth.types';

const tokenKey = 'staffy_access_token';
const usuarioKey = 'staffy_usuario';

export function guardarSesion(sesion: LoginResponse) {
  localStorage.setItem(tokenKey, sesion.access_token);
  localStorage.setItem(usuarioKey, JSON.stringify(sesion.usuario));
}

export function obtenerToken() {
  return localStorage.getItem(tokenKey);
}

export function obtenerUsuario(): UsuarioSesion | null {
  const contenido = localStorage.getItem(usuarioKey);
  if (!contenido) return null;

  try {
    return JSON.parse(contenido) as UsuarioSesion;
  } catch {
    limpiarSesion();
    return null;
  }
}

export function limpiarSesion() {
  localStorage.removeItem(tokenKey);
  localStorage.removeItem(usuarioKey);
}

export function haySesion() {
  return Boolean(obtenerToken() && obtenerUsuario());
}
