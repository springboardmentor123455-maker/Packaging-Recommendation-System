import { Leaf, BarChart3, Package } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface HeaderProps {
  activeTab: 'recommend' | 'dashboard';
  onTabChange: (tab: 'recommend' | 'dashboard') => void;
}

const Header = ({ activeTab, onTabChange }: HeaderProps) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Leaf className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">EcoPackAI</h1>
            <p className="text-xs text-muted-foreground">Sustainable Packaging Intelligence</p>
          </div>
        </div>
        
        <nav className="flex items-center gap-1">
          <Button
            variant={activeTab === 'recommend' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => onTabChange('recommend')}
            className="gap-2"
          >
            <Package className="h-4 w-4" />
            <span className="hidden sm:inline">Recommendations</span>
          </Button>
          <Button
            variant={activeTab === 'dashboard' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => onTabChange('dashboard')}
            className="gap-2"
          >
            <BarChart3 className="h-4 w-4" />
            <span className="hidden sm:inline">BI Dashboard</span>
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
