import React from "react";
import ProgressBar from "./ProgressBar";
import "../pages/Homepage.css";
import { Link } from "react-router-dom";
import DateStringifier from "../utils/DateStringifier";

export const ProjectListItem = ({ project }) => {
  const projectRoute = "/projects/".concat(project.id);

  return (
    <Link to={projectRoute}>
      <div className="project_container">
        <div className="title-info">
          <div className="title">
            <h1>{project.name}</h1>
          </div>

          <div className="progress-bar">
            <ProgressBar progress={project.completion} />
          </div>
        </div>
        <div className="info_container">
          <div className="info">
            <h3>Current Budget:</h3> <p> £{Math.round(project.current_budget)}</p>
            <br />
            <br />
            <h3>Current Deadline:</h3>
            <p> {DateStringifier.getFullDateFromUNIXTimestampSeconds(project.current_deadline_unix)}</p>
            <br />
            <br />
            <h3>Methodology: </h3>
            <p>{project.methodology}</p>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ProjectListItem;
