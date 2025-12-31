function sendMessage() {
  const input = document.getElementById("user-input").value;
  const messages = document.getElementById("messages");

  if (!input) return;
  messages.innerHTML += `<div>👤 ${input}</div>`;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input })
  })
  .then(res => res.json())
  .then(data => {
    // پاک کردن لیست‌های قبلی و فقط نمایش پاسخ جدید
    messages.innerHTML += `<div>🤖 ${data.reply}</div>`;
    messages.scrollTop = messages.scrollHeight;
  })
  .catch(err => {
    messages.innerHTML += `<div style="color:red">انگار مشکلی پیش اومده متاسفم دوست من!</div>`;
  });

  document.getElementById("user-input").value = "";
}

function sendQuick(text) {
  const messages = document.getElementById("messages");
  messages.innerHTML += `<div>👤 ${text}</div>`;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
  .then(res => res.json())
  .then(data => {
    // وقتی کاربر یکی از گزینه‌ها رو انتخاب کرد، فقط نتیجه نمایش داده بشه
    messages.innerHTML += `<div>🤖 ${data.reply}</div>`;
    messages.scrollTop = messages.scrollHeight;
  })
  .catch(err => {
    messages.innerHTML += `<div style="color:red">انگار مشکلی پیش اومده متاسفم دوست من!</div>`;
  });
}
