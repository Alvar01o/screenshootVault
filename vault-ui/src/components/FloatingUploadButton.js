import React, {useState} from "react";
import "./FloatingUploadButton.css";
import { ReactComponent as UploadLogo } from "./upload.svg";

const FloatingUploadButton = (props) => {
//  const [style, setStyle] = useState({ logoHeight:  document.body.offsetHeight + (document.querySelector('header')?.offsetHeight ?? 0) });


//  const handleScroll = () => {
//    let scrollTop = window.scrollY,
//      minHeight =
//        document.body.offsetHeight -
//        (document.querySelector("header")?.offsetHeight ?? 0),
//      logoHeight = Math.max(
//        minHeight,
//        document.body.scrollHeight -
//          scrollTop -
//          (document.querySelector("header")?.offsetHeight ?? 0)
//      );
//        setStyle({ logoHeight });
//  };

  return (
    //style={{ height: style.logoHeight }}
    <div className="rightPanel">
      <div className="floating-upload-button" onClick={props.onClick}>
        <button>
          <UploadLogo />
        </button>
      </div>
    </div>
  );
};
export default FloatingUploadButton;
