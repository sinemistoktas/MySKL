import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./MySchedule.css";
import logo from "../assets/MySKL_Logo.png";

function MySchedule() {
  const [user, setUser] = useState(null);
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [slots, setSlots] = useState({
    Slot1: 0,
    Slot2: 0,
    Slot3: 0,
    Slot4: 0,
    Slot5: 0,
    Slot6: 0,
    Slot7: 0,
    Slot8: 0,
  });

  const timeSlots = {
    Slot1: "10-11",
    Slot2: "11-12",
    Slot3: "12-13",
    Slot4: "13-14",
    Slot5: "14-15",
    Slot6: "15-16",
    Slot7: "16-17",
    Slot8: "17-18",
  };

  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("loggedInUser");
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      setUser(userData);
      fetchSchedule(userData.StudentID);
    } else {
      navigate("/");
    }
  }, [navigate]);

  const fetchSchedule = async (studentId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/schedule/${studentId}`);
      const data = await response.json();
      if (data.hasSchedule) {
        setSchedule(data.schedule);
        setSlots({
          Slot1: data.schedule.Slot_1,
          Slot2: data.schedule.Slot_2,
          Slot3: data.schedule.Slot_3,
          Slot4: data.schedule.Slot_4,
          Slot5: data.schedule.Slot_5,
          Slot6: data.schedule.Slot_6,
          Slot7: data.schedule.Slot_7,
          Slot8: data.schedule.Slot_8,
        });
      } else {
        setSchedule(null);
      }
      setLoading(false);
    } catch (error) {
      console.error("Error fetching schedule:", error);
      setLoading(false);
    }
  };

  const handleSlotChange = (slotKey) => {
    setSlots((prev) => ({
      ...prev,
      [slotKey]: prev[slotKey] === 0 ? 1 : 0,
    }));
  };

  const handleCreateSchedule = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          StudentID: user.StudentID,
          Date: new Date().toISOString().split("T")[0],
          Slots: Object.values(slots),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message);
        setShowForm(false);
        fetchSchedule(user.StudentID);
      } else {
        alert(data.error || "Failed to save schedule");
      }
    } catch (error) {
      console.error("Error creating schedule:", error);
      alert("Error saving schedule. Please try again.");
    }
  };

  const handleDeleteSchedule = async () => {
    if (!schedule) return;
  
    if (window.confirm("Are you sure you want to delete this schedule?")) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/schedule/${user.StudentID}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ Date: new Date().toISOString().split("T")[0] }), // Pass the Date if required by backend
        });
  
        if (response.ok) {
          alert("Schedule deleted successfully");
          setSchedule(null);
          fetchSchedule(user.StudentID);
        } else {
          const error = await response.json();
          alert(error.error || "Failed to delete schedule");
        }
      } catch (error) {
        console.error("Error deleting schedule:", error);
        alert("Error deleting schedule. Please try again.");
      }
    }
  };
  

  if (loading) return <div>Loading...</div>;

  return (
    <div className="schedule-container">
      <div className="schedule-box">
        <div className="header-bar">
          <img src={logo} alt="Logo" className="bar-logo" />
          <h2 className="header-title">My Schedule</h2>
          <button className="logout-btn" onClick={() => navigate("/")}>
            Logout
          </button>
        </div>

        <div className="schedule-content">
          {schedule ? (
            <div>
              <div className="schedule-grid">
                {Object.entries(timeSlots).map(([slot, time]) => (
                  <div
                    key={slot}
                    className={`schedule-slot ${slots[slot] === 1 ? "available" : ""}`}
                  >
                    <p>{time}</p>
                  </div>
                ))}
              </div>
              <div className="schedule-actions">
                <button onClick={handleDeleteSchedule} className="delete-btn">
                  Delete Schedule
                </button>
              </div>
            </div>
          ) : showForm ? (
            <div className="schedule-form">
              <h3>Select your library hours</h3>
              <p className="form-subtitle">
                Tap the time slots when you'll be at the library
              </p>
              <div className="schedule-grid">
                {Object.entries(timeSlots).map(([slot, time]) => (
                  <div
                    key={slot}
                    className={`schedule-slot ${slots[slot] === 1 ? "available" : ""}`}
                    onClick={() => handleSlotChange(slot)}
                  >
                    <p>{time}</p>
                  </div>
                ))}
              </div>
              <div className="form-buttons">
                <button
                  onClick={() => setShowForm(false)}
                  className="cancel-btn"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateSchedule}
                  className="create-schedule-btn"
                >
                  Save
                </button>
              </div>
            </div>
          ) : (
            <div className="no-schedule">
              <p>No schedule set for today</p>
              <button
                onClick={() => setShowForm(true)}
                className="create-schedule-btn"
              >
                Set Schedule
              </button>
            </div>
          )}
        </div>

        <div className="footer-bar">
          <button className="footer-btn" onClick={() => navigate("/main")}>
            Explore
          </button>
          <button className="footer-btn">MySchedule</button>
          <button className="footer-btn" onClick={() => navigate("/myprofile")}>
            MyProfile
          </button>
        </div>
      </div>
    </div>
  );
}

export default MySchedule;
