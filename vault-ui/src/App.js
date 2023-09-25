import React, { useEffect } from "react";
import "./App.css";
import Home from "./Home";
import SignIn from "./Sign-in";
import AuthContext from "./store/auth-context";
function App() {
  const [isLoggedIn, setIsLoggedIn] = React.useState();
  const user = localStorage.getItem("user");
  const realUserInformation = JSON.parse(user || "{}");

  useEffect(() => {
    if (realUserInformation?.token) {
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, [isLoggedIn, realUserInformation?.token]);
  const onLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem("user");
  };
  const onUpdateStatus = (status) => {
    setIsLoggedIn(status);
  };
  return (
    <>
      <AuthContext.Provider
        value={{ isLoggedIn: isLoggedIn, onLogout: onLogout }}
      >
        {isLoggedIn ? (
          <Home></Home>
        ) : (
          <SignIn onUpdateStatus={onUpdateStatus} />
        )}
      </AuthContext.Provider>
    </>
  );
}

export default App;
