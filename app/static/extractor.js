document.addEventListener("DOMContentLoaded", function () {
  const uploadButton = document.getElementById("upload-button");
  const fileInput = document.getElementById("cv-file");
  const uploadStatus = document.getElementById("upload-status");
  const extractedDataText = document.getElementById("extracted-data-text");
  const answerText = document.getElementById("answer-text");
  const fileName = document.getElementById("file-name");

  fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];
    if (file) {
      fileName.textContent = `Selected file: ${file.name}`;
    } else {
      fileName.textContent = "No file selected";
    }
  });

  uploadButton.addEventListener("click", async function () {
    const file = fileInput.files[0];

    if (!file) {
      uploadStatus.textContent = "Please select a file before uploading.";
      uploadStatus.style.color = "red";
      return;
    }

    const formData = new FormData();
    formData.append("cv", file);

    try {
      uploadStatus.textContent = "Uploading...";
      uploadStatus.style.color = "blue";

      const response = await fetch("/cv-extractor", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Network response was not ok");
      }

      const result = await response.json();

      // Update the extracted data
      extractedDataText.textContent = result.text;
      answerText.textContent = result.answer;

      uploadStatus.textContent = "File uploaded successfully!";
      uploadStatus.style.color = "green";
    } catch (error) {
      console.error("Error uploading file:", error);
      uploadStatus.textContent = `Error: ${
        error.message || "Failed to upload the file."
      }`;
      uploadStatus.style.color = "red";
    }
  });
});
