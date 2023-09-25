import React from "react";
import AuthContext from "../../store/auth-context";

const ProfileOptions = (props) => {
const authContext = React.useContext(AuthContext);
const profileHandler = () => {
    console.log("profile");
}
  return (
    <>
      {props.isVisible && (
        <div className="profile-options">
          <ul>
            <li onClick={authContext.onLogout}>Logout</li>
            <li onClick={profileHandler}>Profile</li>
          </ul>
        </div>
      )}
    </>
  );
};

export default ProfileOptions;
