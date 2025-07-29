// Simple script to toggle mobile menu if you want to add later
document.addEventListener("DOMContentLoaded", function() {
  const menuToggle = document.getElementById('menu-toggle');
  const navMenu = document.getElementById('nav-menu');

  if(menuToggle) {
    menuToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
    });
  }
});

// Optional: Alert user on form submit (can be removed)
function confirmSubmission() {
  alert('Your form has been submitted successfully!');
}
