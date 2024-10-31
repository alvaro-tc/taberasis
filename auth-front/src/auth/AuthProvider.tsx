// auth-front/src/auth/AuthProvider.tsx
import { useContext, createContext, useState, useEffect } from "react";
import type { AuthResponse, User } from "../types/types";
import requestNewAccessToken from "./requestNewAccessToken";
import { API_URL } from "./authConstants";

interface AuthContextType {
  isAuthenticated: boolean;
  getAccessToken: () => string;
  setAccessTokenAndRefreshToken: (accessToken: string, refreshToken: string) => void;
  getRefreshToken: () => string | null;
  saveUser: (userData: AuthResponse) => void;
  getUser: () => User | undefined;
  signout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  getAccessToken: () => "",
  setAccessTokenAndRefreshToken: () => {},
  getRefreshToken: () => "",
  saveUser: () => {},
  getUser: () => undefined,
  signout: () => {},
});

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | undefined>();
  const [accessToken, setAccessToken] = useState<string>("");
  const [refreshToken, setRefreshToken] = useState<string>("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const getAccessToken = () => accessToken;
  const getRefreshToken = () => refreshToken || localStorage.getItem("token") ? JSON.parse(localStorage.getItem("token")!).refreshToken : null;

  const setAccessTokenAndRefreshToken = (newAccessToken: string, newRefreshToken: string) => {
    setAccessToken(newAccessToken);
    setRefreshToken(newRefreshToken);
    localStorage.setItem("token", JSON.stringify({ refreshToken: newRefreshToken }));
    setIsAuthenticated(true);
  };

  const saveUser = (userData: AuthResponse) => {
    setAccessTokenAndRefreshToken(userData.tokens.access, userData.tokens.refresh);
    setUser(userData.user);
  };

  const signout = () => {
    localStorage.removeItem("token");
    setAccessToken("");
    setRefreshToken("");
    setUser(undefined);
    setIsAuthenticated(false);
  };

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem("token");
      if (token) {
        const { refreshToken } = JSON.parse(token);
        const newAccessToken = await requestNewAccessToken(refreshToken);
        if (newAccessToken) {
          const userInfo = await retrieveUserInfo(newAccessToken);
          setUser(userInfo);
          setAccessToken(newAccessToken);
          setIsAuthenticated(true);
        }
      }
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        getAccessToken,
        setAccessTokenAndRefreshToken,
        getRefreshToken,
        saveUser,
        getUser: () => user,
        signout,
      }}
    >
      {isLoading ? <div>Loading...</div> : children}
    </AuthContext.Provider>
  );
}

async function retrieveUserInfo(accessToken: string) {
  try {
    const response = await fetch(`${API_URL}/whoami`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    });
    if (response.ok) {
      const json = await response.json();
      return json.user_details;
    }
  } catch (error) {
    console.error(error);
  }
  return undefined;
}

export const useAuth = () => useContext(AuthContext);