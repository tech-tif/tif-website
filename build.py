#!/usr/bin/env python3
# Builds the localized static pages (/, /hi/, /mr/) from content/*.json.
# Run:  python3 build.py    (after editing any content/<lang>.json)
import json, os, html as H, re

DOMAIN = "https://treeindiafoundation.org"
LANGS  = {"en": "", "hi": "hi/", "mr": "mr/"}     # url path per language
HTMLLANG = {"en": "en", "hi": "hi", "mr": "mr"}
MAP_SVG = open(os.path.join(os.path.dirname(__file__), "_map.svg"), encoding="utf-8").read()

SVG = {  # small inline icons reused
 "pil1":'<path d="M12 22V12"/><path d="M12 12c0-4 3-7 7-7 0 4-3 7-7 7Z"/><path d="M12 14c0-3-2.5-5-5-5 0 3 2.5 5 5 5Z"/>',
 "pil2":'<path d="M4 19V6a1 1 0 0 1 1-1h6v15H5a1 1 0 0 1-1-1Z"/><path d="M20 19V6a1 1 0 0 0-1-1h-6v15h6a1 1 0 0 0 1-1Z"/>',
 "pil3":'<circle cx="12" cy="8" r="3"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/><circle cx="5" cy="11" r="2"/><circle cx="19" cy="11" r="2"/>',
 "pil4":'<path d="m9 11 3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h9"/>',
}
def esc(s): return H.escape(s, quote=True)

def icon(paths, sw="1.7"):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'

def head(c, lang):
    path = LANGS[lang]
    canonical = f"{DOMAIN}/{path}"
    alts = "".join(
        f'<link rel="alternate" hreflang="{hl}" href="{DOMAIN}/{LANGS[l]}" />\n'
        for l, hl in HTMLLANG.items())
    alts += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/" />'
    title = esc(c["meta"]["title"]); desc = esc(c["meta"]["desc"])
    og_img = f"{DOMAIN}/assets/TIF_og.jpg"
    ld = {
      "@context":"https://schema.org","@graph":[
        {"@type":["NGO","Organization"],"@id":f"{DOMAIN}/#org","name":"Tree India Foundation",
         "url":DOMAIN,"logo":f"{DOMAIN}/assets/TIF_Logo_Transparent.png","email":"treeindiafoundation1@gmail.com",
         "telephone":"+918237193624",
         "address":{"@type":"PostalAddress","streetAddress":"O - 1111, Three Jewels Society, Tilekar Nagar, Katraj-Kondhwa Road","addressLocality":"Pune","addressRegion":"Maharashtra","postalCode":"411048","addressCountry":"IN"},
         "contactPoint":{"@type":"ContactPoint","telephone":"+918237193624","email":"treeindiafoundation1@gmail.com","contactType":"customer support","availableLanguage":["English","Hindi","Marathi"]}},
        {"@type":"WebSite","@id":f"{DOMAIN}/#website","url":DOMAIN,"name":"Tree India Foundation","publisher":{"@id":f"{DOMAIN}/#org"},"inLanguage":list(HTMLLANG.values())},
        {"@type":"WebPage","@id":f"{canonical}#webpage","url":canonical,"name":c["meta"]["title"],"description":c["meta"]["desc"],"isPartOf":{"@id":f"{DOMAIN}/#website"},"about":{"@id":f"{DOMAIN}/#org"},"inLanguage":HTMLLANG[lang]},
      ]}
    return f'''<!DOCTYPE html>
<html lang="{HTMLLANG[lang]}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canonical}" />
{alts}
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Tree India Foundation" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_img}" />
<meta property="og:locale" content="{ {'en':'en_IN','hi':'hi_IN','mr':'mr_IN'}[lang] }" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{og_img}" />
<link rel="icon" type="image/png" href="/assets/TIF_favicon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/styles.css" />
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>'''

def nav(c, lang):
    def a(active): return ' class="ls-active"' if active else ''
    return f'''<header class="nav" id="nav">
  <a href="#home" class="brand" aria-label="Tree India Foundation home">
    <img class="mark" src="/assets/TIF_Logo_Transparent.png" alt="Tree India Foundation logo" width="150" height="150" />
    <span class="wordmark"><b>{esc(c["brand"]["name"])}</b><span>{esc(c["brand"]["tag"])}</span></span>
  </a>
  <nav class="menu" id="menu">
    <a href="#home" class="link">{esc(c["nav"]["home"])}</a>
    <a href="#about" class="link">{esc(c["nav"]["about"])}</a>
    <a href="#work" class="link">{esc(c["nav"]["work"])}</a>
    <a href="#impact" class="link">{esc(c["nav"]["impact"])}</a>
    <a href="#partner" class="link">{esc(c["nav"]["partner"])}</a>
    <a href="#contact" class="link">{esc(c["nav"]["contact"])}</a>
    <a href="#donate" class="btn btn-leaf">{esc(c["nav"]["donate"])}</a>
    <div class="lang-switch" id="langSwitch" role="group" aria-label="Language">
      <a href="/" data-base="/"{a(lang=="en")}>EN</a>
      <a href="/mr/" data-base="/mr/"{a(lang=="mr")}>मराठी</a>
      <a href="/hi/" data-base="/hi/"{a(lang=="hi")}>हिंदी</a>
    </div>
  </nav>
  <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</header>'''

