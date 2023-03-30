import React, { useEffect, useState, useContext } from "react";
import "./Homepage.css";
import { ListPeople } from "../components/ListPeople";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import AuthContext from "../context/AuthContext";

const PeopleView = () => {
  const { slug } = useParams();

  let [members, setMembers] = useState([]);

  // Deconstructing the relevent sections from AuthContext
  let { authTokens, logoutUser } = useContext(AuthContext);

  // Setting up states
  useEffect(() => {
    getMembers();
  }, []);

  // Obtaining the members involved in the project via a GET request to the api referencing our authorisation token
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

  return (
    <>
      <div className="home-page">
        <Navbar />
        <div className="all-containers">
          <div className="people-list">
            {members.map((member, index) => (
              <ListPeople key={index} member={member} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default PeopleView;
