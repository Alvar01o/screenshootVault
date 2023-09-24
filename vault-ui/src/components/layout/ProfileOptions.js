import { Component } from "react";

const ProfileOptions = () => {
    const logoutHandler = () => {
        localStorage.removeItem('user');
    }
    
    return (<div><a onClick={logoutHandler}>Logout</a></div>)
}

export default ProfileOptions;

