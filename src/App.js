import "./App.css";
import Inventoryadd from "./components/Inventoryadd.js";
import Login from "./components/Login.js";
import Navbar from "./components/Navbar.js";

function App() {
  return (
    <div className="App">
      {/* <Inventoryadd /> */}

      <Navbar />
      <div className="loginbox">
        <Login />
      </div>
    </div>
  );
}

export default App;
