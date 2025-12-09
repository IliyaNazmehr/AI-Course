
  const textInput = document.getElementById("textInput");
  const wordCountDisplay = document.getElementById("wordCount");
  const submitBtn = document.getElementById("submitBtn");
  const MAX_WORDS = 500;

  textInput.addEventListener("input", () => {
    const words = textInput.value.trim().split(/\s+/).filter(Boolean);
    const count = words.length;
    wordCountDisplay.textContent = count;

    // If word limit exceeded, disable submit button
    if (count > MAX_WORDS) {
      textInput.classList.add("is-invalid");
      submitBtn.disabled = true;
      wordCountDisplay.style.color = "red";
    } else {
      textInput.classList.remove("is-invalid");
      submitBtn.disabled = false;
      wordCountDisplay.style.color = "inherit";
    }
  });
