import React, { Component } from "react";
import "./FloatingUploadButton.css";
import { ReactComponent as UploadLogo } from "./upload.svg";

type State  = {
  style: {
      logoHeight: number
  }
}

class FloatingUploadButton extends Component<{}, State> {
  clickHandler = () => {
    //show form in side section of page with neccesary to upload file
    console.log("click");
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

  componentWillMount() {
    this.setState({
      style: {
        logoHeight: 0,
      },
  });
  }
  
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
