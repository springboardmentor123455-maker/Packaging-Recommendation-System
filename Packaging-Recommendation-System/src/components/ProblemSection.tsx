import { AlertTriangle, Target, CheckCircle2, ArrowRight } from 'lucide-react';

export const ProblemSection = () => {
  const problems = [
    'Over 380 million tons of plastic produced annually',
    'Only 9% of plastic waste is recycled globally',
    'Packaging accounts for 40% of plastic usage',
    'Traditional materials take 400+ years to decompose',
  ];

  const objectives = [
    'Recommend eco-friendly packaging alternatives',
    'Balance durability with environmental impact',
    'Optimize cost efficiency without compromising quality',
    'Reduce carbon footprint across supply chains',
  ];

  const outcomes = [
    'Up to 78% reduction in CO₂ emissions',
    'Materials with 92%+ recyclability rates',
    'Cost-competitive sustainable options',
    'Data-driven decision support system',
  ];

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              The Packaging Challenge
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Understanding the problem is the first step toward sustainable solutions
            </p>
          </div>

          {/* Three Column Layout */}
          <div className="grid md:grid-cols-3 gap-8">
            {/* Problem Column */}
            <div className="eco-card border-destructive/20">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-destructive/10 flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-destructive" />
                </div>
                <h3 className="text-xl font-semibold text-foreground">The Problem</h3>
              </div>
              <ul className="space-y-4">
                {problems.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-destructive mt-2 shrink-0" />
                    <span className="text-muted-foreground text-sm leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Objectives Column */}
            <div className="eco-card border-eco-sun/20">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-eco-sun/10 flex items-center justify-center">
                  <Target className="w-6 h-6 text-eco-sun" />
                </div>
                <h3 className="text-xl font-semibold text-foreground">Our Objectives</h3>
              </div>
              <ul className="space-y-4">
                {objectives.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <ArrowRight className="w-4 h-4 text-eco-sun mt-0.5 shrink-0" />
                    <span className="text-muted-foreground text-sm leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Outcomes Column */}
            <div className="eco-card border-eco-leaf/20">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-eco-leaf/10 flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6 text-eco-leaf" />
                </div>
                <h3 className="text-xl font-semibold text-foreground">Expected Outcomes</h3>
              </div>
              <ul className="space-y-4">
                {outcomes.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <CheckCircle2 className="w-4 h-4 text-eco-leaf mt-0.5 shrink-0" />
                    <span className="text-muted-foreground text-sm leading-relaxed">{item}</span>
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
