import React from "react";
import "./RegisterForm.css";
const handleRegister = async (event) => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  console.log(data);
  //    let user = {
  //      email: data.get("email") || "",
  //      password: data.get("password") || "",
  //    };
  //    let response = await login(user);
  //    props.onUpdateStatus(response);
};
function RegisterForm(props) {
  return (
    <form className="register" onSubmit={handleRegister}>
      <div className="register-title">Create a new user</div>
      <input
        type="text"
        name="username"
        placeholder="Enter your username"
      ></input>
      <input type="email" name="email" placeholder="Enter your email"></input>
      <input
        type="password"
        name="password"
        placeholder="Enter password"
      ></input>
      <input
        type="text"
        name="domain"
        placeholder="Enter your domain name"
      ></input>
      <div className="domain-preview">
        https://<span id="domain-slug">example</span>.screenshoot.com
      </div>
      <div className="domain-description">
        <span>Domain name is used to create a unique URL for your vault.</span>
        <br />
        <span>
          For example, if you enter "myvault", your vault will be accessible at
          "myvault.screenshoot.com"
        </span>
      </div>
      <div class="submit-container">
        <button type="submit">Submit</button>
      </div>
    </form>
  );
}

export default RegisterForm;
