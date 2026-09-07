(function () {
  "use strict";

  // Mobile navigation toggle
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
  }

  // Auto-submit filters when selects change (optional UX boost)
  var filterForm = document.getElementById("filter-form");
  if (filterForm) {
    var selects = filterForm.querySelectorAll("select");
    selects.forEach(function (sel) {
      sel.addEventListener("change", function () {
        filterForm.submit();
      });
    });
  }

  // Highlight cards closing within 7 days
  document.querySelectorAll("[data-days-left]").forEach(function (el) {
    var days = parseInt(el.getAttribute("data-days-left"), 10);
    if (!isNaN(days) && days <= 7 && days >= 0) {
      el.classList.add("urgent");
    } else if (!isNaN(days) && days > 7) {
      el.classList.add("normal");
    }
  });
})();
