(function () {
  "use strict";

  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      toggle.setAttribute(
        "aria-label",
        isOpen ? "Close navigation menu" : "Open navigation menu"
      );
    });

    document.addEventListener("click", function (event) {
      if (!nav.classList.contains("is-open")) {
        return;
      }
      if (!nav.contains(event.target) && !toggle.contains(event.target)) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation menu");
      }
    });
  }

  var filterForm = document.getElementById("filter-form");
  if (filterForm) {
    var autoSubmitFields = filterForm.querySelectorAll("select");
    autoSubmitFields.forEach(function (field) {
      field.addEventListener("change", function () {
        filterForm.submit();
      });
    });

    var searchInput = filterForm.querySelector("#q");
    if (searchInput) {
      searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          event.preventDefault();
          filterForm.submit();
        }
      });
    }
  }

  document.querySelectorAll("[data-days-left]").forEach(function (element) {
    var days = parseInt(element.getAttribute("data-days-left"), 10);
    if (Number.isNaN(days)) {
      return;
    }
    if (days <= 7 && days >= 0) {
      element.classList.add("is-urgent");
    } else if (days > 7) {
      element.classList.add("is-normal");
    }
  });
})();
