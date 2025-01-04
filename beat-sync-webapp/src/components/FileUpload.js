import React from "react";

const FileUpload = ({ onUpload, accept, multiple }) => {
  const handleFileChange = (e) => {
    if (multiple) {
      onUpload([...e.target.files]);
    } else {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={handleFileChange}
      />
    </div>
  );
};

export default FileUpload;
