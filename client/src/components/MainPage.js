import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MainPage.css";
import logo from "../assets/MySKL_Logo.png";

function MainPage() {
  const [user, setUser] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("loggedInUser");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      navigate("/");
    }
  }, [navigate]);

  useEffect(() => {
    // Fetch today's schedules
    const fetchSchedules = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/today-schedules");
        const result = await response.json();

        if (response.ok) {
          setSchedules(result.schedules);
        } else {
          console.error("Failed to fetch schedules:", result.error);
        }
      } catch (err) {
        console.error("Error fetching schedules:", err);
      }
    };

    fetchSchedules();
  }, []);
  const handleMatch = (studentId) => {
    alert(`Matched with student ID: ${studentId}`);
    // Add logic to handle the "match" action (e.g., send a request to the server)
  };
  

  const handleLogout = () => {
    localStorage.removeItem("loggedInUser");
    navigate("/");
  };

  if (!user) return null;

  return (
    <div className="main-container">
      <div className="main-box">
        {/* TOP BAR */}
        <div className="header-bar">
          <img src={logo} alt="App Logo" className="bar-logo" />
          <h2 className="header-greeting">Welcome, {user.Stname}!</h2>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>

        {/* MIDDLE CONTENT */}
        <div className="content">
          <h3>Today's Schedules</h3>
          <div className="schedule-list">
            {schedules.length > 0 ? (
              schedules.map((schedule, index) => (
                <div className="schedule-item" key={index}>
                  <p><strong>Student Name:</strong> {schedule.StName}</p>
                  <p><strong>Slots:</strong> {Object.values(schedule).slice(1, 9).join(", ")}</p>
                  <button className="match-btn" onClick={() => handleMatch(schedule.StudentID)}>
                    Match
                  </button>
                </div>
              ))
            ) : (
              <p>No schedules for today.</p>
            )}
          </div>
        </div>

        {/* BOTTOM BAR */}
        <div className="footer-bar">
          <button className="footer-btn">Explore</button>
          <button 
            className="footer-btn"
            onClick={() => navigate("/schedule")}
          >
            MySchedule
          </button>
          <button 
            className="footer-btn"
            onClick={() => navigate("/myprofile")}
          >
            MyProfile
          </button>
        </div>
      </div>
    </div>
  );
}

export default MainPage;
