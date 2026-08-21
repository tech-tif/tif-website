/* Sends every [data-form] submission to the Google Apps Script Web App.
   Each form carries a hidden formType (its data-form value) so the
   Apps Script routes it to the correct Sheet tab. */
(function () {
  function t(key, fallback) {
    return (window.TIF_T && window.TIF_T[key]) || fallback;
  }
  function setNote(form, msg, kind) {
    var n = form.querySelector("[data-note]");
    if (!n) return;
    n.textContent = msg;
    n.className = "form-note " + (kind || "");
  }

  function handle(form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var formType = form.getAttribute("data-form");

      // honeypot: if filled, silently pretend success (likely a bot)
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) { setNote(form, t("form.ok", "Thank you! We'll be in touch."), "ok"); form.reset(); return; }

      // basic required validation
      var missing = false;
      form.querySelectorAll("[required]").forEach(function (f) {
        if (!f.value.trim()) { missing = true; f.style.borderColor = "#b23b3b"; }
        else { f.style.borderColor = ""; }
      });
      if (missing) { setNote(form, t("form.required", "Please fill the required fields."), "err"); return; }

      var url = window.TIF_CONFIG && window.TIF_CONFIG.GAS_URL;
      if (!url) {
        setNote(form, t("form.noconf", "Form not connected yet. Please email treeindiafoundation1@gmail.com."), "err");
        return;
      }

      var data = new FormData(form);
      data.append("formType", formType);
      data.append("language", document.documentElement.getAttribute("lang") || "en");
      data.append("pageUrl", location.href);

      var original = btn ? btn.innerHTML : "";
      if (btn) { btn.disabled = true; btn.innerHTML = '<span class="spin"></span> ' + t("form.sending", "Sending..."); }
      setNote(form, "", "");

      fetch(url, { method: "POST", mode: "no-cors", body: data })
        .then(function () {
          setNote(form, t("form.ok", "Thank you! We'll be in touch soon."), "ok");
          form.reset();
          // re-select default donate amount if present
          var sel = form.querySelector(".amt.sel");
          var amt = form.querySelector('input[name="amount"]');
          if (amt && sel) amt.value = sel.getAttribute("data-amt");
          // close modal after a moment
          var overlay = form.closest(".modal-overlay");
          if (overlay) setTimeout(function () { window.TIF_closeModal && window.TIF_closeModal(); }, 1600);
        })
        .catch(function () {
          setNote(form, t("form.err", "Something went wrong. Please try again or email us."), "err");
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.innerHTML = original; }
        });
    });
  }

  function init() { document.querySelectorAll("[data-form]").forEach(handle); }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
