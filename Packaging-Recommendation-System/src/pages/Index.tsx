import { useState } from 'react';
import Header from '@/components/Header';
import RecommendationPanel from '@/components/RecommendationPanel';
import Dashboard from '@/components/Dashboard';

const Index = () => {
  const [activeTab, setActiveTab] = useState<'recommend' | 'dashboard'>('recommend');

  return (
    <div className="min-h-screen bg-background">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="container py-6">
        {activeTab === 'recommend' ? (
          <RecommendationPanel />
        ) : (
          <Dashboard />
        )}
      </main>
      
      <footer className="border-t py-6">
        <div className="container text-center text-sm text-muted-foreground">
          <p>EcoPackAI — AI-Powered Sustainable Packaging Recommendation System</p>
          <p className="mt-1">Helping businesses make eco-friendly packaging decisions</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
