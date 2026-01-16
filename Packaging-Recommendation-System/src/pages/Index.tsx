import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { LoginPage } from '@/components/LoginPage';
import { Header } from '@/components/Header';
import { HeroSection } from '@/components/HeroSection';
import { ProblemSection } from '@/components/ProblemSection';
import { ArchitectureSection } from '@/components/ArchitectureSection';
import { AdvancedRecommendationEngine } from '@/components/AdvancedRecommendationEngine';
import { MaterialComparison } from '@/components/MaterialComparison';
import { AdvancedDashboard } from '@/components/AdvancedDashboard';
import { AboutSection } from '@/components/AboutSection';
import { Footer } from '@/components/Footer';

const Index = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const [activeSection, setActiveSection] = useState('home');

  const handleNavigate = (section: string) => {
    setActiveSection(section);
    
    const elementMap: Record<string, string> = {
      'home': 'hero',
      'problem': 'problem',
      'architecture': 'architecture',
      'recommend': 'recommend',
      'compare': 'compare',
      'dashboard': 'dashboard',
      'about': 'about',
    };

    const elementId = elementMap[section];
    if (elementId) {
      const element = document.getElementById(elementId);
      if (element) {
        const offset = 80;
        const elementPosition = element.getBoundingClientRect().top + window.scrollY;
        window.scrollTo({
          top: elementPosition - offset,
          behavior: 'smooth',
        });
      }
    }
  };

  // Update active section based on scroll
  useEffect(() => {
    const handleScroll = () => {
      const sections = ['hero', 'problem', 'architecture', 'recommend', 'compare', 'dashboard', 'about'];
      const offset = 150;

      for (const section of sections) {
        const element = document.getElementById(section);
        if (element) {
          const rect = element.getBoundingClientRect();
          if (rect.top <= offset && rect.bottom > offset) {
            const sectionMap: Record<string, string> = {
              'hero': 'home',
              'problem': 'problem',
              'architecture': 'architecture',
              'recommend': 'recommend',
              'compare': 'compare',
              'dashboard': 'dashboard',
              'about': 'about',
            };
            setActiveSection(sectionMap[section] || 'home');
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading EcoPackAI...</p>
        </div>
      </div>
    );
  }

  // Show login if not authenticated
  if (!isAuthenticated) {
    return <LoginPage onLoginSuccess={() => {}} />;
  }

  return (
    <div className="min-h-screen bg-background">
      <Header activeSection={activeSection} onNavigate={handleNavigate} />
      
      <main>
        {/* Hero Section */}
        <div id="hero">
          <HeroSection 
            onGetStarted={() => handleNavigate('recommend')}
            onLearnMore={() => handleNavigate('about')}
          />
        </div>
        
        {/* Task 1: Problem & Objectives */}
        <div id="problem">
          <ProblemSection />
        </div>
        
        {/* Task 2: Architecture */}
        <div id="architecture">
          <ArchitectureSection />
        </div>
        
        {/* Task 3-5: Data, Feature Engineering, Advanced Recommendations */}
        <div id="recommend">
          <AdvancedRecommendationEngine />
        </div>
        
        {/* Task 6: Material Comparison Tool */}
        <div id="compare">
          <MaterialComparison />
        </div>
        
        {/* Task 7: BI Dashboard with Export */}
        <div id="dashboard">
          <AdvancedDashboard />
        </div>
        
        {/* Task 8: Documentation & Innovation */}
        <div id="about">
          <AboutSection />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Index;
