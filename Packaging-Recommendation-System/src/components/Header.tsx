import { Leaf, BarChart3, Info, Lightbulb } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface HeaderProps {
  activeSection: string;
  onNavigate: (section: string) => void;
}

export const Header = ({ activeSection, onNavigate }: HeaderProps) => {
  const navItems = [
    { id: 'home', label: 'Home', icon: Leaf },
    { id: 'recommend', label: 'Recommendations', icon: Lightbulb },
    { id: 'dashboard', label: 'Analytics', icon: BarChart3 },
    { id: 'about', label: 'About', icon: Info },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-effect border-b border-border/50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-2 cursor-pointer" 
            onClick={() => onNavigate('home')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-eco-leaf to-primary flex items-center justify-center shadow-eco-md">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-display font-bold text-lg text-foreground">EcoPackAI</h1>
              <p className="text-[10px] text-muted-foreground -mt-1">Sustainable Packaging</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Button
                key={item.id}
                variant={activeSection === item.id ? 'secondary' : 'ghost'}
                size="sm"
                onClick={() => onNavigate(item.id)}
                className="gap-2"
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </Button>
            ))}
          </nav>

          {/* CTA */}
          <Button variant="eco" size="sm" onClick={() => onNavigate('recommend')}>
            Get Started
          </Button>
        </div>
      </div>
    </header>
  );
};
