import React, { useState } from "react";
import "./ListView.css";
import { FaEdit } from "react-icons/fa";
import DateStringifier from "../utils/DateStringifier";
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

const ListView = ({ tasks }) => {
      const [modalstate, setmodalstate] = useState({
        isOpen: false,
      });

      const openModal = () => {
          var modal = document.getElementById("edit-task-modal");
          var span = document.getElementsByClassName("close")[0];
          modal.style.display = "block";
          span.onclick = function() {
            modal.style.display = "none";
          }
          window.onclick = function(event) {
            if (event.target === modal) {
              modal.style.display = "none";
            }
          }

      };

      const tableRows = tasks.map((task) => {
        return (
          <tr key={task.id}>
            <td>{task.id}</td>
            <td>{task.name}</td>
            <td>{task.completion_status}</td>
            <td>{task.duration}</td>
            <td>{DateStringifier.getFullDateFromUNIXTimestampSeconds(task.start_date_unix)}</td>
            <td><i className="edit-task-icon" onClick={openModal}><FaEdit/></i></td>
          </tr>
        );
      });

      let [name, getName] = useState("");
      let [completionStatus, getCompletionStatus] = useState([]);
      let [duration, getDuration] = useState("");
      let [description, getDescription] = useState("");

      
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
      


    const closeModal = () => setmodalstate({ isOpen: false });


  return (

    <>
    

   

        <div id="edit-task-modal" className="edit-task-modal">
              
              <div className="create-project-content">
                <div className="close" >&times;</div>
                <h1>Edit this task</h1>
               
                  <div className="create-project-div">
                  <div className="create-project-label">Edit task name:</div>
                  <div className="create-project-input"><input
                      className="input-bar"
                      type="text"
                      name="taskname"
                      
                      onChange={(event)=>getName(event.target.value)}
                    /></div>
                  </div>
                  <div className="create-project-div">
                  <div className="create-project-label">Task Description</div>
                  <div className="create-project-input">  <input
                      className="input-bar"
                      type="text"
                      name="taskdescription"
                      
                      onChange={(event)=>getDescription(event.target.value)}
                    /></div>
                  </div>
                 
                  <div className="create-project-div">
                  <div className="create-project-label">Duration:</div>
                  <div className="create-project-input"><input
                      className="input-bar"
                      type="text"
                      name="duration"
                     
                      onChange={(event)=>getDuration(event.target.value)}
                    /></div>
                  </div>
                
                  <div className="create-project-div">
                    <div className="checkList">
                    <div className="create-project-label">Pick task dependencies:</div>
                      <div className="checkList">
                      
                        {tasks.map((task, index) => (
                          <div key={index}>


                            <input
                            type="checkbox"
                            value={task.name}
                            onChange={handleCheck}
                            />

                            <span className={isChecked(task.name)}>{task.name}</span>
                          </div>
                          
                         ))}

                     
                      </div>
                    </div>
                    <button type="submit" className="task-button">Edit Task</button>
                  </div>
                  
                
              </div>
            </div>


      



    <div className="view-container">

 
      
      
      <div className="listview-container">
        <h2 className="title-list">List View</h2>
        <table className="list-table">
          <thead>
            <tr>
              <th className="table-title"> Task ID</th>
              <th className="table-title"> Task name</th>
              <th className="table-title"> Completion status</th>
              <th className="table-title"> Duration </th>
              <th className="table-title"> Startdate </th>
              <th className="table-title"> Edit Task </th>
            </tr>
          </thead>
          
        <tbody>{tableRows}</tbody>
        </table>
      </div>


   

      </div>



    </>
    
  );
};


export default ListView;
