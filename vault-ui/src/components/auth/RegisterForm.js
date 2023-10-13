import React, { useState, useRef, useEffect } from "react";
import slugify from "slugify";
import "./RegisterForm.css";
import InputWithInfo from "../custom-elements/InputWithInfo";
import Input from "../custom-elements/Input";
import { register } from "../../actions/auth-actions";
import {validate} from "react-email-validator";
const RegisterForm = (props) => {
  const username = useRef();
  const domain = useRef();
  const email = useRef();
  const password = useRef();
  const submitRef = useRef();
  const [formIsValid, setFormIsValid] = useState(false);

  const validatePassword = () => {
    let passwordValue = password.current.value;
    if (passwordValue.length >= 6) {
      password.current.classList.remove("invalid");
      password.current.classList.add("valid");
      return true;
    } else {
      password.current.classList.remove("valid");
      password.current.classList.add("invalid");
      return false;
    }
  };

  const validateDomain = () => {
    let domainValue = domain.current.value;
    if (domainValue.length > 0) {
      domain.current.classList.remove("invalid");
      domain.current.classList.add("valid");
      return true;
    } else {
      domain.current.classList.remove("valid");
      domain.current.classList.add("invalid");
      return false;
    }
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    let newUser = {
      username: username.current.value,
      password: password.current.value,
      email: email.current.value,
      domain: domain.current.value,
    };
    register(newUser)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });

      if (formIsValid) {
        console.log("form is valid");
      }
  };

  const checkFormValidity = () => {
    if (
      validateUsername() &&
      validatePassword() &&
      validateEmail()
    ) {
      setFormIsValid(true);
      submitRef.current.disabled = false;
    } else {
      setFormIsValid(false);
      submitRef.current.disabled = true;
    }
  }
  const validateUsername = () => {
    let usernameValue = username.current.value;
    if (usernameValue.length > 0) {
      username.current.classList.remove("invalid");
      username.current.classList.add("valid");
      return true;
    } else {
      username.current.classList.remove("valid");
      username.current.classList.add("invalid");
      return false;
    }
    checkFormValidity();
  };

  const validateEmail = () => {
    let emailValue = email.current.value;
    if (validate(emailValue)) {
      email.current.classList.remove("invalid");
      email.current.classList.add("valid");
      return true;
    } else {
      email.current.classList.remove("valid");
      email.current.classList.add("invalid");
      return false;
    }
    checkFormValidity();
  };

  const handleDomainChange = (event) => {
    let domainv = event.target.value;
    let domainSlug = document.getElementById("domain-slug");
    if (domainv.length > 3) {
      let slugged = slugify(domainv, {
        replacement: "-", // replace spaces with replacement character, defaults to `-`
        remove: undefined, // remove characters that match regex, defaults to `undefined`
        lower: true, // convert to lower case, defaults to `false`
        strict: true, // strip special characters except replacement, defaults to `false`
        locale: "en", // language code of the locale to use
        trim: true, // trim leading and trailing replacement chars, defaults to `true`
      });
      domainSlug.innerText = slugged;
      domain.current.classList.add("valid");
    } else {
      domain.current.classList.remove("valid");
      domainSlug.innerText = "example";
    }
    checkFormValidity();
  };

  return (
    <form className="register" id="register_form" onSubmit={handleRegister}>
      <div className="register-title">Create a new user</div>
      <input
        ref={username}
        type="text"
        name="username"
        onChange={() => validateUsername("username")}
        placeholder="Enter your username"
      />
      <input
        ref={email}
        type="email"
        name="email"
        onChange={() => validateEmail("email")}
        placeholder="Enter your email"
      />
      <input
        ref={password}
        type="password"
        name="password"
        placeholder="Enter password"
        onChange={() => validatePassword("password")}
      />
      <InputWithInfo
        name="domain"
        reference={domain}
        onChange={() => validateDomain("domain")}
        onChangeHandler={handleDomainChange}
        textDescriptioin={[
          "Domain name is used to create a unique URL for your vault.",
          'For example, if you enter "myvault", your vault will be accessible at "myvault.screenshoot.com"',
        ]}
      />
      <div className="domain-preview">
        https://<span id="domain-slug">example</span>.screenshoot.com
      </div>

      <div className="submit-container">
        <button type="submit" ref={submitRef} disabled>
          Submit
        </button>
      </div>
    </form>
  );
};

export default RegisterForm;
