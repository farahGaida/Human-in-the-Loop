import { useEffect, useState } from "react";
import { cvService } from "../api";
import { Clock, CheckCircle, Database, Edit3, ListChecks, Zap } from "lucide-react";

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    cvService.getMetrics().then(res => setMetrics(res.data));
  }, []);

  if (!metrics) return (
    <div className="flex items-center justify-center h-screen bg-[#F8FAFC]">
       <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
    </div>
  );

  // Calculate percentage of work done
  const progress = (metrics.corrected / metrics.total) * 100;

  // Configuration for the stat cards
  const stats = [
    { label: "Dataset", value: metrics.total, sub: "CVs totaux", icon: <Database size={20}/>, color: "text-blue-600", bg: "bg-blue-50" },
    { label: "Validation", value: metrics.corrected, sub: `${Math.round(progress)}% complété`, icon: <CheckCircle size={20}/>, color: "text-green-600", bg: "bg-green-50" },
    { label: "CV Modifiés", value: metrics.actual_changes, sub: "Documents rectifiés", icon: <Edit3 size={20}/>, color: "text-amber-600", bg: "bg-amber-50" },
    { label: "Champs Corrigés", value: metrics.total_fields_fixed, sub: "Entités fixées", icon: <ListChecks size={20}/>, color: "text-red-600", bg: "bg-red-50" },
    { label: "Temps Moyen", value: `${metrics.avg_time}s`, sub: "par document", icon: <Clock size={20}/>, color: "text-purple-600", bg: "bg-purple-50" },
  ];

  return (
    <div className="p-8 bg-[#F8FAFC] min-h-screen">
      <div className="max-w-7xl mx-auto">
        
        <div className="mb-10">
          <h2 className="text-3xl font-black text-slate-900 tracking-tighter uppercase">Pipeline Analytics</h2>
          <p className="text-slate-500 font-medium">Monitoring du flux Human-in-the-Loop</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-10">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
              <div className={`w-10 h-10 ${stat.bg} ${stat.color} rounded-xl flex items-center justify-center mb-4`}>
                {stat.icon}
              </div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">{stat.label}</p>
              <p className="text-3xl font-black text-slate-900 mb-1">{stat.value || 0}</p>
              <p className="text-[11px] font-medium text-slate-500">{stat.sub}</p>
            </div>
          ))}
        </div>

        {/* Info & Action Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white p-8 rounded-[2rem] border border-slate-100 shadow-sm flex flex-col justify-center">
            <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center">
              <Zap className="mr-2 text-blue-600" size={20} /> Analyse du Ground Truth
            </h3>
            <p className="text-slate-600 leading-relaxed">
              Sur les <span className="font-bold text-slate-900">{metrics.corrected} CV</span> validés, 
              l'intervention humaine a permis de corriger <span className="font-bold text-red-600">{metrics.total_fields_fixed} entités</span>. 
              Ces données corrigées servent désormais de base d'entraînement pour améliorer la précision du modèle NER (Named Entity Recognition).
            </p>
          </div>

          <div className="bg-slate-900 p-8 rounded-[2rem] flex flex-col items-center justify-center text-center text-white">
            <h4 className="font-bold text-lg mb-2">Cycle de Réentraînement</h4>
            <p className="text-slate-400 text-sm mb-6">
              {metrics.corrected >= 15 
                ? "Seuil atteint. Prêt pour la V2." 
                : `${15 - metrics.corrected} CV restants.`}
            </p>
            <button className={`w-full py-3 rounded-xl font-bold text-xs uppercase tracking-widest transition-all ${
              metrics.corrected >= 15 ? "bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-900/20" : "bg-slate-800 text-slate-600"
            }`}>
              Générer Modèle V2
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}