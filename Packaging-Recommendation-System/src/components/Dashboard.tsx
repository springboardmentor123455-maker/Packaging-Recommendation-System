import { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  LineChart, Line, Legend, PieChart, Pie, Cell
} from 'recharts';
import { BarChart3, TrendingDown, Recycle, Leaf, DollarSign, Package } from 'lucide-react';
import { getAnalyticsData } from '@/data/packagingMaterials';

export const Dashboard = () => {
  const [analyticsData, setAnalyticsData] = useState<ReturnType<typeof getAnalyticsData> | null>(null);

  useEffect(() => {
    setAnalyticsData(getAnalyticsData());
  }, []);

  if (!analyticsData) return null;

  const COLORS = ['hsl(145, 65%, 42%)', 'hsl(28, 45%, 35%)', 'hsl(200, 75%, 55%)', 'hsl(45, 95%, 58%)'];

  const MetricCard = ({ 
    icon: Icon, 
    title, 
    value, 
    suffix, 
    color 
  }: { 
    icon: React.ElementType; 
    title: string; 
    value: number | string; 
    suffix?: string;
    color: string;
  }) => (
    <div className="eco-card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted-foreground mb-1">{title}</p>
          <p className="text-3xl font-bold text-foreground">
            {value}
            <span className="text-lg text-muted-foreground ml-1">{suffix}</span>
          </p>
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center`} style={{ backgroundColor: `${color}20` }}>
          <Icon className="w-6 h-6" style={{ color }} />
        </div>
      </div>
    </div>
  );

  return (
    <section id="dashboard" className="py-20 bg-secondary/30">
      <div className="container mx-auto px-4">
        <div className="max-w-7xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 eco-badge mb-4">
              <BarChart3 className="w-4 h-4" />
              <span>Analytics Dashboard</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold text-foreground mb-4">
              Business Intelligence Overview
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Real-time analytics and performance metrics for sustainable packaging materials
            </p>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <MetricCard 
              icon={Leaf} 
              title="Avg. Biodegradability" 
              value={analyticsData.summaryMetrics.avgBiodegradability} 
              suffix="%"
              color="hsl(145, 65%, 42%)"
            />
            <MetricCard 
              icon={Recycle} 
              title="Avg. Recyclability" 
              value={analyticsData.summaryMetrics.avgRecyclability} 
              suffix="%"
              color="hsl(200, 75%, 55%)"
            />
            <MetricCard 
              icon={TrendingDown} 
              title="CO₂ Reduction" 
              value={analyticsData.summaryMetrics.avgCO2Reduction} 
              suffix="%"
              color="hsl(28, 45%, 35%)"
            />
            <MetricCard 
              icon={Package} 
              title="Materials Available" 
              value={analyticsData.summaryMetrics.materialCount} 
              suffix=""
              color="hsl(45, 95%, 58%)"
            />
          </div>

          {/* Charts Grid */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* CO2 Comparison Chart */}
            <div className="eco-card">
              <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
                <TrendingDown className="w-5 h-5 text-eco-leaf" />
                CO₂ Impact: Eco vs Traditional
              </h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analyticsData.co2ComparisonData} barCategoryGap="20%">
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      dataKey="name" 
                      tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }}
                      angle={-45}
                      textAnchor="end"
                      height={80}
                    />
                    <YAxis 
                      tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }}
                      label={{ value: 'kg CO₂', angle: -90, position: 'insideLeft', fontSize: 12 }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'hsl(var(--card))', 
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '8px'
                      }}
                    />
                    <Legend />
                    <Bar dataKey="co2Impact" name="Eco Material" fill="hsl(145, 65%, 42%)" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="traditional" name="Traditional Plastic" fill="hsl(0, 0%, 70%)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Cost Analysis Chart */}
            <div className="eco-card">
              <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-eco-earth" />
                Cost Comparison Analysis
              </h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analyticsData.costAnalysisData} barCategoryGap="20%">
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      dataKey="name" 
                      tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }}
                      angle={-45}
                      textAnchor="end"
                      height={80}
                    />
                    <YAxis 
                      tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }}
                      label={{ value: 'USD', angle: -90, position: 'insideLeft', fontSize: 12 }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'hsl(var(--card))', 
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '8px'
                      }}
                      formatter={(value: number) => [`$${value.toFixed(2)}`, '']}
                    />
                    <Legend />
                    <Bar dataKey="eco" name="Eco Material" fill="hsl(28, 45%, 35%)" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="traditional" name="Traditional" fill="hsl(0, 0%, 70%)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Performance Radar */}
            <div className="eco-card">
              <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
                <Leaf className="w-5 h-5 text-eco-sky" />
                Material Performance Overview
              </h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={analyticsData.materialPerformanceData.slice(0, 6)}>
                    <PolarGrid stroke="hsl(var(--border))" />
                    <PolarAngleAxis 
                      dataKey="name" 
                      tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))' }}
                    />
                    <PolarRadiusAxis tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))' }} />
                    <Radar 
                      name="Biodegradability" 
                      dataKey="biodegradability" 
                      stroke="hsl(145, 65%, 42%)" 
                      fill="hsl(145, 65%, 42%)" 
                      fillOpacity={0.3} 
                    />
                    <Radar 
                      name="Recyclability" 
                      dataKey="recyclability" 
                      stroke="hsl(200, 75%, 55%)" 
                      fill="hsl(200, 75%, 55%)" 
                      fillOpacity={0.3} 
                    />
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Eco Score by Category */}
            <div className="eco-card">
              <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-eco-sun" />
                Avg. Eco Score by Category
              </h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={analyticsData.avgEcoScoreByCategory}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={4}
                      dataKey="avgScore"
                      nameKey="category"
                      label={({ category, avgScore }) => `${category}: ${avgScore}`}
                      labelLine={false}
                    >
                      {analyticsData.avgEcoScoreByCategory.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'hsl(var(--card))', 
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '8px'
                      }}
                    />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Insights Panel */}
          <div className="mt-8 grid md:grid-cols-3 gap-4">
            <div className="eco-card border-eco-leaf/20">
              <h4 className="font-semibold text-foreground mb-2">Environmental Impact</h4>
              <p className="text-sm text-muted-foreground">
                Eco-friendly materials show an average of <strong className="text-eco-leaf">{analyticsData.summaryMetrics.avgCO2Reduction}% lower</strong> carbon 
                footprint compared to traditional plastic packaging alternatives.
              </p>
            </div>
            <div className="eco-card border-eco-earth/20">
              <h4 className="font-semibold text-foreground mb-2">Cost Considerations</h4>
              <p className="text-sm text-muted-foreground">
                While initial costs may be higher, sustainable materials offer <strong className="text-eco-earth">long-term value</strong> through 
                reduced waste disposal fees and enhanced brand perception.
              </p>
            </div>
            <div className="eco-card border-eco-sky/20">
              <h4 className="font-semibold text-foreground mb-2">Recyclability Metrics</h4>
              <p className="text-sm text-muted-foreground">
                Our curated materials achieve an average recyclability rate of <strong className="text-eco-sky">{analyticsData.summaryMetrics.avgRecyclability}%</strong>, 
                significantly exceeding industry standards.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
