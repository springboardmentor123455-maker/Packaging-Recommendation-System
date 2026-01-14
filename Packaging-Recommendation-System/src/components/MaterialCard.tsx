import { EcoScoreResult } from '@/lib/ecoScore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Leaf, Recycle, Factory, DollarSign, Shield } from 'lucide-react';

interface MaterialCardProps {
  result: EcoScoreResult;
  rank: number;
  isTop?: boolean;
}

const MaterialCard = ({ result, rank, isTop }: MaterialCardProps) => {
  const { material, ecoScore, costEfficiencyIndex, co2ImpactIndex, suitabilityScore, recommendation } = result;
  
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-emerald-400';
    if (score >= 60) return 'text-amber-400';
    return 'text-red-400';
  };

  const getBadgeVariant = (score: number): "default" | "secondary" | "destructive" | "outline" => {
    if (score >= 80) return 'default';
    if (score >= 60) return 'secondary';
    return 'destructive';
  };

  return (
    <Card className={`transition-all duration-300 hover:scale-[1.02] ${isTop ? 'ring-2 ring-primary shadow-lg shadow-primary/20' : 'hover:shadow-md'}`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className={`flex h-8 w-8 items-center justify-center rounded-full ${isTop ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'} font-bold text-sm`}>
              #{rank}
            </div>
            <div>
              <CardTitle className="text-lg">{material.material_name}</CardTitle>
              <Badge variant="outline" className="mt-1 text-xs">
                {material.material_type}
              </Badge>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-2xl font-bold ${getScoreColor(ecoScore)}`}>
              {ecoScore.toFixed(1)}
            </div>
            <div className="text-xs text-muted-foreground">Eco Score</div>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Leaf className="h-3 w-3" />
              Biodegradability
            </div>
            <Progress value={material.biodegradability_score} className="h-2" />
            <div className="text-xs font-medium">{material.biodegradability_score}%</div>
          </div>
          
          <div className="space-y-1">
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Recycle className="h-3 w-3" />
              Recyclability
            </div>
            <Progress value={material.recyclability_percent} className="h-2" />
            <div className="text-xs font-medium">{material.recyclability_percent}%</div>
          </div>
          
          <div className="space-y-1">
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Factory className="h-3 w-3" />
              CO₂ Impact
            </div>
            <Progress value={co2ImpactIndex} className="h-2" />
            <div className="text-xs font-medium">{material.co2_emission_kg_per_kg} kg/kg</div>
          </div>
          
          <div className="space-y-1">
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <DollarSign className="h-3 w-3" />
              Cost
            </div>
            <div className="text-xs font-medium">${material.cost_per_kg.toFixed(2)}/kg</div>
            <div className="text-xs text-muted-foreground">Efficiency: {costEfficiencyIndex}</div>
          </div>
        </div>
        
        {/* Suitability & Strength */}
        <div className="flex items-center justify-between rounded-lg bg-muted/50 p-3">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm">Suitability</span>
          </div>
          <Badge variant={getBadgeVariant(suitabilityScore)}>
            {suitabilityScore}%
          </Badge>
        </div>
        
        {/* Recommendation */}
        <div className={`rounded-lg p-3 text-sm ${isTop ? 'bg-primary/10 text-primary' : 'bg-muted/30 text-muted-foreground'}`}>
          {recommendation}
        </div>
      </CardContent>
    </Card>
  );
};

export default MaterialCard;
