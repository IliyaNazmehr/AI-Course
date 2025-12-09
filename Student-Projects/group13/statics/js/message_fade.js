
  // Automatically fade out alerts after 3 seconds
  setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      alert.classList.remove('show');
      alert.classList.add('hide');  // optional, adds smoother effect
      setTimeout(() => alert.remove(), 500);  // remove from DOM after fade
    });
  }, 3000); // 3000ms = 3 seconds
