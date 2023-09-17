import { Component } from "react";
import { ReactComponent as ReactPersonLogo } from "./person.svg";
import "./Header.css";
const headerMenu = ["Files", "Tags", "Explore"];

class Header extends Component {
  clickHandler = () => {
    console.log("click");
  };
  render() {
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
                  <a href="">{item}</a>
                </li>
              );
            })}
          </ul>
        </nav>
        <div className="profile" onClick={this.clickHandler}>
          <div className="profile-image">
            <ReactPersonLogo />
          </div>
        </div>
      </header>
    );
  }
}

export default Header;
