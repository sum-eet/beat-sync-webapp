import React from "react";
import axios from "axios";

const GenerateButton = ({ audio, images, onComplete }) => {
  const handleGenerate = async () => {
    const formData = new FormData();
    formData.append("audio", audio);
    images.forEach((image) => {
      formData.append("images", image);
    });

    try {
      // Enforce a minimum delay of 5 seconds
      const delay = new Promise((resolve) => setTimeout(resolve, 5000));

      // Start the video generation request
      const videoRequest = axios.post(
        "https://beat-sync-webapp-backend.onrender.com/upload",
        formData,
        {
          responseType: "blob", // Expect a video file as a blob
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      // Wait for both the backend request and the enforced delay
      const [response] = await Promise.all([videoRequest, delay]);

      // Create a URL for the generated video
      const videoUrl = URL.createObjectURL(new Blob([response.data]));
      onComplete(videoUrl);
    } catch (error) {
      console.error("Error generating video:", error);
      alert("An error occurred while generating the video. Please try again.");
    }
  };

  return (
    <button
      onClick={handleGenerate}
      style={{ padding: "12px 20px", fontSize: "16px" }}
    >
      Generate Video
    </button>
  );
};

export default GenerateButton;
