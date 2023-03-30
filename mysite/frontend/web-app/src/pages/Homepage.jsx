import React, { useEffect, useState, useContext } from "react";
import "./Homepage.css";
import AuthContext from "../context/AuthContext";
import { ProjectListItem } from "../components/ProjectListItem";
import HomeNavbar from "../components/HomeNavbar";
import DateTimePicker from "react-datetime-picker/dist/entry.nostyle";

const Homepage = () => {
  // Sets variables
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [projectBudget, setProjectBudget] = useState("");
  const [projectStart, setProjectStart] = useState(new Date());
  const [projectDeadline, setProjectDeadline] = useState(new Date());
  let [projects, setProjects] = useState([]);
  
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

  const addProject = () => {
    var modal = document.getElementById("add-project-modal");
    var span = document.getElementsByClassName("close")[0];
    modal.style.display = "block";
    span.onclick = function () {
      modal.style.display = "none";
    };
    window.onclick = function (event) {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    };
  };

  // Deconstructing the relevent sections from AuthContext
  let { authTokens, logoutUser, user } = useContext(AuthContext);

  // Setting up states
  useEffect(() => {
    getProjects();
  }, []);

  // Obtaining the projects the user is involved in via a GET request to the api referencing our authorisation token
  let getProjects = async (e) => {
    let response = await fetch("http://127.0.0.1:8000/api/projects/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + String(authTokens.access),
      },
    });
    let data = await response.json();

    // If the response is good - set the state of projects to be the result of the GET request
    if (response.status === 200) {
      setProjects(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };
  var project_id;

  let createProject = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/projects/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + String(authTokens.access),
      },
      body: JSON.stringify({
        name: projectName,
        description: projectDescription,
        client_name: projectName,
        initial_budget: projectBudget,
        current_budget: projectBudget,
        amount_spent: "0",
        start_date: projectStart,
        initial_deadline: projectDeadline,
        current_deadline: projectDeadline,
        methodology: projectName,
        gitHub_token: projectName,
      }),
    });
    let data = await response.json();
    if (response.status === 201) {
      setProjects([...projects, data]);
      project_id = data.id;
    }
  };

  let createMember = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/projects/" + project_id +  "/members/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + String(authTokens.access),
      },
      body: JSON.stringify({
        role : "1",
        project : project_id,
        user : user.id,
        project_manager : "true",
        salary: "1000",
      }),
    });
  };

  return (
    <>
      <div id="add-project-modal" className="create-project-modal">
        <div className="create-project-content">
          <div className="close"> &times; </div>
          <h1>Create New Project</h1>
          <div className="create-project-div">
            <div className="create-project-label">Project Name:</div>
            <div className="create-project-input">
              <input
                className="input-bar"
                type="text"
                placeholder="Enter Project Name"
                onChange={(event) => setProjectName(event.target.value)}
              />
            </div>
          </div>
          <div className="create-project-div">
            <div className="create-project-label">Project Description:</div>
            <div className="create-project-input">
              <textarea
                className="text-area-bar"
                type="text"
                placeholder="Enter Description"
                onChange={(event) => setProjectDescription(event.target.value)}
              />
            </div>
          </div>
          <div className="create-project-div">
            <div className="create-project-label">Project Methodology:</div>
            <div className="create-project-input">
              <textarea
                className="text-area-bar"
                type="text"
                placeholder="Enter Project Methodology"
                onChange={(event) => setProjectDescription(event.target.value)}
              />
            </div>
          </div>
          <div className="create-project-div">
            <div className="create-project-label">Project Start Date:</div>
            <div className="create-project-input">
              <DateTimePicker
                onChange={(newValue) => setProjectStart(newValue)}
              />
            </div>
          </div>
          <div className="create-project-div">
            <div className="create-project-label">Project Deadline:</div>
            <div className="create-project-input">
              <DateTimePicker
                onChange={(newValue) => setProjectDeadline(newValue)}
              />
            </div>
          </div>
          <div className="create-project-div">
            <div className="create-project-label">Project Budget:</div>
            <div className="create-project-input">
              <input
                className="input-bar"
                type="number"
                placeholder="£"
                onChange={(event) => setProjectBudget(event.target.value)}
              />
            </div>
          </div>

          <div className="create-project-div">
            <div className="create-project-label">Add Member(s):</div>

            {membersList.map((each_member, index) => (
              <div key={index} className="create-project-div">
                <input
                  // need to look at functionality again.
                  className="input-bar"
                  type="text"
                  // value={each_member.member}
                  placeholder="Member Name"
                  name="member"
                  id="member"
                  required
                  value={each_member.member}
                  onChange={(e) => changeMember(e, index)}
                />

                <input
                  //doesn't save role to a varirable yet.
                  className="input-bar"
                  type="text"
                  placeholder="Member Role"
                  name="role"
                  id="role"
                  required
                  onChange={(e) => changeRole(e, index)}
                />

                <div className="create-project-div">
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
          </div>
          <span>
            <button onClick={() => {createProject(); createMember();}} className="create-project-btn">
              Create Project
            </button>
          </span>
        </div>
      </div>

      <div className="home-page">
        <HomeNavbar />
        <div className="home-page-content">
          <div className="home-page-menu">
            <button className="add-proj-btn" onClick={addProject}>
              Add Project
            </button>
          </div>
          <div className="projects-list">
            {projects.map((project, index) => (
              <ProjectListItem key={index} project={project} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default Homepage;
