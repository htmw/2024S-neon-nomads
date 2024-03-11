import React from "react";
import { useState } from "react";
import "./Inventoryadd.css";
import "./Navbar";
import Navbar from "./Navbar";

function Inventoryadd() {
  const [toDoList, setToDoList] = useState([]);
  const [task, setTask] = useState("");

  const handleChange = (event) => {
    setTask(event.target.value);
  };

  const addTask = () => {
    const newTask = {
      id: toDoList.length === 0 ? 1 : toDoList[toDoList.length - 1].id + 1,
      taskName: task,
      completed: false,
    };
    setToDoList([...toDoList, newTask]);
  };

  const deleteTask = (id) => {
    setToDoList(toDoList.filter((task) => task.id !== id));
  };

  return (
    <div>
      <Navbar />
      <div className="maincontainer">
        <h2> Add Items to your Inventory</h2>
        <div className="inputdiv">
          <div className="additemform">
            <input type="text" onChange={handleChange}></input>
            <button onClick={addTask}>Add Item</button>
          </div>
        </div>

        <h2>Your Inventory List : </h2>
        <div
          className="displaydiv"
          style={{ backgroundColor: task.completed ? "green" : "white" }}>
          {toDoList.map((task) => {
            return (
              <div>
                <div className="comptask">
                  <p>{task.taskName}</p>
                  <button onClick={() => deleteTask(task.id)}>
                    Delete Item
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default Inventoryadd;
