import React, { useState, useEffect } from "react";
import { cvService } from "../api";
import CVViewer from "../components/CVViewer";
import CorrectionForm from "../components/CorrectionForm";
import { Clock } from "lucide-react"; 

const Annotator = () => {
  const [cv, setCv] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);

  // Fetch the next CV that needs validation from the backend
  const loadData = async () => {
    try {
      const data = await cvService.getPending();
      if (data && data.length > 0) {
        setCv(data[0]);
        const now = Date.now();
        setStartTime(now); // Start the timer for this CV
        setElapsedTime(0); // Reset visual counter
      } else {
        setCv(null); // No more CVs to process
      }
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Timer logic
  useEffect(() => {
    let interval;
    if (cv && startTime) {
      interval = setInterval(() => {
        const seconds = Math.floor((Date.now() - startTime) / 1000);
        setElapsedTime(seconds);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [cv, startTime]);

  // Save the human corrections and the time spent back to the database
  const handleSave = async () => {
    const duration = (Date.now() - startTime) / 1000;

    const correctionData = {
      corrected_name: cv.predicted_name,
      corrected_email: cv.predicted_email,
      corrected_phone: cv.predicted_phone,
      corrected_orgs: cv.predicted_orgs,
      corrected_education: cv.predicted_education,
      corrected_experience: cv.predicted_experience,
      correction_time_seconds: duration,
      status: "validated",
    };

    try {
      await cvService.submitCorrection(cv.id, correctionData);
      loadData(); // Load the next CV automatically
    } catch (error) {
      console.error("Erreur lors de la sauvegarde:", error);
      alert("Erreur lors de la sauvegarde.");
    }
  };

  // Convert seconds into MM:SS format
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Show finished state if no CVs are left
  if (!cv)
    return (
      <div className="flex items-center justify-center h-full bg-gray-50">
        <div className="text-center p-12 bg-white shadow-xl rounded-2xl">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="text-2xl font-bold text-gray-800">Mission terminée !</h2>
          <p className="text-gray-500 mt-2">Tous les CV ont été validés.</p>
        </div>
      </div>
    );

  return (
    <div className="flex h-full w-full overflow-hidden">
      {/* LEFT SIDE: Extracted Text Visualization */}
      <div className="w-1/2 h-full border-r border-gray-200 bg-white">
        <CVViewer text={cv.raw_text} cv_id={cv.cv_id} />
      </div>

      {/* RIGHT SIDE: Correction Form and Real-time Timer */}
      <div className="w-1/2 h-full overflow-y-auto p-6 bg-gray-50">
        <div className="max-w-3xl mx-auto">
          
          {/* Form Header with Timer UI */}
          <div className="flex justify-between items-end mb-4 px-2">
            <div>
              <h2 className="text-lg font-bold text-gray-700">Correction Manuelle</h2>
              <p className="text-xs text-gray-500">ID: {cv.cv_id}</p>
            </div>
            <div className="flex items-center bg-white px-3 py-1 rounded-full shadow-sm border border-gray-200">
              <Clock className="w-3 h-3 mr-2 text-blue-500" />
              <span className="text-sm font-mono font-medium text-gray-600">
                {formatTime(elapsedTime)}
              </span>
            </div>
          </div>

          <CorrectionForm cv={cv} setCv={setCv} onSave={handleSave} />
          
          <div className="mt-6 p-4 bg-blue-50 border border-blue-100 rounded-lg">
             <p className="text-xs text-blue-600 leading-tight">
               <strong>Note MLOps :</strong> Le temps passé sur chaque CV est enregistré 
               pour mesurer la performance du pipeline de labellisation.
             </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Annotator;