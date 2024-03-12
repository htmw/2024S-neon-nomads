import React, { useState } from "react";
import "./Login.css";
import { Link } from "react-router-dom";
import Inventoryadd from "./Inventoryadd";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Submit", { username, password });
  };

  return (
    <div className="container">
      <div>
        <img
          src={"Images/KitchenSyncLogo.jpg"}
          className="applogo"
          alt="logo"
        />
      </div>
      <div className="formcontainer">
        <h2>Login</h2>
        <form onSubmit={handleSubmit} className="loginform">
          <div className="field">
            <input
              type="text"
              id="username"
              value={username}
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
              // required
            />
          </div>
          <div className="field">
            {/* <label htmlFor="password">Password</label> */}
            <input
              type="password"
              id="password"
              value={password}
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              // required
            />
          </div>

          <button type="submit" className="loginbtns">
            <Link to={"/inventory"}>Login</Link>
          </button>
          <button type="submit" className="loginbtns">
            <Link to={"/register"}>New User ?</Link>
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
