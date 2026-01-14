import { useState } from 'react';
import { materials, productCategories, ProductCategory } from '@/data/materials';
import { analyzeAllMaterials, EcoScoreResult } from '@/lib/ecoScore';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import MaterialCard from './MaterialCard';
import { Sparkles, Package, ArrowRight } from 'lucide-react';

const RecommendationPanel = () => {
  const [selectedCategory, setSelectedCategory] = useState<ProductCategory>('electronics');
  const [results, setResults] = useState<EcoScoreResult[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);

  const handleRecommend = async () => {
    setIsAnalyzing(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const analyzed = analyzeAllMaterials(materials, selectedCategory);
    setResults(analyzed);
    setHasAnalyzed(true);
    setIsAnalyzing(false);
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card className="border-2 border-dashed">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="h-5 w-5" />
            Product Configuration
          </CardTitle>
          <CardDescription>
            Select your product category to get AI-powered packaging recommendations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
            <div className="flex-1 space-y-2">
              <label className="text-sm font-medium">Product Category</label>
              <Select value={selectedCategory} onValueChange={(v) => setSelectedCategory(v as ProductCategory)}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {productCategories.map((cat) => (
                    <SelectItem key={cat.value} value={cat.value}>
                      {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <Button 
              onClick={handleRecommend} 
              disabled={isAnalyzing}
              size="lg"
              className="gap-2"
            >
              {isAnalyzing ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  Get Recommendations
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Results Section */}
      {hasAnalyzed && results.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">
              Top Recommendations for{' '}
              <span className="text-primary">
                {productCategories.find(c => c.value === selectedCategory)?.label}
              </span>
            </h2>
            <span className="text-sm text-muted-foreground">
              {results.length} materials analyzed
            </span>
          </div>
          
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {results.slice(0, 6).map((result, index) => (
              <MaterialCard 
                key={result.material.material_name}
                result={result}
                rank={index + 1}
                isTop={index === 0}
              />
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!hasAnalyzed && (
        <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed py-16 text-center">
          <Sparkles className="mb-4 h-12 w-12 text-muted-foreground/50" />
          <h3 className="text-lg font-medium">Ready to Analyze</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Select a product category and click "Get Recommendations" to see eco-friendly packaging options
          </p>
        </div>
      )}
    </div>
  );
};

export default RecommendationPanel;
