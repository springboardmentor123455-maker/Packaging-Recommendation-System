import { Material, ProductCategory, productCategories } from '@/data/materials';

export interface EcoScoreResult {
  material: Material;
  ecoScore: number;
  costEfficiencyIndex: number;
  co2ImpactIndex: number;
  suitabilityScore: number;
  recommendation: string;
}

// Weights for eco-score calculation
const WEIGHTS = {
  biodegradability: 0.30,
  recyclability: 0.25,
  co2Impact: 0.25,
  costEfficiency: 0.20
};

// Normalize CO2 emissions (lower is better, so we invert)
const normalizeCO2 = (co2: number, maxCO2: number): number => {
  return Math.max(0, (1 - co2 / maxCO2) * 100);
};

// Normalize cost (lower is better, so we invert)
const normalizeCost = (cost: number, maxCost: number): number => {
  return Math.max(0, (1 - cost / maxCost) * 100);
};

export const calculateEcoScore = (material: Material, maxCO2: number = 5, maxCost: number = 5): number => {
  const co2Normalized = normalizeCO2(material.co2_emission_kg_per_kg, maxCO2);
  const costNormalized = normalizeCost(material.cost_per_kg, maxCost);
  
  const ecoScore = 
    WEIGHTS.biodegradability * material.biodegradability_score +
    WEIGHTS.recyclability * material.recyclability_percent +
    WEIGHTS.co2Impact * co2Normalized +
    WEIGHTS.costEfficiency * costNormalized;
  
  return Math.round(ecoScore * 100) / 100;
};

export const calculateCostEfficiencyIndex = (material: Material): number => {
  // Higher score = better value (good eco properties per dollar)
  const ecoValue = (material.biodegradability_score + material.recyclability_percent) / 2;
  const efficiency = ecoValue / material.cost_per_kg;
  return Math.round(efficiency * 100) / 100;
};

export const calculateCO2ImpactIndex = (material: Material): number => {
  // Lower CO2 = higher index (better)
  const maxCO2 = 3;
  return Math.round((1 - material.co2_emission_kg_per_kg / maxCO2) * 100);
};

export const checkSuitability = (material: Material, category: ProductCategory): number => {
  const categoryReq = productCategories.find(c => c.value === category);
  if (!categoryReq) return 50;
  
  let score = 100;
  
  // Check strength requirement
  if (material.strength_rating < categoryReq.requirements.minStrength) {
    score -= (categoryReq.requirements.minStrength - material.strength_rating) * 15;
  }
  
  // Check CO2 requirement
  if (material.co2_emission_kg_per_kg > categoryReq.requirements.maxCO2) {
    score -= (material.co2_emission_kg_per_kg - categoryReq.requirements.maxCO2) * 20;
  }
  
  return Math.max(0, Math.round(score));
};

export const getRecommendation = (ecoScore: number, suitability: number): string => {
  if (ecoScore >= 80 && suitability >= 80) {
    return "Highly Recommended - Excellent eco-friendly choice with great product fit";
  } else if (ecoScore >= 70 && suitability >= 70) {
    return "Recommended - Good balance of sustainability and functionality";
  } else if (ecoScore >= 60 || suitability >= 60) {
    return "Acceptable - Consider for specific use cases";
  } else {
    return "Not Recommended - Better alternatives available";
  }
};

export const analyzeAllMaterials = (materials: Material[], category: ProductCategory): EcoScoreResult[] => {
  const results = materials.map(material => {
    const ecoScore = calculateEcoScore(material);
    const costEfficiencyIndex = calculateCostEfficiencyIndex(material);
    const co2ImpactIndex = calculateCO2ImpactIndex(material);
    const suitabilityScore = checkSuitability(material, category);
    const recommendation = getRecommendation(ecoScore, suitabilityScore);
    
    return {
      material,
      ecoScore,
      costEfficiencyIndex,
      co2ImpactIndex,
      suitabilityScore,
      recommendation
    };
  });
  
  // Sort by combined score (eco + suitability)
  return results.sort((a, b) => (b.ecoScore + b.suitabilityScore) - (a.ecoScore + a.suitabilityScore));
};

export const getBestMaterial = (materials: Material[], category: ProductCategory): EcoScoreResult | null => {
  const analyzed = analyzeAllMaterials(materials, category);
  return analyzed.length > 0 ? analyzed[0] : null;
};
