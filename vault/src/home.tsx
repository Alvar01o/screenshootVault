import React, { Component } from "react";
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import FloatingUploadButton from "./components/FloatingUploadButton";
import MainComponent from "./components/MainComponent"; 
import ImageCard from "./components/ImageCard";
interface Props {}
interface State {}


class Home extends Component<Props, State> {

  render() {
    return (
      <>
        <Header></Header>
        <FloatingUploadButton></FloatingUploadButton>
        <MainComponent>
          <ImageCard></ImageCard>
        </MainComponent>
        <Footer></Footer>

      </>
    );
  }
}

export default Home;
