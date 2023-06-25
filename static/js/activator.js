const links = document.querySelectorAll('.nav-link');
   
// Handles highlighting the active page in the nav bar
if (links.length) {
  links.forEach((link) => {
    link.classList.remove('active');
    if (link.href === window.location.href) {
        link.classList.add("active");
    }
  });
  navBrand = document.getElementById("navbar-brand");
  navBrand.classList.remove("active");
  if (navBrand.href === window.location.href) {
    navBrand.classList.add("active");
  }
}
