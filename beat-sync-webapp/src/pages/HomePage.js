import React, { useState } from "react";
import FileUpload from "../components/FileUpload";
import ImagePreview from "../components/ImagePreview";
import GenerateButton from "../components/GenerateButton";
import DownloadLink from "../components/DownloadLink";
import "/Users/sumeetkarwa/Documents/Code/beat-sync-webapp/beat-sync-webapp/src/styles/app.css";

const HomePage = () => {
  const [audio, setAudio] = useState(null);
  const [images, setImages] = useState([]);
  const [videoUrl, setVideoUrl] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleAudioUpload = (file) => setAudio(file);
  const handleImageUpload = (files) => setImages(files);

  const handleGenerateVideo = async (onComplete) => {
    setIsProcessing(true);
    setProgress(0);

    // Simulate progress for now (replace with real updates if available)
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 20;
      });
    }, 500);

    // Complete video generation
    await onComplete();
    setIsProcessing(false);
  };

  return (
    <div className="container">
      <h1 style={{ textAlign: "center" }}>Beat-Sync Video Creator</h1>

      {/* Audio Upload Section */}
      <div className="file-upload">
        <h2 className="section-title">Upload Audio</h2>
        <FileUpload
          onUpload={(file) => handleAudioUpload(file)}
          accept="audio/*"
          multiple={false}
        />
      </div>

      {/* Image Upload Section */}
      <div className="file-upload">
        <h2 className="section-title">Upload Images</h2>
        <FileUpload
          onUpload={(files) => handleImageUpload(files)}
          accept="image/*"
          multiple={true}
        />
        {images.length > 0 && <ImagePreview images={images} />}
      </div>

      {/* Generate Button and Progress Bar */}
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        {audio && images.length > 0 && (
          <>
            <GenerateButton
              audio={audio}
              images={images}
              onComplete={(url) => {
                setVideoUrl(url);
                setIsProcessing(false);
                setProgress(100);
              }}
            />
            {isProcessing && (
              <div className="progress-bar-container">
                <div
                  className="progress-bar"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Video Download/Preview Section */}
      {videoUrl && (
        <div className="video-preview">
          <DownloadLink videoUrl={videoUrl} />
        </div>
      )}
    </div>
  );
};

export default HomePage;
