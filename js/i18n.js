/* Language loading + switching. Text lives in lang/en|mr|hi.json */
(function () {
  var LANGS = ["en", "mr", "hi"];
  var cache = {};
  var current = "en";

  function safeGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function safeSet(key, v) { try { localStorage.setItem(key, v); } catch (e) {} }

  function apply(dict) {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (!(key in dict)) return;
      var val = dict[key];
      if (el.hasAttribute("data-i18n-attr")) {
        el.setAttribute(el.getAttribute("data-i18n-attr"), val);
      } else {
        el.textContent = val;
      }
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-html");
      if (key in dict) el.innerHTML = dict[key];
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-ph");
      if (key in dict) el.setAttribute("placeholder", dict[key]);
    });
    // expose current dictionary for other scripts (forms.js messages)
    window.TIF_T = dict;
    // build English->localized district-name map for the map popups
    var dm = {};
    Object.keys(dict).forEach(function (k) {
      if (k.indexOf("distmap.") === 0) dm[k.slice(8)] = dict[k];
    });
    window.TIF_DISTRICTS = dm;
  }

  function setLang(lang) {
    if (LANGS.indexOf(lang) < 0) lang = "en";
    current = lang;
    document.documentElement.setAttribute("lang", lang);
    safeSet("tif_lang", lang);
    document.querySelectorAll("#langSwitch button").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-lang") === lang);
    });
    if (cache[lang]) { apply(cache[lang]); return; }
    fetch("lang/" + lang + ".json")
      .then(function (r) { return r.json(); })
      .then(function (d) { cache[lang] = d; apply(d); })
      .catch(function () { /* keep inline English fallback */ });
  }

  function init() {
    var saved = safeGet("tif_lang");
    var start = saved || (window.TIF_CONFIG && window.TIF_CONFIG.DEFAULT_LANG) || "en";
    document.querySelectorAll("#langSwitch button").forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    setLang(start);
  }

  window.TIF_setLang = setLang;
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
