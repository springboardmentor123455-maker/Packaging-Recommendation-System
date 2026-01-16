// EcoPackAI - Structured Dataset of Eco-Friendly Packaging Materials
// Task 3: Data Collection & Preparation

export interface PackagingMaterial {
  id: string;
  name: string;
  description: string;
  strength: number; // 1-10 scale
  weightCapacity: number; // kg
  biodegradability: number; // 1-10 scale (10 = fully biodegradable)
  recyclability: number; // percentage 0-100
  co2Impact: number; // kg CO2 per unit (lower is better)
  costPerUnit: number; // USD
  durability: number; // 1-10 scale
  moistureResistance: number; // 1-10 scale
  suitableCategories: ProductCategory[];
  imageUrl?: string;
}

export type ProductCategory = 
  | 'Electronics'
  | 'Food & Beverages'
  | 'Cosmetics'
  | 'Fragile Items';

export const productCategories: { id: ProductCategory; label: string; icon: string; description: string }[] = [
  { 
    id: 'Electronics', 
    label: 'Electronics', 
    icon: '💻',
    description: 'Phones, laptops, gadgets requiring static protection'
  },
  { 
    id: 'Food & Beverages', 
    label: 'Food & Beverages', 
    icon: '🍎',
    description: 'Perishables requiring food-safe, breathable packaging'
  },
  { 
    id: 'Cosmetics', 
    label: 'Cosmetics', 
    icon: '💄',
    description: 'Beauty products needing elegant, protective packaging'
  },
  { 
    id: 'Fragile Items', 
    label: 'Fragile Items', 
    icon: '🏺',
    description: 'Glass, ceramics requiring maximum cushioning'
  },
];

