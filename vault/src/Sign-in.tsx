import * as React from "react";
import { logIng } from "./Actions";
import { ILoginUser } from "./interfaces";

export default function SignIn() {

    //add reducers for validations

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    let user: ILoginUser = {
      email: data.get("email") || "",
      password: data.get("password") || "",
    };
    logIng(user);
  };


  return (
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
      <input type="email" name="email" placeholder="Enter your email"></input>
      <input
        type="password"
        name="password"
        placeholder="Enter password"
      ></input>
      <button type="submit">Submit</button>
    </form>
  );
}
