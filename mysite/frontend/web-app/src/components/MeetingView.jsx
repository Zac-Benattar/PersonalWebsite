import React, { useState, useEffect } from "react";
import CalendarView from "../components/CalendarView";
import Navbar from "./Navbar";
import "./Calendar.css";

export const MeetingsForm = () => {
  return (
    <>
      <div className="home-page">
        <Navbar />

        <div className="mainbody-container">
          <CalendarView />
        </div>
      </div>
    </>
  );
};

export default MeetingsForm;
