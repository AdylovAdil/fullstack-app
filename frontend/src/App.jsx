import React from "react";
import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL;

export default function App() {
  const [items, setItems] = useState([]);
  const [text, setText] = useState("");

  const load = async () => {
    const res = await fetch(API + "/api/data");
    const data = await res.json();
    setItems(data);
  };

  const add = async () => {
    await fetch(API + "/api/data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: text }),
    });
    setText("");
    load();
  };

  const remove = async (id) => {
    await fetch(API + "/api/data/" + id, { method: "DELETE" });
    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Fullstack App</h1>
      <p>Student: YOUR_NAME | ID: YOUR_ID</p>

      <input value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={add}>Add</button>

      <ul>
        {items.map((i) => (
          <li key={i.id}>
            {i.title} <button onClick={() => remove(i.id)}>X</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
