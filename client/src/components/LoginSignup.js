// LoginSignup.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginSignup.css";
import logo from "./MySKL_Logo.png";

const LoginSignup = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: "",
    sex: "",
    major: "",
    studentId: "",
    password: "",
  });

  const navigate = useNavigate();

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isLogin) {
      // --- LOGIN ---
      if (!formData.studentId || !formData.password) {
        alert("Please fill in all the fields");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            StudentID: formData.studentId,
            Password: formData.password,
          }),
        });

        const result = await response.json();

        if (response.ok) {
          // Store the student in localStorage
          localStorage.setItem("loggedInUser", JSON.stringify(result.student));
          alert(result.message); // e.g. "Login successful!"
          // Navigate to main page
          navigate("/main");
        } else {
          alert(result.error || "Invalid credentials");
        }
      } catch (err) {
        console.error("Error during login:", err);
        alert("Error connecting to the server.");
      }
    } else {
      // --- SIGN UP ---
      if (!formData.name || !formData.sex || !formData.major ||
          !formData.studentId || !formData.password) {
        alert("Please fill in all the fields");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            S_name: formData.name,
            Sex: formData.sex,
            Major: formData.major,
            StudentID: formData.studentId,
            Password: formData.password,
          }),
        });

        const result = await response.json();

        if (response.ok) {
          // Store the newly created user in localStorage (the server response might include user data)
          // If your server doesn't return full user data, you could store what you have.
          // For example, you could do:
          // localStorage.setItem("loggedInUser", JSON.stringify({ 
          //   StudentID: formData.studentId, S_name: formData.name, ... 
          // }));
          // For now, let's assume the server returns something like result.student as well
          
          alert(result.message); // e.g. "StandardStudent registered successfully!"
          // Navigate to main page
          navigate("/main");
        } else {
          alert(result.error || "Something went wrong");
        }
      } catch (err) {
        console.error("Error during registration:", err);
        alert("Error connecting to the server.");
      }
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <img src={logo} alt="Logo" className="logo" />
        <h2>{isLogin ? "Login" : "Sign Up"}</h2>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  id="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Enter your name"
                />
              </div>
              <div className="form-group">
                <label htmlFor="sex">Sex</label>
                <select id="sex" value={formData.sex} onChange={handleInputChange}>
                  <option value="" disabled>
                    Select your sex
                  </option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="major">Major</label>
                <input
                  type="text"
                  id="major"
                  value={formData.major}
                  onChange={handleInputChange}
                  placeholder="Enter your major"
                />
              </div>
            </>
          )}
          <div className="form-group">
            <label htmlFor="studentId">Student ID</label>
            <input
              type="text"
              id="studentId"
              value={formData.studentId}
              onChange={handleInputChange}
              placeholder="Enter your student ID"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" className="auth-btn">
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>
        <p onClick={toggleForm} className="toggle-link">
          {isLogin
            ? "Don't have an account? Sign up here."
            : "Already have an account? Login here."}
        </p>
      </div>
    </div>
  );
};

export default LoginSignup;
