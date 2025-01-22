import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MainPage.css";
import logo from "../assets/MySKL_Logo.png";

function MainPage() {
  const [user, setUser] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [matchedSchedule, setMatchedSchedule] = useState(null); // Track the matched schedule
  const [selectedRating, setSelectedRating] = useState(0); // Track the selected rating
  const [ratingSubmitted, setRatingSubmitted] = useState(false); // Track if rating was submitted
  const [availableTable, setAvailableTable] = useState(null); 
  const [error, setError] = useState(null);
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

    const fetchAvailableTable = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/available-table");
        const result = await response.json();

        if (response.ok) {
          setAvailableTable(result.table);
        } else {
          setError(result.message || "No available table found.");
        }
      } catch (err) {
        console.error("Error fetching available table:", err);
        setError("An error occurred while fetching available table.");
      }
    };

    fetchSchedules();
    fetchAvailableTable();
  }, []);

  const handleMatch = async (rateeId, tableId = "0000") => {
    const today = new Date().toISOString().split("T")[0];
    try {
      const response = await fetch("http://127.0.0.1:5000/create-agreement", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ratorID: user.StudentID,
          rateeID: rateeId,
          TableID: tableId,
          AgrDate: today,
        }),
      });

      const result = await response.json();
      if (response.ok) {
        alert("Agreement created successfully!");
        const matched = schedules.find((schedule) => schedule.StudentID === rateeId);
        setMatchedSchedule(matched); // Set the matched schedule
      } else {
        alert(result.error || "Failed to create agreement.");
      }
    } catch (err) {
      console.error("Error creating agreement:", err);
      alert("An error occurred. Please try again.");
    }
  };

  const handleSubmitRating = () => {
    if (selectedRating === 0) {
      alert("Please select a rating before submitting.");
      return;
    }

    alert("Rating submitted successfully!");
    setRatingSubmitted(true); // Mark rating as submitted
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
          <h2 className="header-greeting">Welcome, {user.StName}!</h2>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>

        {/* HEADER SECTION */}
      <div className="page-header">
        <h1>Library Desk Availability</h1>
        <p>Find the earliest available desk or explore today's schedules.</p>
      </div>

        {/* EARLIEST AVAILABLE TABLE */}
        <div className="available-table-section">
          <h3>Earliest Available Table</h3>
          {error && <p className="error-message">{error}</p>}
          {availableTable ? (
            <div className="available-table">
              <p><strong>Table Number:</strong> {availableTable.TableNum}</p>
              <p><strong>Floor:</strong> {availableTable.FloorNumber}</p>
              <p><strong>Has Plug:</strong> {availableTable.HasPlug ? "Yes" : "No"}</p>
              <div className="table-container">
                {getImageForTable(availableTable.Image)}
              </div>
            </div>
          ) : (
            !error && <p>Loading available table...</p>
          )}
        </div>

        {/* MIDDLE CONTENT */}
        <div className="content">
          {ratingSubmitted ? ( // Check if rating has been submitted
            <div className="success-message">
              <h3>You matched and rated!</h3>
            </div>
          ) : matchedSchedule ? (
            <div className="schedule-item">
              <p>
                <strong>Student Name:</strong> {matchedSchedule.StName}
              </p>
              <p>
                <strong>Slots:</strong>{" "}
                {Object.values(matchedSchedule).slice(1, 9).join(", ")}
              </p>
              <div className="table-container">
                {/* Show the table image or fallback */}
                <p>Table ID: {matchedSchedule.TableID}</p>
              </div>
              <div className="rating-section">
                <h4>Rate this agreement:</h4>
                {[1, 2, 3, 4, 5].map((rating) => (
                  <button
                    key={rating}
                    className={`rating-btn ${
                      selectedRating === rating ? "selected" : ""
                    }`}
                    onClick={() => setSelectedRating(rating)}
                  >
                    {rating}
                  </button>
                ))}
                <button
                  className="submit-rating-btn"
                  onClick={handleSubmitRating}
                >
                  Submit Rating
                </button>
              </div>
            </div>
          ) : schedules.length > 0 ? (
            schedules.map((schedule, index) => (
              <div className="schedule-item" key={index}>
                <p>
                  <strong>Student Name:</strong> {schedule.StName}
                </p>
                <p>
                  <strong>Slots:</strong>{" "}
                  {Object.values(schedule).slice(1, 9).join(", ")}
                </p>
                <button
                  className="match-btn"
                  onClick={() =>
                    handleMatch(schedule.StudentID, schedule.TableID || "0000")
                  }
                >
                  Match
                </button>
              </div>
            ))
          ) : (
            <p>No schedules for today.</p>
          )}
        </div>

        {/* BOTTOM BAR */}
        <div className="footer-bar">
          <button className="footer-btn">Explore</button>
          <button className="footer-btn" onClick={() => navigate("/schedule")}>
            MySchedule
          </button>
          <button className="footer-btn" onClick={() => navigate("/myprofile")}>
            MyProfile
          </button>
        </div>
      </div>
    </div>
  );
}

export default MainPage;
