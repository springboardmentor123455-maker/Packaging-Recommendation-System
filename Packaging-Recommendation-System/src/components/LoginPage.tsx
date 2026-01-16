import { useState } from 'react';
import { Leaf, Mail, Lock, User, Building, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/contexts/AuthContext';

interface LoginPageProps {
  onLoginSuccess: () => void;
}

export const LoginPage = ({ onLoginSuccess }: LoginPageProps) => {
  const { login, register, isLoading } = useAuth();
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    company: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (isSignUp) {
      if (!formData.name || !formData.company) {
        setError('Please fill in all fields');
        return;
      }
      const success = await register(formData.email, formData.password, formData.name, formData.company);
      if (success) {
        onLoginSuccess();
      } else {
        setError('Email already registered');
      }
    } else {
      const success = await login(formData.email, formData.password);
      if (success) {
        onLoginSuccess();
      } else {
        setError('Invalid email or password');
      }
    }
  };

  const handleDemoLogin = async () => {
    setFormData({ email: 'demo@ecopackai.com', password: 'demo123', name: '', company: '' });
    const success = await login('demo@ecopackai.com', 'demo123');
    if (success) {
      onLoginSuccess();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-eco-leaf/5 to-eco-sky/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-eco-leaf to-eco-sky flex items-center justify-center">
              <Leaf className="w-6 h-6 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-display font-bold text-foreground mb-2">
            EcoPackAI
          </h1>
          <p className="text-muted-foreground">
            AI-Powered Sustainable Packaging Platform
          </p>
        </div>

        {/* Login Card */}
        <div className="eco-card">
          <div className="flex items-center justify-center gap-4 mb-6">
            <button
              onClick={() => setIsSignUp(false)}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                !isSignUp 
                  ? 'bg-primary text-primary-foreground' 
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setIsSignUp(true)}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                isSignUp 
                  ? 'bg-primary text-primary-foreground' 
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isSignUp && (
              <>
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      id="name"
                      placeholder="Dr. Sarah Chen"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="company">Company</Label>
                  <div className="relative">
                    <Building className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      id="company"
                      placeholder="GreenTech Industries"
                      value={formData.company}
                      onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                      className="pl-10"
                    />
                  </div>
                </div>
              </>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="you@company.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="pl-10"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="pl-10"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">
                {error}
              </div>
            )}

            <Button 
              type="submit" 
              variant="eco" 
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  {isSignUp ? 'Create Account' : 'Sign In'}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </Button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or</span>
            </div>
          </div>

          <Button 
            variant="outline" 
            className="w-full"
            onClick={handleDemoLogin}
            disabled={isLoading}
          >
            <Sparkles className="w-4 h-4 text-eco-leaf" />
            Try Demo Account
          </Button>

          <p className="text-xs text-center text-muted-foreground mt-4">
            Demo credentials: demo@ecopackai.com / demo123
          </p>
        </div>

        {/* Features Preview */}
        <div className="mt-8 grid grid-cols-3 gap-4 text-center">
          <div className="eco-card py-4">
            <div className="text-2xl mb-1">🌱</div>
            <p className="text-xs text-muted-foreground">AI Recommendations</p>
          </div>
          <div className="eco-card py-4">
            <div className="text-2xl mb-1">📊</div>
            <p className="text-xs text-muted-foreground">BI Analytics</p>
          </div>
          <div className="eco-card py-4">
            <div className="text-2xl mb-1">📄</div>
            <p className="text-xs text-muted-foreground">Export Reports</p>
          </div>
        </div>
      </div>
    </div>
  );
};
