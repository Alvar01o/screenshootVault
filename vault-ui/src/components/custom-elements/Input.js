import React, { useRef } from "react";

const Input = (props) => {
  return (
    <>
      <input
        type={props.type}
        id={props.id}
        ref={props.reference}
        name={props.name}
        value={props.value}
        onChange={props.onChange}
        onBlur={props.onBlur}
        placeholder={props.placeholder}
      />
    </>
  );
};
export default Input;