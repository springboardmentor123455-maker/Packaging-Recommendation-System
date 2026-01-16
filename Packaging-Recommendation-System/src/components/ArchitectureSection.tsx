import { Layers, Database, Cpu, BarChart3, Globe, Shield } from 'lucide-react';

export const ArchitectureSection = () => {
  const layers = [
    {
      icon: Globe,
      title: 'Presentation Layer',
      description: 'Responsive React-based interface with interactive visualizations',
      color: 'eco-sky',
    },
    {
      icon: Cpu,
      title: 'Logic Layer',
      description: 'Weighted scoring algorithms and recommendation engine',
      color: 'eco-leaf',
    },
    {
      icon: Database,
      title: 'Data Layer',
      description: 'Structured material database with normalized attributes',
      color: 'eco-earth',
    },
    {
      icon: BarChart3,
      title: 'Analytics Layer',
      description: 'Real-time metrics computation and trend analysis',
      color: 'eco-sun',
    },
  ];

  const requirements = {
    functional: [
      'Material recommendation by product category',
      'Multi-criteria scoring algorithm',
      'Interactive comparison dashboard',
      'Real-time analytics visualization',
    ],
    nonFunctional: [
      'Response time < 200ms',
      'Mobile-responsive design',
      'Extensible architecture',
      'Cloud deployment ready',
    ],
  };

  return (
    <section className="py-20 bg-secondary/30">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 eco-badge mb-4">
              <Layers className="w-4 h-4" />
              <span>System Architecture</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              Modular & Scalable Design
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              A four-layer architecture ensuring separation of concerns and maintainability
            </p>
          </div>

          {/* Architecture Diagram */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-16">
            {layers.map((layer, index) => (
              <div 
                key={index} 
                className="eco-card text-center relative overflow-hidden group"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className={`absolute inset-0 bg-${layer.color}/5 opacity-0 group-hover:opacity-100 transition-opacity`} />
                <div className={`w-14 h-14 rounded-2xl bg-${layer.color}/10 flex items-center justify-center mx-auto mb-4 relative z-10`}>
                  <layer.icon className={`w-7 h-7 text-${layer.color}`} />
                </div>
                <h3 className="font-semibold text-foreground mb-2 relative z-10">{layer.title}</h3>
                <p className="text-sm text-muted-foreground relative z-10">{layer.description}</p>
                
                {/* Connection line */}
                {index < layers.length - 1 && (
                  <div className="hidden lg:block absolute right-0 top-1/2 w-4 h-0.5 bg-border -translate-y-1/2 translate-x-full" />
                )}
              </div>
            ))}
          </div>

          {/* Requirements */}
          <div className="grid md:grid-cols-2 gap-8">
            <div className="eco-card">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Cpu className="w-5 h-5 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Functional Requirements</h3>
              </div>
              <ul className="space-y-3">
                {requirements.functional.map((req, index) => (
                  <li key={index} className="flex items-center gap-3 text-sm text-muted-foreground">
                    <div className="w-2 h-2 rounded-full bg-primary shrink-0" />
                    {req}
                  </li>
                ))}
              </ul>
            </div>

            <div className="eco-card">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-eco-leaf/10 flex items-center justify-center">
                  <Shield className="w-5 h-5 text-eco-leaf" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Non-Functional Requirements</h3>
              </div>
              <ul className="space-y-3">
                {requirements.nonFunctional.map((req, index) => (
                  <li key={index} className="flex items-center gap-3 text-sm text-muted-foreground">
                    <div className="w-2 h-2 rounded-full bg-eco-leaf shrink-0" />
                    {req}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
