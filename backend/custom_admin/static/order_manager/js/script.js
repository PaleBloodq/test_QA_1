document.getElementById("uploadButton").addEventListener("click", function () {
  document.getElementById("fileInput").click();
});

document.getElementById("fileInput").addEventListener("change", function (event) {
  handleFiles(event.target.files);
  event.target.value = "";
});

function handleFiles(files) {
  const thumbnailsContainer = document.getElementById("thumbnails");

  for (const file of files) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const base64String = e.target.result;
      const base64Data = base64String.substring(base64String.indexOf(',') + 1).trim();
      base64Images.push(base64Data);

      const thumbnailWrapper = document.createElement("div");
      thumbnailWrapper.classList.add("relative", "w-16", "h-16", "flex-shrink-0");

      const img = document.createElement("img");
      img.src = e.target.result;
      img.classList.add("w-full", "h-full", "object-cover", "rounded");

      const removeButton = document.createElement("button");
      removeButton.innerHTML = "&times;";
      removeButton.classList.add(
        "absolute",
        "top-0",
        "right-0",
        "bg-red-500",
        "text-white",
        "rounded-full",
        "w-6",
        "h-6",
        "flex",
        "items-center",
        "justify-center",
        "cursor-pointer"
      );

      removeButton.addEventListener("click", function () {
        thumbnailsContainer.removeChild(thumbnailWrapper);
        const index = base64Images.indexOf(base64Data);
        if (index > -1) {
          base64Images.splice(index, 1);
        }
      });

      thumbnailWrapper.appendChild(img);
      thumbnailWrapper.appendChild(removeButton);
      thumbnailsContainer.appendChild(thumbnailWrapper);
    };

    reader.readAsDataURL(file);
  }
}

const messageInput = document.getElementById("messageInput");

messageInput.addEventListener("dragover", function (event) {
  event.preventDefault();
  event.stopPropagation();
  messageInput.classList.add("border-blue-500");
});

messageInput.addEventListener("dragleave", function (event) {
  event.preventDefault();
  event.stopPropagation();
  messageInput.classList.remove("border-blue-500");
});

messageInput.addEventListener("drop", function (event) {
  event.preventDefault();
  event.stopPropagation();
  messageInput.classList.remove("border-blue-500");

  const files = event.dataTransfer.files;
  handleFiles(files);
});