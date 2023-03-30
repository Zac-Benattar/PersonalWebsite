import React, { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import "./NavbarElems";
import "../pages/Homepage.css";
import AuthContext from "../context/AuthContext";

export const HomeNavbar = () => {
  let { user, logoutUser } = useContext(AuthContext);
  const userProfileRoute = "/users/".concat(user.user_id);

  return (
      
      <nav className="home-nav">
        
        <h2 className="user-title">
          <Link to="/">Welcome {user.username}</Link>
        </h2>
        <div className="home-nav-menu">
          <ul>
          <li><Link to={userProfileRoute}>Profile</Link></li>
          <li onClick={logoutUser}>Logout</li> 
          </ul>
        </div>
      </nav>
  );
};

export default HomeNavbar;
