import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import "../pages/tasks.css";

//append array of tasks to ganttChartData const

//ganttChartData const stores array of task arrays

//first element is array of gantt chart data fields (do not change)

//task id unique identifier for each task
//task name is name of task (does not have to be unique but recommend is quite short for for better formatting)

//duration is converted from milliseconds to days
//---> number of days * 24 * 60 * 60 * 1000 = number of milliseconds
//---> this number will then be converted and displayed as number of days
//duration defaults to time between start and end date if left null

//completion status is measured as a percentage of completion
//we do not store data on the task percentage completion - assign arbitrary values to completion status categories instead
//e.g. 50 = started but not completed

//dependecies takes a string containing a list of task ids of tasks that are dependent
//only include tasks dependent on the current task not tasks the current task is dependent on
//dependencies in the depencies string are separated by a comma only (no spaces)
//format of depencies string --> 'dependency1taskid,dpendency2taskid'

function RenderingNotStarted({ tasks }) {
  const tableRows = tasks.map((task) => {
    const startDate = new Date(task.start_date_unix * 1000);
    const dateString =
      startDate.getHours() +
      ":" +
      startDate.getMinutes() +
      " " +
      startDate.getDate() +
      "/" +
      startDate.getMonth() +
      "/" +
      startDate.getFullYear();
    return (
      <div key={task.id}>
        <p className="task-info">{task.name}</p>
      </div>
    );
  });
  return <div>{tableRows}</div>;
}

function RenderingStarted({ tasks }) {
  const tableRows = tasks.map((task) => {
    return (
      <div key={task.id}>
        <p className="task-info">{task.name}</p>
      </div>
    );
  });
  return <div>{tableRows}</div>;
}

function RenderingCompleted({ tasks }) {
  const tableRows = tasks.map((task) => {
    return (
      <div key={task.id}>
        <p className="task-info">{task.name}</p>
      </div>
    );
  });
  return <div>{tableRows}</div>;
}

const BoardView = () => {
  // Deconstructing the relevent sections from AuthContext
  let { authTokens, logoutUser } = useContext(AuthContext);
  const { slug } = useParams();
  let [notStartedTasks, setNotStartedTasks] = useState([]);
  let [startedTasks, setStartedTasks] = useState([]);
  let [finishedTasks, setFinishedTasks] = useState([]);

  // Setting up states
  useEffect(() => {
    getNotStartedTasks();
    getStartedTasks();
    getFinishedTasks();
  }, []);

  // Obtaining the projects the user is involved in via a GET request to the api referencing our authorisation token
  // Need to check this URLSS
  let getNotStartedTasks = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/"
        .concat(slug)
        .concat("/notstartedtasks/"),
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
      setNotStartedTasks(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  // Obtaining the projects the user is involved in via a GET request to the api referencing our authorisation token
  // Need to check this URLSS
  let getStartedTasks = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/"
        .concat(slug)
        .concat("/startedtasks/"),
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
      setStartedTasks(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  // Obtaining the projects the user is involved in via a GET request to the api referencing our authorisation token
  // Need to check this URLSS
  let getFinishedTasks = async (e) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/projects/"
        .concat(slug)
        .concat("/finishedtasks/"),
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
      setFinishedTasks(data);
      // If the respose is unauthorised, log out the user using the imported AuthContext method
    } else if (response.statusText === "Unauthorized") {
      logoutUser();
    }
  };

  return (
    <div className="view-container">
      <div>
        <h2 className="board-title">Board View</h2>
        <table>
          <thead>
            <tr className="board-headers">
              <th>
                <h2 className="task-category">Not started</h2>
              </th>

              <th>
                <h2 className="task-category">Started</h2>
              </th>
              <th>
                <h2 className="task-category">Completed</h2>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="board-view-row">
              <td>
                <RenderingNotStarted tasks={notStartedTasks} />
              </td>

              <td>
                <RenderingStarted tasks={startedTasks} />
              </td>
              <td>
                <RenderingCompleted tasks={finishedTasks} />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default BoardView;
