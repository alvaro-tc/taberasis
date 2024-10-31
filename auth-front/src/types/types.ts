// auth-front/src/types/types.ts
export interface AuthResponse {
  tokens: {
    access: string;
    refresh: string;
  };
  user: User;
}

export interface AuthResponseError {
  error: string;
}

export interface User {
  _id: string;
  name: string;
  username: string;
}

export interface AccessTokenResponse {
  access_token: string;
  error?: string;
}
