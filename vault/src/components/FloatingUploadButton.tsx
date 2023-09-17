import React, { Component } from "react";
import "./FloatingUploadButton.css";
import { ReactComponent as UploadLogo } from "./upload.svg";
interface Props {}
interface State {}

class FloatingUploadButton extends Component<Props, State> {
  clickHandler = () => {
    //show form in side section of page with neccesary to upload file
    console.log("click");
  };
  getInitialState = () => {
    return {
        style: {
            logoHeight: 200
        }
    }
};

  handleScroll = () => {
    let scrollTop = window.scrollY,
      minHeight = 30,
      logoHeight = Math.max(minHeight, 200 - scrollTop);
    this.setState({
      style: {
        logoHeight: logoHeight,
      },
    });
  };
  componentDidMount = () => {
    window.addEventListener("scroll", this.handleScroll);
  };

  componentWillUnmount = () => {
    window.removeEventListener("scroll", this.handleScroll);
  };

  render() {
    return (
      <div
        className="rightPanel"
        style={{ height: this.state.style.logoHeight }}
      >
        <div className="floating-upload-button" onClick={this.clickHandler}>
          <button>
            <UploadLogo />
          </button>
        </div>
      </div>
    );
  }
}

export default FloatingUploadButton;
