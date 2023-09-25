import React from "react";
import { ReactComponent as ReactPersonLogo } from "./person.svg";
import "./Header.css";
import ProfileOptions from "./ProfileOptions";
const headerMenu = [
  { name: "Files", route: "" },
  { name: "Teams", route: "" },
  { name: "Tags", route: "" },
];

const Header = () => {
  const [isProfileOptionsActive, setIsProfileOptionsActive] =
    React.useState(false);

  const toggleProfileOptions = () => {
    setIsProfileOptionsActive(!isProfileOptionsActive);
  };

  return (
    <header>
      <div className="header-content">
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
                  <a href={item.route} className="nav-item">
                    {item.name}
                  </a>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>
      <div className="profile">
        <div className="profile-image" onClick={toggleProfileOptions}>
          <ReactPersonLogo />
        </div>
        <ProfileOptions isVisible={isProfileOptionsActive} />
      </div>
    </header>
  );
};

export default Header;
