export type LoginRequest = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  usuario: UsuarioSesion;
};

export type UsuarioSesion = {
  id: number;
  nombres: string;
  email: string;
  rol: string;
};
