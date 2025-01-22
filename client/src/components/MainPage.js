import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./MainPage.css";
import logo from "../assets/MySKL_Logo.png";

function MainPage() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("loggedInUser");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      // If no logged-in user, redirect to login
      navigate("/");
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("loggedInUser");
    navigate("/");
  };

  if (!user) return null; // or show a loader while fetching user

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

        {/* MIDDLE CONTENT (Empty or repurpose as needed) */}
        <div className="content"></div>

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
