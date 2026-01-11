import React from "react";
import { FileText, ExternalLink } from "lucide-react";

// Component to display the extracted text and a link to the original PDF
const CVViewer = ({ text, cv_id }) => {
  return (
    <div className="flex flex-col h-full w-full bg-white">
      <div className="flex items-center justify-between p-3 border-b bg-gray-50 flex-none">
        <div className="flex items-center text-blue-800">
          <FileText className="w-5 h-5 mr-2" />
          <span className="font-bold text-sm uppercase">Texte Extrait</span>
        </div>

        {/* Check if cv_id exists to create the link to the backend static folder */}
        {cv_id && (
          <a
            href={`http://localhost:8000/static/${cv_id}.pdf`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center text-xs text-blue-600 hover:text-blue-800 font-medium transition"
          >
            <ExternalLink className="w-3 h-3 mr-1" />
            Voir PDF Original
          </a>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 bg-slate-200">
        <div className="bg-white shadow-lg p-8 min-h-full w-full mx-auto">
          <pre className="whitespace-pre-wrap font-mono text-[13px] leading-relaxed text-gray-800">
            {text || "Chargement du texte..."}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default CVViewer;