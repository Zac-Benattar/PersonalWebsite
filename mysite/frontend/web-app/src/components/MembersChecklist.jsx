import React, { useState, useEffect } from "react";
import "../pages/Homepage.css";

const MembersChecklist = ({ index, member }) => {
  const [options, setOptions] = useState([]);

  let [user, setUsers] = useState([]);
  let [members, setMembers] = useState([]);

  // Gets checked elements of a checklist.
  let [checked, setChecked] = useState([]);

  // Add or remove checked item from list.
  const handleCheck = (event) => {
    var updatedList = [...checked];
    console.log("updatedlist", updatedList);
    if (event.target.checked) {
      updatedList.push(event.target.value);
    } else {
      updatedList.splice(checked.indexOf(event.target.value), 1);
    }
    console.log("updated list after", updatedList);
    setChecked(updatedList);
  };

  // return classes based on whether item is checked
  var isChecked = (item) =>
    checked.includes(item) ? "checked-item" : "not-checked-item";

  const checkedItems = checked.length
    ? checked.reduce((total, item) => {
        return total + ", " + item;
      })
    : "";

  useEffect(() => {
    getUsers();
  }, []);

  let getUsers = async () => {
    let response = await fetch("/api/users/" + member.id + "/");
    let data = await response.json();
    console.log("Data:", data);
    setUsers(data);
  };

  // This is where all current users are
  console.log("checked items", checkedItems);

  return (
    <>
      <div>
        <div key={index}>
          <input
            value={user.first_name}
            type="checkbox"
            onChange={handleCheck}
          />
          <span className={isChecked(user.first_name)}>
            {user.first_name}
          </span>
        </div>
      </div>

      <div>{`Items checked are: ${checkedItems}`}</div>
    </>
  );
};

export default MembersChecklist;
