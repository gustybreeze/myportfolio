// ====== Toggle Navigation Menu ======
function toggleMenu() {
  const navLinks = document.getElementById("navLinks");
  navLinks.classList.toggle("show");
}

// Close menu when a link is clicked
document.querySelectorAll("#navLinks a").forEach(link => {
  link.addEventListener("click", () => {
    document.getElementById("navLinks").classList.remove("show");
  });
});

// ====== Dark / Light Mode Toggle ======
const modeToggle = document.getElementById("modeToggle");
const body = document.body;

// Check if user had previously selected dark mode (localStorage)
if (localStorage.getItem("theme") === "dark") {
  body.classList.add("dark-mode");
  modeToggle.textContent = "Light Mode";
} else {
  modeToggle.textContent = "Dark Mode";
}

modeToggle.addEventListener("click", () => {
  body.classList.toggle("dark-mode");

  if (body.classList.contains("dark-mode")) {
    modeToggle.textContent = "Light Mode";
    localStorage.setItem("theme", "dark");
  } else {
    modeToggle.textContent = "Dark Mode";
    localStorage.setItem("theme", "light");
  }
});
