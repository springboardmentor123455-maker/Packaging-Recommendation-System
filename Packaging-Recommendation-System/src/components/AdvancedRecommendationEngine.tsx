import { useState } from 'react';
import { Sparkles, Leaf, DollarSign, Wind, Award, ChevronRight, Settings2, Shield, Scale, Recycle, Info, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { 
  productCategories, 
  packagingMaterials,
  type ProductCategory,
  type PackagingMaterial 
} from '@/data/packagingMaterials';

interface RecommendationParams {
  category: ProductCategory | null;
  weightRequirement: number;
  fragilityLevel: number;
  costSensitivity: number;
  sustainabilityPriority: number;
}

interface AdvancedRecommendation {
  material: PackagingMaterial;
  ecoScore: number;
  suitabilityScore: number;
  costScore: number;
  durabilityScore: number;
  explanation: string[];
  rank: number;
}

interface AdvancedRecommendationEngineProps {
  onRecommendationsGenerated?: (recommendations: AdvancedRecommendation[]) => void;
}

export const AdvancedRecommendationEngine = ({ onRecommendationsGenerated }: AdvancedRecommendationEngineProps) => {
  const [params, setParams] = useState<RecommendationParams>({
    category: null,
    weightRequirement: 10,
    fragilityLevel: 5,
    costSensitivity: 5,
    sustainabilityPriority: 7,
  });
  const [recommendations, setRecommendations] = useState<AdvancedRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showParameters, setShowParameters] = useState(true);

  // Advanced AI-inspired scoring algorithm
  const calculateAdvancedScore = (material: PackagingMaterial): AdvancedRecommendation => {
    const explanations: string[] = [];
    
    // Normalize user inputs to 0-1 scale
    const weightFactor = params.weightRequirement / 50;
    const fragilityFactor = params.fragilityLevel / 10;
    const costFactor = params.costSensitivity / 10;
    const sustainFactor = params.sustainabilityPriority / 10;

    // 1. Suitability Score - Based on category match and weight capacity
    let suitabilityScore = 0;
    if (params.category && material.suitableCategories.includes(params.category)) {
      suitabilityScore += 40;
      explanations.push(`✓ Optimized for ${params.category} products`);
    }
    
    if (material.weightCapacity >= params.weightRequirement) {
      suitabilityScore += 30;
      explanations.push(`✓ Supports weight requirement (${material.weightCapacity}kg capacity)`);
    } else {
      suitabilityScore += (material.weightCapacity / params.weightRequirement) * 20;
      explanations.push(`⚠ Limited weight capacity (${material.weightCapacity}kg vs ${params.weightRequirement}kg needed)`);
    }

    // Fragility matching - higher fragility needs higher strength/durability
    const fragilityMatch = material.strength / 10 >= fragilityFactor;
    if (fragilityMatch) {
      suitabilityScore += 30;
      explanations.push(`✓ Adequate protection for fragility level ${params.fragilityLevel}/10`);
    } else {
      suitabilityScore += ((material.strength / 10) / fragilityFactor) * 20;
    }

    // 2. Eco Score - Sustainability metrics
    let ecoScore = 0;
    const bioScore = material.biodegradability * 10;
    const recycleScore = material.recyclability;
    const co2Score = Math.max(0, 100 - (material.co2Impact + 0.5) * 50);
    
    ecoScore = (bioScore * 0.35 + recycleScore * 0.35 + co2Score * 0.30) * sustainFactor;
    
    if (material.biodegradability >= 9) {
      explanations.push(`✓ Excellent biodegradability (${material.biodegradability}/10)`);
    }
    if (material.co2Impact <= 0) {
      explanations.push(`✓ Carbon-negative production process`);
    } else if (material.co2Impact < 0.5) {
      explanations.push(`✓ Low carbon footprint (${material.co2Impact} kg CO₂)`);
    }

    // 3. Cost Score - Cost efficiency based on user sensitivity
    const maxCost = 1.50;
    const costEfficiency = (maxCost - material.costPerUnit) / maxCost * 100;
    const costScore = costEfficiency * costFactor;
    
    if (material.costPerUnit <= 0.50) {
      explanations.push(`✓ Cost-effective option ($${material.costPerUnit.toFixed(2)}/unit)`);
    }

    // 4. Durability Score
    const durabilityScore = material.durability * 10;
    if (material.durability >= 7) {
      explanations.push(`✓ High durability rating (${material.durability}/10)`);
    }

    // Final weighted calculation based on user priorities
    const totalScore = Math.round(
      suitabilityScore * 0.30 +
      ecoScore * 0.35 +
      costScore * 0.20 +
      durabilityScore * 0.15
    );

    return {
      material,
      ecoScore: Math.round(ecoScore),
      suitabilityScore: Math.round(suitabilityScore),
      costScore: Math.round(costScore),
      durabilityScore: Math.round(durabilityScore),
      explanation: explanations,
      rank: 0,
    };
  };

  const handleGetRecommendations = () => {
    if (!params.category) return;
    
    setIsLoading(true);
    
    setTimeout(() => {
      const results = packagingMaterials
        .filter(m => m.suitableCategories.includes(params.category!))
        .map(material => calculateAdvancedScore(material))
        .sort((a, b) => {
          // Complex sorting: prioritize based on user preferences
          const aTotal = a.suitabilityScore + a.ecoScore * (params.sustainabilityPriority / 10) + 
                        a.costScore * (params.costSensitivity / 10);
          const bTotal = b.suitabilityScore + b.ecoScore * (params.sustainabilityPriority / 10) + 
                        b.costScore * (params.costSensitivity / 10);
          return bTotal - aTotal;
        })
        .map((rec, index) => ({ ...rec, rank: index + 1 }));
      
      setRecommendations(results);
      onRecommendationsGenerated?.(results);
      setShowParameters(false);
      setIsLoading(false);
    }, 1000);
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-eco-leaf';
    if (score >= 40) return 'text-eco-sun';
    return 'text-eco-earth';
  };

  const getScoreBg = (score: number) => {
    if (score >= 70) return 'bg-eco-leaf/10';
    if (score >= 40) return 'bg-eco-sun/10';
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
              <span>Task 5: AI Recommendation Engine</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              Multi-Parameter AI Recommendations
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Configure your product requirements and our weighted scoring algorithm will analyze 
              12+ eco-materials to find the optimal sustainable packaging solution
            </p>
          </div>

          {/* Configuration Panel */}
          <div className={`eco-card mb-8 transition-all duration-500 ${showParameters ? 'opacity-100' : 'opacity-90'}`}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                <Settings2 className="w-5 h-5 text-primary" />
                Product Configuration
              </h3>
              {recommendations.length > 0 && (
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => setShowParameters(!showParameters)}
                >
                  {showParameters ? 'Hide Parameters' : 'Adjust Parameters'}
                </Button>
              )}
            </div>

            {showParameters && (
              <div className="space-y-8">
                {/* Category Selection */}
                <div>
                  <label className="text-sm font-medium text-muted-foreground mb-3 block">
                    Step 1: Select Product Category
                  </label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {productCategories.map((category) => (
                      <button
                        key={category.id}
                        onClick={() => setParams({ ...params, category: category.id })}
                        className={`p-4 rounded-xl border text-left transition-all duration-300 ${
                          params.category === category.id 
                            ? 'ring-2 ring-primary border-primary shadow-eco-glow bg-primary/5' 
                            : 'border-border hover:border-primary/50 bg-card'
                        }`}
                      >
                        <div className="text-3xl mb-2">{category.icon}</div>
                        <h4 className="font-semibold text-foreground text-sm mb-1">{category.label}</h4>
                        <p className="text-xs text-muted-foreground line-clamp-2">{category.description}</p>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Advanced Parameters */}
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Weight Requirement */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <Scale className="w-4 h-4 text-eco-earth" />
                        Weight Requirement
                      </label>
                      <span className="text-sm font-bold text-primary">{params.weightRequirement} kg</span>
                    </div>
                    <Slider
                      value={[params.weightRequirement]}
                      onValueChange={([value]) => setParams({ ...params, weightRequirement: value })}
                      min={1}
                      max={50}
                      step={1}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">Maximum weight the packaging must support</p>
                  </div>

                  {/* Fragility Level */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <Shield className="w-4 h-4 text-eco-sky" />
                        Product Fragility
                      </label>
                      <span className="text-sm font-bold text-primary">{params.fragilityLevel}/10</span>
                    </div>
                    <Slider
                      value={[params.fragilityLevel]}
                      onValueChange={([value]) => setParams({ ...params, fragilityLevel: value })}
                      min={1}
                      max={10}
                      step={1}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">How delicate is your product? (10 = very fragile)</p>
                  </div>

                  {/* Cost Sensitivity */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <DollarSign className="w-4 h-4 text-eco-sun" />
                        Cost Sensitivity
                      </label>
                      <span className="text-sm font-bold text-primary">{params.costSensitivity}/10</span>
                    </div>
                    <Slider
                      value={[params.costSensitivity]}
                      onValueChange={([value]) => setParams({ ...params, costSensitivity: value })}
                      min={1}
                      max={10}
                      step={1}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">How important is minimizing cost? (10 = very important)</p>
                  </div>

                  {/* Sustainability Priority */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <Recycle className="w-4 h-4 text-eco-leaf" />
                        Sustainability Priority
                      </label>
                      <span className="text-sm font-bold text-primary">{params.sustainabilityPriority}/10</span>
                    </div>
                    <Slider
                      value={[params.sustainabilityPriority]}
                      onValueChange={([value]) => setParams({ ...params, sustainabilityPriority: value })}
                      min={1}
                      max={10}
                      step={1}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">How important is environmental impact? (10 = top priority)</p>
                  </div>
                </div>

                {/* Get Recommendations Button */}
                <div className="text-center pt-4">
                  <Button 
                    variant="eco" 
                    size="xl"
                    onClick={handleGetRecommendations}
                    disabled={!params.category || isLoading}
                    className="min-w-[280px]"
                  >
                    {isLoading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Analyzing Materials...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-5 h-5" />
                        Generate AI Recommendations
                      </>
                    )}
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Results */}
          {recommendations.length > 0 && (
            <div className="animate-fade-in">
              <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <Award className="w-5 h-5 text-eco-leaf" />
                AI-Ranked Recommendations for {params.category}
                <span className="text-sm font-normal text-muted-foreground ml-2">
                  ({recommendations.length} materials analyzed)
                </span>
              </h3>
              
              <div className="grid gap-4">
                {recommendations.slice(0, 6).map((rec, index) => (
                  <div 
                    key={rec.material.id}
                    className={`eco-card animate-slide-in-right ${rec.rank === 1 ? 'ring-2 ring-eco-leaf/50 shadow-eco-glow' : ''}`}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="flex flex-col lg:flex-row lg:items-start gap-4">
                      {/* Rank Badge */}
                      <div className={`w-14 h-14 rounded-xl flex flex-col items-center justify-center shrink-0 ${
                        rec.rank === 1 ? 'bg-eco-leaf text-white' : 
                        rec.rank === 2 ? 'bg-eco-sky text-white' :
                        rec.rank === 3 ? 'bg-eco-sun text-white' : 'bg-muted text-muted-foreground'
                      }`}>
                        <span className="text-lg font-bold">#{rec.rank}</span>
                        {rec.rank === 1 && <span className="text-[10px]">BEST</span>}
                      </div>

                      {/* Material Info */}
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold text-foreground mb-1 flex items-center gap-2">
                          {rec.material.name}
                          {rec.rank === 1 && <CheckCircle2 className="w-4 h-4 text-eco-leaf" />}
                        </h4>
                        <p className="text-sm text-muted-foreground mb-3">{rec.material.description}</p>
                        
                        {/* Explanations */}
                        <div className="flex flex-wrap gap-2 mb-3">
                          {rec.explanation.slice(0, 3).map((exp, i) => (
                            <span key={i} className="text-xs bg-muted px-2 py-1 rounded-full text-muted-foreground">
                              {exp}
                            </span>
                          ))}
                        </div>

                        {/* Score Breakdown */}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                          <div className={`px-3 py-2 rounded-lg ${getScoreBg(rec.ecoScore)}`}>
                            <div className="flex items-center gap-1">
                              <Leaf className={`w-3 h-3 ${getScoreColor(rec.ecoScore)}`} />
                              <span className={`text-sm font-bold ${getScoreColor(rec.ecoScore)}`}>
                                {rec.ecoScore}
                              </span>
                            </div>
                            <div className="text-[10px] text-muted-foreground">Eco Score</div>
                          </div>
                          <div className={`px-3 py-2 rounded-lg ${getScoreBg(rec.suitabilityScore)}`}>
                            <div className="flex items-center gap-1">
                              <Shield className={`w-3 h-3 ${getScoreColor(rec.suitabilityScore)}`} />
                              <span className={`text-sm font-bold ${getScoreColor(rec.suitabilityScore)}`}>
                                {rec.suitabilityScore}
                              </span>
                            </div>
                            <div className="text-[10px] text-muted-foreground">Suitability</div>
                          </div>
                          <div className="px-3 py-2 rounded-lg bg-eco-sky/10">
                            <div className="flex items-center gap-1">
                              <Wind className="w-3 h-3 text-eco-sky" />
                              <span className="text-sm font-bold text-eco-sky">
                                {rec.material.co2Impact > 0 ? '+' : ''}{rec.material.co2Impact}
                              </span>
                            </div>
                            <div className="text-[10px] text-muted-foreground">kg CO₂</div>
                          </div>
                          <div className="px-3 py-2 rounded-lg bg-eco-earth/10">
                            <div className="flex items-center gap-1">
                              <DollarSign className="w-3 h-3 text-eco-earth" />
                              <span className="text-sm font-bold text-eco-earth">
                                ${rec.material.costPerUnit.toFixed(2)}
                              </span>
                            </div>
                            <div className="text-[10px] text-muted-foreground">per unit</div>
                          </div>
                        </div>
                      </div>

                      {/* Additional Metrics */}
                      <div className="flex flex-row lg:flex-col gap-3 lg:w-32">
                        <div className="flex-1 lg:flex-none text-center p-3 rounded-lg bg-muted/50">
                          <div className="text-lg font-bold text-foreground">{rec.material.biodegradability * 10}%</div>
                          <div className="text-[10px] text-muted-foreground">Biodegradable</div>
                        </div>
                        <div className="flex-1 lg:flex-none text-center p-3 rounded-lg bg-muted/50">
                          <div className="text-lg font-bold text-foreground">{rec.material.recyclability}%</div>
                          <div className="text-[10px] text-muted-foreground">Recyclable</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Scoring explanation */}
              <div className="mt-8 p-6 rounded-xl bg-muted/50 border border-border">
                <h4 className="font-semibold text-foreground mb-3 flex items-center gap-2">
                  <Info className="w-4 h-4 text-primary" />
                  AI Scoring Methodology (Task 4: Feature Engineering)
                </h4>
                <div className="grid md:grid-cols-2 gap-4 text-sm text-muted-foreground">
                  <div>
                    <strong className="text-foreground">Multi-Criteria Decision Analysis:</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>Suitability Score (30%): Category match + weight capacity + fragility protection</li>
                      <li>Eco Score (35%): Biodegradability + recyclability + CO₂ impact</li>
                    </ul>
                  </div>
                  <div>
                    <strong className="text-foreground">Dynamic Weight Adjustment:</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>Cost Score (20%): Normalized cost efficiency × user sensitivity</li>
                      <li>Durability Score (15%): Material durability rating</li>
                    </ul>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-3 pt-3 border-t border-border">
                  The algorithm applies user-defined priority weights to dynamically adjust scoring, simulating 
                  machine learning-based decision support while maintaining full explainability.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};
