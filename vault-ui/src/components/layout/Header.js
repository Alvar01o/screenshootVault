import { Component } from "react";
import { ReactComponent as ReactPersonLogo } from "./person.svg";
import "./Header.css";
import ProfileOptions from "./ProfileOptions";
const headerMenu = ["Files", "Tags", "Explore"];

const Header = () => {
  const clickHandler = () => {
    console.log("click");
  };
  
  return (
    <header>
      <img
        src="/logo512.png"
        alt=""
        width={30}
        height={30}
        className="logo"
      />
      <nav className="nav-menu">
        <ul>
          {headerMenu.map((item, index) => {
            return (
              <li key={index}>
                <a href="" className="nav-item">{item}</a>
              </li>
            );
          })}
        </ul>
      </nav>
      <div className="profile" onClick={clickHandler}>
        <div className="profile-image">
          <ReactPersonLogo />
          <ProfileOptions/>
        </div>
      </div>
    </header>
  );
}

export default Header;
