// Alerts.js
import React, { useState, useEffect } from "react";
import "./Alerts.css";

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [senderID, setSenderID] = useState("");
  const [alertTime, setAlertTime] = useState("");

  // Fetch alerts from the backend
  const fetchAlerts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/alerts", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (response.ok) {
        setAlerts(data.alerts);
      } else {
        alert(data.error || "Failed to fetch alerts.");
      }
    } catch (error) {
      console.error("Error fetching alerts:", error);
      alert("Error connecting to the server.");
    }
  };

  // Create a new alert
  const handleCreateAlert = async (e) => {
    e.preventDefault();
    if (!senderID || !alertTime) {
      alert("Please fill in all fields.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/alerts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          senderID: parseInt(senderID),
          AlertTime: alertTime,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        fetchAlerts(); // Refresh alerts after creation
      } else {
        alert(data.error || "Failed to create alert.");
      }
    } catch (error) {
      console.error("Error creating alert:", error);
      alert("Error connecting to the server.");
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  return (
    <div className="alerts-container">
      <h2>Library Alerts</h2>
      <form onSubmit={handleCreateAlert} className="alert-form">
        <div className="form-group">
          <label htmlFor="senderID">Sender ID</label>
          <input
            type="text"
            id="senderID"
            value={senderID}
            onChange={(e) => setSenderID(e.target.value)}
            placeholder="Enter your student ID"
          />
        </div>
        <div className="form-group">
          <label htmlFor="alertTime">Alert Time</label>
          <input
            type="datetime-local"
            id="alertTime"
            value={alertTime}
            onChange={(e) => setAlertTime(e.target.value)}
          />
        </div>
        <button type="submit" className="alert-btn">Create Alert</button>
      </form>

      <ul className="alerts-list">
        {alerts.map((alert, index) => (
          <li key={index} className="alert-item">
            <strong>Sender:</strong> {alert.senderID} <br />
            <strong>Time:</strong> {new Date(alert.AlertTime).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Alerts;
