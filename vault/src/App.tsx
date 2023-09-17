import React, {useEffect} from 'react';
import './App.css';
import Home from "./Home";
import SignIn from "./Sign-in";
function App() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const user: string | null = localStorage.getItem("user");
  const realUserInformation = JSON.parse(user || "{}");

  useEffect(() => {
    if (realUserInformation?.token) {
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, [isLoggedIn]); 
  const onUpdateStatus = (status: boolean) => {
    setIsLoggedIn(status);
  }
  return (
    <>
    {isLoggedIn ? <Home></Home> : <SignIn onUpdateStatus={onUpdateStatus}/>}
    </>
  );
}

export default App;
