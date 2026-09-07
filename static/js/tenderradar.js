(function () {
  "use strict";

  function qs(selector, root) {
    return (root || document).querySelector(selector);
  }

  function qsa(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  /* Mobile navigation */
  var toggle = qs("#nav-toggle");
  var nav = qs("#site-nav");

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

  /* Collapsible filter panel (mobile) */
  var filterToggle = qs("#filter-toggle");
  var filterPanel = qs("#filter-panel");

  if (filterToggle && filterPanel) {
    filterToggle.addEventListener("click", function () {
      var collapsed = filterPanel.classList.toggle("is-collapsed");
      filterToggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
      qs(".filter-toggle-label", filterToggle).textContent = collapsed
        ? "Show filters"
        : "Hide filters";
    });

    if (window.matchMedia("(max-width: 960px)").matches) {
      filterPanel.classList.add("is-collapsed");
      filterToggle.setAttribute("aria-expanded", "false");
      qs(".filter-toggle-label", filterToggle).textContent = "Show filters";
    }
  }

  /* Filter form */
  var filterForm = qs("#filter-form");
  if (filterForm) {
    qsa("select", filterForm).forEach(function (field) {
      field.addEventListener("change", function () {
        filterForm.submit();
      });
    });

    filterForm.addEventListener("submit", function () {
      var register = qs(".register-main");
      if (register) {
        sessionStorage.setItem("tenderradar-scroll-target", "register");
      }
    });
  }

  /* Scroll to results after filter */
  if (sessionStorage.getItem("tenderradar-scroll-target") === "register") {
    sessionStorage.removeItem("tenderradar-scroll-target");
    var registerMain = qs(".register-main");
    if (registerMain) {
      registerMain.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  /* Active filter chips */
  var activeFilters = qs("#active-filters");
  if (filterForm && activeFilters) {
    var chipConfig = [
      { name: "q", label: "Keyword" },
      { name: "province", label: "Province" },
      { name: "tender_type", label: "Type" },
      { name: "source", label: "Source" },
    ];

    chipConfig.forEach(function (config) {
      var field = qs('[name="' + config.name + '"]', filterForm);
      if (!field || !field.value) {
        return;
      }

      var displayValue = field.value;
      if (field.tagName === "SELECT") {
        var selected = field.options[field.selectedIndex];
        if (selected) {
          displayValue = selected.text;
        }
      }

      activeFilters.hidden = false;

      var chip = document.createElement("span");
      chip.className = "filter-chip";
      chip.innerHTML =
        config.label + ": " + displayValue +
        ' <button type="button" aria-label="Remove ' + config.label + ' filter">&times;</button>';

      chip.querySelector("button").addEventListener("click", function () {
        field.value = "";
        filterForm.submit();
      });

      activeFilters.appendChild(chip);
    });
  }

  /* Closing date urgency styling */
  qsa("[data-days-left]").forEach(function (element) {
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

  /* Expandable descriptions */
  qsa("[data-expandable]").forEach(function (paragraph) {
    paragraph.classList.add("is-clamped");

    if (paragraph.scrollHeight <= paragraph.clientHeight + 2) {
      return;
    }

    var button = paragraph.parentElement.querySelector(".expand-toggle");
    if (!button) {
      return;
    }

    button.hidden = false;
    button.addEventListener("click", function () {
      var expanded = paragraph.classList.toggle("is-clamped");
      button.setAttribute("aria-expanded", expanded ? "false" : "true");
      button.textContent = expanded ? "Show full description" : "Show less";
    });
  });
})();
