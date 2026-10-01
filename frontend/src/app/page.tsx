"use client"

import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { Zap, IndianRupee, Factory, Activity, Leaf, Sun, Bell, Settings, LayoutDashboard, Search, Calendar, ChevronDown, MessageSquare } from 'lucide-react';

const KPICard = ({ title, value, subtitle, icon: Icon, trend, trendValue, color }: any) => (
  <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex flex-col justify-between">
    <div className="flex items-center justify-between mb-2">
      <div className={`p-2 rounded-lg ${color} bg-opacity-10 text-opacity-100`}>
        <Icon size={20} className={color.replace('bg-', 'text-')} />
      </div>
    </div>
    <div>
      <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
      <div className="text-2xl font-bold text-gray-900 mt-1">{value}</div>
      {trend && (
        <div className={`text-xs mt-2 flex items-center font-medium ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
          {trend === 'up' ? '↑' : '↓'} {trendValue}
          <span className="text-gray-400 ml-1 font-normal">{subtitle}</span>
        </div>
      )}
    </div>
  </div>
);

const STATIC_pieData = [
  { name: 'Press Shop', value: 28, color: '#3b82f6' },
  { name: 'Welding Shop', value: 18, color: '#ef4444' },
  { name: 'Paint Shop', value: 16, color: '#f97316' },
  { name: 'HVAC', value: 14, color: '#a855f7' },
  { name: 'Utilities', value: 12, color: '#06b6d4' },
  { name: 'Assembly', value: 10, color: '#8b5cf6' },
];

const sidebarItems = [
  { name: 'Dashboard', icon: LayoutDashboard },
  { name: 'Energy Monitoring', icon: Zap },
  { name: 'Production', icon: Factory },
  { name: 'Machines', icon: Settings },
  { name: 'Cost & Tariff', icon: IndianRupee },
  { name: 'Renewable Energy', icon: Sun },
  { name: 'Carbon & Sustainability', icon: Leaf },
  { name: 'AI Insights', icon: MessageSquare },
  { name: 'Reports', icon: Activity },
];

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [energyData, setEnergyData] = useState<any[]>([]);
  const [pieData, setPieData] = useState<any[]>(STATIC_pieData);
  const [productionData, setProductionData] = useState<any[]>([]);
  const [intensityData, setIntensityData] = useState<any[]>([]);
  const [costBreakdown, setCostBreakdown] = useState<any[]>([]);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [forecast, setForecast] = useState<any[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLog, setChatLog] = useState<{role: string, text: string}[]>([]);
  const [metrics, setMetrics] = useState<any>({
    total_energy_consumption_kwh: 0,
    energy_cost_currency: 0,
    production_output_units: 0,
    energy_intensity_kwh_per_unit: 0,
    co2_emissions_tco2e: 0,
    renewable_contribution_pct: 0
  });

  React.useEffect(() => {
    const fetchProps = { headers: { 'Authorization': 'Bearer MOCK_TOKEN_ADMIN' } };
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    fetch(`${apiBase}/v1/energy/timeseries`, fetchProps)
        .then(res => res.json())
        .then(data => setEnergyData(data))
        .catch(err => console.error("Error fetching timeseries:", err));

    fetch(`${apiBase}/v1/energy/distribution`, fetchProps)
        .then(res => res.json())
        .then(data => setPieData(data.length > 0 ? data : STATIC_pieData))
        .catch(err => console.error("Error fetching distribution:", err));

    fetch(`${apiBase}/v1/energy/metrics`, fetchProps)
        .then(res => res.json())
        .then(data => setMetrics(data))
        .catch(err => console.error("Error fetching metrics:", err));

    fetch(`${apiBase}/v1/production/timeseries`, fetchProps)
        .then(res => res.json())
        .then(data => setProductionData(data))
        .catch(err => console.error("Error fetching production timeseries:", err));

    fetch(`${apiBase}/v1/production/intensity`, fetchProps)
        .then(res => res.json())
        .then(data => setIntensityData(data))
        .catch(err => console.error("Error fetching intensity:", err));

    fetch(`${apiBase}/v1/cost/breakdown`, fetchProps)
        .then(res => res.json())
        .then(data => setCostBreakdown(data))
        .catch(err => console.error("Error fetching cost breakdown:", err));

    fetch(`${apiBase}/v1/ai/anomalies`, fetchProps)
        .then(res => res.json())
        .then(data => setAnomalies(data))
        .catch(err => console.error("Error fetching anomalies:", err));

    fetch(`${apiBase}/v1/ai/forecast`, fetchProps)
        .then(res => res.json())
        .then(data => setForecast(data))
        .catch(err => console.error("Error fetching forecast:", err));
  }, []);

  const handleChatSubmit = async (e: any) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const newLog = [...chatLog, { role: 'user', text: chatInput }];
    setChatLog(newLog);
    setChatInput('');

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiBase}/v1/ai/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': 'Bearer MOCK_TOKEN_ADMIN'
        },
        body: JSON.stringify({ message: chatInput })
      });
      const data = await res.json();
      setChatLog([...newLog, { role: 'assistant', text: data.reply }]);
    } catch(err) {
      console.error(err);
    }
  };

  const renderContent = () => {
    // Shared KPI Grid for all modules to show data context
    const sharedKPIs = (
      <div className="grid grid-cols-3 md:grid-cols-6 gap-4 mb-6">
        <KPICard title="Total Energy Consumption" value={`${metrics.total_energy_consumption_kwh.toLocaleString(undefined, {maximumFractionDigits:0})} kWh`} subtitle="vs. yesterday" icon={Zap} trend="down" trendValue="6.2%" color="bg-blue-500" />
        <KPICard title="Energy Cost" value={`$ ${metrics.energy_cost_currency.toLocaleString(undefined, {maximumFractionDigits:0})}`} subtitle="vs. yesterday" icon={IndianRupee} trend="down" trendValue="4.8%" color="bg-emerald-500" />
        <KPICard title="Production Output" value={`${metrics.production_output_units.toLocaleString(undefined, {maximumFractionDigits:0})} units`} subtitle="vs. yesterday" icon={Factory} trend="up" trendValue="2.6%" color="bg-purple-500" />
        <KPICard title="Energy Intensity" value={`${metrics.energy_intensity_kwh_per_unit.toFixed(2)} kWh/unit`} subtitle="vs. last week" icon={Activity} trend="down" trendValue="8.5%" color="bg-orange-500" />
        <KPICard title="CO2 Emissions" value={`${metrics.co2_emissions_tco2e.toFixed(1)} tCO2e`} subtitle="vs. last week" icon={Leaf} trend="down" trendValue="10.1%" color="bg-green-600" />
        <KPICard title="Renewable Contribution" value={`${metrics.renewable_contribution_pct.toFixed(1)}%`} subtitle="vs. last week" icon={Sun} trend="up" trendValue="5.2%" color="bg-yellow-500" />
      </div>
    );

    const energyTrendChart = (
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm w-full h-full min-h-[300px]">
        <h3 className="font-bold text-gray-900 mb-4">Energy Consumption Trend</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={energyData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#888'}} />
            <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#888'}} />
            <Tooltip cursor={{fill: '#f8fafc'}} />
            <Bar dataKey="kwh" fill="#10b981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );

    const areaPieChart = (
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm w-full h-full min-h-[300px] relative">
        <h3 className="font-bold text-gray-900 mb-4">Energy by Area</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={pieData} innerRadius={60} outerRadius={80} paddingAngle={2} dataKey="value">
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );

    const costDistributionChart = (
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm w-full h-full min-h-[300px] relative">
        <h3 className="font-bold text-gray-900 mb-4">Cost Tariff Breakdown</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={costBreakdown} innerRadius={60} outerRadius={80} paddingAngle={2} dataKey="amount" nameKey="category">
              {costBreakdown.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip formatter={(value: any) => `$${Number(value).toFixed(2)}`} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );

    const productionTrendChart = (
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm w-full h-full min-h-[300px]">
        <h3 className="font-bold text-gray-900 mb-4">Production Trend (Units)</h3>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={productionData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#888'}} />
            <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#888'}} />
            <Tooltip cursor={{fill: '#f8fafc'}} />
            <Area type="monotone" dataKey="units" stroke="#8b5cf6" fill="#c4b5fd" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );

    const forecastChart = (
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm w-full h-full min-h-[300px]">
        <h3 className="font-bold text-gray-900 mb-4">Energy AI Forecast (Next 12h)</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={forecast}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#888'}} />
            <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#888'}} />
            <Tooltip cursor={{fill: '#f8fafc'}} />
            <Bar dataKey="predicted_kwh" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );

    const anomalyPanel = (
      <div className="bg-white rounded-xl p-5 border border-red-100 shadow-sm w-full h-full min-h-[300px] overflow-auto">
        <h3 className="font-bold text-gray-900 mb-1 flex items-center gap-2"><Bell className="text-red-500" size={18} /> Active Anomalies</h3>
        <p className="text-sm text-gray-500 mb-4">AI-detected abnormal loads requiring attention.</p>
        <div className="space-y-3">
          {anomalies.map((anom, idx) => (
            <div key={idx} className="p-3 border border-red-100 bg-red-50 rounded-lg text-sm">
              <div className="flex justify-between font-bold text-red-700 mb-1">
                <span>{anom.asset_name}</span>
                <span>{anom.time}</span>
              </div>
              <p className="text-red-600 mb-2">{anom.message}</p>
              <div className="flex gap-4 font-medium">
                <span className="text-gray-500">Exp: {anom.expected_kwh.toFixed(1)} kWh</span>
                <span className="text-gray-900">Act: {anom.actual_kwh.toFixed(1)} kWh</span>
                <span className="ml-auto bg-red-600 text-white px-2 py-0.5 rounded text-xs">{anom.severity}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );

    // AI Insight component
    if (activeTab === 'AI Insights') {
      return (
        <div className="flex flex-col h-full">
          <div className="mb-4"><h1 className="text-2xl font-bold text-gray-900">AI Enterprise Assistant</h1></div>
          <div className="flex-1 flex flex-col bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden text-sm">
            
            <div className="flex-1 overflow-auto p-6 space-y-4">
              {chatLog.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center">
                   <MessageSquare size={48} className="text-purple-500 mb-4 bg-purple-50 p-3 rounded-2xl" />
                   <h2 className="text-xl font-bold text-gray-900">Ask EnerOps AI</h2>
                   <p className="text-gray-500 max-w-md mt-2">Interact with the AI to investigate anomalies, summarize saving potential, or forecast costs.</p>
                </div>
              ) : (
                chatLog.map((log, idx) => (
                  <div key={idx} className={`flex ${log.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[70%] p-4 rounded-xl ${log.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-gray-100 text-gray-800 rounded-tl-none font-medium'}`}>
                      {log.text}
                    </div>
                  </div>
                ))
              )}
            </div>

            <form onSubmit={handleChatSubmit} className="p-4 border-t border-gray-100 bg-gray-50">
              <div className="flex items-center bg-white border border-gray-200 rounded-lg px-4 py-3 shadow-sm hover:border-indigo-300 focus-within:border-indigo-500 transition-colors">
                <Search size={20} className="text-gray-400 shrink-0" />
                <input 
                  type="text" 
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Why did energy consumption increase yesterday?" 
                  className="bg-transparent border-none outline-none flex-1 ml-3 placeholder-gray-400 text-gray-900" 
                />
                <button type="submit" disabled={!chatInput.trim()} className="ml-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white px-4 py-1.5 rounded-md font-medium transition-colors">
                   Send
                </button>
              </div>
            </form>
          </div>
        </div>
      );
    }

    return (
      <>
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">{activeTab === 'Dashboard' ? 'Good Morning, Ashish! 👋' : `${activeTab}`}</h1>
          <p className="text-gray-500 text-sm mt-1">{activeTab === 'Dashboard' ? "Here's how your plant is performing today." : `Viewing live analytics for ${activeTab}`}</p>
        </div>
        
        {sharedKPIs}

        <div className={`grid gap-6 mb-6 ${activeTab === 'Dashboard' ? 'grid-cols-3' : 'grid-cols-2'}`}>
           {/* Render context-aware layout */}
           {activeTab === 'Dashboard' && (
             <>
               <div className="col-span-2">{energyTrendChart}</div>
               <div className="col-span-1">{anomalyPanel}</div>
               <div className="col-span-1">{areaPieChart}</div>
               <div className="col-span-2">{forecastChart}</div>
             </>
           )}
           {activeTab === 'Energy Monitoring' && (
             <div className="col-span-2">{energyTrendChart}</div>
           )}
           {activeTab === 'Production' && (
             <>
                <div className="col-span-2">{productionTrendChart}</div>
                <div className="col-span-1">{areaPieChart}</div>
             </>
           )}
           {activeTab === 'Cost & Tariff' && (
             <>
                <div className="col-span-1">{costDistributionChart}</div>
                <div className="col-span-2 flex items-center justify-center bg-white rounded-xl border border-gray-100 p-6 shadow-sm text-gray-500">Peak vs Off-Peak Cost Simulation Component</div>
             </>
           )}
           {!['Dashboard', 'Energy Monitoring', 'Production', 'Cost & Tariff'].includes(activeTab) && (
              <div className="col-span-2 flex items-center justify-center bg-white rounded-xl border border-gray-100 h-64 shadow-sm text-gray-500">
                Detailed data grids for {activeTab} will load here.
              </div>
           )}
        </div>
      </>
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-[#0B1B3D] text-gray-400 flex flex-col">
        <div className="p-4 flex items-center gap-2 text-white font-bold text-xl mb-4">
          <Zap className="text-green-400" />
          EnerOps
          <span className="text-xs text-gray-500 block font-normal w-full -mt-1 leading-tight">Powering a Sustainable Tomorrow</span>
        </div>
        
        <nav className="flex-1 px-3 space-y-1">
          {sidebarItems.map((item) => (
            <button key={item.name} onClick={() => setActiveTab(item.name)} 
              className={`w-full text-left rounded-lg px-3 py-2 flex items-center gap-3 text-sm font-medium transition-colors ${activeTab === item.name ? 'bg-emerald-500 text-white' : 'hover:bg-slate-800'}`}>
              <item.icon size={18} /> {item.name}
            </button>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6 shrink-0">
          <div className="flex items-center bg-gray-100 rounded-lg px-3 py-1.5 w-96">
            <Search size={16} className="text-gray-400" />
            <input type="text" placeholder="Search for machines, lines, reports, insights..." className="bg-transparent border-none outline-none text-sm ml-2 w-full" />
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 text-sm text-gray-600 font-medium">
              <Calendar size={16} /> Fri, 12 Sep 2025
            </div>
            <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 text-sm font-medium">
              Plant 1 - Manufacturing <ChevronDown size={14} className="text-gray-400" />
            </div>
            <div className="flex items-center gap-4 text-gray-500">
              <Sun size={20} />
              <Bell size={20} />
            </div>
          </div>
        </header>

        {/* Dynamic Inner Content based on Sidebar state */}
        <div className="flex-1 overflow-auto p-6">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
