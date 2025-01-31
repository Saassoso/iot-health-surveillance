import React from "react";
import PatientChart from "./components/PatientChart.jsx";

function App() {
  return (
    <div className="p-5">
      <h1 className="text-2xl font-bold text-center mb-5">Patient Monitoring Dashboard</h1>
      <PatientChart />
    </div>
  );
}

export default App;

