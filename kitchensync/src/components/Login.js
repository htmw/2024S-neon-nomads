 import React, { useState } from "react";
 import { useHistory } from "react-router-dom"; // Correctly import useHistory
 import "./Login.css";
 // Removed unused imports

 function Login() {
   const [username, setUsername] = useState("");
   const [password, setPassword] = useState("");
   const history = useHistory(); // Initialize useHistory hook

   const handleSubmit = (event) => {
     event.preventDefault();
     console.log("Submit", { username, password });

     // Navigate to the Inventoryadd component after form submission
     history.push('/inventoryadd'); // Make sure this path matches your route setup
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
         <form onSubmit={handleSubmit}> {/* Use handleSubmit here */}
           <div className="field">
             <input
               type="text"
               id="username"
               value={username}
               placeholder="Username"
               onChange={(e) => setUsername(e.target.value)}
               required
             />
           </div>
           <div className="field">
             <input
               type="password"
               id="password"
               value={password}
               placeholder="Password"
               onChange={(e) => setPassword(e.target.value)}
               required
             />
           </div>

           <button type="submit">Login</button> {/* Removed the <a> tag */}
         </form>
       </div>
     </div>
   );
 }

 export default Login;

                    
                    
/*
import React, { useState, forwardRef } from "react";
import { Link } from "react-router-dom";
import "./Login.css";
import Inventoryadd from "./Inventoryadd";

const LinkWithRef = forwardRef((props, ref) => (
  <Link {...props} ref={ref}>
    {props.children}
  </Link>
));

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
        <form onSubmit={handleSubmit}>
          <div className="field">
            <input
              type="text"
              id="username"
              value={username}
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="field">
            <input
              type="password"
              id="password"
              value={password}
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit">
            <LinkWithRef to="/inventoryadd">Login</LinkWithRef>
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
*/
