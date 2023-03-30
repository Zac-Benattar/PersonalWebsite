import React, { useState, useEffect, useContext } from "react";
import Navbar from "../components/Navbar";
import GanttChart from "../components/GanttChart";
import ListView from "../components/ListView";
import BoardView from "../components/BoardView";
import "./tasks.css";
import { useParams } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const TasksForm = () => {
  // Deconstructing the relevent sections from AuthContext
  let { authTokens, logoutUser, user } = useContext(AuthContext);
  const { slug } = useParams();
  let [tasks, setTasks] = useState([]);
  let [members, setMembers] = useState([]);

  const [modalstate, setmodalstate] = useState({
    isOpen: false,
  });

  const openModal = () => {
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

  const closeModal = () => setmodalstate({ isOpen: false });
  const viewoptions = ["Gantt Chart", "List View", "Board View"];
  const [viewStyle, setviewStyle] = useState(viewoptions[0]);
  const [inputs, setInputs] = useState({});

  function View() {
    if (viewStyle === viewoptions[0]) {
      return <GanttChart tasks={tasks} />;
    } else if (viewStyle === viewoptions[1]) {
      return <ListView tasks={tasks} />;
    } else {
      return <BoardView />;
    }
  }

  // Setting up states
  useEffect(() => {
    getTasks();
    getMembers();
  }, []);

  // Obtaining the tasks for the project via a GET request to the api referencing our authorisation token
  let getTasks = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/".concat(slug).concat("/tasks/"),
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
      setTasks(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  /* Obtaining the members of the project to be chosen for the task via a GET request to the api
   * referencing our authorisation token */

  let getMembers = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/".concat(slug).concat("/members/"),
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
      setMembers(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  const handleChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  // Gets checked elements of a checklist.
  let [checkedTasks, setChecked] = useState([]);

  // Add or remove checked item from list.
  const handleCheck = (event) => {
    var updatedList = [...checkedTasks];
    var id = event.target.value;
    if (event.target.checked) {
      updatedList = [...checkedTasks, event.target.value];
    } else {
      updatedList.splice(checkedTasks.indexOf(id), 1);
    }
    setChecked(updatedList);
  };

  // return classes based on whether item is checked
  var isChecked = (item) =>
    checkedTasks.includes(item) ? "checked-item" : "not-checked-item";

  // This is where all checked skills are stored.

  console.log("tasks", tasks);
  console.log("checked tasks", checkedTasks);

  return (
    <>
      <div className="home-page">
        <Navbar />
        <div className="main_container">
          <p className="title">Task Tracker</p>
          <div className="menu_container">
            <div className="viewType">
              <p> View Type: </p>
              <select
                defaultValue={viewStyle}
                onChange={(e) => setviewStyle(e.target.value)}
                id="viewTypeSelector"
              >
                <option> {viewoptions[0]}</option>
                <option> {viewoptions[1]}</option>
                <option> {viewoptions[2]}</option>
              </select>
            </div>

            <div className="task-page-menu">
              <button className="add-proj-btn" onClick={openModal}>
                Add New Task
              </button>
            </div>

            <div id="add-project-modal" className="create-project-modal">
              <div className="create-project-content">
                <div className="close" onClick={closeModal}>
                  &times;
                </div>
                <h1>Add New task</h1>
                <form onSubmit={handleSubmit}>
                  <div className="create-project-div">
                    <div className="create-project-label">Task Name:</div>
                    <div className="create-project-input">
                      <input
                        className="input-bar"
                        type="text"
                        name="taskname"
                        value={inputs.taskname || ""}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="create-project-div">
                    <div className="create-project-label">Task Description</div>
                    <div className="create-project-input">
                      <input
                        className="input-bar"
                        type="text"
                        name="taskdescription"
                        value={inputs.taskdescription || ""}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="create-project-div">
                    <div className="create-project-label">Task date:</div>
                    <div className="create-project-input">
                      <input
                        className="input-bar"
                        type="date"
                        name="startdate"
                        value={inputs.startdate || ""}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="create-project-div">
                    <div className="create-project-label">Duration:</div>
                    <div className="create-project-input">
                      <input
                        className="input-bar"
                        type="text"
                        name="duration"
                        value={inputs.duration || ""}
                        onChange={handleChange}
                      />
                    </div>
                  </div>

                  <div className="create-project-div">
                    <div className="checkList">
                      <div className="create-project-label">
                        Pick task dependencies:
                      </div>
                      <div className="checkList">
                        {tasks.map((task, index) => (
                          <div key={index}>
                            <input
                              type="checkbox"
                              value={task.name}
                              onChange={handleCheck}
                            />

                            <span className={isChecked(task.name)}>
                              {task.name}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                    <button type="submit" className="task-button">
                      Add Task
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <View />
        </div>
      </div>
    </>
  );
};

export default TasksForm;