export const packagingMaterials: PackagingMaterial[] = [
  {
    id: 'corrugated-cardboard',
    name: 'Corrugated Cardboard',
    description: 'Multi-layered cardboard with fluted inner layer for cushioning. Widely recyclable and made from renewable resources.',
    strength: 7,
    weightCapacity: 30,
    biodegradability: 9,
    recyclability: 95,
    co2Impact: 0.8,
    costPerUnit: 0.45,
    durability: 6,
    moistureResistance: 3,
    suitableCategories: ['Electronics', 'Fragile Items'],
  },
  {
    id: 'molded-pulp',
    name: 'Molded Pulp',
    description: 'Made from recycled paper fibers, shaped to fit products perfectly. Excellent for cushioning and fully compostable.',
    strength: 5,
    weightCapacity: 15,
    biodegradability: 10,
    recyclability: 100,
    co2Impact: 0.3,
    costPerUnit: 0.35,
    durability: 4,
    moistureResistance: 2,
    suitableCategories: ['Electronics', 'Fragile Items', 'Cosmetics'],
  },
  {
    id: 'mushroom-packaging',
    name: 'Mushroom Packaging',
    description: 'Grown from mycelium and agricultural waste. Fully biodegradable within 45 days and carbon-negative production.',
    strength: 6,
    weightCapacity: 20,
    biodegradability: 10,
    recyclability: 100,
    co2Impact: -0.2,
    costPerUnit: 0.85,
    durability: 5,
    moistureResistance: 4,
    suitableCategories: ['Electronics', 'Fragile Items', 'Cosmetics'],
  },
  {
    id: 'seaweed-packaging',
    name: 'Seaweed Packaging',
    description: 'Derived from algae, edible and fully marine-biodegradable. Ideal for food applications with zero waste.',
    strength: 3,
    weightCapacity: 5,
    biodegradability: 10,
    recyclability: 100,
    co2Impact: -0.5,
    costPerUnit: 1.20,
    durability: 3,
    moistureResistance: 2,
    suitableCategories: ['Food & Beverages', 'Cosmetics'],
  },
  {
    id: 'bamboo-packaging',
    name: 'Bamboo Fiber',
    description: 'Fast-growing renewable resource with excellent strength-to-weight ratio. Naturally antimicrobial.',
    strength: 8,
    weightCapacity: 25,
    biodegradability: 8,
    recyclability: 85,
    co2Impact: 0.4,
    costPerUnit: 0.65,
    durability: 7,
    moistureResistance: 5,
    suitableCategories: ['Electronics', 'Food & Beverages', 'Cosmetics', 'Fragile Items'],
  },
  {
    id: 'cornstarch-packaging',
    name: 'Cornstarch Bioplastic',
    description: 'Plant-based alternative to plastic foam. Dissolves in water and composts within 90 days.',
    strength: 4,
    weightCapacity: 10,
    biodegradability: 9,
    recyclability: 80,
    co2Impact: 0.5,
    costPerUnit: 0.55,
    durability: 4,
    moistureResistance: 1,
    suitableCategories: ['Food & Beverages', 'Cosmetics'],
  },
  {
    id: 'recycled-paper-honeycomb',
    name: 'Paper Honeycomb',
    description: 'Lightweight honeycomb structure from recycled paper. Excellent shock absorption with minimal material use.',
    strength: 6,
    weightCapacity: 35,
    biodegradability: 9,
    recyclability: 95,
    co2Impact: 0.35,
    costPerUnit: 0.50,
    durability: 5,
    moistureResistance: 2,
    suitableCategories: ['Electronics', 'Fragile Items'],
  },
  {
    id: 'hemp-packaging',
    name: 'Hemp Fiber',
    description: 'Durable natural fiber requiring minimal water and pesticides to grow. Carbon-sequestering crop.',
    strength: 8,
    weightCapacity: 28,
    biodegradability: 9,
    recyclability: 90,
    co2Impact: 0.25,
    costPerUnit: 0.75,
    durability: 8,
    moistureResistance: 6,
    suitableCategories: ['Electronics', 'Fragile Items', 'Cosmetics'],
  },
  {
    id: 'palm-leaf-packaging',
    name: 'Palm Leaf',
    description: 'Made from fallen palm leaves without harming trees. Heat-resistant and naturally water-repellent.',
    strength: 5,
    weightCapacity: 12,
    biodegradability: 10,
    recyclability: 100,
    co2Impact: 0.15,
    costPerUnit: 0.40,
    durability: 6,
    moistureResistance: 7,
    suitableCategories: ['Food & Beverages', 'Cosmetics'],
  },
  {
    id: 'sugarcane-bagasse',
    name: 'Sugarcane Bagasse',
    description: 'Agricultural byproduct from sugar production. Sturdy, grease-resistant, and fully compostable.',
    strength: 6,
    weightCapacity: 18,
    biodegradability: 9,
    recyclability: 90,
    co2Impact: 0.2,
    costPerUnit: 0.30,
    durability: 5,
    moistureResistance: 6,
    suitableCategories: ['Food & Beverages', 'Cosmetics'],
  },
  {
    id: 'kraft-paper',
    name: 'Kraft Paper',
    description: 'Unbleached paper with high tensile strength. Minimal processing maintains natural fiber strength.',
    strength: 6,
    weightCapacity: 22,
    biodegradability: 9,
    recyclability: 95,
    co2Impact: 0.45,
    costPerUnit: 0.25,
    durability: 5,
    moistureResistance: 3,
    suitableCategories: ['Electronics', 'Food & Beverages', 'Cosmetics', 'Fragile Items'],
  },
  {
    id: 'wool-packaging',
    name: 'Wool Insulation',
    description: 'Natural thermal insulation from sheep wool. Excellent for temperature-sensitive products.',
    strength: 4,
    weightCapacity: 8,
    biodegradability: 10,
    recyclability: 85,
    co2Impact: 0.6,
    costPerUnit: 1.50,
    durability: 7,
    moistureResistance: 5,
    suitableCategories: ['Food & Beverages', 'Cosmetics'],
  },
];

// Task 4: Feature Engineering & Scoring Logic
export interface ScoringWeights {
  biodegradability: number;
  recyclability: number;
  co2Impact: number;
  costEfficiency: number;
  durability: number;
  strengthMatch: number;
}

export const defaultWeights: ScoringWeights = {
  biodegradability: 0.20,
  recyclability: 0.15,
  co2Impact: 0.25,
  costEfficiency: 0.15,
  durability: 0.10,
  strengthMatch: 0.15,
};

// Normalize value to 0-1 scale
const normalize = (value: number, min: number, max: number): number => {
  return Math.max(0, Math.min(1, (value - min) / (max - min)));
};

// Calculate derived metrics
export const calculateCO2ImpactIndex = (co2Impact: number): number => {
  // Lower CO2 is better, so we invert the scale
  // Range: -0.5 (best) to 1.5 (worst)
  return normalize(1 - co2Impact, 0, 1.5);
};

