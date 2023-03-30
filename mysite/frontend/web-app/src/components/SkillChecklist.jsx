import React, { useState } from "react";
import "../pages/Homepage.css";

const SkillChecklist = ({ index, skill }) => {
  // Gets checked elements of a checklist.
  let [checked, setChecked] = useState([]);

  // Add or remove checked item from list.
  const handleCheck = (event) => {
    var updatedList = [...checked];
    if (event.target.checked) {
      updatedList = [...checked, event.target.value];
    } else {
      updatedList.splice(checked.indexOf(event.target.value), 1);
    }
    setChecked(updatedList);
  };

  const checkedItems = checked.length
    ? checked.reduce((total, item) => {
        return total + "," + item;
      })
    : "";

  // return classes based on whether item is checked
  var isChecked = (item) =>
    checked.includes(item) ? "checked-item" : "not-checked-item";

  // This is where all current users are
  console.log("checked items", checked);

  return (
    <div key="index">
      <input type="checkbox" value={skill.name} onClick={handleCheck} />

      <span className={isChecked(skill.name)}>{skill.name}</span>

      <div>{`Items checked are: ${checkedItems}`}</div>
    </div>
  );
};

export default SkillChecklist;
