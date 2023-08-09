import React from "react";
import { IUser } from "../interfaces";

const initializeUser: IUser = {
  name: "",
  email: "",
};

interface IState {
  user: IUser;
}

interface IProps {
  children: React.ReactNode;
}

export const UserContext = React.createContext<IUser>(initializeUser);

export class UserContextProvider extends React.Component<IProps, IState> {
  state: IState = {
    user: initializeUser,
  };

  render() {
    return (
      <UserContext.Provider value={this.state.user}>
        {this.props.children}
      </UserContext.Provider>
    );
  }
}
