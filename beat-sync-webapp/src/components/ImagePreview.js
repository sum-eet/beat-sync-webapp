import React from "react";

const ImagePreview = ({ images }) => {
  return (
    <div>
      <h3>Preview Images</h3>
      <div>
        {images.map((image, index) => (
          <img
            key={index}
            src={URL.createObjectURL(image)}
            alt={`Preview ${index}`}
            style={{ width: "100px", margin: "5px" }}
          />
        ))}
      </div>
    </div>
  );
};

export default ImagePreview;
