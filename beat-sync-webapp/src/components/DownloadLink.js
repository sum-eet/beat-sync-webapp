import React from "react";

const DownloadLink = ({ videoUrl }) => {
  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      {videoUrl && (
        <>
          <h3>Generated Video:</h3>
          <video
            controls
            src={videoUrl}
            style={{
              width: "100%",
              maxWidth: "600px",
              margin: "10px 0",
              borderRadius: "8px",
            }}
          />
          <br />
          <a
            href={videoUrl}
            download="generated_video.mp4"
            style={{
              fontSize: "18px",
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "5px",
              textDecoration: "none",
              cursor: "pointer",
            }}
          >
            Download Video
          </a>
        </>
      )}
    </div>
  );
};

export default DownloadLink;
