// Material database - equivalent to materials.csv
export interface Material {
  material_name: string;
  material_type: string;
  biodegradability_score: number; // 0-100
  recyclability_percent: number; // 0-100
  co2_emission_kg_per_kg: number;
  cost_per_kg: number;
  strength_rating: number; // 1-10
  weight_capacity_kg: number;
}

export const materials: Material[] = [
  {
    material_name: "Recycled Cardboard",
    material_type: "Paper-Based",
    biodegradability_score: 95,
    recyclability_percent: 90,
    co2_emission_kg_per_kg: 0.8,
    cost_per_kg: 0.45,
    strength_rating: 6,
    weight_capacity_kg: 25
  },
  {
    material_name: "Bamboo Fiber",
    material_type: "Plant-Based",
    biodegradability_score: 98,
    recyclability_percent: 85,
    co2_emission_kg_per_kg: 0.3,
    cost_per_kg: 1.20,
    strength_rating: 7,
    weight_capacity_kg: 20
  },
  {
    material_name: "Cornstarch PLA",
    material_type: "Bioplastic",
    biodegradability_score: 88,
    recyclability_percent: 60,
    co2_emission_kg_per_kg: 1.2,
    cost_per_kg: 2.50,
    strength_rating: 5,
    weight_capacity_kg: 15
  },
  {
    material_name: "Mushroom Packaging",
    material_type: "Mycelium",
    biodegradability_score: 100,
    recyclability_percent: 100,
    co2_emission_kg_per_kg: 0.1,
    cost_per_kg: 3.80,
    strength_rating: 4,
    weight_capacity_kg: 10
  },
  {
    material_name: "Seaweed Film",
    material_type: "Marine-Based",
    biodegradability_score: 100,
    recyclability_percent: 95,
    co2_emission_kg_per_kg: 0.2,
    cost_per_kg: 4.50,
    strength_rating: 3,
    weight_capacity_kg: 5
  },
  {
    material_name: "Recycled HDPE",
    material_type: "Recycled Plastic",
    biodegradability_score: 10,
    recyclability_percent: 95,
    co2_emission_kg_per_kg: 1.8,
    cost_per_kg: 0.90,
    strength_rating: 8,
    weight_capacity_kg: 50
  },
  {
    material_name: "Sugarcane Bagasse",
    material_type: "Agricultural Waste",
    biodegradability_score: 92,
    recyclability_percent: 80,
    co2_emission_kg_per_kg: 0.5,
    cost_per_kg: 0.75,
    strength_rating: 5,
    weight_capacity_kg: 12
  },
  {
    material_name: "Hemp Fiber",
    material_type: "Plant-Based",
    biodegradability_score: 96,
    recyclability_percent: 88,
    co2_emission_kg_per_kg: 0.4,
    cost_per_kg: 1.80,
    strength_rating: 8,
    weight_capacity_kg: 30
  },
  {
    material_name: "Molded Pulp",
    material_type: "Paper-Based",
    biodegradability_score: 94,
    recyclability_percent: 92,
    co2_emission_kg_per_kg: 0.6,
    cost_per_kg: 0.55,
    strength_rating: 5,
    weight_capacity_kg: 18
  },
  {
    material_name: "Wheat Straw Board",
    material_type: "Agricultural Waste",
    biodegradability_score: 90,
    recyclability_percent: 75,
    co2_emission_kg_per_kg: 0.7,
    cost_per_kg: 0.65,
    strength_rating: 6,
    weight_capacity_kg: 22
  },
  {
    material_name: "Coconut Coir",
    material_type: "Plant-Based",
    biodegradability_score: 97,
    recyclability_percent: 82,
    co2_emission_kg_per_kg: 0.35,
    cost_per_kg: 1.10,
    strength_rating: 6,
    weight_capacity_kg: 15
  },
  {
    material_name: "rPET Bottles",
    material_type: "Recycled Plastic",
    biodegradability_score: 5,
    recyclability_percent: 98,
    co2_emission_kg_per_kg: 2.1,
    cost_per_kg: 1.05,
    strength_rating: 7,
    weight_capacity_kg: 40
  }
];

export type ProductCategory = 'electronics' | 'food' | 'cosmetics' | 'pharmaceuticals' | 'apparel' | 'fragile';

export const productCategories: { value: ProductCategory; label: string; requirements: { minStrength: number; maxCO2: number } }[] = [
  { value: 'electronics', label: 'Electronics', requirements: { minStrength: 7, maxCO2: 2.0 } },
  { value: 'food', label: 'Food & Beverages', requirements: { minStrength: 4, maxCO2: 1.5 } },
  { value: 'cosmetics', label: 'Cosmetics', requirements: { minStrength: 3, maxCO2: 1.5 } },
  { value: 'pharmaceuticals', label: 'Pharmaceuticals', requirements: { minStrength: 5, maxCO2: 1.8 } },
  { value: 'apparel', label: 'Apparel & Textiles', requirements: { minStrength: 3, maxCO2: 1.2 } },
  { value: 'fragile', label: 'Fragile Items', requirements: { minStrength: 6, maxCO2: 2.0 } }
];
