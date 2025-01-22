// App.js
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginSignup from "./components/LoginSignup";
import MainPage from "./components/MainPage";
import MyProfile from "./components/MyProfile"; // <--- import
import MySchedule from "./components/MySchedule";
import Alerts from "./components/Alerts"; 


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginSignup />} />
        <Route path="/main" element={<MainPage />} />
        <Route path="/myprofile" element={<MyProfile />} /> {/* <--- new route */}
        <Route path="/schedule" element={<MySchedule />} /> {/* New route */}
        <Route path="/alerts" element={<Alerts />} /> {/* New route for alerts */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