def hero(c):
    return f'''<section class="hero" id="home">
  <div class="wrap hero-grid">
    <div class="reveal in">
      <span class="eyebrow">{esc(c["hero"]["eyebrow"])}</span>
      <h1>{esc(c["hero"]["h1"])}</h1>
      <p class="tagline">{esc(c["hero"]["tagline"])}</p>
      <p class="lead">{esc(c["hero"]["lead"])}</p>
      <div class="hero-cta">
        <a href="#partner" class="btn btn-leaf">{esc(c["hero"]["cta1"])}</a>
        <a href="#work" class="btn btn-outline">{esc(c["hero"]["cta2"])}</a>
      </div>
      <div class="hero-strip">
        <div class="s"><b>4</b><span>{esc(c["hero"]["stat1"])}</span></div>
        <div class="s"><b>7</b><span>{esc(c["hero"]["stat2"])}</span></div>
        <div class="s"><b>7</b><span>{esc(c["hero"]["stat3"])}</span></div>
      </div>
    </div>
    <div class="hero-art reveal in">
      <div class="halo"></div>
      <img src="/assets/TIF_Logo_Transparent.png" alt="Tree India Foundation banyan emblem" width="520" height="522" />
    </div>
  </div>
</section>'''

def about(c):
    pil = "".join(
      f'''<div class="pillar"><span class="n">0{i+1}</span><div class="ic">{icon(SVG[f"pil{i+1}"])}</div><h4>{esc(p["t"])}</h4><p>{esc(p["d"])}</p></div>'''
      for i,p in enumerate(c["pillars"]))
    return f'''<section id="about">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">{esc(c["about"]["eyebrow"])}</span>
      <h2>{esc(c["about"]["title"])}</h2>
      <p>{esc(c["about"]["body1"])}</p>
    </div>
    <div class="about-grid">
      <div class="reveal">
        <p style="color:var(--muted);font-size:1.02rem">{esc(c["about"]["body2"])}</p>
      </div>
      <div class="reveal">
        <div class="vm">
          <div class="card"><h4><span class="dot"></span><span>{esc(c["about"]["visionT"])}</span></h4><p>{esc(c["about"]["visionB"])}</p></div>
          <div class="card"><h4><span class="dot"></span><span>{esc(c["about"]["missionT"])}</span></h4><p>{esc(c["about"]["missionB"])}</p></div>
        </div>
      </div>
    </div>
    <div class="pillars-block reveal">
      <span class="eyebrow">{esc(c["about"]["pillarsEyebrow"])}</span>
      <div class="pillars">{pil}</div>
    </div>
  </div>
</section>'''

def aim(c):
    cards="".join(f'''<div class="aim-card reveal"><span class="c">{esc(it["t"])}</span><p>{esc(it["d"])}</p></div>''' for it in c["aim"]["items"])
    return f'''<section id="aim" class="bg-soft">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">{esc(c["aim"]["eyebrow"])}</span>
      <h2>{esc(c["aim"]["title"])}</h2>
      <p style="font-weight:600;color:var(--forest)">{esc(c["aim"]["subtitle"])}</p>
      <p>{esc(c["aim"]["intro"])}</p>
    </div>
    <div class="aim-grid">{cards}</div>
  </div>
</section>'''

