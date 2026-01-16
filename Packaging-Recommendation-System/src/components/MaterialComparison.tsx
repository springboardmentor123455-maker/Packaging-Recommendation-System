import { useState } from 'react';
import { Scale, Plus, X, Check, Leaf, Recycle, Wind, DollarSign, Shield, Droplets, Weight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { packagingMaterials, type PackagingMaterial } from '@/data/packagingMaterials';

const MAX_COMPARE = 3;

export const MaterialComparison = () => {
  const [selectedMaterials, setSelectedMaterials] = useState<PackagingMaterial[]>([]);
  const [isSelectOpen, setIsSelectOpen] = useState(false);

  const handleAddMaterial = (material: PackagingMaterial) => {
    if (selectedMaterials.length < MAX_COMPARE && !selectedMaterials.find(m => m.id === material.id)) {
      setSelectedMaterials([...selectedMaterials, material]);
    }
    setIsSelectOpen(false);
  };

  const handleRemoveMaterial = (materialId: string) => {
    setSelectedMaterials(selectedMaterials.filter(m => m.id !== materialId));
  };

  const availableMaterials = packagingMaterials.filter(
    m => !selectedMaterials.find(sm => sm.id === m.id)
  );

  const getScoreColor = (value: number, max: number, invert = false) => {
    const ratio = value / max;
    const adjusted = invert ? 1 - ratio : ratio;
    if (adjusted >= 0.7) return 'text-eco-leaf bg-eco-leaf/10';
    if (adjusted >= 0.4) return 'text-eco-sun bg-eco-sun/10';
    return 'text-eco-earth bg-eco-earth/10';
  };

  const getBestValue = (attribute: keyof PackagingMaterial, invert = false) => {
    if (selectedMaterials.length === 0) return null;
    const values = selectedMaterials.map(m => m[attribute] as number);
    return invert ? Math.min(...values) : Math.max(...values);
  };

  const attributes = [
    { key: 'strength', label: 'Strength', icon: Shield, max: 10, suffix: '/10', invert: false },
    { key: 'weightCapacity', label: 'Weight Capacity', icon: Weight, max: 35, suffix: ' kg', invert: false },
    { key: 'biodegradability', label: 'Biodegradability', icon: Leaf, max: 10, suffix: '/10', invert: false },
    { key: 'recyclability', label: 'Recyclability', icon: Recycle, max: 100, suffix: '%', invert: false },
    { key: 'co2Impact', label: 'CO₂ Impact', icon: Wind, max: 1.5, suffix: ' kg', invert: true },
    { key: 'costPerUnit', label: 'Cost per Unit', icon: DollarSign, max: 1.5, suffix: '', invert: true, prefix: '$' },
    { key: 'durability', label: 'Durability', icon: Shield, max: 10, suffix: '/10', invert: false },
    { key: 'moistureResistance', label: 'Moisture Resistance', icon: Droplets, max: 10, suffix: '/10', invert: false },
  ];

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 eco-badge mb-4">
              <Scale className="w-4 h-4" />
              <span>Material Comparison</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              Compare Materials Side-by-Side
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Select up to {MAX_COMPARE} materials to compare their attributes and find the best fit for your needs
            </p>
          </div>

          {/* Material Selection Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            {[...Array(MAX_COMPARE)].map((_, index) => {
              const material = selectedMaterials[index];
              return (
                <div
                  key={index}
                  className={`eco-card min-h-[140px] flex flex-col items-center justify-center transition-all ${
                    material ? 'border-primary/30' : 'border-dashed border-2 border-muted-foreground/30'
                  }`}
                >
                  {material ? (
                    <div className="w-full">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h4 className="font-semibold text-foreground">{material.name}</h4>
                          <p className="text-xs text-muted-foreground line-clamp-2 mt-1">
                            {material.description.substring(0, 60)}...
                          </p>
                        </div>
                        <button
                          onClick={() => handleRemoveMaterial(material.id)}
                          className="p-1.5 rounded-lg hover:bg-destructive/10 text-muted-foreground hover:text-destructive transition-colors"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs px-2 py-1 rounded-full bg-eco-leaf/10 text-eco-leaf">
                          {material.biodegradability * 10}% Bio
                        </span>
                        <span className="text-xs px-2 py-1 rounded-full bg-eco-sky/10 text-eco-sky">
                          {material.recyclability}% Recyclable
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="relative w-full">
                      <button
                        onClick={() => setIsSelectOpen(true)}
                        className="w-full flex flex-col items-center gap-2 py-4 text-muted-foreground hover:text-primary transition-colors"
                        disabled={availableMaterials.length === 0}
                      >
                        <div className="w-12 h-12 rounded-xl border-2 border-dashed border-current flex items-center justify-center">
                          <Plus className="w-6 h-6" />
                        </div>
                        <span className="text-sm font-medium">Add Material {index + 1}</span>
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Material Selection Dropdown */}
          {isSelectOpen && availableMaterials.length > 0 && (
            <div className="mb-8 animate-fade-in">
              <div className="eco-card">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-foreground">Select a Material</h4>
                  <button
                    onClick={() => setIsSelectOpen(false)}
                    className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                  {availableMaterials.map(material => (
                    <button
                      key={material.id}
                      onClick={() => handleAddMaterial(material)}
                      className="p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 text-left transition-all group"
                    >
                      <div className="font-medium text-sm text-foreground group-hover:text-primary truncate">
                        {material.name}
                      </div>
                      <div className="text-xs text-muted-foreground mt-1">
                        Eco: {material.biodegradability}/10
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Comparison Table */}
          {selectedMaterials.length >= 2 && (
            <div className="eco-card overflow-hidden animate-fade-in">
              <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
                <Scale className="w-5 h-5 text-primary" />
                Detailed Comparison
              </h3>
              
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left py-3 px-4 text-sm font-semibold text-muted-foreground w-48">
                        Attribute
                      </th>
                      {selectedMaterials.map(material => (
                        <th key={material.id} className="text-center py-3 px-4 text-sm font-semibold text-foreground min-w-[140px]">
                          {material.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {attributes.map((attr, index) => {
                      const bestValue = getBestValue(attr.key as keyof PackagingMaterial, attr.invert);
                      return (
                        <tr 
                          key={attr.key} 
                          className={`border-b border-border/50 ${index % 2 === 0 ? 'bg-muted/20' : ''}`}
                        >
                          <td className="py-4 px-4">
                            <div className="flex items-center gap-2">
                              <attr.icon className="w-4 h-4 text-muted-foreground" />
                              <span className="text-sm font-medium text-foreground">{attr.label}</span>
                            </div>
                          </td>
                          {selectedMaterials.map(material => {
                            const value = material[attr.key as keyof PackagingMaterial] as number;
                            const isBest = value === bestValue;
                            const colorClass = getScoreColor(value, attr.max, attr.invert);
                            return (
                              <td key={material.id} className="py-4 px-4 text-center">
                                <div className="flex items-center justify-center gap-2">
                                  <span className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-semibold ${colorClass}`}>
                                    {attr.prefix || ''}{typeof value === 'number' ? value.toFixed(attr.key === 'costPerUnit' ? 2 : attr.key === 'co2Impact' ? 1 : 0) : value}{attr.suffix}
                                  </span>
                                  {isBest && selectedMaterials.length > 1 && (
                                    <span className="w-5 h-5 rounded-full bg-eco-leaf flex items-center justify-center">
                                      <Check className="w-3 h-3 text-white" />
                                    </span>
                                  )}
                                </div>
                              </td>
                            );
                          })}
                        </tr>
                      );
                    })}
                    {/* Categories Row */}
                    <tr className="bg-muted/30">
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <Leaf className="w-4 h-4 text-muted-foreground" />
                          <span className="text-sm font-medium text-foreground">Suitable For</span>
                        </div>
                      </td>
                      {selectedMaterials.map(material => (
                        <td key={material.id} className="py-4 px-4 text-center">
                          <div className="flex flex-wrap justify-center gap-1">
                            {material.suitableCategories.map(cat => (
                              <span key={cat} className="text-xs px-2 py-1 rounded-full bg-primary/10 text-primary">
                                {cat}
                              </span>
                            ))}
                          </div>
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Summary */}
              <div className="mt-6 pt-6 border-t border-border">
                <h4 className="font-semibold text-foreground mb-4">Quick Summary</h4>
                <div className="grid sm:grid-cols-3 gap-4">
                  {selectedMaterials.map(material => {
                    const overallScore = Math.round(
                      (material.biodegradability / 10 * 0.3 +
                      material.recyclability / 100 * 0.25 +
                      (1 - material.co2Impact / 1.5) * 0.25 +
                      (1 - material.costPerUnit / 1.5) * 0.2) * 100
                    );
                    return (
                      <div key={material.id} className="p-4 rounded-xl bg-muted/50">
                        <h5 className="font-medium text-foreground mb-2">{material.name}</h5>
                        <div className="flex items-center gap-2 mb-3">
                          <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-gradient-to-r from-eco-leaf to-primary rounded-full transition-all duration-500"
                              style={{ width: `${overallScore}%` }}
                            />
                          </div>
                          <span className="text-sm font-bold text-primary">{overallScore}%</span>
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Overall eco-performance score based on weighted criteria
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Empty State */}
          {selectedMaterials.length < 2 && (
            <div className="text-center py-12 text-muted-foreground">
              <Scale className="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p className="text-lg font-medium">Select at least 2 materials to compare</p>
              <p className="text-sm mt-1">Click "Add Material" above to get started</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};