export const calculateCostEfficiencyIndex = (cost: number): number => {
  // Lower cost is better
  // Range: 0.25 (best) to 1.50 (worst)
  return normalize(1.50 - cost, 0, 1.25);
};

export const calculateMaterialSuitabilityScore = (
  material: PackagingMaterial,
  category: ProductCategory,
  weights: ScoringWeights = defaultWeights
): number => {
  // Check category suitability
  if (!material.suitableCategories.includes(category)) {
    return 0;
  }

  // Normalize each attribute
  const biodegradabilityScore = material.biodegradability / 10;
  const recyclabilityScore = material.recyclability / 100;
  const co2Score = calculateCO2ImpactIndex(material.co2Impact);
  const costScore = calculateCostEfficiencyIndex(material.costPerUnit);
  const durabilityScore = material.durability / 10;
  
  // Strength requirements vary by category
  const strengthRequirements: Record<ProductCategory, number> = {
    'Electronics': 7,
    'Food & Beverages': 4,
    'Cosmetics': 5,
    'Fragile Items': 6,
  };
  
  const requiredStrength = strengthRequirements[category];
  const strengthScore = material.strength >= requiredStrength 
    ? 1 
    : material.strength / requiredStrength;

  // Weighted sum
  const totalScore = 
    biodegradabilityScore * weights.biodegradability +
    recyclabilityScore * weights.recyclability +
    co2Score * weights.co2Impact +
    costScore * weights.costEfficiency +
    durabilityScore * weights.durability +
    strengthScore * weights.strengthMatch;

  return Math.round(totalScore * 100);
};

// Task 5: Recommendation Engine
export interface MaterialRecommendation {
  material: PackagingMaterial;
  ecoScore: number;
  co2ImpactIndex: number;
  costEfficiencyIndex: number;
  rank: number;
}

export const getRecommendations = (
  category: ProductCategory,
  weights: ScoringWeights = defaultWeights
): MaterialRecommendation[] => {
  const recommendations = packagingMaterials
    .filter(m => m.suitableCategories.includes(category))
    .map(material => ({
      material,
      ecoScore: calculateMaterialSuitabilityScore(material, category, weights),
      co2ImpactIndex: Math.round(calculateCO2ImpactIndex(material.co2Impact) * 100),
      costEfficiencyIndex: Math.round(calculateCostEfficiencyIndex(material.costPerUnit) * 100),
      rank: 0,
    }))
    .sort((a, b) => b.ecoScore - a.ecoScore)
    .map((rec, index) => ({ ...rec, rank: index + 1 }));

  return recommendations;
};

// Analytics data for BI Dashboard
export const getAnalyticsData = () => {
  const categories = productCategories.map(c => c.id);
  
  return {
    avgEcoScoreByCategory: categories.map(cat => ({
      category: cat,
      avgScore: Math.round(
        getRecommendations(cat).reduce((sum, r) => sum + r.ecoScore, 0) / 
        getRecommendations(cat).length
      ),
    })),
    
    co2ComparisonData: packagingMaterials.slice(0, 8).map(m => ({
      name: m.name.length > 15 ? m.name.substring(0, 12) + '...' : m.name,
      co2Impact: m.co2Impact,
      traditional: 2.5, // Baseline traditional plastic packaging
    })),
    
    costAnalysisData: packagingMaterials.slice(0, 8).map(m => ({
      name: m.name.length > 15 ? m.name.substring(0, 12) + '...' : m.name,
      eco: m.costPerUnit,
      traditional: 0.15, // Traditional plastic cost
    })),
    
    materialPerformanceData: packagingMaterials.map(m => ({
      name: m.name,
      biodegradability: m.biodegradability * 10,
      recyclability: m.recyclability,
      durability: m.durability * 10,
    })),
    
    summaryMetrics: {
      avgBiodegradability: Math.round(
        packagingMaterials.reduce((sum, m) => sum + m.biodegradability, 0) / 
        packagingMaterials.length * 10
      ),
      avgRecyclability: Math.round(
        packagingMaterials.reduce((sum, m) => sum + m.recyclability, 0) / 
        packagingMaterials.length
      ),
      avgCO2Reduction: Math.round(
        (2.5 - packagingMaterials.reduce((sum, m) => sum + m.co2Impact, 0) / 
        packagingMaterials.length) / 2.5 * 100
      ),
      materialCount: packagingMaterials.length,
    },
  };
};
