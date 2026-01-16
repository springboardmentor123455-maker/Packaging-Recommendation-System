import { ArrowRight, Leaf, Recycle, TrendingDown } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface HeroSectionProps {
  onGetStarted: () => void;
  onLearnMore: () => void;
}

export const HeroSection = ({ onGetStarted, onLearnMore }: HeroSectionProps) => {
  const stats = [
    { icon: Recycle, value: '92%', label: 'Avg Recyclability' },
    { icon: TrendingDown, value: '78%', label: 'CO₂ Reduction' },
    { icon: Leaf, value: '12+', label: 'Eco Materials' },
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-eco-leaf/5" />
      
      {/* Floating decorative elements */}
      <div className="absolute top-20 left-10 w-64 h-64 bg-eco-leaf/10 rounded-full blur-3xl animate-pulse-eco" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse-eco" style={{ animationDelay: '1.5s' }} />
      
      {/* Leaf decorations */}
      <div className="absolute top-1/4 right-1/4 opacity-20 animate-float">
        <Leaf className="w-16 h-16 text-eco-leaf" />
      </div>
      <div className="absolute bottom-1/3 left-1/5 opacity-15 animate-float" style={{ animationDelay: '2s' }}>
        <Leaf className="w-12 h-12 text-primary" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 eco-badge mb-6 animate-fade-in">
            <Leaf className="w-4 h-4" />
            <span>AI-Powered Sustainable Solutions</span>
          </div>

          {/* Main headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-display font-bold text-foreground mb-6 leading-tight animate-fade-in" style={{ animationDelay: '0.1s' }}>
            Revolutionize Packaging with{' '}
            <span className="eco-gradient-text">Intelligent Eco-Design</span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed animate-fade-in" style={{ animationDelay: '0.2s' }}>
            EcoPackAI leverages advanced algorithms to recommend optimal sustainable packaging materials, 
            balancing environmental impact, durability, and cost efficiency for your products.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16 animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <Button variant="eco" size="xl" onClick={onGetStarted} className="group">
              Get Recommendations
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="outline" size="xl" onClick={onLearnMore}>
              Learn More
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-6 max-w-xl mx-auto animate-fade-in" style={{ animationDelay: '0.4s' }}>
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary/10 mb-3">
                  <stat.icon className="w-6 h-6 text-primary" />
                </div>
                <div className="text-2xl sm:text-3xl font-bold text-foreground">{stat.value}</div>
                <div className="text-xs sm:text-sm text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom wave */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full">
          <path 
            d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" 
            fill="hsl(var(--background))"
          />
        </svg>
      </div>
    </section>
  );
};
