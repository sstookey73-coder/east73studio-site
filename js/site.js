// East 73 Studio — the only script on the site. No tracking, no cookies.
(function () {
  // Current year in the footer
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Gentle fade-in for images marked .fade (CSS skips it for reduced motion)
  document.querySelectorAll("img.fade").forEach(function (img) {
    if (img.complete) { img.classList.add("is-loaded"); return; }
    img.addEventListener("load", function () { img.classList.add("is-loaded"); });
    img.addEventListener("error", function () { img.classList.add("is-loaded"); });
  });
})();
