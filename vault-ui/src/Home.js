import React from "react";
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import FloatingUploadButton from "./components/FloatingUploadButton";
import MainComponent from "./components/MainComponent"; 
import ImageCard from "./components/ImageCard";
import UploadFileForm from "./components/UploadFileForm";
const Home = () => {
  const clickHandler = () => {
    //show form in side section of page with neccesary to upload file
    console.log("click");
  };

  return (
    <>
      <Header></Header>
      <FloatingUploadButton onClick={clickHandler}></FloatingUploadButton>
      <MainComponent>
        <ImageCard></ImageCard>
        <UploadFileForm/>
      </MainComponent>
      <Footer></Footer>

    </>
  );
}
export default Home;
