import React from "react";
import "./Userregistration.css";
import Navbar from "./Navbar";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function Userregistration() {
  const navigate = useNavigate();

  return (
    <div>
      <Navbar />
      <div className="urbody">
        <h2> Welcome to Kitchen Sync.</h2>
        <div className="urcontainer">
          <form className="regform">
            <input type="text" placeholder="First Name"></input>
            <input type="text" placeholder="Last Name"></input>
            <input type="text" placeholder="Email Address"></input>
            <input type="number" placeholder="Age"></input>
            <input type="password" placeholder="Password"></input>
            <input type="password" placeholder="Confirm Password"></input>
            <button type="submit" className="regsubmitbtn">
              <Link to={"/inventory"}>Register</Link>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Userregistration;
