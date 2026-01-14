import { materials } from '@/data/materials';
import { calculateEcoScore, calculateCO2ImpactIndex } from '@/lib/ecoScore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts';
import { TrendingUp, Leaf, Factory, DollarSign } from 'lucide-react';

const Dashboard = () => {
  // Prepare data for charts
  const ecoScoreData = materials.map(m => ({
    name: m.material_name.split(' ').slice(0, 2).join(' '),
    ecoScore: calculateEcoScore(m),
    biodegradability: m.biodegradability_score,
    recyclability: m.recyclability_percent
  })).sort((a, b) => b.ecoScore - a.ecoScore);

  const co2Data = materials.map(m => ({
    name: m.material_name.split(' ').slice(0, 2).join(' '),
    co2: m.co2_emission_kg_per_kg,
    co2Index: calculateCO2ImpactIndex(m)
  })).sort((a, b) => a.co2 - b.co2);

  const typeDistribution = materials.reduce((acc, m) => {
    acc[m.material_type] = (acc[m.material_type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const pieData = Object.entries(typeDistribution).map(([name, value]) => ({
    name,
    value
  }));

  const COLORS = ['hsl(142, 76%, 36%)', 'hsl(142, 69%, 58%)', 'hsl(48, 96%, 53%)', 'hsl(262, 83%, 58%)', 'hsl(221, 83%, 53%)', 'hsl(0, 84%, 60%)'];

  // Radar chart data for top 5 materials
  const radarData = materials.slice(0, 5).map(m => ({
    material: m.material_name.split(' ')[0],
    Biodegradability: m.biodegradability_score,
    Recyclability: m.recyclability_percent,
    'Low CO₂': calculateCO2ImpactIndex(m),
    Strength: m.strength_rating * 10,
    'Cost Efficiency': Math.min(100, (1 / m.cost_per_kg) * 50)
  }));

  // Summary stats
  const avgEcoScore = materials.reduce((sum, m) => sum + calculateEcoScore(m), 0) / materials.length;
  const avgCO2 = materials.reduce((sum, m) => sum + m.co2_emission_kg_per_kg, 0) / materials.length;
  const avgCost = materials.reduce((sum, m) => sum + m.cost_per_kg, 0) / materials.length;
  const highBioCount = materials.filter(m => m.biodegradability_score >= 90).length;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Eco Score</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">{avgEcoScore.toFixed(1)}</div>
            <p className="text-xs text-muted-foreground">Across {materials.length} materials</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg CO₂ Emission</CardTitle>
            <Factory className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgCO2.toFixed(2)} kg</div>
            <p className="text-xs text-muted-foreground">Per kg of material</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${avgCost.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Per kg of material</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High Biodegradable</CardTitle>
            <Leaf className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-500">{highBioCount}</div>
            <p className="text-xs text-muted-foreground">Materials with 90%+ score</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 1 */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Eco Score Comparison</CardTitle>
            <CardDescription>Materials ranked by overall sustainability score</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={ecoScoreData} layout="vertical" margin={{ left: 80 }}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis type="number" domain={[0, 100]} />
                  <YAxis dataKey="name" type="category" tick={{ fontSize: 12 }} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'hsl(var(--card))', 
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="ecoScore" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>CO₂ Emissions by Material</CardTitle>
            <CardDescription>Lower emissions indicate greener materials</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={co2Data}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'hsl(var(--card))', 
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="co2" fill="hsl(142, 76%, 36%)" radius={[4, 4, 0, 0]} name="CO₂ (kg/kg)" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Material Type Distribution</CardTitle>
            <CardDescription>Breakdown by material category</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Material Properties Radar</CardTitle>
            <CardDescription>Multi-dimensional comparison of top materials</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid className="stroke-muted" />
                  <PolarAngleAxis dataKey="material" tick={{ fontSize: 11 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name="Biodegradability" dataKey="Biodegradability" stroke="hsl(142, 76%, 36%)" fill="hsl(142, 76%, 36%)" fillOpacity={0.3} />
                  <Radar name="Recyclability" dataKey="Recyclability" stroke="hsl(221, 83%, 53%)" fill="hsl(221, 83%, 53%)" fillOpacity={0.3} />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
