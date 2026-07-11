"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { authAPI } from "@/lib/api";
import { User } from "@/types";

/**
 * 认证上下文类型
 */
interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (
    username: string,
    email: string,
    password: string
  ) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * 从 localStorage 读取 token
 */
function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

/**
 * 认证上下文提供组件
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // 初始化：从 localStorage 恢复登录状态
  useEffect(() => {
    let cancelled = false;
    const storedToken = getStoredToken();

    if (storedToken) {
      setToken(storedToken);
      authAPI
        .getProfile()
        .then((response) => {
          if (!cancelled) setUser(response.data);
        })
        .catch(() => {
          if (!cancelled) {
            localStorage.removeItem("token");
            setToken(null);
          }
        })
        .finally(() => {
          if (!cancelled) setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }

    return () => {
      cancelled = true;
    };
  }, []);

  /**
   * 用户登录
   */
  const login = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password });
    const { access_token, user: userData } = response.data;

    localStorage.setItem("token", access_token);
    setToken(access_token);
    setUser(userData);
    router.push("/dashboard");
  };

  /**
   * 用户注册
   */
  const register = async (
    username: string,
    email: string,
    password: string
  ) => {
    const response = await authAPI.register({ username, email, password });
    const { access_token, user: userData } = response.data;

    localStorage.setItem("token", access_token);
    setToken(access_token);
    setUser(userData);
    router.push("/dashboard");
  };

  /**
   * 用户登出
   */
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{ user, token, isLoading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

/**
 * 使用认证上下文的 Hook
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth 必须在 AuthProvider 内部使用");
  }
  return context;
}
