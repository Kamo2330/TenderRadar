(function () {
  "use strict";

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }

  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* Mobile menu */
  var menuBtn = $("#menu-btn");
  var mainNav = $("#main-nav");

  if (menuBtn && mainNav) {
    menuBtn.addEventListener("click", function () {
      var open = mainNav.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  /* Advanced filters toggle */
  var advToggle = $("#advanced-toggle");
  var advPanel = $("#search-advanced");
  var filterForm = $("#filter-form");

  function openAdvanced() {
    if (!advPanel || !advToggle) return;
    advPanel.classList.add("is-open");
    advToggle.setAttribute("aria-expanded", "true");
    advToggle.textContent = "Hide filters";
  }

  if (advToggle && advPanel) {
    var hasAdvanced =
      $("#province", filterForm)?.value ||
      $("#tender_type", filterForm)?.value ||
      $("#source", filterForm)?.value ||
      ($("#sort", filterForm)?.value && $("#sort", filterForm).value !== "newest");

    if (hasAdvanced) {
      openAdvanced();
    }

    advToggle.addEventListener("click", function () {
      var isOpen = advPanel.classList.toggle("is-open");
      advToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      advToggle.textContent = isOpen ? "Hide filters" : "Advanced filters";
    });
  }

  /* Auto-submit selects */
  if (filterForm) {
    $$("select", filterForm).forEach(function (el) {
      el.addEventListener("change", function () {
        filterForm.submit();
      });
    });
  }

  /* Filter tags */
  var tagsEl = $("#filter-tags");
  if (filterForm && tagsEl) {
    var tagFields = [
      { name: "q", label: "Search" },
      { name: "province", label: "Province" },
      { name: "tender_type", label: "Type" },
      { name: "source", label: "Source" },
    ];

    tagFields.forEach(function (cfg) {
      var field = $('[name="' + cfg.name + '"]', filterForm);
      if (!field || !field.value) return;

      var text = field.value;
      if (field.tagName === "SELECT") {
        text = field.options[field.selectedIndex]?.text || text;
      }

      tagsEl.hidden = false;
      var tag = document.createElement("span");
      tag.className = "filter-tag";
      tag.innerHTML = cfg.label + ": " + text + ' <button type="button" aria-label="Remove">&times;</button>';
      tag.querySelector("button").addEventListener("click", function () {
        field.value = "";
        filterForm.submit();
      });
      tagsEl.appendChild(tag);
    });
  }

  /* Urgency badges */
  $$("[data-days]").forEach(function (el) {
    var days = parseInt(el.getAttribute("data-days"), 10);
    if (isNaN(days)) return;
    el.classList.add(days <= 7 && days >= 0 ? "is-urgent" : "is-ok");
  });

  /* Clickable table rows */
  $$(".data-row[data-href]").forEach(function (row) {
    row.addEventListener("click", function (e) {
      if (e.target.closest("a")) return;
      var href = row.getAttribute("data-href");
      if (href) window.open(href, "_blank", "noopener");
    });

    row.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        var href = row.getAttribute("data-href");
        if (href) window.open(href, "_blank", "noopener");
      }
    });
  });

  /* Highlight search terms in titles */
  var query = $("#q")?.value?.trim();
  if (query && query.length >= 2) {
    var terms = query.split(/\s+/).filter(Boolean);
    var pattern = new RegExp("(" + terms.map(function (t) {
      return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }).join("|") + ")", "gi");

    $$(".row-title").forEach(function (el) {
      var html = el.textContent.replace(pattern, "<mark class=\"highlight\">$1</mark>");
      if (html !== el.textContent) el.innerHTML = html;
    });
  }

  /* Scroll to results on search */
  if (window.location.search && $("#tender-results")) {
    requestAnimationFrame(function () {
      $("#tender-results").scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
})();
