import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MyProfile.css";
import logo from "../assets/MySKL_Logo.png";

function MyProfile() {
  const [user, setUser] = useState(null);
  const [emoji, setEmoji] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("loggedInUser");
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);
      if (parsedUser) {
        fetchEmoji(parsedUser.StudentID); // Fetch emoji for premium users
      }
    } else {
      navigate("/");
    }
  }, [navigate]);

  // Fetch emoji for premium users
  const fetchEmoji = async (studentId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/premium-emoji/${studentId}`);
      const result = await response.json();

      if (response.ok && result.emoji) {
        setEmoji(result.emoji); // Set the emoji in the state
        
      } else {
        console.error("Failed to fetch emoji:", result.error);
      }
    } catch (err) {
      console.error("Error fetching emoji:", err);
    }
  };

  // Render the emoji image
  const getEmojiImage = () => {
    if (!emoji) return null;
    
    console.log("Failed to fetch emoji:", emoji);
    return (

      <img
        src={`/emojis/${emoji}.png`} // Use the dynamically fetched emoji value
        alt="Premium Emoji"
        className="emoji-icon"
      />
    );
  };

  // Logout functionality
  const handleLogout = () => {
    localStorage.removeItem("loggedInUser");
    navigate("/");
  };

  if (!user) return null;

  const { StudentID, StName, Major, Gender, StRating, Level, XP } = user;

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
          {emoji && (
            <div className="emoji-container">
              {getEmojiImage()}
            </div>
          )}
          <p><strong>Name:</strong> {StName || "Not Available"}</p>
          <p><strong>Student ID:</strong> {StudentID}</p>
          <p><strong>Major:</strong> {Major}</p>
          <p><strong>Gender:</strong> {Gender}</p>
          <p><strong>Rating:</strong> {StRating ?? "N/A"}</p>
          <p><strong>Level:</strong> {Level ?? "N/A"}</p>
          <p><strong>XP:</strong> {XP ?? "N/A"}</p>
          <p><strong>User Type:</strong> {UserType || "Standard"}</p>
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
