function toggleMenu() {
  const navLinks = document.getElementById("navLinks");
  navLinks.classList.toggle("show");
}

// Optional: Scroll to section on link click (smooth effect already via CSS)
document.querySelectorAll(".nav-links a").forEach(link => {
  link.addEventListener("click", () => {
    document.getElementById("navLinks").classList.remove("show");
  });
});

  const modeToggle = document.getElementById("modeToggle");
  const body = document.body;

  modeToggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    
    if (body.classList.contains("dark-mode")) {
      modeToggle.textContent = "Light Mode";
    } else {
      modeToggle.textContent = "Dark Mode";
    }
  });
