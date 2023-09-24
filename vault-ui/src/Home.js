import React from "react";
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import FloatingUploadButton from "./components/FloatingUploadButton";
import MainComponent from "./components/MainComponent"; 
import ImageCard from "./components/ImageCard";

const Home = () => {
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
export default Home;
