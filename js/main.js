/* Nav, mobile menu, scroll reveal, donate selector, map popups, modals */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var yr = document.getElementById("year"); if (yr) yr.textContent = new Date().getFullYear();

    // nav scroll state
    var nav = document.getElementById("nav");
    window.addEventListener("scroll", function () {
      nav.classList.toggle("scrolled", window.scrollY > 30);
    }, { passive: true });

    // mobile menu
    var ham = document.getElementById("hamburger"), menu = document.getElementById("menu");
    ham.addEventListener("click", function () {
      var o = menu.classList.toggle("open"); ham.setAttribute("aria-expanded", o);
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { menu.classList.remove("open"); ham.setAttribute("aria-expanded", "false"); });
    });

    // language switch: keep the current section when changing language
    document.querySelectorAll("#langSwitch a[data-base]").forEach(function (a) {
      var base = a.getAttribute("data-base");
      function sync() { a.setAttribute("href", base + (location.hash || "")); }
      sync();
      window.addEventListener("hashchange", sync);
    });

    // active link on scroll
    var links = [].slice.call(document.querySelectorAll(".menu a.link"));
    document.querySelectorAll("section[id]").forEach(function (s) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) {
            links.forEach(function (l) { l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id); });
          }
        });
      }, { rootMargin: "-45% 0px -50% 0px" });
      io.observe(s);
    });

    // reveal on scroll
    var rev = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); rev.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { rev.observe(el); });

    // donate amount selector
    var amounts = document.getElementById("amounts");
    if (amounts) {
      var custom = document.getElementById("customAmt");
      amounts.addEventListener("click", function (e) {
        var tgt = e.target.closest(".amt"); if (!tgt) return;
        amounts.querySelectorAll(".amt").forEach(function (a) { a.classList.remove("sel"); });
        tgt.classList.add("sel");
        if (custom) custom.value = tgt.getAttribute("data-amt");
      });
    }

    /* ---------- Maharashtra map popups ---------- */
    var wrap = document.getElementById("mhWrap");
    var svg = document.getElementById("mhMap");
    var pop = document.getElementById("mhPop");
    if (wrap && svg && pop) {
      var pinned = null;
      function labelFor(name, isPri) {
        var L = window.TIF_L || {};
        var loc = (L.districts && L.districts[name]) || name;
        var badge = isPri ? '<span class="badge">' + (L.legendPri || "TIF priority district") + '</span>' : "";
        var note = isPri ? '<p>' + (L.popNote || "Active programme geography for Tree India Foundation.") + '</p>' : "";
        return badge + '<h5>' + loc + '</h5>' + note;
      }
      function showFor(path) {
        var name = path.getAttribute("data-d");
        var isPri = path.classList.contains("mh-pri");
        pop.innerHTML = labelFor(name, isPri);
        var b = path.getBBox();
        var r = svg.getBoundingClientRect(), wr = wrap.getBoundingClientRect();
        var sx = r.width / svg.viewBox.baseVal.width, sy = r.height / svg.viewBox.baseVal.height;
        var px = (r.left - wr.left) + (b.x + b.width / 2) * sx;
        var py = (r.top - wr.top) + (b.y + b.height / 2) * sy;
        pop.style.left = px + "px";
        pop.style.top = py + "px";
        pop.classList.add("show");
      }
      function hide() { pop.classList.remove("show"); if (pinned) { pinned.classList.remove("active"); pinned = null; } }

      svg.querySelectorAll("path").forEach(function (p) {
        p.addEventListener("mouseenter", function () { if (!pinned) showFor(p); });
        p.addEventListener("mouseleave", function () { if (!pinned) pop.classList.remove("show"); });
        p.addEventListener("click", function (e) {
          e.stopPropagation();
          if (pinned === p) { hide(); return; }
          if (pinned) pinned.classList.remove("active");
          pinned = p; p.classList.add("active"); showFor(p);
        });
      });
      document.addEventListener("click", function () { hide(); });
      window.addEventListener("resize", function () { if (pinned) showFor(pinned); });
    }

    /* ---------- Modals ---------- */
    var overlay = document.getElementById("modalOverlay");
    function openModal(name) {
      if (!overlay) return;
      overlay.querySelectorAll("[data-modal-panel]").forEach(function (m) {
        m.hidden = m.getAttribute("data-modal-panel") !== name;
      });
      overlay.classList.add("open");
      document.body.style.overflow = "hidden";
      var first = overlay.querySelector("[data-modal-panel]:not([hidden]) input");
      if (first) setTimeout(function () { first.focus(); }, 60);
    }
    function closeModal() {
      if (!overlay) return;
      overlay.classList.remove("open");
      document.body.style.overflow = "";
    }
    window.TIF_closeModal = closeModal;
    document.querySelectorAll("[data-modal]").forEach(function (btn) {
      btn.addEventListener("click", function () { openModal(btn.getAttribute("data-modal")); });
    });
    if (overlay) {
      overlay.addEventListener("click", function (e) { if (e.target === overlay) closeModal(); });
      overlay.querySelectorAll(".modal-close").forEach(function (b) { b.addEventListener("click", closeModal); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });
    }
  });
})();