def work(c):
    # icons chosen to fit the 5 programmes (green skills, journeys, nature, educators, community)
    ic=['<path d="M12 22V8"/><path d="M12 8c0-3 2-5 5-5 0 3-2 5-5 5Z"/><path d="M12 12c0-2.5-2-4-4.5-4C7.5 10.5 9.5 12 12 12Z"/>',
        '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5 5-2Z"/>',
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>',
        '<path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1 2.5 3 6 3s6-2 6-3v-5"/><path d="M22 10v6"/>',
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>']
    cards="".join(
      f'''<div class="prog reveal"><div class="ic">{icon(ic[i])}</div><h3>{esc(it["t"])}</h3><p class="prog-sub">{esc(it["sub"])}</p><p>{esc(it["d1"])}</p><p>{esc(it["d2"])}</p></div>'''
      for i,it in enumerate(c["work"]["items"]))
    return f'''<section id="work">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">{esc(c["work"]["eyebrow"])}</span><h2>{esc(c["work"]["title"])}</h2><p>{esc(c["work"]["intro"])}</p></div>
    <div class="prog-grid">{cards}</div>
  </div>
</section>'''

def where(c):
    chips="".join(f'<span class="chip"><span class="pin"></span><span>{esc(d)}</span></span>' for d in c["where"]["districts"])
    sdg="".join(f'<div class="sdg-badge" style="background:{s["color"]}"><b>{s["n"]}</b><span>{esc(s["label"])}</span></div>' for s in c["where"]["sdgs"])
    return f'''<section id="where">
  <div class="wrap work-grid">
    <div class="reveal">
      <span class="eyebrow">{esc(c["where"]["eyebrow"])}</span>
      <h2 style="font-size:clamp(1.8rem,3.5vw,2.6rem);margin-top:16px">{esc(c["where"]["title"])}</h2>
      <p style="color:var(--muted);margin-top:14px">{esc(c["where"]["intro"])}</p>
      <div class="districts">{chips}</div>
      <div class="sdg"><h4>{esc(c["where"]["sdg"])}</h4><div class="sdg-row">{sdg}</div></div>
    </div>
    <div class="reveal">
      <div class="mh-wrap" id="mhWrap">{MAP_SVG}<div class="mh-pop" id="mhPop" aria-hidden="true"></div></div>
      <div class="mh-legend"><span><i class="k-pri"></i><span>{esc(c["where"]["legendPri"])}</span></span><span><i class="k-oth"></i><span>{esc(c["where"]["legendOth"])}</span></span></div>
      <p class="mh-hint">{esc(c["where"]["hint"])}</p>
    </div>
  </div>
</section>'''

def impact(c):
    st="".join(f'<div class="stat reveal"><b>{s["n"]}</b><span>{esc(s["label"])}</span></div>' for s in c["impact"]["stats"])
    return f'''<section id="impact" class="impact">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">{esc(c["impact"]["eyebrow"])}</span><h2>{esc(c["impact"]["title"])}</h2><p>{esc(c["impact"]["intro"])}</p></div>
    <div class="stat-grid">{st}</div>
    <p class="note">{esc(c["impact"]["note"])}</p>
  </div>
</section>'''

def involved(c):
    ic=['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4M10 10h4M10 14h4"/>',
        '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 12 5 5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>']
    modal=["volunteer","partner",None]
    cards=""
    for i,it in enumerate(c["involved"]["items"]):
        if i==0: btn=f'<button class="btn btn-forest" data-modal="volunteer">{esc(it["btn"])}</button>'
        elif i==1: btn=f'<button class="btn btn-forest" data-modal="partner">{esc(it["btn"])}</button>'
        else: btn=f'<a href="#donate" class="btn btn-forest">{esc(it["btn"])}</a>'
        cards+=f'<div class="path reveal"><div class="ic">{icon(ic[i],"1.6")}</div><h3>{esc(it["t"])}</h3><p>{esc(it["d"])}</p>{btn}</div>'
    return f'''<section id="involved" class="bg-soft">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">{esc(c["involved"]["eyebrow"])}</span><h2>{esc(c["involved"]["title"])}</h2><p>{esc(c["involved"]["intro"])}</p></div>
    <div class="paths">{cards}</div>
  </div>
</section>'''

def partner(c):
    cards="".join(f'<div class="csr-card reveal"><h4>{esc(it["t"])}</h4><p>{esc(it["d"])}</p></div>' for it in c["partner"]["items"])
    return f'''<section id="partner" class="partner">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">{esc(c["partner"]["eyebrow"])}</span><h2>{esc(c["partner"]["title"])}</h2><p>{esc(c["partner"]["body"])}</p></div>
    <div class="csr-grid">{cards}</div>
  </div>
</section>'''

def donate(c):
    amt=[("500","₹500"),("1000","₹1,000"),("2500","₹2,500"),("5000","₹5,000"),("10000","₹10,000"),("25000","₹25,000")]
    amts="".join(f'<div class="amt{" sel" if v=="1000" else ""}" data-amt="{v}">{lab}</div>' for v,lab in amt)
    f=c["form"]
    return f'''<section id="donate" class="donate">
  <div class="wrap donate-grid">
    <div class="reveal">
      <span class="eyebrow">{esc(c["donate"]["eyebrow"])}</span>
      <h2>{esc(c["donate"]["title"])}</h2>
      <p>{esc(c["donate"]["body"])}</p>
      <p style="font-size:.9rem;color:rgba(255,255,255,.62);margin-top:20px">{esc(c["donate"]["legal"])}</p>
    </div>
    <div class="donate-card reveal">
      <form data-form="donate" novalidate>
        <h4>{esc(c["donate"]["cardT"])}</h4>
        <div class="amounts" id="amounts">{amts}</div>
        <input class="amt-custom" id="customAmt" name="amount" type="number" min="1" placeholder="{esc(c["donate"]["custom"])}" value="1000" />
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" />
        <div class="field" style="margin-top:12px"><input name="name" type="text" placeholder="{esc(f["name"])}" required /></div>
        <div class="field"><input name="email" type="email" placeholder="{esc(f["email"])}" required /></div>
        <div class="field"><input name="phone" type="tel" placeholder="{esc(f["phoneOpt"])}" /></div>
        <button class="btn btn-leaf" type="submit">{esc(c["donate"]["btn"])}</button>
        <div class="form-note" data-note></div>
        <small>{esc(c["donate"]["small"])}</small>
      </form>
    </div>
  </div>
</section>'''

def contact(c):
    f=c["form"]; ct=c["contact"]
    opts="".join(f'<option>{esc(f[k])}</option>' for k in ("topic.vol","topic.part","topic.csr","topic.press","topic.other"))
    tel="+91"+ct["phoneVal"].replace("+91","").replace(" ","")
    return f'''<section id="contact">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">{esc(ct["eyebrow"])}</span><h2>{esc(ct["title"])}</h2><p>{esc(ct["intro"])}</p></div>
    <div class="contact-grid">
      <div class="contact-info reveal">
        <div class="row"><div class="ic">{icon('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>')}</div><div><h5>{esc(ct["email"])}</h5><a href="mailto:treeindiafoundation1@gmail.com">treeindiafoundation1@gmail.com</a></div></div>
        <div class="row"><div class="ic">{icon('<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20Z"/>')}</div><div><h5>{esc(ct["web"])}</h5><a href="https://treeindiafoundation.org">treeindiafoundation.org</a></div></div>
        <div class="row"><div class="ic">{icon('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>')}</div><div><h5>{esc(ct["office"])}</h5><p>{esc(ct["officeVal"])}</p></div></div>
        <div class="row"><div class="ic">{icon('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13 1 .35 1.94.66 2.85a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.23-1.23a2 2 0 0 1 2.11-.45c.91.31 1.85.53 2.85.66A2 2 0 0 1 22 16.92Z"/>')}</div><div><h5>{esc(ct["phone"])}</h5><p><a href="tel:{tel}">{esc(ct["phoneVal"])}</a></p></div></div>
      </div>
      <form class="form reveal" data-form="contact" novalidate>
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" />
        <div class="field"><label>{esc(f["name"])}</label><input name="name" type="text" placeholder="{esc(f["namePh"])}" required /></div>
        <div class="field"><label>{esc(f["email"])}</label><input name="email" type="email" placeholder="{esc(f["emailPh"])}" required /></div>
        <div class="field"><label>{esc(f["topic"])}</label><select name="topic">{opts}</select></div>
        <div class="field"><label>{esc(f["msg"])}</label><textarea name="message" placeholder="{esc(f["msgPh"])}" required></textarea></div>
        <button class="btn btn-leaf" type="submit">{esc(f["send"])}</button>
        <div class="form-note" data-note></div>
      </form>
    </div>
  </div>
</section>'''

def cta(c):
    return f'''<section class="cta-band"><div class="wrap"><h2>{esc(c["cta"]["title"])}</h2><p>{esc(c["cta"]["body"])}</p><a href="#contact" class="btn btn-leaf">{esc(c["cta"]["btn"])}</a></div></section>'''

def footer(c):
    pil="".join(f'<li><a href="#about">{esc(p["t"])}</a></li>' for p in c["pillars"])
    n=c["nav"]
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="brand"><img class="mark" src="/assets/TIF_Logo_Transparent.png" alt="Tree India Foundation logo" style="height:54px" width="54" height="54" /><span class="wordmark"><b>{esc(c["brand"]["name"])}</b><span>{esc(c["brand"]["tag"])}</span></span></div>
        <p class="about">{esc(c["footer"]["about"])}</p>
      </div>
      <div><h5>{esc(c["footer"]["explore"])}</h5><ul>
        <li><a href="#about">{esc(n["about"])}</a></li><li><a href="#work">{esc(n["work"])}</a></li>
        <li><a href="#impact">{esc(n["impact"])}</a></li><li><a href="#involved">{esc(n["involved"])}</a></li>
        <li><a href="#partner">{esc(n["partner"])}</a></li><li><a href="#contact">{esc(n["contact"])}</a></li>
      </ul></div>
      <div><h5>{esc(c["footer"]["pillars"])}</h5><ul>{pil}</ul></div>
      <div><h5>{esc(c["footer"]["reach"])}</h5><ul>
        <li><a href="mailto:treeindiafoundation1@gmail.com">treeindiafoundation1@gmail.com</a></li>
        <li><a href="tel:+918237193624">+91 82371 93624</a></li>
        <li><a href="#donate">{esc(n["donate"])}</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom"><span>© <span id="year"></span> Tree India Foundation. {esc(c["footer"]["rights"])}</span><span>{esc(c["footer"]["regd"])}</span></div>
  </div>
</footer>'''

def modals(c):
    f=c["form"]; m=c["modal"]
    return f'''<div class="modal-overlay" id="modalOverlay">
  <div class="modal" data-modal-panel="volunteer" role="dialog" aria-modal="true" hidden>
    <div class="modal-head"><button class="modal-close" aria-label="Close">✕</button><span class="eyebrow">{esc(c["involved"]["items"][0]["t"])}</span><h3>{esc(m["vol.t"])}</h3><p>{esc(m["vol.s"])}</p></div>
    <form data-form="volunteer" novalidate>
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" />
      <div class="field"><label>{esc(f["name"])}</label><input name="name" type="text" required /></div>
      <div class="field"><label>{esc(f["email"])}</label><input name="email" type="email" required /></div>
      <div class="field"><label>{esc(f["phone"])}</label><input name="phone" type="tel" /></div>
      <div class="field"><label>{esc(f["district"])}</label><input name="district" type="text" /></div>
      <div class="field"><label>{esc(m["vol.help"])}</label><textarea name="message"></textarea></div>
      <button class="btn btn-leaf" type="submit">{esc(f["submit"])}</button><div class="form-note" data-note></div>
    </form>
  </div>
  <div class="modal" data-modal-panel="partner" role="dialog" aria-modal="true" hidden>
    <div class="modal-head"><button class="modal-close" aria-label="Close">✕</button><span class="eyebrow">{esc(c["involved"]["items"][1]["t"])}</span><h3>{esc(m["part.t"])}</h3><p>{esc(m["part.s"])}</p></div>
    <form data-form="partner" novalidate>
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" />
      <div class="field"><label>{esc(f["name"])}</label><input name="name" type="text" required /></div>
      <div class="field"><label>{esc(m["part.org"])}</label><input name="organisation" type="text" required /></div>
      <div class="field"><label>{esc(f["email"])}</label><input name="email" type="email" required /></div>
      <div class="field"><label>{esc(f["phone"])}</label><input name="phone" type="tel" /></div>
      <div class="field"><label>{esc(f["district"])}</label><input name="district" type="text" /></div>
      <div class="field"><label>{esc(m["part.about"])}</label><textarea name="message"></textarea></div>
      <button class="btn btn-leaf" type="submit">{esc(f["submit"])}</button><div class="form-note" data-note></div>
    </form>
  </div>
</div>'''

def page(c, lang):
    f=c["form"]
    tif_l = {
      "legendPri":c["where"]["legendPri"], "popNote":c["where"]["popNote"], "districts":c["where"]["distmap"],
      "form":{"ok":f["ok"],"err":f["err"],"required":f["required"],"sending":f["sending"],"noconf":f["noconf"]}
    }
    inline = f'<script>window.TIF_L={json.dumps(tif_l, ensure_ascii=False)};</script>'
    body = "\n".join([nav(c,lang),hero(c),about(c),aim(c),work(c),where(c),impact(c),involved(c),partner(c),donate(c),contact(c),cta(c),footer(c),modals(c)])
    return head(c,lang)+f'''
<body>
{body}
{inline}
<script src="/js/config.js"></script>
<script src="/js/forms.js"></script>
<script src="/js/main.js"></script>
</body>
</html>'''

def main():
    for lang,path in LANGS.items():
        with open(f"content/{lang}.json", encoding="utf-8") as fh:
            c=json.load(fh)
        outdir = "." if path=="" else path.rstrip("/")
        os.makedirs(outdir, exist_ok=True)
        out = os.path.join(outdir,"index.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(page(c,lang))
        print("wrote", out)

if __name__=="__main__":
    main()
