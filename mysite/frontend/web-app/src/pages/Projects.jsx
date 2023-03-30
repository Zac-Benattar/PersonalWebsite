import React, { useEffect, useState, useContext } from "react";
import DateTimePicker from "react-datetime-picker";
import { Link, useLocation, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import SuccessChanceDisplay from "../components/SuccessChanceDisplay";
import AuthContext from "../context/AuthContext";
import "./Homepage.css";
import { FaTrash } from "react-icons/fa";
import DateStringifier from "../utils/DateStringifier";

const Projects = () => {
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [projectNewBudget, setProjectNewBudget] = useState("");
  const [projectStart, setProjectStart] = useState(new Date());
  const [projectNewDeadline, setProjectNewDeadline] = useState(new Date());

  // list to store members in a project
  const [membersList, setMembersList] = useState([{ member: "" }]);
  const [rolesList, setRolesList] = useState([{ role: "" }]);

  console.log(membersList);

  const addMember = () => {
    setMembersList([...membersList, { member: "" }]);
  };

  const addMemberRole = () => {
    setRolesList([...rolesList, { role: "" }]);
  };

  const removeMember = (index) => {
    const list = [...membersList];
    list.splice(index, 1);
    setMembersList(list);
  };

  const removeRole = (index) => {
    const list = [...rolesList];
    list.splice(index, 1);
    setRolesList(list);
  };

  const changeMember = (e, index) => {
    const { name, value } = e.target;
    const list = [...membersList];
    list[index][name] = value;
    setMembersList(list);
  };

  const changeRole = (e, index) => {
    const { name } = e.target;
    var value = e.target.value;

    console.log("rolename", name);
    console.log("role value", value);
    const list = [...rolesList];
    list[index] = value;
    setRolesList(list);
  };

  // Deconstructing the relevent sections from AuthContext
  let { authTokens, logoutUser, user } = useContext(AuthContext);

  // Defining the states
  let [project, setProject] = useState([]);
  let [riskEvaluation, setRiskEvaluation] = useState([]);
  let [suggestions, setSuggestions] = useState([]);

  // Get slug parameter given when Project is referenced in router
  const { slug } = useParams();

  // Setting up states
  useEffect(() => {
    getProject();
    getRiskEvaluation();
    setProjectName(project.name);
    setProjectDescription(project.description);
    setProjectNewBudget(project.current_budget);
    setProjectNewDeadline(project.current_deadline);
    setProjectStart(project.start_date);
    getSuggestions();
  }, []);

  // Obtaining the specific project via a GET request to the api referencing our authorisation token
  let getProject = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/".concat(slug),
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      }
    );
    let data = await response.json();

    // If the response is good - set the state of project to be the result of the GET request
    if (response.status === 200) {
      setProject(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  let updateProject = async () => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/".concat(slug) + "/",
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
        body: JSON.stringify({
          name: projectName,
          description: projectDescription,
          client_name: projectName,
          initial_budget: project.initial_budget,
          current_budget: projectNewBudget,
          amount_spent: project.initial_budget,
          start_date: projectStart,
          initial_deadline: project.initial_deadline,
          current_deadline: projectNewDeadline,
          methodology: projectName,
          gitHub_token: projectName,
        }),
      }
    );

    let data = await response.json();
    if (response.status === 200) {
      setProject(data);
    }
    else { 
      alert("Editing project is limited to project manager only")
    }
  };

  let deleteProject = async () => {
    let response = fetch(
      "http://127.0.0.1:8000/api/projects/".concat(slug) + "/",
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      }
    );
    if (response.status === 204) {
      alert("Project Deleted!");
    } else {
      alert("Project deletion is only allowed for project managers");
    }
  };

  // Obtaining the specific project's most recent risk evaulation via a GET request to the api referencing our authorisation token
  let getRiskEvaluation = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/"
        .concat(slug)
        .concat("/generateriskevaluation"),
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      }
    );
    let data = await response.json();

    // If the response is good - set the state of riskevaluation to be the result of the GET request
    if (response.status === 200) {
      setRiskEvaluation(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  const editProject = () => {
    var edit_modal = document.getElementById("add-project-modal");
    var close_button = document.getElementsByClassName("close")[0];

    edit_modal.style.display = "block";
    close_button.onclick = function () {
      edit_modal.style.display = "none";
    };

    window.onclick = function (event) {
      if (event.target === edit_modal) {
        edit_modal.style.display = "none";
      }
    };
  };

  let getSuggestions = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/"
        .concat(slug)
        .concat("/suggestions/"),
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      }
    );
    let data = await response.json();

    // If the response is good - set the state of projects to be the result of the GET request
    if (response.status === 200) {
      setSuggestions(data);
      console.log(suggestions);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  return (
    <>
      <div id="add-project-modal" className="edit-modal">
        <div className="edit-modal-content">
          <div className="close"> &times; </div>
          <h1>Edit this project: </h1>
          <div className="edit-project-div">
            <div className="edit-project-label">Edit Project Name:</div>
            <div className="edit-project-div">
              <input
                className="input-bar"
                type="text"
                placeholder="project-name"
                defaultValue={project.name}
                onChange={(event) => setProjectName(event.target.value)}
              />
            </div>
          </div>

          <div className="edit-project-div">
            <div className="edit-project-label">Edit Project Description:</div>
            <div className="edit-project-div">
              <textarea
                className="text-area-bar"
                type="text"
                placeholder="Enter Description"
                defaultValue={project.description}
                onChange={(event) => setProjectDescription(event.target.value)}
              />
            </div>
          </div>

          <div className="edit-project-div">
            <div className="edit-project-label">Edit Project Start Date:</div>
            <div className="edit-project-div">
              <DateTimePicker
                defaultValue={project.start_date}
                onChange={(newValue) => setProjectStart(newValue)}
              />
            </div>
          </div>

          <div className="edit-project-div">
            <div className="edit-project-label">Edit Project Deadline:</div>
            <div className="edit-project-div">
              <DateTimePicker
                defaultValue={project.current_deadline}
                onChange={(newValue) => setProjectNewDeadline(newValue)}
              />
            </div>
          </div>

          <div className="edit-project-div">
            <div className="edit-project-label">Edit Project Budget:</div>
            <div className="edit-project-div">
              <input
                className="input-bar"
                type="number"
                placeholder="£"
                defaultValue={project.current_budget}
                onChange={(event) => setProjectNewBudget(event.target.value)}
              />
            </div>
          </div>

          <div className="edit-project-div">
            <div className="edit-project-label">Add Member(s):</div>

            {membersList.map((each_member, index) => (
              <div key={index} className="edit-project-div">
                <input
                  // need to look at functionality again.
                  className="input-bar"
                  type="text"
                  // value={each_member.member}
                  placeholder="Member Name"
                  onChange={(e) => (changeMember(e,index), index)}
                />

                <input
                  //doesn't save role to a varirable yet.
                  className="input-bar"
                  type="text"
                  placeholder="Member Role"
                  onChange={(e)=>changeRole(e, index)}
                />

                <div className="edit-project-div">
                  {membersList.length - 1 === index && (
                    <button
                      className="member-button"
                      onClick={(event) => {
                        addMember();
                        addMemberRole();
                      }}
                    >
                      <span> Add a member </span>
                    </button>
                  )}

                  {membersList.length > 1 && (
                    <button
                      className="member-button"
                      onClick={(event) => {
                        removeMember(index);
                        removeRole(index);
                      }}
                    >
                      <span> Remove Member </span>
                    </button>
                  )}
                </div>
              </div>
            ))}

            <span>
              <button onClick={updateProject} className="create-project-btn">
                Save Project
              </button>
            </span>
          </div>
        </div>
      </div>

      <div className="home-page">
        <Navbar />
        <div className="projects-page-content">
          {riskEvaluation.map((riskEvaluation, index) => (
            <SuccessChanceDisplay
              key={index}
              risk_evaluation={riskEvaluation}
              suggestions={suggestions}
            />
          ))}

          <div className="project-info-container">
            <Link to={"/"}>
              <i onClick={deleteProject} className="delete-proj-btn">
                <FaTrash />
              </i>
            </Link>
            <div className="project-name">
              <h1>{project.name}</h1>
            </div>
            <div className="project-description">
              <h3 className="des-title"> Project Description: </h3>
              <p className="des">{project.description}</p>
              <br />
              <br />
              <h3 className="des-title"> Project methodology: </h3>
              <p className="des">{project.methodology}</p>
              <br />
              <br />
              <h3 className="des-title"> Project budget: </h3>
              <p className="des"> £{Math.round(project.current_budget)}</p>
              <br />
              <br />
              <h3 className="des-title"> Project deadine: </h3>
              <p className="des"> {DateStringifier.getFullDateFromUNIXTimestampSeconds(project.current_deadline_unix)}</p>
            </div>

            <div className="project-buttons">
              <button className="proj-button" onClick={editProject}>
                Edit project info
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Projects;
