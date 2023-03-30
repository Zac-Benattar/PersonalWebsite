import React, { useState } from "react";
import { Link } from "react-router-dom";

const Register = (props) => {
    const [email, setEmail] = useState('');
    const [password, setPass] = useState('');
    const [username, setUsername] = useState('');
    const [firstname, setFirstName] = useState('');
    const [lastname, setLastName] = useState('');
    const [phone, setPhonenumber] = useState('');
    const [confirmPassword, setConfirmPass] = useState('');
    const [isError, setError] = useState(null);

    const onPassChange = (e) => {
      setPass({...password, 
              pass: e.target.value,
            });
      setError(null);
      let caps, small, num, specialSymbol;
      if (password.length < 4) {
        setError(
          "Password should contain minimum 4 characters, with one UPPERCASE, lowercase, number and special character: @$! % * ? &"
        );
        return;
      } else {
        caps = (password.match(/[A-Z]/g) || []).length;
        small = (password.match(/[a-z]/g) || []).length;
        num = (password.match(/[0-9]/g) || []).length;
        specialSymbol = (password.match(/\W/g) || []).length;
        if (caps < 1) {
          setError("Must add one UPPERCASE letter");
          return;
        } else if (small < 1) {
          setError("Must add one lowercase letter");
          return;
        } else if (num < 1) {
          setError("Must add one number");
          return;
        } else if (specialSymbol < 1) {
          setError("Must add one special symbol: @$! % * ? &");
          return;
        }
      }
    };

    const onSubmit = async (e) => {
      try {
        if (passwordConfirmation()) {
          console.log('attempted to create a user')
          console.log(password)
          createUser()
        } else {
          e.preventDefault();
          e.persist();
        }
      } catch (error) {
        throw error;
      }
    };

    let createUser = async (e) => {

      console.log(JSON.stringify({
        username: username,
        password: confirmPassword,
        email: email,
        phone: phone
      }))

      let response = await fetch("http://127.0.0.1:8000/api/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
          username: username,
          password: confirmPassword,
          email: email,
          phone: phone
        })
      });
  
      if (response.status === 201) {
        alert("Account successfully created!");
        return true
      }

      return false
    };

    function passwordConfirmation() {
      var password = document.getElementById("password").value;
      var confirmPassword = document.getElementById("password-confirmed").value;
     
      if (password === "" || confirmPassword === "") {
          alert("Error: The password field is Empty.");
          return false;
      } else if (password !== confirmPassword) {
          alert("Please make sure your passwords match.")
          return false;
      }

      return true;
    }

  return (
    <div className="reg-auth-form-container">
      <form className="register-form" onSubmit={onSubmit}>
        <h2> Register here </h2>
        <label htmlFor="firstname">First name:</label>
        <input
          data-testid="input-boxes" 
          value={firstname}
          onChange={(e) => setFirstName(e.target.value)}
          type="text"
          placeholder="First Name"
          id="name"
          name="name"
        />
        <label htmlFor="lastname">Last name:</label>
        <input
          data-testid="input-boxes" 
          value={lastname}
          onChange={(e) => setLastName(e.target.value)}
          type="text"
          placeholder="Last name"
          id="last name"
          name="last name"
        />
          <label htmlFor="username">Username:</label>
        <input
          data-testid="input-boxes" 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          type="text"
          placeholder="Username"
          id="username"
          name="username"
        />
        <label htmlFor="email">Email:</label>
        <input
          data-testid="input-boxes"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          placeholder="example@email.com"
          id="email"
          name="email"
        />
        <label htmlFor="phone">Phone:</label>
        <input
          data-testid="input-boxes"
          value={phone}
          onChange={(e) => setPhonenumber(e.target.value)}
          type="text"
          placeholder="Enter phone number"
          id="phone"
          name="phone"
        />
        <label htmlFor="password">Password:</label>
        {isError !== null && <p className="errors"> - {isError}</p>}
        <input
          data-testid="input-boxes"
          value={password}
          onChange={(e) => {onPassChange(e);setPass(e.target.value);}}
          type="password"
          placeholder="********"
          id="password"
          name="password"    
        />
        <label htmlFor="confirm-password">Retype Password:</label>
        <input
          data-testid="input-boxes" 
          value={confirmPassword}
          onChange={(e) => setConfirmPass(e.target.value)}
          type="password"
          placeholder="********"
          id="password-confirmed"
          name="password-confirmed"
        />

        <button onClick={() => { onSubmit() }} className="register-button" type="submit">
          Register
        </button>
      </form>
      <Link data-testid="link-button" className="link-btn" to="/login">Have an account? Login Here</Link>
    </div>
  );
};

export default Register;
