import { Lightbulb, Rocket, BookOpen, Cloud, Code, Database, Zap, Globe } from 'lucide-react';

export const AboutSection = () => {
  const innovations = [
    {
      icon: Zap,
      title: 'Weighted Scoring Algorithm',
      description: 'Multi-criteria decision analysis with configurable weights for personalized recommendations',
    },
    {
      icon: Database,
      title: 'Structured Eco-Database',
      description: 'Comprehensive material profiles with normalized attributes and derived metrics',
    },
    {
      icon: Globe,
      title: 'Category-Aware Matching',
      description: 'Intelligent strength and durability requirements based on product category needs',
    },
    {
      icon: Code,
      title: 'Real-Time Analytics',
      description: 'Dynamic computation of eco-scores, CO₂ impact indices, and cost efficiency metrics',
    },
  ];

  const futureScope = [
    'Machine learning model training on real-world packaging outcomes',
    'Supply chain integration for real-time availability data',
    'Carbon credit calculation and reporting module',
    'Multi-language support for global enterprise deployment',
    'API endpoints for third-party e-commerce integration',
  ];

  return (
    <section id="about" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 eco-badge mb-4">
              <BookOpen className="w-4 h-4" />
              <span>Documentation</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              Innovation & Future Scope
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Technical achievements, deployment readiness, and roadmap for continued development
            </p>
          </div>

          {/* Innovation Highlights */}
          <div className="mb-16">
            <h3 className="text-xl font-semibold text-foreground mb-8 flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-eco-sun" />
              Key Innovations
            </h3>
            <div className="grid sm:grid-cols-2 gap-6">
              {innovations.map((item, index) => (
                <div key={index} className="eco-card group">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0 group-hover:bg-primary/20 transition-colors">
                      <item.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-foreground mb-2">{item.title}</h4>
                      <p className="text-sm text-muted-foreground leading-relaxed">{item.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Deployment & Technical Stack */}
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            <div className="eco-card">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-eco-sky/10 flex items-center justify-center">
                  <Cloud className="w-6 h-6 text-eco-sky" />
                </div>
                <h3 className="text-xl font-semibold text-foreground">Deployment Readiness</h3>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-eco-leaf mt-2 shrink-0" />
                  <span className="text-sm text-muted-foreground">
                    <strong className="text-foreground">Local Development:</strong> Fully functional standalone application
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-eco-leaf mt-2 shrink-0" />
                  <span className="text-sm text-muted-foreground">
                    <strong className="text-foreground">Cloud Ready:</strong> Compatible with major cloud platforms (AWS, Azure, GCP)
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-eco-leaf mt-2 shrink-0" />
                  <span className="text-sm text-muted-foreground">
                    <strong className="text-foreground">Container Support:</strong> Docker-ready architecture for seamless deployment
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-eco-leaf mt-2 shrink-0" />
                  <span className="text-sm text-muted-foreground">
                    <strong className="text-foreground">CDN Optimized:</strong> Static assets optimized for global distribution
                  </span>
                </li>
              </ul>
            </div>

            <div className="eco-card">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-eco-earth/10 flex items-center justify-center">
                  <Code className="w-6 h-6 text-eco-earth" />
                </div>
                <h3 className="text-xl font-semibold text-foreground">Technical Stack</h3>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Frontend', value: 'React 18 + TypeScript' },
                  { label: 'Styling', value: 'Tailwind CSS' },
                  { label: 'Charts', value: 'Recharts Library' },
                  { label: 'Build Tool', value: 'Vite' },
                  { label: 'State', value: 'React Hooks' },
                  { label: 'Architecture', value: 'Component-Based' },
                ].map((tech, index) => (
                  <div key={index} className="p-3 rounded-lg bg-muted/50">
                    <div className="text-xs text-muted-foreground">{tech.label}</div>
                    <div className="text-sm font-medium text-foreground">{tech.value}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Future Scope */}
          <div className="eco-card border-primary/20">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <Rocket className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-foreground">Future Development Roadmap</h3>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              {futureScope.map((item, index) => (
                <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors">
                  <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center shrink-0 mt-0.5">
                    <span className="text-xs font-semibold text-primary">{index + 1}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
