import * as React from "react";
import { login } from "./Actions";
import { ILoginUser } from "./interfaces";
import "./Sign-in.css";
export default function SignIn(props: any) {
    //add reducers for validations
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    let user: ILoginUser = {
      email: data.get("email") || "",
      password: data.get("password") || "",
    };
    let response:boolean = await login(user);
    props.onUpdateStatus(response);

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
