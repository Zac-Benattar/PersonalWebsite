import React, { useContext } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import "./NavbarElems";
import "../pages/Homepage.css";
import AuthContext from "../context/AuthContext";

const Navbar = () => {
  let { logoutUser } = useContext(AuthContext);

  const { slug } = useParams();
  const baseRoute = "/projects/".concat(slug);
  const suggestionsRoute = baseRoute.concat("/suggestions/");
  const tasksRoute = baseRoute.concat("/tasks/");
  const peopleRoute = baseRoute.concat("/people/");
  const meetingsRoute = baseRoute.concat("/meetings");

  return (
    <div>
      <nav className="nav">
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to={baseRoute}>Project Overview</Link>
          </li>
          <li>
            <Link to={suggestionsRoute}>Suggestions</Link>
          </li>
          <li>
            <Link to={tasksRoute}>Tasks</Link>
          </li>
          <li>
            <Link to={peopleRoute}>People</Link>
          </li>
          <li>
            <Link to={meetingsRoute}>Meetings</Link>
          </li>
          <li onClick={logoutUser}>Logout</li>
        </ul>
      </nav>
    </div>
  );
};

export default Navbar;
