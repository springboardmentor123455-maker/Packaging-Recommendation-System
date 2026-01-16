import { useState } from 'react';
import { Sparkles, Leaf, DollarSign, Wind, Award, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { 
  productCategories, 
  getRecommendations, 
  type ProductCategory,
  type MaterialRecommendation 
} from '@/data/packagingMaterials';

interface RecommendationEngineProps {
  onRecommendationsGenerated?: (recommendations: MaterialRecommendation[]) => void;
}

export const RecommendationEngine = ({ onRecommendationsGenerated }: RecommendationEngineProps) => {
  const [selectedCategory, setSelectedCategory] = useState<ProductCategory | null>(null);
  const [recommendations, setRecommendations] = useState<MaterialRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleGetRecommendations = () => {
    if (!selectedCategory) return;
    
    setIsLoading(true);
    
    // Simulate processing delay for UX
    setTimeout(() => {
      const results = getRecommendations(selectedCategory);
      setRecommendations(results);
      onRecommendationsGenerated?.(results);
      setIsLoading(false);
    }, 800);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-eco-leaf';
    if (score >= 60) return 'text-eco-sun';
    return 'text-eco-earth';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-eco-leaf/10';
    if (score >= 60) return 'bg-eco-sun/10';
    return 'bg-eco-earth/10';
  };

  return (
    <section id="recommend" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 eco-badge mb-4">
              <Sparkles className="w-4 h-4" />
              <span>AI Recommendation Engine</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              Get Personalized Recommendations
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Select your product category and our algorithm will analyze material properties 
              to recommend the optimal sustainable packaging solutions
            </p>
          </div>

          {/* Category Selection */}
          <div className="mb-10">
            <h3 className="text-sm font-medium text-muted-foreground mb-4 text-center">
              Step 1: Select Product Category
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {productCategories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`eco-card text-left transition-all duration-300 ${
                    selectedCategory === category.id 
                      ? 'ring-2 ring-primary border-primary shadow-eco-glow' 
                      : 'hover:border-primary/50'
                  }`}
                >
                  <div className="text-3xl mb-3">{category.icon}</div>
                  <h4 className="font-semibold text-foreground mb-1">{category.label}</h4>
                  <p className="text-xs text-muted-foreground line-clamp-2">{category.description}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Get Recommendations Button */}
          <div className="text-center mb-12">
            <Button 
              variant="eco" 
              size="xl"
              onClick={handleGetRecommendations}
              disabled={!selectedCategory || isLoading}
              className="min-w-[250px]"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing Materials...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Get Recommendations
                </>
              )}
            </Button>
          </div>

          {/* Results */}
          {recommendations.length > 0 && (
            <div className="animate-fade-in">
              <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <Award className="w-5 h-5 text-eco-leaf" />
                Top Recommendations for {selectedCategory}
              </h3>
              
              <div className="grid gap-4">
                {recommendations.slice(0, 5).map((rec, index) => (
                  <div 
                    key={rec.material.id}
                    className="eco-card flex flex-col sm:flex-row sm:items-center gap-4 animate-slide-in-right"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    {/* Rank Badge */}
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${
                      rec.rank === 1 ? 'bg-eco-leaf text-white' : 'bg-muted text-muted-foreground'
                    }`}>
                      <span className="text-lg font-bold">#{rec.rank}</span>
                    </div>

                    {/* Material Info */}
                    <div className="flex-1 min-w-0">
                      <h4 className="font-semibold text-foreground mb-1">{rec.material.name}</h4>
                      <p className="text-sm text-muted-foreground line-clamp-2">{rec.material.description}</p>
                    </div>

                    {/* Metrics */}
                    <div className="flex flex-wrap sm:flex-nowrap items-center gap-4">
                      {/* Eco Score */}
                      <div className={`px-4 py-2 rounded-lg ${getScoreBg(rec.ecoScore)}`}>
                        <div className="flex items-center gap-1.5">
                          <Leaf className={`w-4 h-4 ${getScoreColor(rec.ecoScore)}`} />
                          <span className={`text-lg font-bold ${getScoreColor(rec.ecoScore)}`}>
                            {rec.ecoScore}
                          </span>
                        </div>
                        <div className="text-xs text-muted-foreground">Eco Score</div>
                      </div>

                      {/* CO2 Impact */}
                      <div className="px-4 py-2 rounded-lg bg-eco-sky/10">
                        <div className="flex items-center gap-1.5">
                          <Wind className="w-4 h-4 text-eco-sky" />
                          <span className="text-lg font-bold text-eco-sky">
                            {rec.material.co2Impact > 0 ? '+' : ''}{rec.material.co2Impact}
                          </span>
                        </div>
                        <div className="text-xs text-muted-foreground">kg CO₂</div>
                      </div>

                      {/* Cost */}
                      <div className="px-4 py-2 rounded-lg bg-eco-earth/10">
                        <div className="flex items-center gap-1.5">
                          <DollarSign className="w-4 h-4 text-eco-earth" />
                          <span className="text-lg font-bold text-eco-earth">
                            ${rec.material.costPerUnit.toFixed(2)}
                          </span>
                        </div>
                        <div className="text-xs text-muted-foreground">per unit</div>
                      </div>

                      <ChevronRight className="w-5 h-5 text-muted-foreground hidden sm:block" />
                    </div>
                  </div>
                ))}
              </div>

              {/* Scoring explanation */}
              <div className="mt-8 p-6 rounded-xl bg-muted/50 border border-border">
                <h4 className="font-semibold text-foreground mb-3">Scoring Methodology</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  The Eco Score is computed using a weighted multi-criteria algorithm that evaluates: 
                  <strong> Biodegradability (20%)</strong>, 
                  <strong> Recyclability (15%)</strong>, 
                  <strong> CO₂ Impact (25%)</strong>, 
                  <strong> Cost Efficiency (15%)</strong>, 
                  <strong> Durability (10%)</strong>, and 
                  <strong> Category Strength Match (15%)</strong>. 
                  All attributes are normalized to a 0-1 scale before applying weights.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};
