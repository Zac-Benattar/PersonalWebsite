import React from "react";
import DateStringifier from "../utils/DateStringifier";

export const SuccessChanceDisplay = ({ risk_evaluation, suggestions }) => {
  const suggestionCount = suggestions.length;

  return (
    <div className="risk-info-container">
      <div className="project-risk-score">
        <p className="risk-percentage">
          This project has a {parseFloat(risk_evaluation.success_chance).toFixed(2)}% chance of success
          as of {DateStringifier.getTimeFromUNIXTimestampSeconds(risk_evaluation.date_unix)}
        </p>
      </div>

      <div className="project-risk-score">
        <p className="risk-percentage">
          Your project currently has {suggestionCount} suggestions.{" "}
        </p>
      </div>
    </div>
  );
};

export default SuccessChanceDisplay;
