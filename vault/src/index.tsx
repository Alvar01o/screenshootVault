import React from "react";
import ReactDOM from "react-dom/client";
import SignIn from "./Sign-in";
import reportWebVitals from "./reportWebVitals";
import Home from "./Home";
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
root.render(<main>{isLogged() ? <Home></Home> : <SignIn />}</main>);

reportWebVitals();
