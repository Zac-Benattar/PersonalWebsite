import React, { useState, useEffect } from "react";
import "../pages/Homepage.css";
import { FaTrash } from "react-icons/fa";

export const ListPeople = ({ member }) => {
  let [user, setUsers] = useState([]);
  let [role, setRoles] = useState([]);
  let [skills, setSkills] = useState([]);

  useEffect(() => {
    getUser();
    getRoles();
    getSkills();
  }, []);

  let getUser = async () => {
    let response = await fetch("/api/users/" + member.id + "/");
    let data = await response.json();
    setUsers(data);
  };

  let getRoles = async () => {
    let response = await fetch("/api/roles/" + member.role + "/");
    let data = await response.json();
    setRoles(data);
  };

  let getSkills = async () => {
    let response = await fetch("/api/users/" + member.user + "/skills/");
    let data = await response.json();

    setSkills(data);
  };

  return (
    <div className="people-container">
      <i className="delete-people-btn">
        <FaTrash />
      </i>
      <div className="people-info">
        <h2>
          Name: {user.first_name} {user.last_name}
        </h2>
        <h3> Role: {role.name} </h3>

        <ul className="all-skills">
          {skills.map((skill, index) => (
            <li key={index} className="skill">
              {skill.name}
            </li>
          ))}
        </ul>
        <p> Work hours: {member.work_hours}</p>
        <p>Phone Number: {user.phone}</p>
      </div>
    </div>
  );
};
