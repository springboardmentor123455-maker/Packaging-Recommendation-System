import { Leaf, Heart } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="py-12 bg-primary text-primary-foreground">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            {/* Logo & Tagline */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-display font-bold text-lg">EcoPackAI</h3>
                <p className="text-xs text-white/70">AI-Powered Sustainable Packaging</p>
              </div>
            </div>

            {/* Mission Statement */}
            <p className="text-sm text-white/80 text-center max-w-md">
              Empowering businesses to make environmentally conscious packaging decisions 
              through intelligent recommendation systems.
            </p>

            {/* Credits */}
            <div className="flex items-center gap-2 text-sm text-white/70">
              <span>Built with</span>
              <Heart className="w-4 h-4 text-red-400 fill-red-400" />
              <span>for the planet</span>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="mt-8 pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-white/60">
              © 2024 EcoPackAI. Sustainable Solutions for Tomorrow.
            </p>
            <div className="flex items-center gap-6 text-xs text-white/60">
              <span>Tasks 1-8 Implementation</span>
              <span>•</span>
              <span>Full-Stack Application</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};
