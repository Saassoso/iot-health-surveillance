import React, { useEffect, useState } from "react";
import { database, ref, onValue } from "../firebase";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip,
  Title,
} from "chart.js";

// Register necessary components
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Legend, Tooltip, Title);

const PatientDataChart = () => {
  const [patientData, setPatientData] = useState([]);

  useEffect(() => {
    const dataRef = ref(database, "patient_data"); // Firebase path
    onValue(dataRef, (snapshot) => {
      if (snapshot.exists()) {
        const rawData = snapshot.val();

        const formattedData = Object.entries(rawData).map(([id, entry]) => ({
          id, // Patient ID
          timestamp: new Date(entry.timestamp * 1000), // Convert Unix timestamp
          heartRate: entry.data?.heart_rate?.avg ?? null,
          spo2: entry.data?.spo2?.avg ?? null,
          temperature: entry.data?.temperature?.avg ?? null,
        }));

        setPatientData(formattedData);
      }
    });
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold text-center mb-4">Patient Health Monitoring</h2>

      <Line
        data={{
          labels: patientData.map((d) =>
            d.timestamp.toLocaleTimeString("en-US", { hour12: false })
          ),
          datasets: [
            {
              label: "Heart Rate (BPM)",
              data: patientData.map((d) => d.heartRate),
              borderColor: "red",
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              borderWidth: 2,
              pointRadius: 3,
              tension: 0.3, // Smooth curves
            },
            {
              label: "SpO2 (%)",
              data: patientData.map((d) => d.spo2),
              borderColor: "blue",
              backgroundColor: "rgba(0, 0, 255, 0.2)",
              borderWidth: 2,
              pointRadius: 3,
              tension: 0.3,
            },
            {
              label: "Temperature (°C)",
              data: patientData.map((d) => d.temperature),
              borderColor: "green",
              backgroundColor: "rgba(0, 255, 0, 0.2)",
              borderWidth: 2,
              pointRadius: 3,
              tension: 0.3,
            },
          ],
        }}
        options={{
          responsive: true,
          plugins: {
            legend: {
              display: true,
              position: "top",
              labels: {
                font: { size: 14 },
                color: "#333",
              },
            },
            tooltip: {
              mode: "index",
              intersect: false,
            },
            title: {
              display: true,
              text: "Real-Time Patient Data",
              font: { size: 16 },
              color: "#333",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Time",
                font: { size: 14 },
                color: "#666",
              },
            },
            y: {
              title: {
                display: true,
                text: "Measurements",
                font: { size: 14 },
                color: "#666",
              },
            },
          },
        }}
      />
    </div>
  );
};

export default PatientDataChart;
