import React from "react";
import { CheckCircle, Building2, User, Mail, Phone, GraduationCap, Briefcase } from "lucide-react";

// Component for the correction form side of the application
const CorrectionForm = ({ cv, setCv, onSave }) => {
    return (
        <div className="space-y-5 p-5 bg-white rounded-xl shadow-md border border-gray-100">
            <h3 className="text-xl font-extrabold text-gray-800 border-b pb-3 flex justify-between items-center">
                <span className="flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
                    Champs à corriger
                </span>
                <span className="text-[10px] px-2 py-1 bg-gray-100 rounded font-mono text-gray-500">
                    ID: {cv.cv_id}
                </span>
            </h3>
            
            {/* Section : Personal Information */}
            <div className="space-y-4">
                <div>
                    <label className="flex items-center text-xs font-bold text-blue-700 uppercase mb-1">
                        <User className="w-3 h-3 mr-1" /> Nom Complet
                    </label>
                    <input 
                        className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition"
                        value={cv.predicted_name || ""} 
                        onChange={(e) => setCv({...cv, predicted_name: e.target.value})}
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="flex items-center text-xs font-bold text-blue-700 uppercase mb-1">
                            <Mail className="w-3 h-3 mr-1" /> Email
                        </label>
                        <input 
                            className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition"
                            value={cv.predicted_email || ""} 
                            onChange={(e) => setCv({...cv, predicted_email: e.target.value})}
                        />
                    </div>
                    <div>
                        <label className="flex items-center text-xs font-bold text-blue-700 uppercase mb-1">
                            <Phone className="w-3 h-3 mr-1" /> Téléphone
                        </label>
                        <input 
                            className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition"
                            value={cv.predicted_phone || ""} 
                            onChange={(e) => setCv({...cv, predicted_phone: e.target.value})}
                        />
                    </div>
                </div>
            </div>

            {/* Section : Professional Background */}
            <div className="pt-2 space-y-4">
                <div>
                    <label className="flex items-center text-xs font-bold text-blue-700 uppercase mb-1">
                        <Building2 className="w-3 h-3 mr-1" /> Dernière Organisation
                    </label>
                    <input 
                        className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition"
                        value={cv.predicted_orgs || ""} 
                        onChange={(e) => setCv({...cv, predicted_orgs: e.target.value})}
                    />
                </div>

                <div>
                    <label className="flex items-center text-xs font-bold text-blue-700 uppercase mb-1">
                        <GraduationCap className="w-3 h-3 mr-1" /> Éducation / Diplômes
                    </label>
                    <textarea 
                        rows="3"
                        className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition"
                        value={cv.predicted_education || ""} 
                        onChange={(e) => setCv({...cv, predicted_education: e.target.value})}
                    />
                </div>

                <div>
                    <label className="flex items-center text-xs font-bold text-blue-700 uppercase mb-1">
                        <Briefcase className="w-3 h-3 mr-1" /> Expérience Professionnelle
                    </label>
                    <textarea 
                        rows="6"
                        className="w-full p-2.5 bg-blue-50 border border-blue-100 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition"
                        placeholder="Détails des expériences..."
                        value={cv.predicted_experience || ""} 
                        onChange={(e) => setCv({...cv, predicted_experience: e.target.value})}
                    />
                </div>
            </div>

            <button 
                onClick={onSave}
                className="w-full bg-green-600 text-white py-4 rounded-xl font-black text-lg hover:bg-green-700 active:scale-[0.98] transition-all shadow-md hover:shadow-lg mt-4 flex justify-center items-center"
            >
                VALIDER & SUIVANT
            </button>
        </div>
    );
};

export default CorrectionForm;