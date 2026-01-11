import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Annotator from "./pages/Annotator";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <Router>
      <div className="h-screen flex flex-col">
        {/* navigaation bar */}
        <nav className="bg-blue-900 text-white p-4 flex justify-between items-center shadow-lg">
          <div className="font-black tracking-tighter text-xl">Human in the Loop</div>
          <div className="space-x-6">
            <Link to="/" className="hover:text-blue-400 font-medium transition">Annotateur</Link>
            <Link to="/dashboard" className="hover:text-blue-400 font-medium transition">Dashboard</Link>
          </div>
        </nav>

        {/* page content */}
        <div className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<Annotator />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;