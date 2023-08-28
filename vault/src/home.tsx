import React, { Component } from "react";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import FilesContainer from "./components/FilesContainer";
interface Props {}
interface State {}

class Home extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
  }

  componentDidMount() {}

  shouldComponentUpdate(nextProps: Props, nextState: State) {
    return true;
  }

  componentDidUpdate(prevProps: Props, prevState: State) {}

  componentWillUnmount() {}

  render() {
    return (
      <div>
        <ResponsiveAppBar />
        <FilesContainer />
      </div>
    );
  }
}

export default Home;
