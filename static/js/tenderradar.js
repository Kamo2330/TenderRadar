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
    });
  }

  /* Advanced filters */
  var advToggle = $("#advanced-toggle");
  var advPanel = $("#search-advanced");
  var filterForm = $("#filter-form");

  function setAdvanced(open) {
    if (!advPanel || !advToggle) return;
    advPanel.classList.toggle("is-open", open);
    advToggle.setAttribute("aria-expanded", open ? "true" : "false");
    advToggle.textContent = open ? "Hide filters" : "Advanced filters";
  }

  if (advToggle && advPanel) {
    var hasAdvanced =
      ($("#province", filterForm) && $("#province", filterForm).value) ||
      ($("#tender_type", filterForm) && $("#tender_type", filterForm).value) ||
      ($("#source", filterForm) && $("#source", filterForm).value) ||
      ($("#sort", filterForm) && $("#sort", filterForm).value !== "newest");

    if (hasAdvanced) setAdvanced(true);

    advToggle.addEventListener("click", function () {
      setAdvanced(!advPanel.classList.contains("is-open"));
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
    [
      { name: "q", label: "Search" },
      { name: "province", label: "Province" },
      { name: "tender_type", label: "Type" },
      { name: "source", label: "Source" },
    ].forEach(function (cfg) {
      var field = $('[name="' + cfg.name + '"]', filterForm);
      if (!field || !field.value) return;

      var text = field.value;
      if (field.tagName === "SELECT" && field.selectedIndex >= 0) {
        text = field.options[field.selectedIndex].text;
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

  /* Clickable cards */
  $$(".tender-card[data-href]").forEach(function (card) {
    card.addEventListener("click", function (e) {
      if (e.target.closest("a")) return;
      var href = card.getAttribute("data-href");
      if (href) window.open(href, "_blank", "noopener");
    });

    card.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        var href = card.getAttribute("data-href");
        if (href) window.open(href, "_blank", "noopener");
      }
    });
  });

  /* Highlight search */
  var qField = $("#q");
  var query = qField ? qField.value.trim() : "";
  if (query.length >= 2) {
    var terms = query.split(/\s+/).filter(Boolean);
    var pattern = new RegExp("(" + terms.map(function (t) {
      return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }).join("|") + ")", "gi");

    $$(".tender-title").forEach(function (el) {
      var html = el.textContent.replace(pattern, '<mark class="highlight">$1</mark>');
      if (html !== el.textContent) el.innerHTML = html;
    });
  }

  /* Scroll to results */
  if (window.location.search && $("#tender-results")) {
    requestAnimationFrame(function () {
      $("#tender-results").scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
})();
