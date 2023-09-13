import React, { Component } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
interface Props {}
interface State {}


class Home extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
  }

  render() {
    return (
      <section>
        <Header></Header>
        <main></main>
        <Footer></Footer>
      </section>
    );
  }
}

export default Home;
