import React, { useState, useEffect } from "react";
import "../pages/Homepage.css";

const TaskDependenciesChecklist = ({ index, task }) => {
  // Gets checked elements of a checklist.
  let [checkedTasks, setCheckedTask] = useState([]);

  // Add or remove checked item from list.
  const handleCheck = (event) => {
    var updatedList = [...checkedTasks];
    if (event.target.checkedTasks) {
      updatedList = [...checkedTasks, event.target.value];
    } else {
      updatedList.splice(checkedTasks.indexOf(event.target.value), 1);
    }
    setCheckedTask(updatedList);
  };

  const checkedItems = checkedTasks.length
    ? checkedTasks.reduce((total, item) => {
        return total + "," + item;
      })
    : "";

  // return classes based on whether item is checked
  var isChecked = (item) =>
    checkedTasks.includes(item) ? "checked-item" : "not-checked-item";

  // This is where all current users are
  console.log("checked items", checkedTasks);

  return (
    <div key="index">
      <input type="checkbox" value={task.name} onClick={handleCheck} />

      <span className={isChecked(task.name)}>{task.name}</span>

      <div>{`Items checked are: ${checkedItems}`}</div>
    </div>
  );
};

export default TaskDependenciesChecklist;
