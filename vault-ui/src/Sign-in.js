import * as React from "react";
import { login } from "./actions/auth-actions";
import "./Sign-in.css";
import RegisterForm from "./components/auth/RegisterForm";

export default function SignIn(props) {
  const [activeView, setActiveView] = React.useState("login");

  //add reducers for validations
  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    let user = {
      email: data.get("email") || "",
      password: data.get("password") || "",
    };
    let response = await login(user);
    props.onUpdateStatus(response);
  };
  const signUp = (event) => {
    event.preventDefault();
    setActiveView("register");
  }

  return (
    <>
      {activeView === "login" ? (
        <form className="login" onSubmit={handleSubmit}>
          <blockquote>
            "Your Files, Our Fortress: Secure Storage Solutions"
          </blockquote>
          <img
            src="/logo512.png"
            alt=""
            width={100}
            height={100}
            className="login-logo"
          />
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
          ></input>
          <input
            type="password"
            name="password"
            placeholder="Enter password"
          ></input>
          <button type="submit">Submit</button>
          <br />
          <span onClick={signUp}>Sign up</span>
        </form>
      ) : (
        <RegisterForm/>
      )}
    </>
  );
}
