import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import SignIn from "./Sign-in";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

const isLogged = () => {
  const user: string | null = localStorage.getItem("user");
  const realUserInformation = JSON.parse(user || "{}");
  if (realUserInformation?.token) {
    return true;
  } else {
    return false;
  }
};
root.render(<main>{isLogged() ? <h1>Logged</h1> : <SignIn />}</main>);

reportWebVitals();
