import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface User {
  id: string;
  email: string;
  name: string;
  company: string;
  role: 'admin' | 'analyst' | 'viewer';
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (email: string, password: string, name: string, company: string) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Simulated user database
const mockUsers: Record<string, User & { password: string }> = {
  'demo@ecopackai.com': {
    id: 'user-001',
    email: 'demo@ecopackai.com',
    password: 'demo123',
    name: 'Dr. Sarah Chen',
    company: 'GreenTech Industries',
    role: 'admin',
  },
  'analyst@ecopackai.com': {
    id: 'user-002',
    email: 'analyst@ecopackai.com',
    password: 'analyst123',
    name: 'Michael Torres',
    company: 'EcoSolutions Corp',
    role: 'analyst',
  },
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored session
    const storedUser = localStorage.getItem('ecopackai_user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const mockUser = mockUsers[email];
    if (mockUser && mockUser.password === password) {
      const { password: _, ...userWithoutPassword } = mockUser;
      setUser(userWithoutPassword);
      localStorage.setItem('ecopackai_user', JSON.stringify(userWithoutPassword));
      setIsLoading(false);
      return true;
    }
    
    setIsLoading(false);
    return false;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('ecopackai_user');
  };

  const register = async (email: string, password: string, name: string, company: string): Promise<boolean> => {
    setIsLoading(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    if (mockUsers[email]) {
      setIsLoading(false);
      return false; // User already exists
    }

    const newUser: User = {
      id: `user-${Date.now()}`,
      email,
      name,
      company,
      role: 'viewer',
    };
    
    setUser(newUser);
    localStorage.setItem('ecopackai_user', JSON.stringify(newUser));
    setIsLoading(false);
    return true;
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated: !!user, 
      isLoading, 
      login, 
      logout, 
      register 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
