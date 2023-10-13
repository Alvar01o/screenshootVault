import React, { useState } from "react";
import "./InputWithInfo.css";
import { BsFillQuestionCircleFill } from "react-icons/bs";
import Input from "./Input";

const InputWithInfo = (props) => {
  const [viewInfo, setViewInfo] = useState(false);

  const infoClickHandler = () => {
    setViewInfo(!viewInfo);
  };

  return (
    <>
      <div className="inputWithInfo">
        <Input

          type="text"
          name={props.name}
          reference={props.reference}
          onChange={props.onChangeHandler}
          placeholder={props.placeholder}
        />
        <BsFillQuestionCircleFill onClick={infoClickHandler} />
      </div>
      <div
        className={
          viewInfo ? "field-description d-block" : "field-description d-none"
        }
      >
        {props.textDescriptioin.map((text, index) => (
          <span key={index}>{text}</span>
        ))}
      </div>
    </>
  );
};
export default InputWithInfo;
