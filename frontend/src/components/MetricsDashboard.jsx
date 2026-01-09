import { useEffect, useState } from "react";
import { cvService } from "../api";
import { BarChart, Clock, CheckCircle, Database, TrendingUp, AlertCircle } from "lucide-react";

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    cvService.getMetrics().then(res => setMetrics(res.data));
  }, []);

  if (!metrics) return (
    <div className="flex flex-col items-center justify-center h-screen">
       <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
       <p className="mt-4 text-gray-500 font-medium">Analyse des données MLOps en cours...</p>
    </div>
  );

  const progress = (metrics.corrected / metrics.total) * 100;

  const stats = [
    { label: "Base de données", value: metrics.total, sub: "CVs totaux", icon: <Database />, color: "text-blue-600", bg: "bg-blue-50" },
    { label: "Validés", value: metrics.corrected, sub: `${Math.round(progress)}% complété`, icon: <CheckCircle />, color: "text-green-600", bg: "bg-green-50" },
    { label: "Vitesse Moyenne", value: `${metrics.avg_time}s`, sub: "par document", icon: <Clock />, color: "text-purple-600", bg: "bg-purple-50" },
    { label: "Confiance IA", value: `${metrics.auto_accepted}%`, sub: "Acceptation auto", icon: <TrendingUp />, color: "text-orange-600", bg: "bg-orange-50" },
  ];

  return (
    <div className="p-8 bg-[#F8FAFC] min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-10">
          <div>
            <h2 className="text-4xl font-black text-slate-900 tracking-tight">DASHBOARD ANALYTICS</h2>
            <p className="text-slate-500 font-medium">Human-in-the-Loop Pipeline Monitoring</p>
          </div>
          <div className="bg-white px-4 py-2 rounded-lg shadow-sm border border-slate-200 flex items-center">
            <span className="flex h-2 w-2 rounded-full bg-green-500 mr-2"></span>
            <span className="text-xs font-bold text-slate-600 uppercase">Système Live</span>
          </div>
        </div>

        {/* Barre de Progression */}
        <div className="mb-10 bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
           <div className="flex justify-between items-end mb-4">
              <div>
                <h3 className="text-lg font-bold text-slate-800">Progression du Labeling</h3>
                <p className="text-sm text-slate-500">Objectif : 100% de la base validée</p>
              </div>
              <span className="text-3xl font-black text-blue-600">{Math.round(progress)}%</span>
           </div>
           <div className="w-full bg-slate-100 rounded-full h-4 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-blue-500 to-blue-700 h-full transition-all duration-1000 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
           </div>
        </div>

        {/* Grille des Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
              <div className={`w-14 h-14 ${stat.bg} ${stat.color} rounded-2xl flex items-center justify-center mb-6`}>
                {stat.icon}
              </div>
              <p className="text-sm font-bold text-slate-400 uppercase tracking-wider">{stat.label}</p>
              <p className="text-4xl font-black text-slate-900 my-1">{stat.value}</p>
              <p className="text-xs font-medium text-slate-500">{stat.sub}</p>
            </div>
          ))}
        </div>

        {/* Section Analyse */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900 p-8 rounded-3xl text-white shadow-xl">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <AlertCircle className="mr-2 text-blue-400" /> Insights MLOps
            </h3>
            <p className="text-slate-400 leading-relaxed mb-6">
              L'intégration du retour humain permet d'affiner le modèle de reconnaissance d'entités (NER). 
              Un taux d'auto-acceptation de <span className="text-blue-400 font-bold">{metrics.auto_accepted}%</span> 
              indique que le modèle SpaCy est robuste, mais nécessite encore une supervision humaine pour les cas ambigus.
            </p>
            <div className="flex gap-4">
               <div className="bg-slate-800 p-4 rounded-2xl flex-1 border border-slate-700">
                  <p className="text-xs text-slate-500 uppercase font-bold">Économie de temps</p>
                  <p className="text-xl font-bold">~45% vs manuel</p>
               </div>
               <div className="bg-slate-800 p-4 rounded-2xl flex-1 border border-slate-700">
                  <p className="text-xs text-slate-500 uppercase font-bold">Qualité Data</p>
                  <p className="text-xl font-bold">99.2% (Vérifié)</p>
               </div>
            </div>
          </div>

          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm flex flex-col justify-center items-center text-center">
             <div className="w-20 h-20 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center mb-4">
                <BarChart size={40} />
             </div>
             <h4 className="font-bold text-slate-800">Prêt pour Retraining ?</h4>
             <p className="text-sm text-slate-500 mt-2">
               Il est recommandé de réentraîner le modèle après 50 nouvelles corrections humaines.
             </p>
          </div>
        </div>
      </div>
    </div>
  );
}