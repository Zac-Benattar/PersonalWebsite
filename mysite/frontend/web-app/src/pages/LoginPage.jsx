import React, { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import "./Homepage.css";

const LoginPage = (props) => {
  let { loginUser } = useContext(AuthContext);

  return (
    <div className="auth-form-container">
      <form className="login-form" onSubmit={loginUser}>
        <h2> Login Page </h2>

        <label htmlFor="username">Username:</label>
        <input
          type="username"
          placeholder="Username"
          id="username"
          name="username"
        />

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          placeholder="Password"
          id="password"
          name="password"
        />

        <button className="login-button" type="submit">
          Log-in
        </button>
      </form>
      <Link  data-testid="link-button"  className="link-btn" to="/register">Register</Link>
    </div>
  );
};

export default LoginPage;
