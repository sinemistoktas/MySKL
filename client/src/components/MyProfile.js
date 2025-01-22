import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MyProfile.css";
import logo from "../assets/MySKL_Logo.png";

function MyProfile() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("loggedInUser");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      // If no user is found, redirect to login
      navigate("/");
    }
  }, [navigate]);

  // Logout on top bar
  const handleLogout = () => {
    localStorage.removeItem("loggedInUser");
    navigate("/");
  };

  // If user is null, return null or a loader
  if (!user) return null;

  // Destructure user fields
  const {
    StudentID,
    Stname,
    Major,
    Gender,
    stRating,
    Level,
    XP
  } = user;

  return (
    <div className="profile-container">
      <div className="profile-box">
        
        {/* ========== TOP BAR ========== */}
        <div className="header-bar">
          <img src={logo} alt="Logo" className="bar-logo" />
          <h2 className="header-title">My Profile</h2>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>

        {/* ========== CONTENT ========== */}
        <div className="profile-content">
          <h3>Personal Information</h3>
          <p><strong>Name:</strong> {Stname}</p>
          <p><strong>Student ID:</strong> {StudentID}</p>
          <p><strong>Major:</strong> {Major}</p>
          <p><strong>Gender:</strong> {Gender}</p>
          <p><strong>Rating:</strong> {stRating ?? "N/A"}</p>
          <p><strong>Level:</strong> {Level ?? "N/A"}</p>
          <p><strong>XP:</strong> {XP ?? "N/A"}</p>
        </div>

        {/* ========== FOOTER BAR ========== */}
        <div className="footer-bar">
          <button 
            className="footer-btn" 
            onClick={() => navigate("/main")}
          >
            Explore
          </button>
          <button 
            className="footer-btn" 
            onClick={() => navigate("/schedule")}
          >
            MySchedule
          </button>
          <button 
            className="footer-btn" 
          >
            MyProfile
          </button>
        </div>
      </div>
    </div>
  );
}

export default MyProfile;
